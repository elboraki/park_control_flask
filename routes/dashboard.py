from flask import Blueprint, render_template, jsonify
from models.vehicule import Vehicule
from models.employee import Employee
from models.reservation import Reservation
from models.utilisateur import Utilisateur
from models.etat import Etat
from models.database import db
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from routes.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    return render_template('dashboard/dashboard.html')

@dashboard_bp.route('/api/dashboard/vehicle-stats')
@login_required
def vehicle_stats():
    try:
        # Get vehicle count by state
        vehicle_states = db.session.query(
            Etat.libelle,
            func.count(Vehicule.id)
        ).join(Vehicule).group_by(Etat.libelle).all()
        
        # Get vehicle count by brand
        vehicle_brands = db.session.query(
            Vehicule.marque,
            func.count(Vehicule.id)
        ).group_by(Vehicule.marque).all()
        
        return jsonify({
            'states': [{'label': state, 'count': count} for state, count in vehicle_states],
            'brands': [{'label': brand, 'count': count} for brand, count in vehicle_brands]
        })
    except Exception as e:
        print(f"Error in vehicle_stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/api/dashboard/reservation-stats')
@login_required
def reservation_stats():
    try:
        # Get reservations for the last 6 months
        six_months_ago = datetime.now() - timedelta(days=180)
        
        # Monthly reservations using MySQL date functions
        monthly_reservations = db.session.query(
            func.date_format(Reservation.date_debut, '%Y-%m').label('month'),
            func.count(Reservation.id)
        ).filter(Reservation.date_debut >= six_months_ago)\
         .group_by('month')\
         .order_by('month')\
         .all()
        
        # Reservations by vehicle
        vehicle_reservations = db.session.query(
            Vehicule.immatriculation,
            func.count(Reservation.id)
        ).join(Reservation)\
         .group_by(Vehicule.immatriculation)\
         .order_by(func.count(Reservation.id).desc())\
         .limit(5)\
         .all()
        
        return jsonify({
            'monthly': [{'month': month, 'count': count} 
                       for month, count in monthly_reservations],
            'vehicles': [{'vehicle': vehicle, 'count': count} 
                        for vehicle, count in vehicle_reservations]
        })
    except Exception as e:
        print(f"Error in reservation_stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/api/dashboard/employee-stats')
@login_required
def employee_stats():
    try:
        # Get employee count by poste (position)
        employee_postes = db.session.query(
            Employee.poste_id,
            func.count(Employee.id)
        ).group_by(Employee.poste_id).all()
        
        # Get employee count by hire date (grouped by year)
        employee_years = db.session.query(
            extract('year', Employee.date_hire).label('year'),
            func.count(Employee.id)
        ).group_by('year')\
         .order_by('year')\
         .all()
        
        return jsonify({
            'departments': [{'label': f'Poste {poste_id}', 'count': count} 
                           for poste_id, count in employee_postes],
            'roles': [{'label': f'Année {year}', 'count': count} 
                     for year, count in employee_years]
        })
    except Exception as e:
        print(f"Error in employee_stats: {str(e)}")
        return jsonify({'error': str(e)}), 500 