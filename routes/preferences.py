from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from data.destinations import get_destination_by_slug
from logic.itinerary import parse_dates_and_duration
preferences_bp = Blueprint('preferences', __name__, url_prefix='/preferences')

def get_default_preferences():
    return {'vibes': ['adventure', 'foodie', 'explorer'], 'interests': ['beaches', 'nature', 'food', 'photography', 'adventure', 'cafes'], 'budget_tier': 'standard', 'stay_type': '3_star', 'diet': 'no_preference', 'dining': ['local_food', 'street_food', 'cafes']}

@preferences_bp.route('', methods=['GET', 'POST'])
@preferences_bp.route('/', methods=['GET', 'POST'])
def preferences_view():
    selected_slugs = session.get('selected_destinations', [])
    if not selected_slugs:
        flash('Please select at least 1 destination before setting preferences.', 'warning')
        return redirect(url_for('destinations.list_destinations'))
    trip_details = session.get('trip_details', {})
    departure_date = trip_details.get('departure_date', '').strip() if isinstance(trip_details, dict) else ''
    if not departure_date:
        flash('Please select a trip start date before setting preferences.', 'warning')
        return redirect(url_for('destinations.list_destinations'))
    if request.method == 'POST':
        vibes = request.form.getlist('vibe') or ['adventure', 'explorer']
        interests = request.form.getlist('interest') or ['nature', 'food', 'photography']
        budget_tier = request.form.get('budget', 'standard').strip()
        stay_type = request.form.get('stay', '3_star').strip()
        diet = request.form.get('diet', 'no_preference').strip()
        dining = request.form.getlist('dining') or ['local_food', 'cafes']
        session['preferences'] = {'vibes': vibes, 'interests': interests, 'budget_tier': budget_tier, 'stay_type': stay_type, 'diet': diet, 'dining': dining}
        session.modified = True
        flash('Preferences saved! Your personalized itinerary has been crafted.', 'success')
        return redirect(url_for('itinerary.itinerary_view'))
    preferences = session.get('preferences')
    if not preferences:
        preferences = get_default_preferences()
        session['preferences'] = preferences
        session.modified = True
    trip_details = session.get('trip_details', {'start_location': '', 'departure_date': '', 'return_date': '', 'travellers': 4})
    selected_dest_objects = [get_destination_by_slug(s) for s in selected_slugs if get_destination_by_slug(s)]
    suggested_total_days = sum((d.get('suggested_days', 3) for d in selected_dest_objects))
    if suggested_total_days < 2:
        suggested_total_days = 2
    dep_date = trip_details.get('departure_date', '')
    ret_date = trip_details.get('return_date', '')
    start_d, end_d, computed_days, _ = parse_dates_and_duration(dep_date, ret_date, default_days=suggested_total_days)
    if start_d:
        dates_range_display = f"{start_d.strftime('%d %b')} – {end_d.strftime('%d %b %Y')}"
    else:
        dates_range_display = f'{computed_days} Days / {max(1, computed_days - 1)} Nights'
    travellers = max(1, int(trip_details.get('travellers', 4)))
    avg_base_rate = sum((d.get('base_cost_per_day', 3000) for d in selected_dest_objects)) / len(selected_dest_objects) if selected_dest_objects else 3000
    stay_multipliers = {'hostel': 0.7, 'budget_hotel': 0.85, '3_star': 1.0, '4_star': 1.4, '5_star': 2.2}
    stay_mult = stay_multipliers.get(preferences.get('stay_type', '3_star'), 1.0)
    dining_list = preferences.get('dining', [])
    dining_mult = 1.0 + (0.12 if 'fine_dining' in dining_list else 0.0) - (0.04 if 'street_food' in dining_list else 0.0)
    tier_multipliers = {'budget': 0.75, 'standard': 1.0, 'premium': 1.35, 'luxury': 2.1}
    tier_estimates = {}
    for tier_code, tier_mult in tier_multipliers.items():
        comp_mult = tier_mult * 0.6 + stay_mult * 0.4
        raw_total = avg_base_rate * computed_days * travellers * comp_mult * dining_mult
        t_cost = max(5000, int(round(raw_total / 100.0) * 100))
        t_lower = int(round(t_cost * 0.88 / 100.0) * 100)
        t_upper = int(round(t_cost * 1.15 / 100.0) * 100)
        t_person = int(round(t_cost / travellers))
        tier_estimates[tier_code] = {'total': t_cost, 'total_display': f'{t_cost:,}', 'lower': t_lower, 'lower_display': f'{t_lower:,}', 'upper': t_upper, 'upper_display': f'{t_upper:,}', 'per_person': t_person, 'per_person_display': f'{t_person:,}'}
    current_budget_code = preferences.get('budget_tier', 'standard')
    current_estimate = tier_estimates.get(current_budget_code, tier_estimates['standard'])
    return render_template('preferences.html', preferences=preferences, trip_details=trip_details, selected_dest_objects=selected_dest_objects, computed_days=computed_days, dates_range_display=dates_range_display, avg_base_rate=avg_base_rate, travellers=travellers, tier_estimates=tier_estimates, current_estimate=current_estimate)
