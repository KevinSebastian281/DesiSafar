"""
Budget and cost calculation engine for DesiSafar.
Computes multi-category estimated expenses, per-person splits,
daily averages, tier comparisons, and daily spend breakdowns.
"""

from datetime import datetime, timedelta
from data.destinations import get_destination_by_slug, get_all_destinations
from data.stays_and_food import get_suggested_stay
from logic.itinerary import parse_dates_and_duration


TIER_MULTIPLIERS = {
    "budget": 0.75,
    "standard": 1.0,
    "premium": 1.35,
    "luxury": 2.1,
}

STAY_MULTIPLIERS = {
    "hostel": 0.7,
    "budget_hotel": 0.85,
    "3_star": 1.0,
    "4_star": 1.4,
    "5_star": 2.2,
}


def calculate_budget(selected_slugs, preferences=None, trip_details=None):
    """
    Calculate the full financial breakdown of the trip.
    """
    if not selected_slugs:
        selected_slugs = ["goa", "gokarna"]

    preferences = preferences or {}
    trip_details = trip_details or {}

    departure_str = trip_details.get("departure_date", "")
    return_str = trip_details.get("return_date", "")
    travellers = max(1, int(trip_details.get("travellers", 4)))
    start_location = trip_details.get("start_location", "").strip()

    budget_tier = preferences.get("budget_tier", "standard")
    stay_type = preferences.get("stay_type", "3_star")

    # Destination Objects and Suggested Stays
    dest_objects = []
    for slug in selected_slugs:
        d = get_destination_by_slug(slug)
        if d:
            d_copy = d.copy()
            d_copy["suggested_stay"] = get_suggested_stay(slug, budget_tier, stay_type)
            dest_objects.append(d_copy)

    if not dest_objects:
        all_d = get_all_destinations()
        d0 = all_d[0].copy()
        d0["suggested_stay"] = get_suggested_stay(d0["slug"], budget_tier, stay_type)
        dest_objects = [d0]

    # Calculate suggested total days based on the sum of suggested days of selected destinations
    suggested_total_days = sum(d.get("suggested_days", 3) for d in dest_objects)
    if suggested_total_days < 2:
        suggested_total_days = 2

    # Compute dates and duration
    start_date, end_date, total_days, total_nights = parse_dates_and_duration(
        departure_str, return_str, default_days=suggested_total_days
    )

    # Base pricing calculation
    avg_base_day_rate = sum(d.get("base_cost_per_day", 3000) for d in dest_objects) / len(dest_objects)
    tier_mult = TIER_MULTIPLIERS.get(budget_tier, 1.0)
    stay_mult = STAY_MULTIPLIERS.get(stay_type, 1.0)

    # Combined composite multiplier
    composite_multiplier = (tier_mult * 0.6) + (stay_mult * 0.4)

    # Raw total for the group
    raw_total = avg_base_day_rate * total_days * travellers * composite_multiplier
    # Round to clean hundred
    total_cost = int(round(raw_total / 100.0) * 100)
    if total_cost < 5000:
        total_cost = 5000

    per_person = int(round(total_cost / travellers))
    daily_avg_total = int(round(total_cost / total_days))
    daily_avg_person = int(round(total_cost / (total_days * travellers)))

    # Estimates range
    lower_est = int(round((total_cost * 0.88) / 100.0) * 100)
    expected_est = total_cost
    upper_est = int(round((total_cost * 1.15) / 100.0) * 100)

    # Category Percentages
    # 39% Stay, 19% Transit, 16% Food, 15% Activities, 11% Misc = 100%
    cat_stay_amt = int(round(total_cost * 0.39))
    cat_transit_amt = int(round(total_cost * 0.19))
    cat_food_amt = int(round(total_cost * 0.16))
    cat_activity_amt = int(round(total_cost * 0.15))
    cat_misc_amt = total_cost - (cat_stay_amt + cat_transit_amt + cat_food_amt + cat_activity_amt)

    # Stay Sublabel and hotel references
    stay_sublabels = {
        "hostel": f"{total_nights} Nights (Backpacker Hostels & Dorms)",
        "budget_hotel": f"{total_nights} Nights (Budget Hotels & Guesthouses)",
        "3_star": f"{total_nights} Nights (3-Star & Boutique Coastal Stays)",
        "4_star": f"{total_nights} Nights (4-Star Resorts & Heritage Stays)",
        "5_star": f"{total_nights} Nights (5-Star Luxury Villas & Palaces)",
    }
    stay_sublabel = stay_sublabels.get(stay_type, f"{total_nights} Nights (3-Star Stays)")

    suggested_stays_list = [
        {
            "dest_name": d["name"],
            "hotel_name": d["suggested_stay"]["name"],
            "area": d["suggested_stay"]["area"],
            "rating": d["suggested_stay"]["rating"],
        }
        for d in dest_objects
        if d.get("suggested_stay")
    ]

    categories = [
        {
            "id": "stay",
            "name": "Accommodation",
            "icon": "🏨",
            "percentage": 39,
            "amount": cat_stay_amt,
            "per_person": int(round(cat_stay_amt / travellers)),
            "sublabel": stay_sublabel,
            "suggested_stays": suggested_stays_list,
        },
        {
            "id": "transit",
            "name": "Transportation",
            "icon": "🚗",
            "percentage": 19,
            "amount": cat_transit_amt,
            "per_person": int(round(cat_transit_amt / travellers)),
            "sublabel": "Cabs, Inter-city Rail / Expressways & Fuel",
        },
        {
            "id": "food",
            "name": "Food & Dining",
            "icon": "🍜",
            "percentage": 16,
            "amount": cat_food_amt,
            "per_person": int(round(cat_food_amt / travellers)),
            "sublabel": "Breakfasts, Highway Dhabas & Local Dining",
        },
        {
            "id": "activity",
            "name": "Activities & Sightseeing",
            "icon": "🎟️",
            "percentage": 15,
            "amount": cat_activity_amt,
            "per_person": int(round(cat_activity_amt / travellers)),
            "sublabel": "Entry Passes, Boat Rides & Adventure Sports",
        },
        {
            "id": "misc",
            "name": "Miscellaneous & Buffer",
            "icon": "💳",
            "percentage": 11,
            "amount": cat_misc_amt,
            "per_person": int(round(cat_misc_amt / travellers)),
            "sublabel": "Tolls, Parking, Tips & Emergency Contingency",
        },
    ]

    # Day-by-Day Spend Generation
    day_spend_list = []
    # Distribute destinations across days
    num_dests = len(dest_objects)
    base_daily = total_cost / total_days
    
    # Weight factors across trip days (arrival and transit days slightly higher due to tickets/cabs)
    for day_i in range(1, total_days + 1):
        dest_idx = min(num_dests - 1, (day_i - 1) * num_dests // total_days)
        dest = dest_objects[dest_idx]

        if day_i == 1:
            day_loc = f"{dest['name']}"
            weight = 1.05
            snippet = "Airport/station transfer, accommodation check-in & welcome dinner"
        elif day_i == total_days:
            day_loc = f"{dest['name']} / Departure"
            weight = 0.95
            snippet = "Souvenir bazaar, café brunch & return transit"
        elif len(dest_objects) > 1 and day_i == (total_days // 2 + 1):
            day_loc = "Transit"
            weight = 1.15
            snippet = f"Scenic drive transfer to {dest['name']}, check-in & sunset"
        elif day_i % 2 == 0:
            day_loc = f"{dest['name']}"
            weight = 1.08
            h = dest.get("highlights", ["Sightseeing"])[0]
            snippet = f"{h} & authentic local dining"
        else:
            day_loc = f"{dest['name']}"
            weight = 0.92
            h = dest.get("highlights", ["Scenic sights", "Local trail"])[1] if len(dest.get("highlights", [])) > 1 else "Local exploration"
            snippet = f"{h} & relaxing evening"

        day_cost = int(round((base_daily * weight) / 100.0) * 100)
        day_spend_list.append({
            "day_num": day_i,
            "location": day_loc,
            "cost": day_cost,
            "snippet": snippet,
        })

    # Adjust day costs so sum is close to total_cost and compute bar widths
    max_day_cost = max(d["cost"] for d in day_spend_list) if day_spend_list else 1
    for d in day_spend_list:
        d["bar_pct"] = max(20, min(100, int((d["cost"] / max_day_cost) * 100)))

    # Plan Comparison Tiers
    tier_definitions = [
        {
            "id": "budget",
            "title": "Budget-Friendly",
            "desc": "Focus on essentials, hostels/guesthouses, and shared transit.",
            "multiplier": TIER_MULTIPLIERS["budget"] * STAY_MULTIPLIERS["hostel"],
        },
        {
            "id": "standard",
            "title": "Standard",
            "desc": "Balanced comfort, boutique 3-star stays, private rental cabs, and top experiences.",
            "multiplier": TIER_MULTIPLIERS["standard"] * STAY_MULTIPLIERS["3_star"],
        },
        {
            "id": "premium",
            "title": "Premium",
            "desc": "4-star stays, dedicated chauffeur cab, fine dining, and guided activities.",
            "multiplier": TIER_MULTIPLIERS["premium"] * STAY_MULTIPLIERS["4_star"],
        },
        {
            "id": "luxury",
            "title": "Luxury",
            "desc": "5-star luxury heritage villas, private boat charters & VIP trails.",
            "multiplier": TIER_MULTIPLIERS["luxury"] * STAY_MULTIPLIERS["5_star"],
        },
    ]

    tier_comparisons = []
    for t in tier_definitions:
        t_total = int(round((avg_base_day_rate * total_days * travellers * t["multiplier"]) / 1000.0) * 1000)
        t_per_person = int(round(t_total / travellers))
        tier_comparisons.append({
            "id": t["id"],
            "title": t["title"],
            "total_display": f"₹{t_total:,}",
            "per_person_display": f"₹{t_per_person:,}",
            "desc": t["desc"],
            "is_active": (t["id"] == budget_tier),
        })

    # Context Header data
    dest_names = " + ".join([d["name"] for d in dest_objects])
    date_context_str = (
        f"{start_date.strftime('%d')}–{end_date.strftime('%d %B %Y')} ({total_days} Days · {total_nights} Nights)"
        if start_date
        else f"{total_days} Days · {total_nights} Nights"
    )
    plan_tag_str = f"{budget_tier.capitalize()} Plan"

    return {
        "total_cost": total_cost,
        "total_cost_display": f"₹{total_cost:,}",
        "per_person": per_person,
        "per_person_display": f"₹{per_person:,}",
        "travellers": travellers,
        "total_days": total_days,
        "total_nights": total_nights,
        "daily_avg_total": daily_avg_total,
        "daily_avg_total_display": f"₹{daily_avg_total:,}",
        "daily_avg_person": daily_avg_person,
        "daily_avg_person_display": f"₹{daily_avg_person:,}",
        "lower_estimate_display": f"₹{lower_est:,}",
        "expected_estimate_display": f"₹{expected_est:,}",
        "upper_estimate_display": f"₹{upper_est:,}",
        "categories": categories,
        "daily_spend": day_spend_list,
        "tier_comparisons": tier_comparisons,
        "destinations_display": dest_names,
        "date_context_str": date_context_str,
        "plan_tag_str": plan_tag_str,
        "budget_tier": budget_tier,
    }
