"""
Destination catalog and lookup functions for DesiSafar.
Contains 16 curated Indian travel destinations with metadata, categories,
highlights, and estimated base pricing.
"""

CATEGORIES = [
    {"id": "all", "label": "All Destinations", "icon": "🗺️"},
    {"id": "beaches", "label": "Beaches", "icon": "🏖️"},
    {"id": "mountains", "label": "Mountains", "icon": "🏔️"},
    {"id": "nature", "label": "Nature", "icon": "🌿"},
    {"id": "heritage", "label": "Heritage", "icon": "🏛️"},
    {"id": "cities", "label": "Cities", "icon": "🏙️"},
    {"id": "adventure", "label": "Adventure", "icon": "🧗"},
    {"id": "food", "label": "Food & Culinary", "icon": "🍛"},
    {"id": "spiritual", "label": "Spiritual", "icon": "🪔"},
]

# Comprehensive transit hubs and gateways across all Indian regions
ALL_INDIA_HUBS = [
    # Metros & Major Air/Rail Gateways
    "Delhi, NCR",
    "Mumbai, Maharashtra",
    "Bengaluru, Karnataka",
    "Kolkata, West Bengal",
    "Chennai, Tamil Nadu",
    "Hyderabad, Telangana",
    "Pune, Maharashtra",
    "Ahmedabad, Gujarat",
    "Jaipur, Rajasthan",
    "Jodhpur, Rajasthan",
    "Udaipur, Rajasthan",
    "Kochi, Kerala",
    "Chandigarh, Punjab/Haryana",
    "Lucknow, Uttar Pradesh",
    "Agra, Uttar Pradesh",
    "Varanasi, Uttar Pradesh",
    "Goa (Dabolim/Mopa), Goa",
    "Guwahati, Assam",
    "Surat, Gujarat",
    "Indore, Madhya Pradesh",
    "Bhopal, Madhya Pradesh",
    "Nagpur, Maharashtra",
    "Patna, Bihar",
    "Bhubaneswar, Odisha",
    "Coimbatore, Tamil Nadu",
    "Visakhapatnam, Andhra Pradesh",
    "Vijayawada, Andhra Pradesh",
    "Vadodara, Gujarat",
    "Dehradun, Uttarakhand",
    "Amritsar, Punjab",
    "Thiruvananthapuram, Kerala",
    "Mysuru (Mysore), Karnataka",
    "Mangalore, Karnataka",
    "Ranchi, Jharkhand",
    "Raipur, Chhattisgarh",
    "Madurai, Tamil Nadu",
    "Kozhikode (Calicut), Kerala",
    "Shillong, Meghalaya",
    "Srinagar, Jammu & Kashmir",
    "Jammu Tawi, Jammu & Kashmir",
    "Shimla, Himachal Pradesh",
    "Port Blair (Andaman & Nicobar Islands)",
]

# Destination-specific nearby hubs mapping
NEARBY_HUBS_MAP = {
    "delhi": [
        "Delhi, NCR",
        "Noida, Uttar Pradesh",
        "Gurugram, Haryana",
        "Chandigarh, Punjab/Haryana",
        "Jaipur, Rajasthan",
        "Agra, Uttar Pradesh",
    ],
    "agra": [
        "Agra (Kheria Airport), Uttar Pradesh",
        "Delhi, NCR",
        "Jaipur, Rajasthan",
        "Gwalior, Madhya Pradesh",
        "Lucknow, Uttar Pradesh",
    ],
    "bangalore": [
        "Bengaluru (Kempegowda Airport), Karnataka",
        "Mysuru (Mysore), Karnataka",
        "Chennai, Tamil Nadu",
        "Coimbatore, Tamil Nadu",
        "Hyderabad, Telangana",
        "Pune, Maharashtra",
    ],
    "chandigarh": [
        "Chandigarh (Shaheed Bhagat Singh Airport), Punjab/Haryana",
        "Delhi, NCR",
        "Amritsar, Punjab",
        "Shimla, Himachal Pradesh",
        "Dehradun, Uttarakhand",
    ],
    "goa": [
        "Goa (Dabolim Airport), Goa",
        "Goa (Mopa Airport), Goa",
        "Madgaon Junction, Goa",
        "Panaji, Goa",
        "Belagavi, Karnataka",
        "Hubli-Dharwad, Karnataka",
        "Mumbai, Maharashtra",
        "Pune, Maharashtra",
        "Mangalore, Karnataka",
    ],
    "munnar": [
        "Kochi (Cochin Airport), Kerala",
        "Ernakulam Junction, Kerala",
        "Aluva Rail Hub, Kerala",
        "Coimbatore, Tamil Nadu",
        "Madurai, Tamil Nadu",
        "Kottayam, Kerala",
        "Bengaluru, Karnataka",
    ],
    "manali": [
        "Chandigarh, Punjab/Haryana",
        "Kullu-Bhuntar Airport, Himachal Pradesh",
        "Delhi, NCR",
        "Ambala Cantt, Haryana",
        "Kalka, Haryana",
        "Mandi, Himachal Pradesh",
        "Shimla, Himachal Pradesh",
    ],
    "jaipur": [
        "Jaipur International Airport, Rajasthan",
        "Delhi, NCR",
        "Agra, Uttar Pradesh",
        "Ajmer, Rajasthan",
        "Jodhpur, Rajasthan",
        "Ahmedabad, Gujarat",
    ],
    "jodhpur": [
        "Jodhpur Airport, Rajasthan",
        "Jaipur, Rajasthan",
        "Udaipur, Rajasthan",
        "Bikaner, Rajasthan",
        "Ahmedabad, Gujarat",
        "Delhi, NCR",
    ],
    "kashmir": [
        "Srinagar Airport, Jammu & Kashmir",
        "Jammu Tawi, Jammu & Kashmir",
        "Delhi, NCR",
        "Chandigarh, Punjab/Haryana",
        "Amritsar, Punjab",
    ],
    "gokarna": [
        "Goa (Dabolim/Mopa), Goa",
        "Mangalore International Airport, Karnataka",
        "Hubli-Dharwad, Karnataka",
        "Kumta Rail Station, Karnataka",
        "Bengaluru, Karnataka",
        "Pune, Maharashtra",
    ],
    "ooty": [
        "Coimbatore International Airport, Tamil Nadu",
        "Mettupalayam, Tamil Nadu",
        "Mysuru (Mysore), Karnataka",
        "Bengaluru, Karnataka",
        "Kozhikode (Calicut), Kerala",
    ],
    "hampi": [
        "Hubli-Dharwad, Karnataka",
        "Hospet Junction, Karnataka",
        "Bellary, Karnataka",
        "Bengaluru, Karnataka",
        "Goa (Dabolim/Mopa), Goa",
        "Hyderabad, Telangana",
    ],
    "rishikesh": [
        "Dehradun (Jolly Grant Airport), Uttarakhand",
        "Haridwar Junction, Uttarakhand",
        "Delhi, NCR",
        "Rishikesh (Yog Nagari), Uttarakhand",
        "Chandigarh, Punjab/Haryana",
    ],
    "mussoorie": [
        "Dehradun (Jolly Grant Airport), Uttarakhand",
        "Haridwar Junction, Uttarakhand",
        "Delhi, NCR",
        "Chandigarh, Punjab/Haryana",
    ],
    "mahabaleshwar": [
        "Pune International Airport, Maharashtra",
        "Mumbai, Maharashtra",
        "Satara Rail Junction, Maharashtra",
        "Kolhapur, Maharashtra",
    ],
    "mysore": [
        "Mysuru (Mysore Airport / Rail Hub), Karnataka",
        "Bengaluru (Kempegowda Airport), Karnataka",
        "Mangalore, Karnataka",
        "Coimbatore, Tamil Nadu",
        "Kozhikode, Kerala",
    ],
    "pune": [
        "Pune International Airport, Maharashtra",
        "Mumbai, Maharashtra",
        "Nashik, Maharashtra",
        "Goa (Dabolim/Mopa), Goa",
        "Bengaluru, Karnataka",
    ],
    "kolkata": [
        "Kolkata (Netaji Subhash Chandra Bose Airport), West Bengal",
        "Howrah / Sealdah Rail Hubs, West Bengal",
        "Bhubaneswar, Odisha",
        "Patna, Bihar",
        "Ranchi, Jharkhand",
        "Guwahati, Assam",
    ],
    "kerala": [
        "Kochi (Cochin Airport), Kerala",
        "Thiruvananthapuram, Kerala",
        "Alappuzha (Alleppey), Kerala",
        "Kozhikode, Kerala",
        "Bengaluru, Karnataka",
        "Chennai, Tamil Nadu",
    ],
    "andaman-nicobar": [
        "Port Blair (Veer Savarkar Airport), Andaman",
        "Chennai, Tamil Nadu",
        "Kolkata, West Bengal",
        "Bengaluru, Karnataka",
        "Delhi, NCR",
        "Mumbai, Maharashtra",
    ],
    "udaipur": [
        "Udaipur (Maharana Pratap Airport), Rajasthan",
        "Ahmedabad, Gujarat",
        "Jaipur, Rajasthan",
        "Jodhpur, Rajasthan",
        "Mount Abu, Rajasthan",
    ],
    "varkala": [
        "Thiruvananthapuram (Trivandrum Airport), Kerala",
        "Kollam Junction, Kerala",
        "Varkala Sivagiri, Kerala",
        "Kochi, Kerala",
    ],
    "coorg": [
        "Mysuru (Mysore), Karnataka",
        "Mangalore International Airport, Karnataka",
        "Kannur International Airport, Kerala",
        "Bengaluru, Karnataka",
        "Hassan, Karnataka",
    ],
    "pondicherry": [
        "Chennai International Airport, Tamil Nadu",
        "Puducherry Airport, Puducherry",
        "Villupuram Junction, Tamil Nadu",
        "Bengaluru, Karnataka",
        "Tiruchirappalli, Tamil Nadu",
    ],
    "mumbai": [
        "Mumbai (CSMT / Mumbai Airport), Maharashtra",
        "Navi Mumbai, Maharashtra",
        "Thane, Maharashtra",
        "Pune, Maharashtra",
        "Surat, Gujarat",
        "Nashik, Maharashtra",
    ],
    "hyderabad": [
        "Hyderabad (RGIA Airport / Secunderabad), Telangana",
        "Warangal, Telangana",
        "Vijayawada, Andhra Pradesh",
        "Bengaluru, Karnataka",
        "Pune, Maharashtra",
    ],
    "varanasi": [
        "Varanasi (Lal Bahadur Shastri Airport), Uttar Pradesh",
        "Prayagraj (Allahabad), Uttar Pradesh",
        "Lucknow, Uttar Pradesh",
        "Patna, Bihar",
        "Delhi, NCR",
        "Kolkata, West Bengal",
    ],
}

STARTING_HUBS = ALL_INDIA_HUBS


def get_nearby_starting_hubs(selected_slugs=None):
    """
    Return a curated list of starting hubs tailored to the selected destinations,
    followed by the comprehensive list of all Indian hubs.
    """
    hubs = []
    seen = set()

    if selected_slugs:
        for slug in selected_slugs:
            nearby = NEARBY_HUBS_MAP.get(slug, [])
            for h in nearby:
                if h not in seen:
                    seen.add(h)
                    hubs.append(h)

    for h in ALL_INDIA_HUBS:
        if h not in seen:
            seen.add(h)
            hubs.append(h)

    return hubs

DESTINATIONS = {
    "goa": {
        "slug": "goa",
        "name": "Goa",
        "state": "Goa",
        "state_full": "Goa • Coastal Belt",
        "category": "beaches adventure food",
        "primary_category_display": "🏖️ Beaches",
        "description": "Sun-drenched coastal haven renowned for its golden beaches, Portuguese heritage architecture, and beach shacks.",
        "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
        "best_time": "Nov – Mar",
        "duration": "3–5 Days",
        "modal_title": "Goa",
        "modal_state": "Goa, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🏖️ Beaches", "🧗 Adventure", "🍛 Food"],
        "modal_description": "Sun-drenched coastal haven renowned for its golden beaches, Portuguese heritage architecture, vibrant beach shacks, and exhilarating water sports.",
        "modal_best_time": "Nov – Mar",
        "modal_duration": "3 – 5 Days",
        "vibe": "Coastal & Lively",
        "highlights": [
            "Sunset at Anjuna & Palolem Beaches",
            "Heritage Latin Quarter walk in Fontainhas",
            "Authentic Goan fish curry & beach shacks",
        ],
        "base_cost_per_day": 3500,
        "suggested_days": 4,
    },
    "munnar": {
        "slug": "munnar",
        "name": "Munnar",
        "state": "Kerala",
        "state_full": "Kerala • Western Ghats",
        "category": "mountains nature food",
        "primary_category_display": "🏔️ Mountains",
        "description": "Rolling emerald tea plantations, mist-covered valleys, and aromatic spice gardens nestled in the Western Ghats.",
        "image_url": "https://www.ekeralatourism.net/wp-content/uploads/2019/01/best-time-munnar.jpg",
        "best_time": "Sep – May",
        "duration": "2–3 Days",
        "modal_title": "Munnar",
        "modal_state": "Kerala, India",
        "modal_hero_img": "https://www.ekeralatourism.net/wp-content/uploads/2019/01/best-time-munnar.jpg",
        "categories_list": ["🏔️ Mountains", "🌿 Nature", "🍛 Food"],
        "modal_description": "Rolling emerald tea plantations, mist-covered valleys, and aromatic spice gardens nestled high in the Western Ghats of God's Own Country.",
        "modal_best_time": "Sep – May",
        "modal_duration": "2 – 3 Days",
        "vibe": "Serene & Refreshing",
        "highlights": [
            "Kolukkumalai Sunrise over tea estates",
            "Eravikulam National Park & Nilgiri Tahr",
            "Cardamom & spice plantation walks",
        ],
        "base_cost_per_day": 2800,
        "suggested_days": 3,
    },
    "manali": {
        "slug": "manali",
        "name": "Manali",
        "state": "Himachal Pradesh",
        "state_full": "Himachal Pradesh • Beas Valley",
        "category": "mountains adventure nature",
        "primary_category_display": "🏔️ Mountains",
        "description": "Premier mountain hub along the Beas River offering alpine snow views, paragliding, river rafting, and cafe culture.",
        "image_url": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80",
        "best_time": "Oct – Jun",
        "duration": "3–4 Days",
        "modal_title": "Manali",
        "modal_state": "Himachal Pradesh, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🏔️ Mountains", "🧗 Adventure", "🌿 Nature"],
        "modal_description": "Nestled along the Beas River, Manali is India's premier mountain hub offering alpine snow views, paragliding, river rafting, and cafe culture.",
        "modal_best_time": "Oct – Jun",
        "modal_duration": "3 – 4 Days",
        "vibe": "Alpine & Adventurous",
        "highlights": [
            "Solang Valley & Atal Tunnel excursion",
            "Old Manali bohemian cafes & live music",
            "Jogini Waterfall pine forest trek",
        ],
        "base_cost_per_day": 3200,
        "suggested_days": 4,
    },
    "jaipur": {
        "slug": "jaipur",
        "name": "Jaipur",
        "state": "Rajasthan",
        "state_full": "Rajasthan • Pink City",
        "category": "heritage cities food",
        "primary_category_display": "🏛️ Heritage",
        "description": "The magnificent Pink City of royal palaces, grand hill forts, vibrant craft bazaars, and regal Rajasthani cuisine.",
        "image_url": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80",
        "best_time": "Oct – Mar",
        "duration": "2–3 Days",
        "modal_title": "Jaipur",
        "modal_state": "Rajasthan, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🏛️ Heritage", "🏙️ Cities", "🍛 Food"],
        "modal_description": "The Pink City showcases royal Rajput architecture, magnificent hilltop forts, bustling textile bazaars, and iconic royal palaces.",
        "modal_best_time": "Oct – Mar",
        "modal_duration": "2 – 3 Days",
        "vibe": "Regal & Historic",
        "highlights": [
            "Amer Fort & Hawa Mahal photography",
            "City Palace & Jantar Mantar observatory",
            "Authentic Dal Baati Churma & Pyaz Kachori",
        ],
        "base_cost_per_day": 3000,
        "suggested_days": 3,
    },
    "kashmir": {
        "slug": "kashmir",
        "name": "Kashmir (Srinagar)",
        "state": "Jammu & Kashmir",
        "state_full": "Jammu & Kashmir • Paradise Valley",
        "category": "mountains nature spiritual",
        "primary_category_display": "🏔️ Mountains",
        "description": "Paradise on Earth featuring tranquil Dal Lake shikara rides, snow-kissed Himalayan peaks, and Mughal gardens.",
        "image_url": "https://images.unsplash.com/photo-1598091383021-15ddea10925d?auto=format&fit=crop&w=800&q=80",
        "best_time": "Apr – Oct",
        "duration": "4–6 Days",
        "modal_title": "Kashmir (Srinagar)",
        "modal_state": "Jammu & Kashmir, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1598091383021-15ddea10925d?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🏔️ Mountains", "🌿 Nature", "🪔 Spiritual"],
        "modal_description": "Renowned as heaven on earth with tranquil Dal Lake houseboats, snow-capped Pir Panjal ranges, and fragrant saffron valleys.",
        "modal_best_time": "Apr – Oct",
        "modal_duration": "4 – 6 Days",
        "vibe": "Dreamy & Majestic",
        "highlights": [
            "Sunset Shikara ride on Dal Lake",
            "Gulmarg Gondola & snow meadows",
            "Pahalgam Betaab Valley & pine trails",
        ],
        "base_cost_per_day": 4200,
        "suggested_days": 5,
    },
    "gokarna": {
        "slug": "gokarna",
        "name": "Gokarna",
        "state": "Karnataka",
        "state_full": "Karnataka • Arabian Coast",
        "category": "beaches spiritual nature",
        "primary_category_display": "🏖️ Beaches",
        "description": "A tranquil coastal pilgrimage town bordered by pristine untouched beaches like Om Beach surrounded by cliffside walking trails.",
        "image_url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
        "best_time": "Oct – Mar",
        "duration": "2–3 Days",
        "modal_title": "Gokarna",
        "modal_state": "Karnataka, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🏖️ Beaches", "🪔 Spiritual", "🌿 Nature"],
        "modal_description": "Laidback coastal sanctuary with holy temples, secluded coves like Half Moon Beach, and panoramic cliff-hugging trails.",
        "modal_best_time": "Oct – Mar",
        "modal_duration": "2 – 3 Days",
        "vibe": "Laidback & Spiritual",
        "highlights": [
            "Om Beach & Kudle Beach cliff trail",
            "Mahabaleshwar Temple darshan",
            "Sunset sea-view café dinners",
        ],
        "base_cost_per_day": 2600,
        "suggested_days": 3,
    },
    "ooty": {
        "slug": "ooty",
        "name": "Ooty",
        "state": "Tamil Nadu",
        "state_full": "Tamil Nadu • Nilgiri Hills",
        "category": "mountains nature heritage",
        "primary_category_display": "🏔️ Mountains",
        "description": "Queen of Hill Stations set in the blue Nilgiri Mountains, famed for heritage toy train rides and eucalyptus-scented breezes.",
        "image_url": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80",
        "best_time": "Oct – Jun",
        "duration": "2–3 Days",
        "modal_title": "Ooty",
        "modal_state": "Tamil Nadu, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🏔️ Mountains", "🌿 Nature", "🏛️ Heritage"],
        "modal_description": "Queen of Hill Stations set in the blue Nilgiri Mountains, famed for heritage steam toy train rides and aromatic tea estates.",
        "modal_best_time": "Oct – Jun",
        "modal_duration": "2 – 3 Days",
        "vibe": "Colonial & Scenic",
        "highlights": [
            "UNESCO Nilgiri Mountain Railway toy train",
            "Doddabetta Peak viewpoint",
            "Botanical Gardens & handmade chocolate tasting",
        ],
        "base_cost_per_day": 2900,
        "suggested_days": 3,
    },
    "hampi": {
        "slug": "hampi",
        "name": "Hampi",
        "state": "Karnataka",
        "state_full": "Karnataka • Tungabhadra Basin",
        "category": "heritage adventure spiritual",
        "primary_category_display": "🏛️ Heritage",
        "description": "Surreal UNESCO World Heritage site with boulder-strewn landscapes, majestic 14th-century ruins, and riverside cafes.",
        "image_url": "https://www.holidaymonk.com/wp-content/uploads/2020/10/Vastuchitra_Stone-Chariot-Hampi.jpg",
        "best_time": "Oct – Mar",
        "duration": "2–3 Days",
        "modal_title": "Hampi",
        "modal_state": "Karnataka, India",
        "modal_hero_img": "https://www.holidaymonk.com/wp-content/uploads/2020/10/Vastuchitra_Stone-Chariot-Hampi.jpg",
        "categories_list": ["🏛️ Heritage", "🧗 Adventure", "🪔 Spiritual"],
        "modal_description": "Surreal open-air museum of Vijayanagara Empire stone monuments, dramatic boulder fields, coracle boat rides, and sunsets on Matanga Hill.",
        "modal_best_time": "Oct – Mar",
        "modal_duration": "2 – 3 Days",
        "vibe": "Mystical & Ancient",
        "highlights": [
            "Virupaksha Temple & Iconic Stone Chariot",
            "Matanga Hill sunrise boulder climb",
            "Coracle ride on the Tungabhadra River",
        ],
        "base_cost_per_day": 2400,
        "suggested_days": 3,
    },
    "rishikesh": {
        "slug": "rishikesh",
        "name": "Rishikesh",
        "state": "Uttarakhand",
        "state_full": "Uttarakhand • Himalayan Foothills",
        "category": "adventure spiritual nature",
        "primary_category_display": "🧗 Adventure",
        "description": "Yoga Capital of the World where the emerald Ganga flows from the Himalayas, offering white-water rafting and Ganga Aarti.",
        "image_url": "https://imgcld.yatra.com/ytimages/image/upload/v1486015791/Rishikesh_overview.jpg",
        "best_time": "Sep – May",
        "duration": "2–4 Days",
        "modal_title": "Rishikesh",
        "modal_state": "Uttarakhand, India",
        "modal_hero_img": "https://imgcld.yatra.com/ytimages/image/upload/v1486015791/Rishikesh_overview.jpg",
        "categories_list": ["🧗 Adventure", "🪔 Spiritual", "🌿 Nature"],
        "modal_description": "Yoga Capital of the World where the emerald Ganga flows from the Himalayas, offering white-water river rafting, bungee jumping, and sacred evening aartis.",
        "modal_best_time": "Sep – May",
        "modal_duration": "2 – 4 Days",
        "vibe": "Soulful & High-Energy",
        "highlights": [
            "Ganga white-water river rafting",
            "Parmarth Niketan Triveni Ghat evening aarti",
            "Beatles Ashram & cliffside organic cafes",
        ],
        "base_cost_per_day": 2700,
        "suggested_days": 3,
    },
    "udaipur": {
        "slug": "udaipur",
        "name": "Udaipur",
        "state": "Rajasthan",
        "state_full": "Rajasthan • Mewar Kingdom",
        "category": "heritage nature food",
        "primary_category_display": "🏛️ Heritage",
        "description": "The City of Lakes with gleaming marble palaces, romantic boat cruises on Lake Pichola, and rooftop sunset dining.",
        "image_url": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?auto=format&fit=crop&w=800&q=80",
        "best_time": "Oct – Mar",
        "duration": "2–3 Days",
        "modal_title": "Udaipur",
        "modal_state": "Rajasthan, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🏛️ Heritage", "🌿 Nature", "🍛 Food"],
        "modal_description": "Romantic Venice of the East adorned with shimmering lakes, ornate marble palaces, tranquil ghats, and royal Mewari heritage.",
        "modal_best_time": "Oct – Mar",
        "modal_duration": "2 – 3 Days",
        "vibe": "Romantic & Regal",
        "highlights": [
            "Lake Pichola sunset boat cruise to Jagmandir",
            "City Palace royal courtyards & museum",
            "Rooftop candlelit dinner overlooking lake",
        ],
        "base_cost_per_day": 3600,
        "suggested_days": 3,
    },
    "varkala": {
        "slug": "varkala",
        "name": "Varkala",
        "state": "Kerala",
        "state_full": "Kerala • South Coast",
        "category": "beaches nature spiritual",
        "primary_category_display": "🏖️ Beaches",
        "description": "Dramatic red laterite cliffs towering over the Arabian Sea, bohemian cliffside cafes, and natural mineral springs.",
        "image_url": "https://images.unsplash.com/photo-1621682372775-533449e550ed?auto=format&fit=crop&w=800&q=80",
        "best_time": "Nov – Mar",
        "duration": "2–3 Days",
        "modal_title": "Varkala",
        "modal_state": "Kerala, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1621682372775-533449e550ed?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🏖️ Beaches", "🌿 Nature", "🪔 Spiritual"],
        "modal_description": "Dramatic crimson cliffs overlooking the Arabian Sea, bohemian cafes, natural water springs, and world-class ayurvedic wellness.",
        "modal_best_time": "Nov – Mar",
        "modal_duration": "2 – 3 Days",
        "vibe": "Bohemian & Coastal",
        "highlights": [
            "Varkala North Cliff sunset cafe walk",
            "Papanasam Beach mineral water bath",
            "Ayurvedic massage & coastal wellness",
        ],
        "base_cost_per_day": 2700,
        "suggested_days": 3,
    },
    "coorg": {
        "slug": "coorg",
        "name": "Coorg (Kodagu)",
        "state": "Karnataka",
        "state_full": "Karnataka • Western Ghats",
        "category": "nature mountains food",
        "primary_category_display": "🌿 Nature",
        "description": "The Scotland of India, known for fragrant coffee and spice estates, lush rainforests, misty peaks, and cascading waterfalls.",
        "image_url": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80",
        "best_time": "Oct – Apr",
        "duration": "2–3 Days",
        "modal_title": "Coorg (Kodagu)",
        "modal_state": "Karnataka, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🌿 Nature", "🏔️ Mountains", "🍛 Food"],
        "modal_description": "Scotland of India known for fragrant Arabica coffee estates, spice trails, Kodava culinary delights (Pandi Curry), and Abbey Falls.",
        "modal_best_time": "Oct – Apr",
        "modal_duration": "2 – 3 Days",
        "vibe": "Lush & Peaceful",
        "highlights": [
            "Coffee & pepper plantation immersive tour",
            "Abbey Falls & Raja's Seat valley sunset",
            "Namdroling Golden Temple Tibetan monastery",
        ],
        "base_cost_per_day": 3100,
        "suggested_days": 3,
    },
    "pondicherry": {
        "slug": "pondicherry",
        "name": "Pondicherry",
        "state": "Puducherry",
        "state_full": "Puducherry • Coromandel Coast",
        "category": "beaches heritage food",
        "primary_category_display": "🏖️ Beaches",
        "description": "Charming coastal town blending yellow French colonial villas, bougainvillea streets, chic bakeries, and Auroville.",
        "image_url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
        "best_time": "Oct – Mar",
        "duration": "2–3 Days",
        "modal_title": "Pondicherry",
        "modal_state": "Puducherry, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🏖️ Beaches", "🏛️ Heritage", "🍛 Food"],
        "modal_description": "Charming coastal union territory blending mustard-yellow French colonial villas, serene bougainvillea lanes, French bakeries, and Auroville.",
        "modal_best_time": "Oct – Mar",
        "modal_duration": "2 – 3 Days",
        "vibe": "French Riviera & Zen",
        "highlights": [
            "White Town heritage bicycle trail",
            "Matrimandir meditation in Auroville",
            "Rock Beach evening promenade & creperies",
        ],
        "base_cost_per_day": 3000,
        "suggested_days": 3,
    },
    "mumbai": {
        "slug": "mumbai",
        "name": "Mumbai",
        "state": "Maharashtra",
        "state_full": "Maharashtra • Financial Capital",
        "category": "cities food heritage",
        "primary_category_display": "🏙️ Cities",
        "description": "India's dynamic maximum city featuring iconic colonial architecture, Marine Drive promenades, and legendary street food.",
        "image_url": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80",
        "best_time": "Nov – Feb",
        "duration": "2–4 Days",
        "modal_title": "Mumbai",
        "modal_state": "Maharashtra, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🏙️ Cities", "🍛 Food", "🏛️ Heritage"],
        "modal_description": "India's pulsating city of dreams, boasting Victorian Gothic architecture, Queen's Necklace Marine Drive, Bollywood glamour, and iconic street culinary staples.",
        "modal_best_time": "Nov – Feb",
        "modal_duration": "2 – 4 Days",
        "vibe": "Electric & Coastal",
        "highlights": [
            "Marine Drive & Gateway of India walk",
            "Colaba Causeway & Kala Ghoda art district",
            "Chowpatty Pav Bhaji & Vada Pav food trail",
        ],
        "base_cost_per_day": 4500,
        "suggested_days": 3,
    },
    "hyderabad": {
        "slug": "hyderabad",
        "name": "Hyderabad",
        "state": "Telangana",
        "state_full": "Telangana • City of Pearls",
        "category": "cities food heritage",
        "primary_category_display": "🏙️ Cities",
        "description": "City of Pearls and Nizams, where centuries-old historical monuments like Charminar meet world-famous Biryani.",
        "image_url": "https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&w=800&q=80",
        "best_time": "Oct – Mar",
        "duration": "2–3 Days",
        "modal_title": "Hyderabad",
        "modal_state": "Telangana, India",
        "modal_hero_img": "https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&w=800&q=80",
        "categories_list": ["🏙️ Cities", "🍛 Food", "🏛️ Heritage"],
        "modal_description": "The regal City of Pearls where Nizam royalty meets cutting-edge tech, famed for Golconda Fort acoustic marvels, Charminar, and authentic Hyderabadi Dum Biryani.",
        "modal_best_time": "Oct – Mar",
        "modal_duration": "2 – 3 Days",
        "vibe": "Nizami & Flavorsome",
        "highlights": [
            "Charminar & Laad Bazaar pearl shopping",
            "Golconda Fort sound and light show",
            "Authentic Hyderabadi Dum Biryani & Irani Chai",
        ],
        "base_cost_per_day": 3300,
        "suggested_days": 3,
    },
    "varanasi": {
        "slug": "varanasi",
        "name": "Varanasi",
        "state": "Uttar Pradesh",
        "state_full": "Uttar Pradesh • Holy Ganges",
        "category": "spiritual heritage food",
        "primary_category_display": "🪔 Spiritual",
        "description": "One of the world's oldest living cities on the sacred Ganges, famous for ancient ghats, evocative evening aartis, and silk weaving.",
        "image_url": "https://cdn.audleytravel.com/4767/3405/79/209236-the-ghats-varanasi.jpg",
        "best_time": "Oct – Mar",
        "duration": "2–3 Days",
        "modal_title": "Varanasi",
        "modal_state": "Uttar Pradesh, India",
        "modal_hero_img": "https://cdn.audleytravel.com/4767/3405/79/209236-the-ghats-varanasi.jpg",
        "categories_list": ["🪔 Spiritual", "🏛️ Heritage", "🍛 Food"],
        "modal_description": "The spiritual capital of India along the holy River Ganga, legendary for its 84 ghats, soul-stirring Ganga Aarti, maze-like gallis, and Banarasi cuisine.",
        "modal_best_time": "Oct – Mar",
        "modal_duration": "2 – 3 Days",
        "vibe": "Timeless & Spiritual",
        "highlights": [
            "Sunrise boat ride on the holy Ganges",
            "Dashashwamedh Ghat grand evening Aarti",
            "Kashi Vishwanath corridor & Banarasi Paan",
        ],
        "base_cost_per_day": 2500,
        "suggested_days": 3,
    },
}


from data.stays_and_food import STAYS_AND_FOOD, VERIFIED_DATE_DISCLAIMER


def _enrich_destination(dest):
    """Attach hotel and restaurant data to a destination dict."""
    if not dest:
        return None
    d = dest.copy()
    slug = d.get("slug")
    data = STAYS_AND_FOOD.get(slug, {"hotels": [], "restaurants": []})
    d["hotels"] = data.get("hotels", [])
    d["restaurants"] = data.get("restaurants", [])
    d["disclaimer"] = VERIFIED_DATE_DISCLAIMER
    return d


def get_all_destinations():
    """Return all destinations as a list of dictionaries with hotels and restaurants."""
    return [_enrich_destination(d) for d in DESTINATIONS.values()]


def get_destination_by_slug(slug):
    """Return a single destination dictionary by slug, or None."""
    dest = DESTINATIONS.get(slug)
    return _enrich_destination(dest) if dest else None


def filter_destinations(query="", category="all"):
    """
    Filter destinations by search query and category.
    Server-side filtering for zero-JS functionality.
    """
    query = (query or "").strip().lower()
    category = (category or "all").strip().lower()
    results = []

    for d in DESTINATIONS.values():
        # Category filter check
        cat_match = True
        if category and category != "all":
            dest_cats = [c.strip() for c in d["category"].split()]
            cat_match = category in dest_cats

        # Search query check
        query_match = True
        if query:
            searchable_text = f"{d['name']} {d['state']} {d['description']} {d['category']} {' '.join(d.get('highlights', []))}".lower()
            query_match = query in searchable_text

        if cat_match and query_match:
            results.append(_enrich_destination(d))

    return results
