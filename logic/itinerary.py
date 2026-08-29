from datetime import datetime, timedelta
import math
from data.destinations import get_destination_by_slug, get_all_destinations
from data.stays_and_food import get_suggested_stay, get_suggested_restaurant
from data.destination_insights import get_all_destination_insights
from data.transportation import get_transport_db_entry, get_destination_attractions, select_best_transport, calculate_group_transport_cost

def parse_dates_and_duration(departure_str, return_str, default_days=4):
    start_date = None
    end_date = None
    if departure_str and departure_str.strip():
        try:
            start_date = datetime.strptime(departure_str.strip(), '%Y-%m-%d')
            if return_str and return_str.strip():
                try:
                    end_date = datetime.strptime(return_str.strip(), '%Y-%m-%d')
                    if end_date < start_date:
                        end_date = start_date + timedelta(days=default_days - 1)
                    num_days = max(1, (end_date - start_date).days + 1)
                except ValueError:
                    end_date = start_date + timedelta(days=default_days - 1)
                    num_days = default_days
            else:
                end_date = start_date + timedelta(days=default_days - 1)
                num_days = default_days
        except ValueError:
            start_date = None
            end_date = None
            num_days = max(1, default_days)
    else:
        num_days = max(1, default_days)
    num_nights = max(1, num_days - 1)
    return (start_date, end_date, num_days, num_nights)

def get_stay_display_name(stay_code):
    mapping = {'hostel': 'Backpacker Hostel', 'budget_hotel': 'Budget Hotel', '3_star': '3-Star Hotel', '4_star': '4-Star Resort', '5_star': '5-Star Luxury Stay'}
    return mapping.get(stay_code, '3-Star Hotel')

def get_budget_display_name(budget_code):
    mapping = {'budget': 'Budget / Backpacker', 'standard': 'Comfort', 'comfort': 'Comfort', 'premium': 'Premium', 'luxury': 'Luxury'}
    return mapping.get(budget_code, 'Comfort')

def get_diet_display_name(diet_code):
    mapping = {'no_preference': 'No Preference', 'vegetarian': 'Vegetarian', 'non_vegetarian': 'Non-Vegetarian', 'vegan': 'Vegan'}
    return mapping.get(diet_code, 'No Preference')

def get_daily_food_rate(budget_tier, dining_prefs, diet):
    tier = (budget_tier or 'standard').lower()
    if tier in ['budget', 'backpacker']:
        base = 400
    elif tier in ['premium', 'luxury']:
        base = 1500
    else:
        base = 800
    if 'fine_dining' in dining_prefs:
        base += 250
    if 'street_food' in dining_prefs and tier != 'budget':
        base -= 100
    return max(300, base)

def generate_itinerary(selected_slugs, preferences=None, trip_details=None, modifier='normal'):
    if not selected_slugs:
        selected_slugs = ['jaipur']
    preferences = preferences or {}
    trip_details = trip_details or {}
    departure_str = trip_details.get('departure_date', '')
    return_str = trip_details.get('return_date', '')
    travellers = max(1, int(trip_details.get('travellers', 4)))
    start_location = trip_details.get('start_location', '').strip()
    vibes = preferences.get('vibes', [])
    interests = preferences.get('interests', [])
    budget_tier = preferences.get('budget_tier', 'standard').lower()
    if budget_tier == 'standard':
        budget_tier = 'comfort'
    stay_type = preferences.get('stay_type', '3_star')
    diet = preferences.get('diet', 'no_preference')
    dining = preferences.get('dining', [])
    dest_objects = []
    for slug in selected_slugs:
        d = get_destination_by_slug(slug)
        if d:
            d_copy = d.copy()
            d_copy['suggested_stay'] = get_suggested_stay(slug, budget_tier, stay_type)
            d_copy['suggested_restaurant'] = get_suggested_restaurant(slug, budget_tier, diet)
            dest_objects.append(d_copy)
    if not dest_objects:
        all_d = get_all_destinations()
        d0 = all_d[0].copy()
        d0['suggested_stay'] = get_suggested_stay(d0['slug'], budget_tier, stay_type)
        d0['suggested_restaurant'] = get_suggested_restaurant(d0['slug'], budget_tier, diet)
        dest_objects = [d0]
    suggested_total_days = sum((d.get('suggested_days', 3) for d in dest_objects))
    if suggested_total_days < 1:
        suggested_total_days = 3
    start_date, end_date, total_days, total_nights = parse_dates_and_duration(departure_str, return_str, default_days=suggested_total_days)
    num_dests = len(dest_objects)
    base_days_per_dest = max(1, total_days // num_dests)
    remainder = total_days % num_dests
    destination_days_map = []
    for i, dest in enumerate(dest_objects):
        alloc_days = base_days_per_dest + (1 if i < remainder else 0)
        for d_num in range(1, alloc_days + 1):
            destination_days_map.append({'destination': dest, 'dest_day_index': d_num, 'dest_total_days': alloc_days, 'is_dest_first_day': d_num == 1, 'is_dest_last_day': d_num == alloc_days})
    destination_days_map = destination_days_map[:total_days]
    daily_food_per_person = get_daily_food_rate(budget_tier, dining, diet)
    daily_food_group = daily_food_per_person * travellers
    days_itinerary = []
    trip_total_transport = 0
    trip_total_food = 0
    trip_total_activities = 0
    for day_idx, item in enumerate(destination_days_map, start=1):
        dest = item['destination']
        dest_slug = dest.get('slug', 'jaipur')
        dest_day = item['dest_day_index']
        stay = dest.get('suggested_stay')
        restaurant = dest.get('suggested_restaurant')
        stay_name = stay['name'] if stay else get_stay_display_name(stay_type)
        stay_area = f" ({stay['area']})" if stay and stay.get('area') else ''
        rest_name = restaurant['name'] if restaurant else 'Local Culinary Spot'
        rest_area = f" ({restaurant['area']})" if restaurant and restaurant.get('area') else ''
        if start_date:
            current_date = start_date + timedelta(days=day_idx - 1)
            date_str = current_date.strftime('%d %b %Y')
        else:
            date_str = f'Day {day_idx} of {total_days}'
        attractions_list = get_destination_attractions(dest_slug)
        offset = (dest_day - 1) * 3 % max(1, len(attractions_list))
        day_attractions = []
        for k in range(3):
            att_idx = (offset + k) % len(attractions_list)
            day_attractions.append(attractions_list[att_idx])
        morning_att = day_attractions[0]
        afternoon_att = day_attractions[1]
        evening_att = day_attractions[2]
        transit_1 = select_best_transport(dest_slug=dest_slug, from_place=stay_name, to_place=morning_att['name'], budget_tier=budget_tier, travellers=travellers, is_walkable=stay_name in morning_att.get('walkable_to', []), special_transport=morning_att.get('special_transport'), modifier=modifier)
        is_m_to_a_walk = afternoon_att['name'] in morning_att.get('walkable_to', []) or (morning_att.get('cluster') == afternoon_att.get('cluster') and modifier in ['budget', 'cheaper'])
        transit_2 = select_best_transport(dest_slug=dest_slug, from_place=morning_att['name'], to_place=afternoon_att['name'], budget_tier=budget_tier, travellers=travellers, is_walkable=is_m_to_a_walk, special_transport=afternoon_att.get('special_transport'), modifier=modifier)
        is_a_to_e_walk = evening_att['name'] in afternoon_att.get('walkable_to', [])
        transit_3 = select_best_transport(dest_slug=dest_slug, from_place=afternoon_att['name'], to_place=evening_att['name'], budget_tier=budget_tier, travellers=travellers, is_walkable=is_a_to_e_walk, special_transport=evening_att.get('special_transport'), modifier=modifier)
        ticket_morning = morning_att.get('ticket_inr', 0) * travellers
        ticket_afternoon = afternoon_att.get('ticket_inr', 0) * travellers
        ticket_evening = evening_att.get('ticket_inr', 0) * travellers
        day_ticket_cost = ticket_morning + ticket_afternoon + ticket_evening
        day_transit_cost = transit_1['group_cost'] + transit_2['group_cost'] + transit_3['group_cost']
        day_total_cost = day_transit_cost + daily_food_group + day_ticket_cost
        trip_total_transport += day_transit_cost
        trip_total_food += daily_food_group
        trip_total_activities += day_ticket_cost
        if day_idx == 1 and total_days > 1:
            day_title = f"Arrival & Discovery in {dest['name']}"
        elif day_idx == total_days and total_days > 1:
            day_title = f"Signature Sights & Farewell in {dest['name']}"
        else:
            day_title = f"{morning_att['name']} & {evening_att['name']}"
        location_label = f"{dest['name']}, {dest['state']}"
        slots = [{'slot_name': 'Morning', 'slot_time': '09:00 AM – 12:30 PM', 'attraction_name': morning_att['name'], 'desc': morning_att.get('desc', ''), 'ticket_display': f"₹{morning_att.get('ticket_inr', 0)}/person (Group: ₹{ticket_morning})" if morning_att.get('ticket_inr', 0) > 0 else 'Free Entry', 'transit': transit_1}, {'slot_name': 'Afternoon', 'slot_time': '01:00 PM – 04:30 PM', 'attraction_name': afternoon_att['name'], 'desc': afternoon_att.get('desc', ''), 'ticket_display': f"₹{afternoon_att.get('ticket_inr', 0)}/person (Group: ₹{ticket_afternoon})" if afternoon_att.get('ticket_inr', 0) > 0 else 'Free Entry', 'lunch_recommendation': f'Lunch at {rest_name}{rest_area}: {get_meal_recommendation(dest, diet, dining)}', 'transit': transit_2}, {'slot_name': 'Evening', 'slot_time': '05:00 PM – 08:30 PM', 'attraction_name': evening_att['name'], 'desc': evening_att.get('desc', ''), 'ticket_display': f"₹{evening_att.get('ticket_inr', 0)}/person (Group: ₹{ticket_evening})" if evening_att.get('ticket_inr', 0) > 0 else 'Free Entry', 'dinner_recommendation': f"Evening dinner & sunset stroll around {dest['name']}", 'transit': transit_3}]
        days_itinerary.append({'day_num': day_idx, 'date_str': date_str, 'day_title': day_title, 'location_label': location_label, 'slots': slots, 'suggested_stay': stay, 'suggested_restaurant': restaurant, 'day_cost': {'transport': day_transit_cost, 'food': daily_food_group, 'activities': day_ticket_cost, 'total': day_total_cost, 'total_display': f'₹{day_total_cost:,}', 'per_person_display': f'₹{int(round(day_total_cost / travellers)):,}'}})
    trip_total_misc = int(round((trip_total_transport + trip_total_food + trip_total_activities) * 0.1))
    overall_total_cost = trip_total_transport + trip_total_food + trip_total_activities + trip_total_misc
    cost_per_person = int(round(overall_total_cost / travellers))
    benchmark_rates = {'budget': 1600, 'comfort': 2800, 'premium': 5200, 'luxury': 8500}
    tier_benchmark_pp = benchmark_rates.get(budget_tier, 2800) * total_days
    tier_benchmark_group = tier_benchmark_pp * travellers
    ratio = overall_total_cost / max(1, tier_benchmark_group)
    if ratio <= 1.05:
        budget_status = 'within'
        budget_status_label = '🟢 Within Budget'
        budget_status_class = 'status-green'
    elif ratio <= 1.25:
        budget_status = 'slight_above'
        budget_status_label = '🟡 Slightly Above Budget'
        budget_status_class = 'status-yellow'
    else:
        budget_status = 'over'
        budget_status_label = '🔴 Over Budget'
        budget_status_class = 'status-red'
    budget_protection_active = False
    budget_protection_msg = ''
    if ratio > 1.2 and budget_tier == 'budget':
        budget_protection_active = True
        budget_protection_msg = 'Your selected budget may not be sufficient for this itinerary. We have created the closest affordable plan with budget buses & public transport, and highlighted where additional spending may be required.'
    dest_names = ' + '.join([d['name'] for d in dest_objects])
    trip_type_display = {'budget': 'Budget Explorer', 'comfort': 'Comfort Traveler', 'premium': 'Premium Traveler', 'luxury': 'Luxury Experience'}.get(budget_tier, 'Comfort Traveler')
    dates_range_display = f"{start_date.strftime('%d %b')} – {end_date.strftime('%d %b %Y')}" if start_date else f'{total_days} Days · {total_nights} Nights'
    summary = {'destinations_display': dest_names, 'duration_display': f'{total_days} Days / {total_nights} Nights', 'total_days': total_days, 'total_nights': total_nights, 'travellers': travellers, 'travelers_count': travellers, 'travelers_display': f'{travellers} People' if travellers != 1 else '1 Person', 'start_location': start_location or 'Flexible Starting Hub', 'dates_range_display': dates_range_display, 'budget_tier': budget_tier, 'trip_type_display': trip_type_display, 'trip_style_display': f"{(vibes[0].title() if vibes else 'Explorer')} / {trip_type_display}", 'experience_display': ' & '.join(interests[:2]).title() if interests else 'Sightseeing', 'estimated_budget_display': f'₹{overall_total_cost:,}', 'food_display': get_diet_display_name(diet), 'hotel_display': get_stay_display_name(stay_type), 'active_modifier': modifier}
    budget_summary = {'transportation': trip_total_transport, 'transportation_display': f'₹{trip_total_transport:,}', 'food': trip_total_food, 'food_display': f'₹{trip_total_food:,}', 'activities': trip_total_activities, 'activities_display': f'₹{trip_total_activities:,}', 'other': trip_total_misc, 'other_display': f'₹{trip_total_misc:,}', 'total_cost': overall_total_cost, 'total_cost_display': f'₹{overall_total_cost:,}', 'per_person': cost_per_person, 'per_person_display': f'₹{cost_per_person:,}', 'status': budget_status, 'status_label': budget_status_label, 'status_class': budget_status_class, 'protection_active': budget_protection_active, 'protection_msg': budget_protection_msg}
    return {'summary': summary, 'days': days_itinerary, 'destinations': dest_objects, 'destination_insights': get_all_destination_insights(selected_slugs), 'budget_summary': budget_summary}

def get_meal_recommendation(dest, diet, dining):
    slug = dest.get('slug', '')
    if diet == 'vegetarian' or diet == 'vegan':
        veg_dishes = {'goa': 'Goan vegetable caldin & poi bread with fresh sol kadhi', 'munnar': 'Authentic Kerala sadhya served on banana leaf', 'manali': 'Hot Himachali siddu with pure ghee and dal', 'jaipur': 'Royal Rajasthani Dal Baati Churma & Gatte ki Sabzi', 'kashmir': 'Kashmiri Dum Aloo, Nadru Yakhni & saffron Kahwa', 'gokarna': 'Coastal temple meals & avocado toasts at beach shacks', 'ooty': 'Fresh Nilgiri tea, piping hot sambar vadas & homemade chocolates', 'hampi': 'South Indian unlimited thali with freshly baked woodfired pizzas', 'rishikesh': 'Ayurvedic sattvic organic bowl & masala chai', 'udaipur': 'Mewari ker sangri, missi roti & rabdi', 'varkala': 'Fresh coconut curry, appam, and fresh fruit bowls', 'coorg': 'Bamboo shoot curry (Baimbale) & rice akki roti', 'pondicherry': 'French croissant, café au lait & crepes in White Town', 'mumbai': 'Iconic Pav Bhaji, Bhel Puri, and Bombay sandwich', 'hyderabad': 'Authentic Hyderabadi Veg Dum Biryani & Mirchi ka Salan', 'varanasi': 'Kashi Kachori Sabzi, Malaiyo & Banarasi Paan', 'bangalore': 'Crispy Masala Dosa, filter coffee & Bisibelebath', 'chandigarh': 'Piping hot Chole Bhature, Amritsari Kulcha & sweet Lassi', 'jodhpur': 'Pyaaz Ki Kachori, Mirchi Vada & Mawa Kachori', 'kerala': 'Appam with vegetable stew & traditional sadhya', 'mahabaleshwar': 'Fresh strawberry with fresh cream & corn pattice', 'mussoorie': 'Steaming vegetable momos, Maggi & Landour apple pie', 'kolkata': 'Luchi with Chholar Dal, Radhabhallavi & Mishti Doi', 'andaman-nicobar': 'Fresh coconut water, tropical fruit salads & South Indian thali', 'pune': 'Pithla Bhakri, Bun Maska Chai & SPDP chaat', 'mysore': 'Mylari Butter Dosa, Kesari Bath & hot filter coffee'}
        return veg_dishes.get(slug, 'Traditional pure-vegetarian regional thali')
    else:
        non_veg_dishes = {'goa': 'Authentic Goan Fish Curry, Prawn Balchão & Kingfish Fry', 'munnar': 'Malabar Chicken Curry with flaky Kerala parottas', 'manali': 'Himachali Trout Fish fry with mint chutney', 'jaipur': 'Royal Laal Maas & Keema Baati', 'kashmir': 'Traditional Wazwan Rogan Josh, Gushtaba & Rista', 'gokarna': 'Fresh coastal butter garlic prawns & seafood thali', 'ooty': 'Badaga chicken curry & spiced mutton biryani', 'hampi': 'Riverside grilled fish & woodfired chicken pizzas', 'rishikesh': 'Organic valley salad, woodfired pizzas & herbal teas', 'udaipur': 'Mewari Junglee Maas & royal mutton curries', 'varkala': 'Karimeen Pollichathu (pearl spot fish wrapped in banana leaf)', 'coorg': 'Famous Kodava Pandi Curry & Koli curry with Kadambuttu', 'pondicherry': 'French Poulet Rôti & Creole seafood bouillabaisse', 'mumbai': 'Bombil Fry, Crab masala & authentic Bohri Biryani', 'hyderabad': 'World-famous Hyderabadi Mutton Dum Biryani & Haleem', 'varanasi': 'Mughlai seekh kebabs & spicy mutton curry', 'bangalore': 'Guntur chicken fry, mutton biryani & craft beer', 'chandigarh': 'Butter Chicken with garlic naan & tandoori chicken', 'jodhpur': 'Junglee Maas, Laal Maas & spicy mutton chops', 'kerala': 'Kerala fish moilee, beef fry & Malabar biryani', 'mahabaleshwar': 'Spicy Malvani mutton curry & fried fish', 'mussoorie': 'Tibetan chicken momos, thukpa & Landour roast chicken', 'kolkata': 'Kolkata Mutton Biryani, Kosha Mangsho & Mustard Ilish', 'andaman-nicobar': 'Grilled lobster, butter garlic crab & red snapper fry', 'pune': 'Chicken Sukka, Kolhapuri Tambda-Pandhra Rassa', 'mysore': 'Mysore mutton biryani & Andhra chilli chicken'}
        return non_veg_dishes.get(slug, 'Regional specialty curries and fresh local delicacies')
