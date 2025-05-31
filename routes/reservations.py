from flask import Blueprint, render_template, request, jsonify
from models.reservation import Reservation
from models.vehicule import Vehicule
from models.employee import Employee
from models.utilisateur import Utilisateur
from models.database import db
from datetime import datetime

reservations_bp = Blueprint('reservations', __name__)

@reservations_bp.route('/reservations')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get paginated reservations
    pagination = Reservation.query.order_by(Reservation.date_debut.desc()).paginate(page=page, per_page=per_page, error_out=False)
    reservations = pagination.items
    
    # Get all vehicles, employees, and users for the forms
    vehicules = Vehicule.query.all()
    employees = Employee.query.all()
    utilisateurs = Utilisateur.query.all()
    
    return render_template('reservations/reservations.html', 
                         reservations=reservations,
                         vehicules=vehicules,
                         employees=employees,
                         utilisateurs=utilisateurs,
                         pagination=pagination)

@reservations_bp.route('/reservations/add', methods=['POST'])
def add_reservation():
    try:
        data = request.get_json()
        
        # Convert string dates to datetime objects
        date_debut = datetime.strptime(data['date_debut'], '%Y-%m-%dT%H:%M')
        date_fin = datetime.strptime(data['date_fin'], '%Y-%m-%dT%H:%M')
        
        # Check if the vehicle is available for the selected period
        existing_reservation = Reservation.query.filter(
            Reservation.vehicule_id == data['vehicule_id'],
            Reservation.date_debut <= date_fin,
            Reservation.date_fin >= date_debut
        ).first()
        
        if existing_reservation:
            return jsonify({
                'success': False, 
                'error': 'Le véhicule est déjà réservé pour cette période'
            }), 400
        
        reservation = Reservation(
            date_debut=date_debut,
            date_fin=date_fin,
            utilisateur_id=data['utilisateur_id'],
            vehicule_id=data['vehicule_id'],
            employee_id=data['employee_id']
        )
        
        db.session.add(reservation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'reservation': {
                'id': reservation.id,
                'date_reservation': reservation.date_reservation.isoformat(),
                'date_debut': reservation.date_debut.isoformat(),
                'date_fin': reservation.date_fin.isoformat(),
                'utilisateur_id': reservation.utilisateur_id,
                'vehicule_id': reservation.vehicule_id,
                'employee_id': reservation.employee_id
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@reservations_bp.route('/reservations/<int:reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    try:
        data = request.get_json()
        reservation = Reservation.query.get(reservation_id)
        
        if not reservation:
            return jsonify({'success': False, 'error': 'Reservation not found'}), 404
        
        # Convert string dates to datetime objects
        date_debut = datetime.strptime(data['date_debut'], '%Y-%m-%dT%H:%M')
        date_fin = datetime.strptime(data['date_fin'], '%Y-%m-%dT%H:%M')
        
        # Check if the vehicle is available for the selected period (excluding current reservation)
        existing_reservation = Reservation.query.filter(
            Reservation.vehicule_id == data['vehicule_id'],
            Reservation.date_debut <= date_fin,
            Reservation.date_fin >= date_debut,
            Reservation.id != reservation_id
        ).first()
        
        if existing_reservation:
            return jsonify({
                'success': False, 
                'error': 'Le véhicule est déjà réservé pour cette période'
            }), 400
        
        reservation.date_debut = date_debut
        reservation.date_fin = date_fin
        reservation.utilisateur_id = data['utilisateur_id']
        reservation.vehicule_id = data['vehicule_id']
        reservation.employee_id = data['employee_id']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'reservation': {
                'id': reservation.id,
                'date_reservation': reservation.date_reservation.isoformat(),
                'date_debut': reservation.date_debut.isoformat(),
                'date_fin': reservation.date_fin.isoformat(),
                'utilisateur_id': reservation.utilisateur_id,
                'vehicule_id': reservation.vehicule_id,
                'employee_id': reservation.employee_id
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@reservations_bp.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    try:
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            db.session.delete(reservation)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Reservation not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400 