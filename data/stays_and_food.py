"""
DesiSafar — Hotels & Restaurants reference data
Compiled from live Google Places results (Aug 2026) for the 16 destinations
already featured on the DesiSafar destinations page.

Structure: STAYS_AND_FOOD[<destination_slug>] = {
    "hotels": [ {name, area, rating, phone}, ... ],
    "restaurants": [ {name, area, rating, phone, price_level}, ... ]
}
"""

VERIFIED_DATE_DISCLAIMER = "Details last verified Aug 2026 — please confirm before booking"

STAYS_AND_FOOD = {
    "goa": {
        "hotels": [
            {"name": "Hilton Goa Resort", "area": "Candolim, North Goa", "rating": 4.5, "phone": "+91 832 664 9800"},
            {"name": "Holiday Inn Resort Goa, an IHG Hotel", "area": "Mobor Beach, Cavelossim, South Goa", "rating": 4.7, "phone": "+91 832 662 6000"},
            {"name": "Bambolim Beach Resort", "area": "Bambolim, Goa", "rating": 4.1, "phone": "+91 832 674 8000"},
        ],
        "restaurants": [
            {"name": "The Second House", "area": "Saligao, Goa", "rating": 4.5, "phone": "+91 85302 66603", "price_level": 4},
            {"name": "The Fishermans Wharf", "area": "Cavelossim, Goa (riverside seafood)", "rating": 4.5, "phone": "+91 90110 18866", "price_level": None},
            {"name": "Elephant and Co. Anjuna", "area": "Anjuna, Goa", "rating": 4.7, "phone": "+91 76663 61130", "price_level": None},
        ],
    },
    "munnar": {
        "hotels": [
            {"name": "Grand Plaza Munnar", "area": "Moolakadai, Munnar town", "rating": 4.6, "phone": "+91 97464 70119"},
            {"name": "Blanket Hotel & Spa", "area": "Pallivasal, Munnar", "rating": 4.8, "phone": "+91 82818 06633"},
            {"name": "Tea County Munnar", "area": "Ikka Nagar, Munnar town", "rating": 4.5, "phone": "+91 4865 230 460"},
        ],
        "restaurants": [
            {"name": "Munnar Samrudhi Restaurant", "area": "Moolakadai, Munnar", "rating": 4.7, "phone": "+91 94965 80200", "price_level": 2},
            {"name": "Parakkat Spice Merchant Restaurant", "area": "Chithirapuram, Munnar", "rating": 4.8, "phone": "+91 70254 58888", "price_level": 2},
            {"name": "The Hornbill Restaurant", "area": "Pothamedu, Munnar (Blackberry Hills Resort)", "rating": 4.5, "phone": "+91 85902 40881", "price_level": 2},
        ],
    },
    "manali": {
        "hotels": [
            {"name": "Hotel Rio Sol Resort and Villas", "area": "Aleo, Manali", "rating": 4.9, "phone": "+91 98164 02223"},
            {"name": "Apple Field House", "area": "Old Manali", "rating": 4.7, "phone": "+91 94187 48343"},
            {"name": "Mountain Top Hotel", "area": "Hadimba Temple Rd, Manali", "rating": 4.1, "phone": "+91 76509 08765"},
        ],
        "restaurants": [
            {"name": "The Lazy Dog Lounge", "area": "Old Manali (riverside)", "rating": 4.3, "phone": "+91 70182 28644", "price_level": None},
            {"name": "Cafe 1986", "area": "Mall Road, Manali", "rating": 4.6, "phone": "+91 88986 90000", "price_level": None},
            {"name": "IL Forno", "area": "Hadimba Temple Rd, Manali (Italian)", "rating": 4.4, "phone": "+91 98160 40144", "price_level": 2},
        ],
    },
    "jaipur": {
        "hotels": [
            {"name": "Rajasthan Palace — Heritage Boutique Hotel", "area": "Adarsh Nagar, Jaipur", "rating": 4.6, "phone": "+91 70166 62608"},
            {"name": "WelcomHeritage Kurki Palace", "area": "Nirman Nagar, Jaipur", "rating": 4.6, "phone": "+91 92515 54897"},
            {"name": "ibis Jaipur City Centre", "area": "Civil Lines, Jaipur", "rating": 4.5, "phone": "+91 141 475 5000"},
        ],
        "restaurants": [
            {"name": "Handi Restaurant", "area": "MI Road, Jaipur (Rajasthani non-veg)", "rating": 4.1, "phone": "+91 98291 74873", "price_level": 2},
            {"name": "Suvarna Mahal", "area": "Rambagh Palace, Jaipur (fine dining)", "rating": 4.7, "phone": "+91 141 667 1234", "price_level": None},
            {"name": "Govindam Retreat", "area": "Gangori Bazaar, Jaipur (thali + live Sufi music)", "rating": 4.4, "phone": "+91 99299 49258", "price_level": 2},
        ],
    },
    "kashmir": {
        "hotels": [
            {"name": "Zostel Srinagar", "area": "Nishat, Srinagar (near Dal Lake)", "rating": 4.6, "phone": "+91 11 4116 9723"},
            {"name": "The Stay Villa", "area": "Lal Chowk, Srinagar", "rating": 4.8, "phone": "+91 87130 00025"},
            {"name": "Four Points by Sheraton Srinagar", "area": "Sonwar Bagh, Srinagar", "rating": 4.2, "phone": "+91 194 246 9000"},
        ],
        "restaurants": [
            {"name": "Stream Restaurant", "area": "Boulevard Rd, Srinagar (Wazwan, Dal Lake view)", "rating": 4.7, "phone": "+91 194 250 0244", "price_level": None},
            {"name": "Little Persia", "area": "Munawar Link Rd, Srinagar", "rating": 4.4, "phone": "+91 88999 85589", "price_level": None},
            {"name": "Kake Di Hatti", "area": "Khayam, Srinagar (vegetarian North Indian)", "rating": 4.6, "phone": "+91 88002 81213", "price_level": None},
        ],
    },
    "gokarna": {
        "hotels": [
            {"name": "Zostel Gokarna", "area": "Kudle Beach Rd, Gokarna", "rating": 4.5, "phone": "+91 44 4011 5827"},
            {"name": "Arthigamya Spa & Resort", "area": "Kudle Beach Rd, Gokarna", "rating": 4.0, "phone": "+91 88806 88806"},
            {"name": "Ocean Breeze Cottage and Cafe", "area": "Main Beach, Gokarna", "rating": 4.3, "phone": "+91 97429 85562"},
        ],
        "restaurants": [
            {"name": "The Coco Leaf", "area": "Main Beach, Gokarna", "rating": 4.5, "phone": "+91 80505 08585", "price_level": None},
            {"name": "Sunset Cafe Beach Stay", "area": "Main Beach, Gokarna", "rating": 4.5, "phone": "+91 82176 85525", "price_level": None},
            {"name": "Mantra Cafe", "area": "Kudle Beach Rd, Gokarna (Zostel in-house)", "rating": 4.1, "phone": None, "price_level": 2},
        ],
    },
    "ooty": {
        "hotels": [
            {"name": "Hotel Lakeview", "area": "West Mere, Ooty", "rating": 4.0, "phone": "+91 423 244 3580"},
            {"name": "Silent Valley Farm Resort", "area": "Adasolai Rd, Ooty", "rating": 4.5, "phone": "+91 94878 17756"},
            {"name": "Al Woodlands Residency", "area": "Bombay Castel, Ooty (opp. Rose Garden)", "rating": 4.5, "phone": "+91 90436 98405"},
        ],
        "restaurants": [
            {"name": "The Periodic Table", "area": "Upper Bazar, Ooty (fine dining)", "rating": 4.5, "phone": "+91 94870 00222", "price_level": 4},
            {"name": "Earl's Secret", "area": "Pudumund, Ooty (colonial-era heritage restaurant)", "rating": 4.4, "phone": "+91 94870 00222", "price_level": None},
            {"name": "Angaara Restaurant", "area": "Upper Bazar, Ooty", "rating": 4.3, "phone": None, "price_level": 2},
        ],
    },
    "hampi": {
        "hotels": [
            {"name": "Heritage Resort Hampi", "area": "Hosamalapanagudi, Hampi", "rating": 4.4, "phone": "+91 98456 02838"},
            {"name": "Hampi Delmont Resort", "area": "Hanmanhalli, Hampi (pure vegetarian)", "rating": 4.5, "phone": "+91 63620 92020"},
            {"name": "Hotel Hampi International", "area": "Station Rd, Hosapete", "rating": 3.9, "phone": "+91 92431 61111"},
        ],
        "restaurants": [
            {"name": "Mango Tree Restaurant", "area": "Old Busstand, Kamalapura, Hampi", "rating": 4.3, "phone": "+91 94487 65213", "price_level": None},
            {"name": "The Nest — Lakefront Restaurant", "area": "Tirumalapur Village, Hampi (Feathers Resort)", "rating": 4.6, "phone": "+91 76769 86517", "price_level": 2},
            {"name": "Taste of Brahmins", "area": "Near Virupaksha Temple, Hampi (breakfast)", "rating": 4.8, "phone": "+91 94820 06076", "price_level": 1},
        ],
    },
    "rishikesh": {
        "hotels": [
            {"name": "Aloha On The Ganges", "area": "Tapovan, Rishikesh", "rating": 4.4, "phone": "+91 95550 88000"},
            {"name": "Oslo by Around Stays", "area": "Tapovan, Rishikesh", "rating": 4.3, "phone": "+91 98123 44442"},
            {"name": "Hotel Shivanta Laxmanjhula", "area": "Laxman Jhula, Rishikesh", "rating": 3.1, "phone": "+91 84396 38175"},
        ],
        "restaurants": [
            {"name": "The Sitting Elephant", "area": "Palika Nagar, Rishikesh (rooftop, Ganga view)", "rating": 4.7, "phone": "+91 79 6580 4730", "price_level": 2},
            {"name": "Sky Deck Restaurant", "area": "Adarsh Gram, Rishikesh", "rating": 4.8, "phone": "+91 95208 87794", "price_level": 2},
            {"name": "Jal & Jalebi", "area": "Veerbhadra, Rishikesh (Ganga Kinare, riverside)", "rating": 4.3, "phone": "+91 90155 44000", "price_level": None},
        ],
    },
    "udaipur": {
        "hotels": [
            {"name": "Pax Grand Blue", "area": "Shivaji Nagar, Udaipur", "rating": 4.7, "phone": "+91 99911 66775"},
            {"name": "Udaigarh Udaipur — Heritage Hotel", "area": "Lal Ghat, Old City, Udaipur (lake view rooftop)", "rating": 4.1, "phone": "+91 96600 55500"},
            {"name": "Hotel Subcity", "area": "Sector 8, Central Area, Udaipur", "rating": 4.8, "phone": "+91 98797 60780"},
        ],
        "restaurants": [
            {"name": "1559 AD", "area": "Near Fateh Sagar Lake, Udaipur", "rating": 4.4, "phone": "+91 73570 41559", "price_level": 2},
            {"name": "Khamma Ghani Restaurant", "area": "Rang Sagar, Udaipur (lakeside)", "rating": 4.1, "phone": "+91 73406 66622", "price_level": None},
            {"name": "Ghati Pe", "area": "Ambavgarh, Udaipur (rooftop city view)", "rating": 4.9, "phone": "+91 73000 76035", "price_level": None},
        ],
    },
    "varkala": {
        "hotels": [
            {"name": "Skylar Seaview Resort", "area": "South Cliff, Varkala", "rating": 4.6, "phone": "+91 87140 19666"},
            {"name": "SANDRA Eco Beach Resort", "area": "Odayam Beach, Varkala", "rating": 4.6, "phone": "+91 99957 03366"},
            {"name": "Varkala Villa", "area": "South Cliff, Varkala (homestay)", "rating": 4.4, "phone": "+91 98952 98300"},
        ],
        "restaurants": [
            {"name": "Cafe Trip is Life", "area": "South Cliff, Varkala", "rating": 4.5, "phone": "+91 79074 83838", "price_level": 2},
            {"name": "Cafe Sarwaa on the Cliff", "area": "South Cliff, Varkala", "rating": 4.6, "phone": None, "price_level": 2},
            {"name": "BLG Surf Bistro", "area": "Edava, Varkala", "rating": 4.5, "phone": "+91 62387 96719", "price_level": None},
        ],
    },
    "coorg": {
        "hotels": [
            {"name": "Coorg Wilderness Resort & Spa", "area": "Mekeri, Madikeri", "rating": 4.6, "phone": "+91 63646 01941"},
            {"name": "Silent Brook Resort", "area": "Jodupala, Madikeri", "rating": 4.4, "phone": "+91 77608 72451"},
            {"name": "Hotel Oxyrich Coorg", "area": "Thalathmane, Madikeri", "rating": 4.5, "phone": "+91 90191 52900"},
        ],
        "restaurants": [
            {"name": "BELLI'S Restaurant", "area": "Stuart Hill, Madikeri (authentic Coorgi)", "rating": 4.3, "phone": "+91 99729 88175", "price_level": None},
            {"name": "Chimmy's Cafe and Roastery", "area": "Madikeri", "rating": 4.9, "phone": "+91 72599 41441", "price_level": 2},
            {"name": "Silver Oaks Madikeri", "area": "Bhagavathi Nagar, Madikeri", "rating": 4.6, "phone": None, "price_level": 2},
        ],
    },
    "pondicherry": {
        "hotels": [
            {"name": "The Promenade", "area": "White Town, Puducherry (seafront)", "rating": 4.2, "phone": "+91 413 222 7750"},
            {"name": "Villa Shanti Hotel Restaurant", "area": "White Town, Puducherry", "rating": 4.3, "phone": "+91 413 420 0028"},
            {"name": "French Rivera (White Town)", "area": "White Town, Puducherry", "rating": 4.7, "phone": "+91 94435 63331"},
        ],
        "restaurants": [
            {"name": "THE SPOT", "area": "White Town, Puducherry (beachfront)", "rating": 4.7, "phone": "+91 63844 40648", "price_level": None},
            {"name": "Mira", "area": "White Town, Puducherry (Grand Hotel d'Europe)", "rating": 4.7, "phone": "+91 79 6921 9999", "price_level": 3},
            {"name": "Copper Kitchen", "area": "Ellaipillaichavady, Puducherry", "rating": 4.6, "phone": "+91 99445 49977", "price_level": 2},
        ],
    },
    "mumbai": {
        "hotels": [
            {"name": "Fariyas Hotel Mumbai", "area": "Colaba, Mumbai", "rating": 4.0, "phone": "+91 22 6141 6141"},
            {"name": "Sai Palace Grand Hotel & Restaurant", "area": "Malad West, Mumbai", "rating": 4.3, "phone": "+91 22 6910 8888"},
            {"name": "Hotel Royal Palace Fort", "area": "Ballard Estate, Fort, Mumbai", "rating": 4.6, "phone": "+91 91378 82540"},
        ],
        "restaurants": [
            {"name": "The Bombay Canteen", "area": "Kamala Mills, Lower Parel, Mumbai", "rating": 4.5, "phone": "+91 88808 02424", "price_level": None},
            {"name": "Lake View Cafe", "area": "Powai, Mumbai (The Westin, lake view)", "rating": 4.7, "phone": "+91 86574 15264", "price_level": None},
            {"name": "Native Bombay", "area": "Ballard Estate, Fort, Mumbai", "rating": 4.5, "phone": "+91 96190 66000", "price_level": None},
        ],
    },
    "hyderabad": {
        "hotels": [
            {"name": "Hyderabad Marriott Hotel & Convention Centre", "area": "Tank Bund, Hussain Sagar, Hyderabad", "rating": 4.4, "phone": "+91 40 6652 2999"},
            {"name": "New Hotel Suhail", "area": "Troop Bazaar, Abids, Hyderabad", "rating": 4.3, "phone": "+91 40 2461 0299"},
            {"name": "Hyatt Hyderabad Gachibowli", "area": "Financial District, Gachibowli, Hyderabad", "rating": 4.3, "phone": "+91 40 4848 1234"},
        ],
        "restaurants": [
            {"name": "Exotica Banjara Hills", "area": "Banjara Hills, Hyderabad", "rating": 4.3, "phone": "+91 96521 15500", "price_level": None},
            {"name": "Exotica Hitech City", "area": "Madhapur, Hyderabad (rooftop)", "rating": 4.3, "phone": "+91 96520 65500", "price_level": None},
            {"name": "Jewel Of Nizam", "area": "The Golkonda Hotel, Masab Tank, Hyderabad", "rating": 4.1, "phone": "+91 40 6611 0101", "price_level": 4},
        ],
    },
    "varanasi": {
        "hotels": [
            {"name": "HOTEL STAY BANARAS", "area": "Sigra, Varanasi", "rating": 4.4, "phone": "+91 95949 50095"},
            {"name": "Hotel Nandini", "area": "Godauliya, Varanasi", "rating": 3.7, "phone": None},
            {"name": "HOTEL VARANASI INN", "area": "Sigra, Varanasi", "rating": 3.9, "phone": "+91 81760 03999"},
        ],
        "restaurants": [
            {"name": "Charcoal Fine Dining", "area": "Sigra, Varanasi", "rating": 4.6, "phone": "+91 93369 29765", "price_level": 2},
            {"name": "Cupid Roof Multi Cuisine Restaurant", "area": "Akhri Bypass, Varanasi (rooftop city view)", "rating": 4.7, "phone": "+91 73070 49656", "price_level": 2},
            {"name": "Desi Mandapam Baati Chokha Restaurant", "area": "Durgakund Rd, Varanasi", "rating": 4.9, "phone": "+91 98393 66001", "price_level": 2},
        ],
    },
}


def get_stays_and_food(slug):
    """Retrieve hotels and restaurants list for a destination slug."""
    return STAYS_AND_FOOD.get(slug, {"hotels": [], "restaurants": []})


def get_suggested_stay(slug, budget_tier="standard", stay_type="3_star"):
    """
    Select the most suitable hotel recommendation for a destination.
    Optionally maps user budget / stay preference.
    """
    data = get_stays_and_food(slug)
    hotels = data.get("hotels", [])
    if not hotels:
        return None

    # If hostel/budget preference and multiple choices exist, pick accordingly or default to first
    if stay_type in ["hostel", "budget_hotel"] or budget_tier == "budget":
        # Look for Zostel / budget hotel if present, otherwise sort by rating/index
        for h in hotels:
            if "zostel" in h["name"].lower() or "cottage" in h["name"].lower() or "house" in h["name"].lower():
                return h
        return hotels[-1]
    elif stay_type in ["4_star", "5_star"] or budget_tier in ["premium", "luxury"]:
        # Pick top resort / luxury if available
        for h in hotels:
            if "resort" in h["name"].lower() or "palace" in h["name"].lower() or "grand" in h["name"].lower():
                return h
        return hotels[0]

    return hotels[0]


def get_suggested_restaurant(slug, budget_tier="standard", diet="no_preference"):
    """
    Select the most suitable restaurant recommendation for a destination.
    """
    data = get_stays_and_food(slug)
    restaurants = data.get("restaurants", [])
    if not restaurants:
        return None

    if diet == "vegetarian":
        for r in restaurants:
            if "vegetarian" in r.get("area", "").lower() or "thali" in r.get("area", "").lower():
                return r

    if budget_tier == "luxury":
        for r in restaurants:
            if r.get("price_level") == 4 or "fine dining" in r.get("area", "").lower():
                return r

    return restaurants[0]
