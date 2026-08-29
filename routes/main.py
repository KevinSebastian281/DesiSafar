from flask import Blueprint, render_template, session, redirect, url_for, flash
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/reset')
def reset_session():
    session['selected_destinations'] = []
    session['trip_details'] = {'start_location': '', 'departure_date': '', 'return_date': '', 'travellers': 4}
    session.pop('preferences', None)
    session.modified = True
    flash('Trip selections have been reset. Start building a new journey!', 'info')
    return redirect(url_for('destinations.list_destinations'))
