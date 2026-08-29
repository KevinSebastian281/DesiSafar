from flask import Blueprint, render_template, session, redirect, url_for, flash
from logic.budget import calculate_budget
budget_bp = Blueprint('budget', __name__, url_prefix='/budget')

@budget_bp.route('', methods=['GET'])
@budget_bp.route('/', methods=['GET'])
def budget_view():
    selected_slugs = session.get('selected_destinations', [])
    if not selected_slugs:
        flash('Please select your destinations first to view budget.', 'warning')
        return redirect(url_for('destinations.list_destinations'))
    trip_details = session.get('trip_details', {})
    departure_date = trip_details.get('departure_date', '').strip() if isinstance(trip_details, dict) else ''
    if not departure_date:
        flash('Please select a trip start date first.', 'warning')
        return redirect(url_for('destinations.list_destinations'))
    preferences = session.get('preferences')
    if not preferences:
        flash('Please set your travel preferences first.', 'info')
        return redirect(url_for('preferences.preferences_view'))
    budget_data = calculate_budget(selected_slugs=selected_slugs, preferences=preferences, trip_details=trip_details)
    return render_template('budget.html', budget=budget_data)
