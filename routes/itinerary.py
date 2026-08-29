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

    preferences = session.get("preferences")
    if not preferences:
        flash("Please set your travel preferences first.", "info")
        return redirect(url_for("preferences.preferences_view"))

    trip_details = session.get("trip_details", {})

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
