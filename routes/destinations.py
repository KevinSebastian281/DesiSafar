from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from data.destinations import CATEGORIES, STARTING_HUBS, get_all_destinations, get_destination_by_slug, filter_destinations, get_nearby_starting_hubs
from logic.itinerary import parse_dates_and_duration
destinations_bp = Blueprint('destinations', __name__, url_prefix='/destinations')

def get_or_create_trip_session():
    if 'selected_destinations' not in session:
        session['selected_destinations'] = []
    if 'trip_details' not in session:
        session['trip_details'] = {'start_location': '', 'departure_date': '', 'return_date': '', 'travellers': 4}
    session.modified = True

@destinations_bp.route('', methods=['GET'])
@destinations_bp.route('/', methods=['GET'])
def list_destinations():
    get_or_create_trip_session()
    search_query = request.args.get('q', '').strip()
    active_category = request.args.get('category', 'all').strip().lower()
    filtered = filter_destinations(query=search_query, category=active_category)
    all_dests = get_all_destinations()
    selected_slugs = session.get('selected_destinations', [])
    selected_dest_objects = [get_destination_by_slug(s) for s in selected_slugs if get_destination_by_slug(s)]
    starting_hubs = get_nearby_starting_hubs(selected_slugs)
    suggested_total_days = sum((d.get('suggested_days', 3) for d in selected_dest_objects))
    if suggested_total_days < 2:
        suggested_total_days = 4 if not selected_dest_objects else 2
    trip_details = session.get('trip_details', {})
    dep_date = trip_details.get('departure_date', '')
    ret_date = trip_details.get('return_date', '')
    if dep_date and (not ret_date):
        try:
            start_d = datetime.strptime(dep_date, '%Y-%m-%d')
            auto_ret = (start_d + timedelta(days=suggested_total_days - 1)).strftime('%Y-%m-%d')
            ret_date = auto_ret
            trip_details['return_date'] = auto_ret
            session['trip_details'] = trip_details
            session.modified = True
        except ValueError:
            pass
    start_d, end_d, computed_days, computed_nights = parse_dates_and_duration(dep_date, ret_date, default_days=suggested_total_days)
    return render_template('destinations.html', destinations=filtered, all_destinations=all_dests, categories=CATEGORIES, starting_hubs=starting_hubs, active_category=active_category, search_query=search_query, selected_destinations=selected_slugs, selected_dest_objects=selected_dest_objects, selected_dest_count=len(selected_slugs), trip_details=trip_details, computed_days=computed_days, computed_nights=computed_nights)

@destinations_bp.route('/<slug>', methods=['GET'])
def detail(slug):
    dest = get_destination_by_slug(slug)
    if not dest:
        flash(f"Destination '{slug}' not found.", 'warning')
        return redirect(url_for('destinations.list_destinations'))
    category = request.args.get('category', 'all')
    q = request.args.get('q', '')
    return redirect(url_for('destinations.list_destinations', category=category, q=q, _anchor=f'modal-{slug}'))

@destinations_bp.route('/toggle', methods=['POST'])
def toggle_destination():
    get_or_create_trip_session()
    slug = request.form.get('slug', '').strip()
    category = request.form.get('category', 'all')
    q = request.form.get('q', '')
    dest = get_destination_by_slug(slug)
    if not dest:
        flash('Invalid destination selected.', 'warning')
        return redirect(url_for('destinations.list_destinations', category=category, q=q))
    selected = session.get('selected_destinations', [])
    if slug in selected:
        selected.remove(slug)
        session['selected_destinations'] = selected
        session.modified = True
        flash(f"Removed {dest['name']} from your trip.", 'info')
    elif len(selected) >= 5:
        flash('You can select up to 5 destinations for a single route.', 'warning')
    else:
        selected.append(slug)
        session['selected_destinations'] = selected
        session.modified = True
        flash(f"Added {dest['name']} to your trip!", 'success')
    return redirect(url_for('destinations.list_destinations', category=category, q=q))

@destinations_bp.route('/remove', methods=['POST'])
def remove_destination():
    get_or_create_trip_session()
    slug = request.form.get('remove_slug') or request.form.get('slug', '')
    slug = slug.strip()
    selected = session.get('selected_destinations', [])
    if slug in selected:
        selected.remove(slug)
        session['selected_destinations'] = selected
        session.modified = True
        dest = get_destination_by_slug(slug)
        dest_name = dest['name'] if dest else slug
        flash(f'Removed {dest_name} from your route.', 'info')
    return redirect(url_for('destinations.list_destinations'))

@destinations_bp.route('/update_trip', methods=['POST'])
def update_trip_details():
    get_or_create_trip_session()
    start_location = request.form.get('start_location', '').strip()
    departure_date = request.form.get('departure_date', '').strip()
    return_date = request.form.get('return_date', '').strip()
    try:
        travellers = max(1, min(20, int(request.form.get('travellers', 4))))
    except ValueError:
        travellers = 4
    selected = session.get('selected_destinations', [])
    selected_dest_objects = [get_destination_by_slug(s) for s in selected if get_destination_by_slug(s)]
    suggested_total_days = sum((d.get('suggested_days', 3) for d in selected_dest_objects))
    if suggested_total_days < 2:
        suggested_total_days = 4 if not selected_dest_objects else 2
    if departure_date and (not return_date):
        try:
            start_d = datetime.strptime(departure_date, '%Y-%m-%d')
            return_date = (start_d + timedelta(days=suggested_total_days - 1)).strftime('%Y-%m-%d')
        except ValueError:
            pass
    session['trip_details'] = {'start_location': start_location, 'departure_date': departure_date, 'return_date': return_date, 'travellers': travellers}
    session.modified = True
    if not selected:
        flash('Please select at least 1 destination to continue to preferences.', 'warning')
        return redirect(url_for('destinations.list_destinations'))
    if not departure_date:
        flash('Please select a trip start date to continue to preferences.', 'warning')
        return redirect(url_for('destinations.list_destinations'))
    return redirect(url_for('preferences.preferences_view'))
