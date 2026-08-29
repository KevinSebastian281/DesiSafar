from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from logic.itinerary import generate_itinerary
itinerary_bp = Blueprint('itinerary', __name__, url_prefix='/itinerary')

@itinerary_bp.route('', methods=['GET', 'POST'])
@itinerary_bp.route('/', methods=['GET', 'POST'])
def itinerary_view():
    selected_slugs = session.get('selected_destinations', [])
    if not selected_slugs:
        flash('Please select your destinations first to build an itinerary.', 'warning')
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
    modifier = request.args.get('modifier') or request.form.get('modifier') or session.get('itinerary_modifier', 'normal')
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action in ['cheaper', 'comfortable', 'optimize', 'normal']:
            modifier = action
            session['itinerary_modifier'] = modifier
            session.modified = True
            if modifier == 'cheaper':
                flash(' Itinerary updated to prioritize economical buses, shared autos, and walking!', 'success')
            elif modifier == 'comfortable':
                flash(' Itinerary upgraded with comfortable private autos and direct cabs!', 'success')
            elif modifier == 'optimize':
                flash(' Route optimized! Clustered nearby attractions to minimize transit time.', 'success')
            elif modifier == 'normal':
                flash('Reset itinerary to standard budget settings.', 'info')
            return redirect(url_for('itinerary.itinerary_view', modifier=modifier))
    itinerary_data = generate_itinerary(selected_slugs=selected_slugs, preferences=preferences, trip_details=trip_details, modifier=modifier)
    return render_template('itinerary.html', summary=itinerary_data['summary'], days=itinerary_data['days'], destinations=itinerary_data['destinations'], destination_insights=itinerary_data.get('destination_insights', []), budget_summary=itinerary_data['budget_summary'], active_modifier=modifier)
