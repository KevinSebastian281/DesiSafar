import requests
import re
BASE_URL = 'http://127.0.0.1:5000'

def run_e2e_flow():
    session = requests.Session()
    print('--- 1. Testing Landing Page (/) ---')
    res = session.get(f'{BASE_URL}/')
    assert res.status_code == 200, f'Landing page failed with {res.status_code}'
    assert 'Plan your dream India trip in' in res.text
    print('[PASS] Landing page rendered successfully.')
    print('\n--- 2. Testing Reset Route (/reset) & Default Empty States ---')
    res = session.get(f'{BASE_URL}/reset')
    assert res.status_code == 200
    assert 'Trip selections have been reset.' in res.text
    assert 'id="startLocationInput" name="start_location" class="form-input" placeholder="Type any starting place or pick from list..." list="startingCitiesList" value=""' in res.text
    print('[PASS] Session reset and empty default starting point/dates verified.')
    print('\n--- 3. Testing Destination Modals for Where to Stay & Where to Eat ---')
    res = session.get(f'{BASE_URL}/destinations')
    assert res.status_code == 200
    assert 'Where to Stay' in res.text
    assert 'Where to Eat' in res.text
    assert 'Hilton Goa Resort' in res.text
    assert 'Blanket Hotel' in res.text
    assert 'The Second House' in res.text
    assert 'Munnar Samrudhi Restaurant' in res.text
    assert 'Details last verified Aug 2026' in res.text
    print('[PASS] Modal Where to Stay and Where to Eat sections & Aug 2026 disclaimer verified.')
    print('\n--- 4. Testing Category Filter & Search on /destinations ---')
    res = session.get(f'{BASE_URL}/destinations?category=beaches')
    assert res.status_code == 200
    assert 'Goa' in res.text
    assert 'Gokarna' in res.text
    print('[PASS] Category filter (beaches) verified.')
    res = session.get(f'{BASE_URL}/destinations?q=shikara')
    assert res.status_code == 200
    assert 'Kashmir' in res.text
    print('[PASS] Destination search (shikara -> Kashmir) verified.')
    print('\n--- 5. Adding Destinations (Goa + Munnar) & Verifying Nearby Hubs ---')
    res = session.post(f'{BASE_URL}/destinations/toggle', data={'slug': 'goa'}, allow_redirects=True)
    assert res.status_code == 200
    assert 'Added Goa to your trip!' in res.text
    res = session.post(f'{BASE_URL}/destinations/toggle', data={'slug': 'munnar'}, allow_redirects=True)
    assert res.status_code == 200
    assert 'Added Munnar to your trip!' in res.text
    assert 'Goa (Dabolim Airport), Goa' in res.text or 'Goa (Mopa Airport), Goa' in res.text
    assert 'Kochi (Cochin Airport), Kerala' in res.text or 'Ernakulam Junction, Kerala' in res.text
    print('[PASS] 2 destinations added and dynamic nearby transit hubs verified in datalist.')
    print('\n--- 5b. Verifying Access to /preferences is Blocked Without Start Date ---')
    res_blocked = session.get(f'{BASE_URL}/preferences', allow_redirects=True)
    assert res_blocked.status_code == 200
    assert 'Please select a trip start date before setting preferences.' in res_blocked.text
    assert 'Where do you want to go?' in res_blocked.text
    print('[PASS] Blocked direct navigation to preferences without start date verified.')
    res_empty_post = session.post(f'{BASE_URL}/destinations/update_trip', data={'start_location': 'Indiranagar, Bengaluru', 'departure_date': '', 'travellers': '3'}, allow_redirects=True)
    assert res_empty_post.status_code == 200
    assert 'Please select a trip start date to continue to preferences.' in res_empty_post.text
    assert 'Where do you want to go?' in res_empty_post.text
    print('[PASS] Blocked empty start date form submission verified.')
    print('\n--- 6. Auto-Calculating Return Date based on Places Selected ---')
    res = session.post(f'{BASE_URL}/destinations/update_trip', data={'start_location': 'Indiranagar, Bengaluru', 'departure_date': '2026-11-01', 'return_date': '', 'travellers': '3'}, allow_redirects=True)
    assert res.status_code == 200
    assert 'What kind of trip are you imagining?' in res.text
    assert 'Goa' in res.text
    assert 'Munnar' in res.text
    assert '3 Travellers' in res.text
    assert 'Indiranagar, Bengaluru' in res.text
    assert '01 Nov – 07 Nov 2026' in res.text
    print('[PASS] Custom starting point accepted and return date auto-calculated (01 Nov - 07 Nov 2026).')
    print('\n--- 7. Checking Preferences Dynamic Pricing & Snapshot ---')
    res = session.get(f'{BASE_URL}/preferences')
    assert res.status_code == 200
    assert 'price-range-budget' in res.text
    assert 'price-range-luxury' in res.text
    assert 'snapshotCost' in res.text
    print('[PASS] Estimated price tags under budget buttons and preference snapshot rendered.')
    print('\n--- 8. Submitting Preferences (Romantic, Foodie, 4-Star, Vegetarian) ---')
    res = session.post(f'{BASE_URL}/preferences', data={'vibe': ['romantic', 'foodie', 'explorer'], 'interest': ['beaches', 'food', 'cafes', 'photography'], 'budget': 'premium', 'stay': '4_star', 'diet': 'vegetarian', 'dining': ['local_food', 'street_food', 'cafes']}, allow_redirects=True)
    assert res.status_code == 200
    assert 'Your Travel Itinerary' in res.text
    assert 'Goa + Munnar' in res.text
    assert '7 Days / 6 Nights' in res.text
    assert '3 People' in res.text
    assert 'Vegetarian' in res.text
    assert '4-Star Resort' in res.text
    print('[PASS] Preferences saved and generated itinerary (Step 3) rendered successfully.')
    print('\n--- 9. Checking Itinerary Day Stays & Dining Recommendations ---')
    assert 'Suggested Stay' in res.text
    assert 'Suggested Dining' in res.text
    assert 'Hilton Goa Resort' in res.text or 'Holiday Inn Resort Goa' in res.text
    assert 'Blanket Hotel &amp; Spa' in res.text or 'Blanket Hotel & Spa' in res.text or 'Grand Plaza' in res.text
    print('[PASS] Dynamic suggested hotel and restaurant recommendations verified on Itinerary days.')
    print('\n--- 10. Checking Budget Page (/budget) Hotel Connection ---')
    res = session.get(f'{BASE_URL}/budget')
    assert res.status_code == 200
    assert 'What will your trip cost?' in res.text
    assert 'for 3 travellers' in res.text
    assert 'Accommodation' in res.text
    assert 'Hilton Goa Resort' in res.text or 'Holiday Inn Resort Goa' in res.text
    print('[PASS] Step 4 budget breakdown verified with real hotel connection.')
    print('\n--- 11. Verifying Clean Markup on Live Server Pages ---')
    for path in ['/', '/destinations', '/preferences', '/itinerary', '/budget']:
        page_res = session.get(f'{BASE_URL}{path}')
        inline_events = re.findall('\\son[a-z]+\\s*=', page_res.text, re.IGNORECASE)
        assert not inline_events, f'Found inline handler {inline_events} in {path}'
    print('[PASS] Clean markup audit PASSED on all live routes.')
    print('\n==========================================')
    print('ALL END-TO-END VERIFICATION CHECKS PASSED!')
    print('==========================================')
if __name__ == '__main__':
    run_e2e_flow()
