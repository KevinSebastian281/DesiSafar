"""
Step 3 routes for DesiSafar: Generated personalized day-by-day itinerary.
"""

from flask import Blueprint, render_template, session, redirect, url_for, flash
from logic.itinerary import generate_itinerary

itinerary_bp = Blueprint("itinerary", __name__, url_prefix="/itinerary")


@itinerary_bp.route("", methods=["GET"])
@itinerary_bp.route("/", methods=["GET"])
def itinerary_view():
    """Display dynamically computed itinerary."""
    selected_slugs = session.get("selected_destinations", [])
    if not selected_slugs:
        flash("Please select your destinations first to build an itinerary.", "warning")
        return redirect(url_for("destinations.list_destinations"))

    trip_details = session.get("trip_details", {})
    departure_date = trip_details.get("departure_date", "").strip() if isinstance(trip_details, dict) else ""
    if not departure_date:
        flash("Please select a trip start date first.", "warning")
        return redirect(url_for("destinations.list_destinations"))

    preferences = session.get("preferences")
    if not preferences:
        flash("Please set your travel preferences first.", "info")
        return redirect(url_for("preferences.preferences_view"))

    itinerary_data = generate_itinerary(
        selected_slugs=selected_slugs,
        preferences=preferences,
        trip_details=trip_details,
    )

    return render_template(
        "itinerary.html",
        summary=itinerary_data["summary"],
        days=itinerary_data["days"],
        destinations=itinerary_data["destinations"],
    )
