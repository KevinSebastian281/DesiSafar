# DesiSafar — India Trip & Itinerary Planner (Flask Backend)

DesiSafar is an India-focused group trip itinerary planner built with a **pure server-rendered, zero-JavaScript architecture** using **Python, Flask, Jinja2 templates, and standard HTML forms**.

---

## 🌟 Key Features

1. **Zero JavaScript Architecture**:
   - **No `<script>` tags, no inline `on*` event handlers, and no frontend JavaScript frameworks**.
   - All searching, category filtering, modal detail inspection, destination addition/removal, step progression, dynamic multi-day itinerary generation, and budget calculations are processed **100% server-side**.
2. **Session-Backed Multi-Step Wizard**:
   - **Step 1: Destinations (`/destinations`)** — Search across 16 curated Indian destinations, filter by category chip (Beaches, Mountains, Heritage, etc.), preview modal details.
     - **"Where to Stay" & "Where to Eat"**: Every destination modal features curated Google Places listings with ratings (`★ 4.6`), localities, price tiers (`₹₹`), direct `tel:` call links, and a verified date disclaimer.
     - **Dynamic Starting Point**: Defaults to nothing (`""`). The input menu dynamically includes all airports/railway gateways near your selected destinations followed by all-India transit hubs, or allows typing any custom starting location.
     - **Dynamic Dates**: Defaults to nothing (`""`). The user defines their start date, and the end date is automatically calculated based on the suggested duration of the selected destinations (e.g. Goa 4d + Munnar 3d = 7 days).
   - **Step 2: Preferences (`/preferences`)** — Select travel vibes, activity interests, spending tiers (Budget, Standard, Premium, Luxury), lodging categories, and diet preferences.
   - **Step 3: Itinerary (`/itinerary`)** — Dynamically synthesized day-by-day travel schedules with real dates, time slots (Morning, Afternoon, Evening), local transit blocks, personalized culinary recommendations, and **suggested hotel + restaurant recommendations per destination**.
   - **Step 4: Budget (`/budget`)** — Multi-category financial distribution (Stays, Transport, Food, Activities, Misc), equal per-person cost splits, daily averages, budget tier comparisons, and **named hotel references** under the Accommodation breakdown.
3. **Step Guards & State Reset**:
   - Step guards redirect users back with server-side flash notifications if prerequisite selections are missing.
   - Session reset route (`/reset`) clears all trip state and returns to Step 1.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+ installed

### 2. Installation
Clone or navigate to the repository directory and install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the Development Server
Run the Flask server:

```bash
flask run --port=5000
```
Or run directly:

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

### 4. Running the Test Suite
Execute the automated test suite with pytest:

```bash
python -m pytest -v
```

---

## 📁 Project Structure

```
desisafar/
├── app.py                  # Flask application factory, configuration, session settings
├── data/
│   └── destinations.py     # 16-destination catalog with metadata, categories, pricing
├── logic/
│   ├── itinerary.py        # Dynamic rule-based day-by-day itinerary engine
│   └── budget.py           # Multi-category budget calculation & per-person split engine
├── routes/
│   ├── main.py             # Landing page (/) and session reset (/reset)
│   ├── destinations.py     # Step 1: list, search, category filter, detail, add/remove
│   ├── preferences.py      # Step 2: travel style & lodging preferences
│   ├── itinerary.py        # Step 3: personalized generated itinerary
│   └── budget.py           # Step 4: trip budget breakdown & cost split
├── templates/
│   ├── base.html           # Shared layout with flash alerts, wizard nav, brand header
│   ├── index.html          # Landing page (Page 1)
│   ├── destinations.html   # Step 1: Destination explorer & route builder
│   ├── preferences.html    # Step 2: Trip style & travel preferences
│   ├── itinerary.html      # Step 3: Generated day-by-day itinerary
│   └── budget.html         # Step 4: Trip budget breakdown & cost split
├── static/
│   ├── css/                # Original stylesheets (styles.css, destinations.css, navbar.css, etc.)
│   ├── images/             # Logos, badges, and feature graphics
│   └── videos/             # DesiSafar.mp4
├── tests/
│   └── test_app.py         # Automated unit & integration tests
├── requirements.txt         # Flask, python-dotenv
└── README.md
```

---

## 📊 Data Layer & Pricing Assumptions

Since the original static prototype did not include a database or live transit API, realistic mock data and lookup heuristics are structured in Python:

1. **Per-Destination Base Daily Cost (`base_cost_per_day`)**:
   - Goa: ₹3,500/day
   - Munnar: ₹2,800/day
   - Manali: ₹3,200/day
   - Jaipur: ₹3,000/day
   - Kashmir: ₹4,200/day
   - Gokarna: ₹2,600/day
   - Ooty: ₹2,900/day
   - Hampi: ₹2,400/day
   - Rishikesh: ₹2,700/day
   - Udaipur: ₹3,600/day
   - Varkala: ₹2,700/day
   - Coorg: ₹3,100/day
   - Pondicherry: ₹3,000/day
   - Mumbai: ₹4,500/day
   - Hyderabad: ₹3,300/day
   - Varanasi: ₹2,500/day

2. **Multiplier Scales**:
   - **Budget Tier Multipliers**: Budget-Friendly (`0.75×`), Standard (`1.0×`), Premium (`1.35×`), Luxury (`2.1×`).
   - **Accommodation Multipliers**: Hostel (`0.7×`), Budget Hotel (`0.85×`), 3-Star (`1.0×`), 4-Star (`1.4×`), 5-Star (`2.2×`).

3. **Expense Distribution Formula**:
   - Accommodation: **39%**
   - Transportation: **19%**
   - Food & Dining: **16%**
   - Activities & Sightseeing: **15%**
   - Miscellaneous Buffer: **11%**
   - Total: **100%**
