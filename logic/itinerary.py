"""
Itinerary generation engine for DesiSafar.
Rule-based dynamic multi-day itinerary builder based on selected destinations,
dates, travel style, and preferences. Zero JavaScript server-side generation.
"""

from datetime import datetime, timedelta
from data.destinations import get_destination_by_slug, get_all_destinations
from data.stays_and_food import get_suggested_stay, get_suggested_restaurant


def parse_dates_and_duration(departure_str, return_str, default_days=4):
    """
    Parse departure and return date strings.
    If departure date is empty, returns None for dates and uses default_days
    (calculated from the sum of suggested days of selected places).
    """
    start_date = None
    end_date = None

    if departure_str and departure_str.strip():
        try:
            start_date = datetime.strptime(departure_str.strip(), "%Y-%m-%d")
            if return_str and return_str.strip():
                try:
                    end_date = datetime.strptime(return_str.strip(), "%Y-%m-%d")
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
    return start_date, end_date, num_days, num_nights


def get_stay_display_name(stay_code):
    mapping = {
        "hostel": "Backpacker Hostel",
        "budget_hotel": "Budget Hotel",
        "3_star": "3-Star Hotel",
        "4_star": "4-Star Resort",
        "5_star": "5-Star Luxury Stay",
    }
    return mapping.get(stay_code, "3-Star Hotel")


def get_budget_display_name(budget_code):
    mapping = {
        "budget": "Budget-Friendly",
        "standard": "Standard",
        "premium": "Premium",
        "luxury": "Luxury",
    }
    return mapping.get(budget_code, "Standard")


def get_diet_display_name(diet_code):
    mapping = {
        "no_preference": "No Preference",
        "vegetarian": "Vegetarian",
        "non_vegetarian": "Non-Vegetarian",
        "vegan": "Vegan",
    }
    return mapping.get(diet_code, "No Preference")


def generate_itinerary(selected_slugs, preferences=None, trip_details=None):
    """
    Generate a complete, structured itinerary for the selected destinations and user preferences.
    """
    if not selected_slugs:
        # Default fallback to Manali if nothing is chosen
        selected_slugs = ["manali"]

    preferences = preferences or {}
    trip_details = trip_details or {}

    # Extract trip settings (default to empty string if not set)
    departure_str = trip_details.get("departure_date", "")
    return_str = trip_details.get("return_date", "")
    travellers = int(trip_details.get("travellers", 4))
    start_location = trip_details.get("start_location", "").strip()

    # Extract preferences
    vibes = preferences.get("vibes", [])
    interests = preferences.get("interests", ["beaches", "nature", "food", "photography"])
    budget_tier = preferences.get("budget_tier", "standard")
    stay_type = preferences.get("stay_type", "3_star")
    diet = preferences.get("diet", "no_preference")
    dining = preferences.get("dining", ["local_food", "street_food", "cafes"])

    # Load destination objects and attach suggested stays/food
    dest_objects = []
    for slug in selected_slugs:
        d = get_destination_by_slug(slug)
        if d:
            d_copy = d.copy()
            d_copy["suggested_stay"] = get_suggested_stay(slug, budget_tier, stay_type)
            d_copy["suggested_restaurant"] = get_suggested_restaurant(slug, budget_tier, diet)
            dest_objects.append(d_copy)

    if not dest_objects:
        all_d = get_all_destinations()
        d0 = all_d[0].copy()
        d0["suggested_stay"] = get_suggested_stay(d0["slug"], budget_tier, stay_type)
        d0["suggested_restaurant"] = get_suggested_restaurant(d0["slug"], budget_tier, diet)
        dest_objects = [d0]

    # Calculate suggested total days based on the sum of suggested days of selected destinations
    suggested_total_days = sum(d.get("suggested_days", 3) for d in dest_objects)
    if suggested_total_days < 2:
        suggested_total_days = 2

    # Compute dates and days
    start_date, end_date, total_days, total_nights = parse_dates_and_duration(
        departure_str, return_str, default_days=suggested_total_days
    )

    # Allocate days per destination
    num_dests = len(dest_objects)
    base_days_per_dest = max(1, total_days // num_dests)
    remainder = total_days % num_dests

    destination_days_map = []
    for i, dest in enumerate(dest_objects):
        alloc_days = base_days_per_dest + (1 if i < remainder else 0)
        for d_num in range(1, alloc_days + 1):
            destination_days_map.append({
                "destination": dest,
                "dest_day_index": d_num,
                "dest_total_days": alloc_days,
                "is_dest_first_day": (d_num == 1),
                "is_dest_last_day": (d_num == alloc_days),
            })

    # Adjust list to match exact total_days
    destination_days_map = destination_days_map[:total_days]

    # Generate day-by-day itinerary cards
    days_itinerary = []
    for day_idx, item in enumerate(destination_days_map, start=1):
        dest = item["destination"]
        dest_day = item["dest_day_index"]
        dest_total = item["dest_total_days"]
        stay = dest.get("suggested_stay")
        restaurant = dest.get("suggested_restaurant")

        stay_name = stay["name"] if stay else get_stay_display_name(stay_type)
        stay_area = f" ({stay['area']})" if stay and stay.get("area") else ""
        rest_name = restaurant["name"] if restaurant else "Local Culinary Spot"
        rest_area = f" ({restaurant['area']})" if restaurant and restaurant.get("area") else ""

        if start_date:
            current_date = start_date + timedelta(days=day_idx - 1)
            date_str = current_date.strftime("%d %b %Y")
        else:
            date_str = f"Day {day_idx} of {total_days}"

        is_trip_first_day = (day_idx == 1)
        is_trip_last_day = (day_idx == total_days)

        highlights = dest.get("highlights", ["Explore scenic sights", "Sample local dishes", "Sunset viewpoints"])
        h1 = highlights[0] if len(highlights) > 0 else f"Explore {dest['name']}"
        h2 = highlights[1] if len(highlights) > 1 else "Scenic viewpoint & photography"
        h3 = highlights[2] if len(highlights) > 2 else "Local culinary & bazaar exploration"

        # Construct activities according to day stage and preferences
        activities = []
        if is_trip_first_day:
            day_title = f"Arrival & {dest['name']} Exploration"
            location_label = f"{dest['name']} · {dest['state']}"
            from_text = f" from {start_location}" if start_location else ""
            activities.append({"time": "10:00 AM", "text": f"Arrive at {dest['name']}{from_text} & check in"})
            activities.append({"time": "11:30 AM", "text": f"Freshen up at {stay_name}{stay_area}"})
            activities.append({"time": "02:00 PM", "text": f"Welcome lunch at {rest_name}{rest_area}: {get_meal_recommendation(dest, diet, dining)}"})
            activities.append({"time": "04:30 PM", "text": f"{h1}"})
            activities.append({"time": "07:30 PM", "text": f"Evening stroll & {h3}"})

        elif is_trip_last_day:
            day_title = f"{dest['name']} Farewell & Departure"
            location_label = f"{dest['name']} & Transit"
            towards_text = f" towards {start_location}" if start_location else ""
            activities.append({"time": "08:30 AM", "text": f"Breakfast at {stay_name} & morning walk"})
            activities.append({"time": "10:30 AM", "text": f"Check-out and souvenir shopping for authentic local specialties"})
            activities.append({"time": "01:00 PM", "text": f"Farewell lunch at {rest_name}: authentic local delicacies"})
            activities.append({"time": "03:30 PM", "text": f"Transit departure{towards_text}"})

        elif item["is_dest_first_day"]:
            # Transit between destinations in a multi-destination journey
            day_title = f"Scenic Transit to {dest['name']} & Check-in"
            location_label = f"Transit to {dest['name']}"
            activities.append({"time": "08:00 AM", "text": f"Morning scenic transfer to {dest['name']}"})
            activities.append({"time": "12:00 PM", "text": f"Arrive in {dest['name']} & check-in at {stay_name}{stay_area}"})
            activities.append({"time": "01:30 PM", "text": f"Welcome lunch at {rest_name}: {get_meal_recommendation(dest, diet, dining)}"})
            activities.append({"time": "04:00 PM", "text": f"{h1}"})
            activities.append({"time": "07:30 PM", "text": f"Dinner and relaxing evening in {dest['name']}"})

        elif dest_day == 2:
            day_title = f"Deep Dive: {h1}"
            location_label = f"{dest['name']} Highlights"
            activities.append({"time": "08:30 AM", "text": "Hearty breakfast with fresh local flavors"})
            activities.append({"time": "10:00 AM", "text": f"Signature experience: {h1}"})
            activities.append({"time": "01:00 PM", "text": f"Mid-day culinary stop at {rest_name}: {get_meal_recommendation(dest, diet, dining)}"})
            activities.append({"time": "03:30 PM", "text": f"Afternoon adventure: {h2}"})
            activities.append({"time": "06:30 PM", "text": f"Golden hour sunset & evening relaxation"})

        else:
            day_title = f"Hidden Gems & {h2}"
            location_label = f"{dest['name']} Exploration"
            activities.append({"time": "09:00 AM", "text": "Morning exploration and photography"})
            activities.append({"time": "11:00 AM", "text": f"{h2}"})
            activities.append({"time": "01:30 PM", "text": f"Lunch at {rest_name}{rest_area}"})
            activities.append({"time": "04:00 PM", "text": f"{h3}"})
            activities.append({"time": "08:00 PM", "text": "Group dinner and campfire / rooftop chillout"})

        days_itinerary.append({
            "day_num": day_idx,
            "date_str": date_str,
            "day_title": day_title,
            "location_label": location_label,
            "activities": activities,
            "suggested_stay": stay,
            "suggested_restaurant": restaurant,
        })

    # Destination names summary
    dest_names = " + ".join([d["name"] for d in dest_objects])

    # Compute rough estimated total cost for summary
    base_sum = sum(d.get("base_cost_per_day", 3000) for d in dest_objects) / len(dest_objects)
    tier_mult = {"budget": 0.75, "standard": 1.0, "premium": 1.35, "luxury": 2.1}.get(budget_tier, 1.0)
    stay_mult = {"hostel": 0.7, "budget_hotel": 0.85, "3_star": 1.0, "4_star": 1.4, "5_star": 2.2}.get(stay_type, 1.0)
    total_est_cost = int(base_sum * total_days * travellers * (tier_mult * 0.6 + stay_mult * 0.4))
    # Round to nearest hundred
    total_est_cost = round(total_est_cost, -2)

    # Vibe summary display
    vibe_labels = [v.capitalize() for v in vibes[:2]]
    trip_style_display = " & ".join(vibe_labels) if vibe_labels else "Standard Exploration"

    dates_range_display = (
        f"{start_date.strftime('%d %b')} – {end_date.strftime('%d %b %Y')}"
        if start_date
        else f"{total_days} Days · {total_nights} Nights"
    )

    summary = {
        "destinations_display": dest_names,
        "duration_display": f"{total_days} Days / {total_nights} Nights",
        "travelers_display": f"{travellers} People",
        "total_days": total_days,
        "total_nights": total_nights,
        "travellers": travellers,
        "start_location": start_location or "Flexible Origin",
        "dates_range_display": dates_range_display,
        "estimated_budget_display": f"₹{total_est_cost:,}",
        "estimated_budget_raw": total_est_cost,
        "trip_style_display": trip_style_display,
        "food_display": get_diet_display_name(diet),
        "hotel_display": get_stay_display_name(stay_type),
        "experience_display": get_budget_display_name(budget_tier),
    }

    return {
        "summary": summary,
        "days": days_itinerary,
        "destinations": dest_objects,
    }


def get_meal_recommendation(dest, diet, dining):
    """Helper to return personalized food text based on destination and diet preference."""
    slug = dest.get("slug", "")
    if diet == "vegetarian" or diet == "vegan":
        veg_dishes = {
            "goa": "Goan vegetable caldin & poi bread with fresh sol kadhi",
            "munnar": "Authentic Kerala sadhya served on banana leaf",
            "manali": "Hot Himachali siddu with pure ghee and dal",
            "jaipur": "Royal Rajasthani Dal Baati Churma & Gatte ki Sabzi",
            "kashmir": "Kashmiri Dum Aloo, Nadru Yakhni & saffron Kahwa",
            "gokarna": "Coastal temple meals & avocado toasts at beach shacks",
            "ooty": "Fresh Nilgiri tea, piping hot sambar vadas & homemade chocolates",
            "hampi": "South Indian unlimited thali with freshly baked woodfired pizzas",
            "rishikesh": "Ayurvedic sattvic organic bowl & masala chai",
            "udaipur": "Mewari ker sangri, missi roti & rabdi",
            "varkala": "Fresh coconut curry, appam, and fresh fruit bowls",
            "coorg": "Bamboo shoot curry (Baimbale) & rice akki roti",
            "pondicherry": "French croissant, café au lait & crepes in White Town",
            "mumbai": "Iconic Pav Bhaji, Bhel Puri, and Bombay sandwich",
            "hyderabad": "Authentic Hyderabadi Veg Dum Biryani & Mirchi ka Salan",
            "varanasi": "Kashi Kachori Sabzi, Malaiyo & Banarasi Paan",
        }
        return veg_dishes.get(slug, "Traditional pure-vegetarian regional thali")
    else:
        non_veg_dishes = {
            "goa": "Authentic Goan Fish Curry, Prawn Balchão & Kingfish Fry",
            "munnar": "Malabar Chicken Curry with flaky Kerala parottas",
            "manali": "Himachali Trout Fish fry with mint chutney",
            "jaipur": "Royal Laal Maas & Keema Baati",
            "kashmir": "Traditional Wazwan Rogan Josh, Gushtaba & Rista",
            "gokarna": "Fresh coastal butter garlic prawns & seafood thali",
            "ooty": "Badaga chicken curry & spiced mutton biryani",
            "hampi": "Riverside grilled fish & woodfired chicken pizzas",
            "rishikesh": "Organic valley salad, woodfired pizzas & herbal teas",
            "udaipur": "Mewari Junglee Maas & royal mutton curries",
            "varkala": "Karimeen Pollichathu (pearl spot fish wrapped in banana leaf)",
            "coorg": "Famous Kodava Pandi Curry & Koli curry with Kadambuttu",
            "pondicherry": "French Poulet Rôti & Creole seafood bouillabaisse",
            "mumbai": "Bombil Fry, Crab masala & authentic Bohri Biryani",
            "hyderabad": "World-famous Hyderabadi Mutton Dum Biryani & Haleem",
            "varanasi": "Mughlai seekh kebabs & spicy mutton curry",
        }
        return non_veg_dishes.get(slug, "Regional specialty curries and fresh local delicacies")
