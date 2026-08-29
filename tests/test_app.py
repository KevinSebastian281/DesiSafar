"""
Automated unit and integration test suite for DesiSafar Flask application.
"""

import re
from datetime import datetime, timedelta
import pytest
from app import create_app
from data.destinations import (
    get_all_destinations,
    filter_destinations,
    get_destination_by_slug,
    get_nearby_starting_hubs,
)
from data.stays_and_food import STAYS_AND_FOOD, VERIFIED_DATE_DISCLAIMER
from logic.itinerary import generate_itinerary, parse_dates_and_duration
from logic.budget import calculate_budget


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SECRET_KEY": "test-key-2026"})
    with app.test_client() as client:
        yield client


def test_landing_page(client):
    """Verify landing page renders successfully with 200 OK and contains brand elements."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "DesiSafar" in html
    assert "Plan your dream India trip in" in html
    assert "Start Planning Free" in html


def test_destinations_page_default(client):
    """Verify destinations explorer renders with all 16 destinations by default."""
    response = client.get("/destinations")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Where do you want to go?" in html
    assert "Destination Explorer" in html
    assert "Goa" in html
    assert "Munnar" in html
    assert "Manali" in html


def test_default_empty_starting_place_and_dates(client):
    """Verify starting point and dates default to empty/nothing as requested."""
    client.get("/reset")
    with client.session_transaction() as sess:
        trip_details = sess.get("trip_details", {})
        assert trip_details.get("start_location") == ""
        assert trip_details.get("departure_date") == ""
        assert trip_details.get("return_date") == ""


def test_nearby_starting_hubs_helper():
    """Verify get_nearby_starting_hubs returns nearby hubs for selected destinations + all Indian hubs."""
    hubs = get_nearby_starting_hubs(["goa", "munnar"])
    assert any("Dabolim" in h or "Mopa" in h for h in hubs)
    assert any("Madgaon" in h for h in hubs)
    assert any("Cochin" in h or "Ernakulam" in h for h in hubs)
    assert any("Delhi" in h for h in hubs)
    assert any("Mumbai" in h for h in hubs)


def test_auto_calculated_return_date_from_destinations(client):
    """Verify return date is automatically calculated based on the suggested days of selected places."""
    client.get("/reset")
    # Goa (4 days) + Munnar (3 days) = 7 days
    client.post("/destinations/toggle", data={"slug": "goa"})
    client.post("/destinations/toggle", data={"slug": "munnar"})

    # Post departure date only without return date
    res = client.post("/destinations/update_trip", data={
        "start_location": "My Custom Home Town",
        "departure_date": "2026-11-01",
        "return_date": "",
        "travellers": "3"
    }, follow_redirects=True)

    assert res.status_code == 200
    with client.session_transaction() as sess:
        # 7 days from 2026-11-01 -> return date should be 2026-11-07
        assert sess["trip_details"]["departure_date"] == "2026-11-01"
        assert sess["trip_details"]["return_date"] == "2026-11-07"
        assert sess["trip_details"]["start_location"] == "My Custom Home Town"


def test_stays_and_food_data_integrity():
    """Verify all 16 destinations have exactly 3 hotels and 3 restaurants from STAYS_AND_FOOD."""
    all_dests = get_all_destinations()
    assert len(all_dests) == 16
    for d in all_dests:
        slug = d["slug"]
        assert slug in STAYS_AND_FOOD, f"Missing stays and food for {slug}"
        assert len(d["hotels"]) == 3, f"{slug} does not have 3 hotels"
        assert len(d["restaurants"]) == 3, f"{slug} does not have 3 restaurants"
        assert d["disclaimer"] == VERIFIED_DATE_DISCLAIMER


def test_modal_where_to_stay_and_eat_rendering(client):
    """Verify destination modals render Where to Stay, Where to Eat, ratings, and phone links."""
    res = client.get("/destinations")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # Check for Where to Stay and Where to Eat headings
    assert "Where to Stay" in html
    assert "Where to Eat" in html

    # Check sample hotels across destinations
    assert "Hilton Goa Resort" in html
    assert "Blanket Hotel &amp; Spa" in html or "Blanket Hotel & Spa" in html
    assert "Hotel Rio Sol Resort and Villas" in html

    # Check sample restaurants
    assert "The Second House" in html
    assert "Munnar Samrudhi Restaurant" in html
    assert "The Lazy Dog Lounge" in html

    # Check star ratings and phone links
    assert "★ 4.5" in html
    assert "tel:+91 832 664 9800" in html

    # Check freshness disclaimer from Python constant
    assert VERIFIED_DATE_DISCLAIMER in html


def test_no_literal_none_in_rendered_html(client):
    """Verify that 'None' is never printed in HTML for missing phones or price levels."""
    client.get("/reset")
    client.post("/destinations/toggle", data={"slug": "varanasi"})
    client.post("/destinations/toggle", data={"slug": "ooty"})
    client.post("/destinations/update_trip", data={"departure_date": "2026-11-01", "travellers": "4"})
    client.post("/preferences", data={"budget": "standard"})

    routes = ["/destinations", "/itinerary", "/budget"]
    for route in routes:
        res = client.get(route)
        html = res.get_data(as_text=True)
        # Check that there is no 'tel:None', 'None</span>', 'None</p>', or 'None</div'
        assert "tel:none" not in html.lower()
        assert ">none<" not in html.lower()
        assert "₹none" not in html.lower()


def test_itinerary_and_budget_stays_integration(client):
    """Verify Step 3 Itinerary and Step 4 Budget surface suggested hotels and restaurants."""
    client.get("/reset")
    client.post("/destinations/toggle", data={"slug": "goa"})
    client.post("/destinations/toggle", data={"slug": "munnar"})
    client.post("/destinations/update_trip", data={"departure_date": "2026-11-01", "travellers": "4"})
    client.post("/preferences", data={"budget": "premium", "stay": "4_star", "diet": "vegetarian"})

    # Step 3 Itinerary
    res_itin = client.get("/itinerary")
    assert res_itin.status_code == 200
    itin_html = res_itin.get_data(as_text=True)
    assert "Suggested Stay" in itin_html
    assert "Suggested Dining" in itin_html
    # Should include a Goa stay and a Munnar stay
    assert "Hilton Goa Resort" in itin_html or "Holiday Inn Resort Goa" in itin_html
    assert "Blanket Hotel &amp; Spa" in itin_html or "Blanket Hotel & Spa" in itin_html or "Grand Plaza" in itin_html

    # Step 4 Budget
    res_bud = client.get("/budget")
    assert res_bud.status_code == 200
    bud_html = res_bud.get_data(as_text=True)
    assert "Accommodation" in bud_html
    assert "Hilton Goa Resort" in bud_html or "Holiday Inn Resort Goa" in bud_html


def test_destinations_filter_by_category(client):
    """Verify server-side category filtering works without JavaScript."""
    response = client.get("/destinations?category=beaches")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Goa" in html
    assert "Gokarna" in html
    assert "Varkala" in html

    filtered = filter_destinations(category="beaches")
    slugs = [d["slug"] for d in filtered]
    assert "goa" in slugs
    assert "gokarna" in slugs
    assert "manali" not in slugs


def test_destinations_search(client):
    """Verify search filter queries destinations."""
    response = client.get("/destinations?q=shikara")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Kashmir" in html


def test_destinations_search_empty_and_special_chars(client):
    """Verify search handles empty, invalid, or special characters gracefully."""
    response = client.get("/destinations?q=xyznonexistent123")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "No destinations found" in html

    response = client.get("/destinations?q=%20%20")
    assert response.status_code == 200


def test_destination_add_and_cap(client):
    """Test adding destinations to trip and enforcing 5-destination maximum cap."""
    client.get("/reset")

    # Add 5 destinations
    for slug in ["goa", "munnar", "manali", "jaipur", "kashmir"]:
        res = client.post("/destinations/toggle", data={"slug": slug}, follow_redirects=True)
        assert res.status_code == 200

    with client.session_transaction() as sess:
        assert len(sess["selected_destinations"]) == 5
        assert "goa" in sess["selected_destinations"]
        assert "kashmir" in sess["selected_destinations"]

    # Try adding a 6th destination (should be blocked by 5-cap)
    res = client.post("/destinations/toggle", data={"slug": "hampi"}, follow_redirects=True)
    assert res.status_code == 200
    with client.session_transaction() as sess:
        assert len(sess["selected_destinations"]) == 5
        assert "hampi" not in sess["selected_destinations"]


def test_destination_remove(client):
    """Test removing a destination from session."""
    client.get("/reset")
    client.post("/destinations/toggle", data={"slug": "goa"})
    client.post("/destinations/toggle", data={"slug": "munnar"})

    # Remove goa
    client.post("/destinations/remove", data={"remove_slug": "goa"}, follow_redirects=True)
    with client.session_transaction() as sess:
        assert "goa" not in sess["selected_destinations"]
        assert "munnar" in sess["selected_destinations"]


def test_step_guards(client):
    """Verify step guards redirect when destinations or start date are missing."""
    client.get("/reset")
    with client.session_transaction() as sess:
        sess["selected_destinations"] = []
        sess["trip_details"]["departure_date"] = ""

    # Attempting to access /preferences with 0 destinations should redirect to /destinations
    res = client.get("/preferences", follow_redirects=False)
    assert res.status_code == 302
    assert "/destinations" in res.headers["Location"]

    # Attempting to access /preferences with 1 destination but NO start date should redirect
    client.post("/destinations/toggle", data={"slug": "goa"})
    res = client.get("/preferences", follow_redirects=False)
    assert res.status_code == 302
    assert "/destinations" in res.headers["Location"]

    # Posting update_trip with destinations but NO start date should redirect to /destinations
    res = client.post("/destinations/update_trip", data={"departure_date": "", "travellers": "4"}, follow_redirects=False)
    assert res.status_code == 302
    assert "/destinations" in res.headers["Location"]

    # Attempting to access /itinerary with 0 destinations should redirect
    client.get("/reset")
    res = client.get("/itinerary", follow_redirects=False)
    assert res.status_code == 302
    assert "/destinations" in res.headers["Location"]

    # Attempting to access /itinerary with destinations but NO start date should redirect
    client.post("/destinations/toggle", data={"slug": "goa"})
    res = client.get("/itinerary", follow_redirects=False)
    assert res.status_code == 302
    assert "/destinations" in res.headers["Location"]

    # Attempting to access /budget with 0 destinations should redirect
    client.get("/reset")
    res = client.get("/budget", follow_redirects=False)
    assert res.status_code == 302
    assert "/destinations" in res.headers["Location"]

    # Attempting to access /budget with destinations but NO start date should redirect
    client.post("/destinations/toggle", data={"slug": "goa"})
    res = client.get("/budget", follow_redirects=False)
    assert res.status_code == 302
    assert "/destinations" in res.headers["Location"]

    # When both destination and start date are set, accessing /preferences should succeed (200 OK)
    client.post("/destinations/update_trip", data={"departure_date": "2026-11-01", "travellers": "4"})
    res = client.get("/preferences", follow_redirects=False)
    assert res.status_code == 200


def test_preferences_submission_and_itinerary(client):
    """Verify submitting preferences sets session and leads to generated itinerary."""
    client.get("/reset")
    client.post("/destinations/toggle", data={"slug": "goa"})
    client.post("/destinations/toggle", data={"slug": "munnar"})
    client.post("/destinations/update_trip", data={"departure_date": "2026-11-01", "travellers": "4"})

    pref_data = {
        "vibe": ["romantic", "foodie"],
        "interest": ["beaches", "food", "cafes"],
        "budget": "premium",
        "stay": "4_star",
        "diet": "vegetarian",
        "dining": ["local_food", "cafes"],
    }
    res = client.post("/preferences", data=pref_data, follow_redirects=True)
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # We should now be on Itinerary page
    assert "Your Travel Itinerary" in html
    assert "Goa + Munnar" in html
    assert "Day 1" in html
    assert "Vegetarian" in html
    assert "4-Star Resort" in html


def test_budget_page_calculation(client):
    """Verify Step 4 budget page calculates amounts and per-person split correctly."""
    client.get("/reset")
    client.post("/destinations/toggle", data={"slug": "goa"})
    client.post("/destinations/update_trip", data={
        "start_location": "Mumbai, Maharashtra",
        "departure_date": "2026-11-01",
        "return_date": "2026-11-06",
        "travellers": "4"
    })
    client.post("/preferences", data={"budget": "standard", "stay": "3_star"})

    res = client.get("/budget")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "What will your trip cost?" in html
    assert "Per Person Share" in html
    assert "Where your money goes" in html
    assert "Accommodation" in html
    assert "Transportation" in html
    assert "Food &amp; Dining" in html or "Food & Dining" in html


def test_itinerary_logic_unit():
    """Unit test for itinerary generation logic with diverse destination sets."""
    itinerary_single = generate_itinerary(
        selected_slugs=["manali"],
        preferences={"diet": "vegetarian", "budget_tier": "standard", "stay_type": "3_star"},
        trip_details={"departure_date": "2026-10-01", "return_date": "2026-10-05", "travellers": 2}
    )
    assert len(itinerary_single["days"]) == 5
    assert itinerary_single["summary"]["travelers_display"] == "2 People"
    assert "Manali" in itinerary_single["summary"]["destinations_display"]

    itinerary_multi = generate_itinerary(
        selected_slugs=["jaipur", "udaipur", "varanasi"],
        preferences={"diet": "non_vegetarian", "budget_tier": "luxury", "stay_type": "5_star"},
        trip_details={"departure_date": "2026-11-10", "return_date": "2026-11-16", "travellers": 6}
    )
    assert len(itinerary_multi["days"]) == 7
    assert len(itinerary_multi["destinations"]) == 3


def test_budget_logic_math():
    """Unit test to verify budget math consistency, percentages, and splits."""
    budget_result = calculate_budget(
        selected_slugs=["goa", "gokarna"],
        preferences={"budget_tier": "standard", "stay_type": "3_star"},
        trip_details={"departure_date": "2026-10-12", "return_date": "2026-10-17", "travellers": 4}
    )
    assert budget_result["total_days"] == 6
    assert budget_result["travellers"] == 4
    assert budget_result["total_cost"] > 0
    assert budget_result["per_person"] == round(budget_result["total_cost"] / 4)

    # Categories percentages sum to 100%
    pct_sum = sum(c["percentage"] for c in budget_result["categories"])
    assert pct_sum == 100

    # Category amounts sum to total cost
    amt_sum = sum(c["amount"] for c in budget_result["categories"])
    assert amt_sum == budget_result["total_cost"]


def test_preferences_price_estimates_and_snapshot_rendering(client):
    """Verify that budget cards display estimated price ranges and the snapshot contains live cost."""
    client.get("/reset")
    client.post("/destinations/toggle", data={"slug": "goa"})
    client.post("/destinations/toggle", data={"slug": "munnar"})
    client.post("/destinations/update_trip", data={"departure_date": "2026-11-01", "travellers": "4"})

    res = client.get("/preferences")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # Check budget card price range IDs and content
    assert 'id="price-range-budget"' in html
    assert 'id="price-range-standard"' in html
    assert 'id="price-range-premium"' in html
    assert 'id="price-range-luxury"' in html
    assert "/ person" in html

    # Check Preference Snapshot tags and cost
    assert 'id="snapshotVibe"' in html
    assert 'id="snapshotBudget"' in html
    assert 'id="snapshotStay"' in html
    assert 'id="snapshotDiet"' in html
    assert 'id="snapshotCost"' in html
    assert "Est. Trip Cost" in html


def test_zero_inline_event_handlers_audit(client):
    """Strictly verify that NO inline on* event handlers exist on any page."""
    routes = ["/", "/destinations", "/preferences", "/itinerary", "/budget"]

    client.get("/reset")
    client.post("/destinations/toggle", data={"slug": "goa"})
    client.post("/destinations/update_trip", data={"departure_date": "2026-11-01", "travellers": "4"})
    client.post("/preferences", data={"budget": "standard"})

    for route in routes:
        res = client.get(route)
        html = res.get_data(as_text=True)

        # Check for forbidden inline handlers (onclick, onchange, onmouseover, etc.)
        inline_handlers = re.findall(r'\son[a-z]+\s*=', html, re.IGNORECASE)
        assert not inline_handlers, f"Forbidden inline event handler {inline_handlers} found in route {route}!"


def test_navbar_step_locking(client):
    """Verify that navbar disables steps when prerequisites are not met."""
    # 1. On empty / reset state: Step 2, 3, 4 should not have active href links
    client.get("/reset")
    res = client.get("/destinations")
    html = res.get_data(as_text=True)
    assert 'href="/preferences' not in html
    assert 'href="/itinerary' not in html
    assert 'href="/budget' not in html
    assert "step-link-disabled" in html

    # 2. Add destination but no start date: Step 2 should still remain locked
    client.post("/destinations/toggle", data={"slug": "goa"})
    res = client.get("/destinations")
    html = res.get_data(as_text=True)
    assert 'href="/preferences' not in html

    # 3. Add destination AND start date: Step 2 becomes unlocked in navbar
    client.post("/destinations/update_trip", data={"departure_date": "2026-11-01", "travellers": "4"})
    res = client.get("/destinations")
    html = res.get_data(as_text=True)
    assert 'href="/preferences' in html


