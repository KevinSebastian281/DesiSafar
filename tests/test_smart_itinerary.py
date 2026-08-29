import pytest
import math
from app import app
from data.transportation import TRANSPORTATION_DATABASE, DESTINATION_ATTRACTIONS, calculate_group_transport_cost, select_best_transport, get_transport_db_entry, get_destination_attractions
from logic.itinerary import generate_itinerary

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-desi-safar'
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess.clear()
        yield client
SPECIFIED_18_DESTINATIONS = ['jaipur', 'bangalore', 'chandigarh', 'coorg', 'goa', 'jodhpur', 'kerala', 'mahabaleshwar', 'mussoorie', 'munnar', 'kolkata', 'ooty', 'andaman-nicobar', 'mumbai', 'pune', 'mysore', 'rishikesh', 'varanasi']

def test_all_18_destinations_present_in_database():
    for slug in SPECIFIED_18_DESTINATIONS:
        assert slug in TRANSPORTATION_DATABASE, f'Missing transportation data for {slug}'
        db_entry = TRANSPORTATION_DATABASE[slug]
        modes = [v for k, v in db_entry.items() if isinstance(v, dict)]
        assert len(modes) >= 3, f'{slug} has fewer than 3 transit modes'
        assert slug in DESTINATION_ATTRACTIONS, f'Missing attraction clusters for {slug}'
        attractions = DESTINATION_ATTRACTIONS[slug]
        assert len(attractions) >= 3, f'{slug} has fewer than 3 attractions'
        for att in attractions:
            assert 'name' in att
            assert 'cluster' in att
            assert 'ticket_inr' in att

def test_rishikesh_has_unique_transportation_values():
    rishikesh_data = TRANSPORTATION_DATABASE['rishikesh']
    mysore_data = TRANSPORTATION_DATABASE['mysore']
    assert rishikesh_data != mysore_data, 'Rishikesh transportation data matches Mysore!'
    rishikesh_modes = [v for k, v in rishikesh_data.items() if isinstance(v, dict)]
    mode_names = [m.get('name', '') for m in rishikesh_modes]
    assert any(('Vikram' in name or 'Shared' in name for name in mode_names)), 'Rishikesh missing Vikram/Shared transport'
    assert any(('Auto' in name for name in mode_names)), 'Rishikesh missing Auto Rickshaw'
    assert any(('Cab' in name or 'Taxi' in name for name in mode_names)), 'Rishikesh missing Cab'
    mysore_modes = [v for k, v in mysore_data.items() if isinstance(v, dict)]
    mysore_names = [m.get('name', '') for m in mysore_modes]
    assert any(('KSRTC' in name or 'Mysore' in name for name in mysore_names))

def test_group_transport_cost_private_vehicle_vs_per_person():
    cab_mode = {'name': 'Private Sedan Cab', 'fare_inr': 350, 'unit': 'per_vehicle', 'capacity': 4}
    cost_1 = calculate_group_transport_cost(cab_mode, travellers=1)
    assert cost_1['total_group_cost'] == 350
    assert cost_1['fare_per_person'] == 350
    cost_4 = calculate_group_transport_cost(cab_mode, travellers=4)
    assert cost_4['total_group_cost'] == 350
    assert cost_4['fare_per_person'] == 88
    cost_5 = calculate_group_transport_cost(cab_mode, travellers=5)
    assert cost_5['total_group_cost'] == 700
    assert cost_5['vehicles_needed'] == 2
    cost_8 = calculate_group_transport_cost(cab_mode, travellers=8)
    assert cost_8['total_group_cost'] == 700
    assert cost_8['vehicles_needed'] == 2
    cost_9 = calculate_group_transport_cost(cab_mode, travellers=9)
    assert cost_9['total_group_cost'] == 1050
    assert cost_9['vehicles_needed'] == 3

def test_group_transport_cost_per_person_unit():
    bus_mode = {'name': 'City Local Bus', 'fare_inr': 25, 'unit': 'per_person', 'capacity': 50}
    assert calculate_group_transport_cost(bus_mode, travellers=1)['total_group_cost'] == 25
    assert calculate_group_transport_cost(bus_mode, travellers=4)['total_group_cost'] == 100
    assert calculate_group_transport_cost(bus_mode, travellers=10)['total_group_cost'] == 250

def test_different_budgets_generate_different_itineraries():
    trip = {'departure_date': '2026-11-01', 'return_date': '2026-11-03', 'travellers': 4}
    itin_budget = generate_itinerary(selected_slugs=['jaipur'], preferences={'budget_tier': 'budget', 'stay_type': 'hostel', 'diet': 'vegetarian'}, trip_details=trip)
    itin_comfort = generate_itinerary(selected_slugs=['jaipur'], preferences={'budget_tier': 'comfort', 'stay_type': '3_star', 'diet': 'vegetarian'}, trip_details=trip)
    itin_premium = generate_itinerary(selected_slugs=['jaipur'], preferences={'budget_tier': 'premium', 'stay_type': '4_star', 'diet': 'vegetarian'}, trip_details=trip)
    cost_b = itin_budget['budget_summary']['total_cost']
    cost_c = itin_comfort['budget_summary']['total_cost']
    cost_p = itin_premium['budget_summary']['total_cost']
    assert cost_b < cost_c < cost_p, f'Budget ordering failed: {cost_b} < {cost_c} < {cost_p}'
    day1_b_transit = itin_budget['days'][0]['slots'][0]['transit']
    day1_p_transit = itin_premium['days'][0]['slots'][0]['transit']
    assert day1_b_transit['mode'] in ['bus', 'auto', 'walking']
    assert day1_p_transit['mode'] in ['cab', 'special']

def test_day_slots_contain_morning_afternoon_evening_and_transport():
    itin = generate_itinerary(selected_slugs=['goa'], preferences={'budget_tier': 'comfort', 'stay_type': '3_star', 'diet': 'non_vegetarian'}, trip_details={'departure_date': '2026-11-01', 'return_date': '2026-11-03', 'travellers': 2})
    for day in itin['days']:
        slots = day['slots']
        assert len(slots) == 3
        slot_names = [s['slot_name'] for s in slots]
        assert slot_names == ['Morning', 'Afternoon', 'Evening']
        for s in slots:
            assert s['attraction_name']
            assert s['desc']
            assert 'ticket_display' in s
            assert 'transit' in s
            t = s['transit']
            assert 'provider' in t
            assert 'route_text' in t
            assert 'group_cost' in t
            assert 'fare_display' in t
            assert 'tag' in t
        assert 'day_cost' in day
        assert day['day_cost']['total'] > 0
        assert day['day_cost']['transport'] >= 0
        assert day['day_cost']['food'] > 0

def test_smart_alternative_modifiers():
    trip = {'departure_date': '2026-11-01', 'return_date': '2026-11-03', 'travellers': 4}
    pref = {'budget_tier': 'comfort', 'stay_type': '3_star', 'diet': 'no_preference'}
    normal = generate_itinerary(['jaipur'], pref, trip, modifier='normal')
    cheaper = generate_itinerary(['jaipur'], pref, trip, modifier='cheaper')
    comfortable = generate_itinerary(['jaipur'], pref, trip, modifier='comfortable')
    cost_normal = normal['budget_summary']['total_cost']
    cost_cheaper = cheaper['budget_summary']['total_cost']
    cost_comfortable = comfortable['budget_summary']['total_cost']
    assert cost_cheaper <= cost_normal
    assert cost_comfortable >= cost_normal

def test_budget_protection_logic():
    trip = {'departure_date': '2026-11-01', 'return_date': '2026-11-06', 'travellers': 2}
    pref = {'budget_tier': 'budget', 'stay_type': 'hostel', 'diet': 'no_preference'}
    andaman_itin = generate_itinerary(['andaman-nicobar'], pref, trip)
    if andaman_itin['budget_summary']['protection_active']:
        assert 'Your selected budget may not be sufficient for this itinerary' in andaman_itin['budget_summary']['protection_msg']

def test_itinerary_page_renders_with_rich_components(client):
    client.get('/reset')
    client.post('/destinations/toggle', data={'slug': 'jaipur'})
    client.post('/destinations/update_trip', data={'departure_date': '2026-11-01', 'return_date': '2026-11-03', 'travellers': '4', 'start_location': 'Delhi'})
    client.post('/preferences', data={'vibe': ['culture', 'heritage'], 'interest': ['monuments', 'food'], 'budget': 'standard', 'stay': '3_star', 'diet': 'vegetarian', 'dining': ['local_food', 'street_food']}, follow_redirects=True)
    res = client.get('/itinerary')
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert 'Your DesiSafar Plan' in html
    assert 'Jaipur' in html
    assert '4 Travelers' in html or '4 Traveler' in html
    assert 'Make It Cheaper' in html
    assert 'Make It More Comfortable' in html
    assert 'Optimize Route' in html
    assert 'Edit Trip' in html
    assert 'Morning' in html
    assert 'Afternoon' in html
    assert 'Evening' in html
    assert 'Estimated Fare:' in html
    assert 'Group Cost:' in html
    assert 'Estimated Cost:' in html
    assert 'Trip Budget Summary' in html
    assert 'Transportation:' in html
    assert 'Food &amp; Dining:' in html or 'Food & Dining:' in html
    assert 'Activities &amp; Entry:' in html or 'Activities & Entry:' in html
    assert 'Total Estimated Trip Cost:' in html
    assert 'Estimated Cost Per Person:' in html
    assert 'Budget' in html

def test_itinerary_modifier_post_action(client):
    client.get('/reset')
    client.post('/destinations/toggle', data={'slug': 'rishikesh'})
    client.post('/destinations/update_trip', data={'departure_date': '2026-11-01', 'return_date': '2026-11-03', 'travellers': '2', 'start_location': 'Dehradun'})
    client.post('/preferences', data={'vibe': ['spiritual', 'adventure'], 'budget': 'standard', 'stay': '3_star', 'diet': 'vegetarian'}, follow_redirects=True)
    res_cheap = client.post('/itinerary', data={'action': 'cheaper'}, follow_redirects=True)
    assert res_cheap.status_code == 200
    html_cheap = res_cheap.get_data(as_text=True)
    assert 'economical' in html_cheap.lower() or 'cheaper' in html_cheap.lower() or 'Vikram' in html_cheap or ('Bus' in html_cheap) or ('Walk' in html_cheap)

def test_itinerary_generation_for_all_18_destinations_across_tiers():
    for slug in SPECIFIED_18_DESTINATIONS:
        for tier in ['budget', 'comfort', 'premium']:
            res = generate_itinerary(selected_slugs=[slug], preferences={'budget_tier': tier, 'stay_type': '3_star', 'diet': 'no_preference'}, trip_details={'departure_date': '2026-11-01', 'return_date': '2026-11-03', 'travellers': 3})
            assert len(res['days']) >= 2
            assert res['budget_summary']['total_cost'] > 0
            assert res['budget_summary']['per_person'] > 0
            assert res['budget_summary']['status'] in ['within', 'slight_above', 'over']
            for day in res['days']:
                assert len(day['slots']) == 3
                for slot in day['slots']:
                    assert slot['transit']['provider']
                    assert slot['transit']['group_cost'] >= 0

def test_solo_traveler_itinerary_math():
    res = generate_itinerary(selected_slugs=['mumbai'], preferences={'budget_tier': 'comfort', 'stay_type': '3_star', 'diet': 'vegetarian'}, trip_details={'departure_date': '2026-11-01', 'return_date': '2026-11-03', 'travellers': 1})
    assert res['summary']['travellers'] == 1
    assert res['budget_summary']['total_cost'] == res['budget_summary']['per_person']
    for day in res['days']:
        assert day['day_cost']['total'] > 0

def test_large_group_capacity_multi_vehicle_math():
    cab_mode = {'name': 'Sedan Cab', 'fare_inr': 400, 'unit': 'per_vehicle', 'capacity': 4}
    cost = calculate_group_transport_cost(cab_mode, travellers=14)
    assert cost['vehicles_needed'] == 4
    assert cost['total_group_cost'] == 1600

def test_multi_destination_composite_itinerary():
    res = generate_itinerary(selected_slugs=['jaipur', 'jodhpur', 'varanasi'], preferences={'budget_tier': 'comfort', 'stay_type': '3_star', 'diet': 'vegetarian'}, trip_details={'departure_date': '2026-11-01', 'return_date': '2026-11-07', 'travellers': 4})
    assert res['summary']['total_days'] == 7
    dest_names = [d['name'] for d in res['destinations']]
    assert 'Jaipur' in dest_names
    assert 'Jodhpur' in dest_names
    assert 'Varanasi' in dest_names

def test_driver_and_vehicle_details_presence():
    from data.transportation import get_driver_and_cab_details
    for slug in ['jaipur', 'rishikesh', 'munnar', 'goa', 'mumbai', 'bangalore', 'kerala', 'varanasi']:
        driver = get_driver_and_cab_details(slug, route_text='Hotel → Monument')
        assert 'driver_name' in driver
        assert 'driver_phone' in driver
        assert 'car_model' in driver
        assert 'car_number' in driver
        assert 'otp' in driver
        assert driver['driver_rating'] >= 4.0
        assert len(driver['car_number']) >= 8

def test_driver_modal_and_data_attributes_rendered_in_html(client):
    client.post('/destinations/toggle', data={'slug': 'jaipur'})
    client.post('/destinations/update_trip', data={'departure_date': '2026-11-01', 'return_date': '2026-11-03', 'travellers': '4'})
    client.post('/preferences', data={'budget': 'premium'})
    res = client.get('/itinerary')
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert 'id="driverModalOverlay"' in html
    assert 'data-has-driver="true"' in html
    assert 'data-car-plate=' in html
    assert 'data-driver-name=' in html
    assert 'RJ 14 TA 8421' in html or 'Rajesh' in html

def test_hidden_spots_and_famous_food_data():
    from data.destination_insights import get_destination_insights, get_all_destination_insights
    for slug in ['jaipur', 'goa', 'rishikesh', 'munnar', 'mumbai', 'varanasi', 'kerala']:
        insights = get_destination_insights(slug)
        assert insights['name']
        assert len(insights['hidden_spots']) >= 2
        assert len(insights['famous_food']) >= 2
        spot = insights['hidden_spots'][0]
        assert 'name' in spot
        assert 'badge' in spot
        assert 'description' in spot
        assert 'best_time' in spot
        assert 'local_tip' in spot
        food = insights['famous_food'][0]
        assert 'dish' in food
        assert 'diet_type' in food
        assert 'description' in food
        assert 'famous_spot' in food
        assert 'foodie_tip' in food

def test_destination_insights_rendered_in_itinerary_html(client):
    client.post('/destinations/toggle', data={'slug': 'jaipur'})
    client.post('/destinations/update_trip', data={'departure_date': '2026-11-01', 'return_date': '2026-11-03', 'travellers': '4'})
    client.post('/preferences', data={'budget': 'comfort'})
    res = client.get('/itinerary')
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert 'destination-insights-section' in html
    assert 'Hidden Spots &amp; Famous Food' in html or 'Hidden Spots' in html
    assert 'Secret Hidden Spots' in html
    assert 'Famous Food &amp; Must-Try Joints' in html
    assert 'Panna Meena Ka Kund' in html or 'Pyaaz Kachori' in html
