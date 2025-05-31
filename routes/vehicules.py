from flask import Blueprint, render_template, request, jsonify
from models.vehicule import Vehicule
from models.etat import Etat
from models.database import db

vehicules_bp = Blueprint('vehicules', __name__)

@vehicules_bp.route('/vehicules')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get paginated vehicles
    pagination = Vehicule.query.paginate(page=page, per_page=per_page, error_out=False)
    vehicules = pagination.items
    
    # Get all states for the forms
    etats = Etat.query.all()
    
    return render_template('vehicules/vehicules.html', 
                         vehicules=vehicules, 
                         etats=etats,
                         pagination=pagination)

@vehicules_bp.route('/vehicules/add', methods=['POST'])
def add_vehicule():
    try:
        data = request.get_json()
        vehicule = Vehicule(
            immatriculation=data['immatriculation'],
            marque=data['marque'],
            modele=data['modele'],
            etat_id=data['etat_id']
        )
        db.session.add(vehicule)
        db.session.commit()
        return jsonify({'success': True, 'vehicule': {
            'id': vehicule.id,
            'immatriculation': vehicule.immatriculation,
            'marque': vehicule.marque,
            'modele': vehicule.modele,
            'etat_id': vehicule.etat_id
        }})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@vehicules_bp.route('/vehicules/<int:vehicule_id>', methods=['PUT'])
def update_vehicule(vehicule_id):
    try:
        data = request.get_json()
        vehicule = Vehicule.query.get(vehicule_id)
        if vehicule:
            vehicule.immatriculation = data['immatriculation']
            vehicule.marque = data['marque']
            vehicule.modele = data['modele']
            vehicule.etat_id = data['etat_id']
            db.session.commit()
            return jsonify({'success': True, 'vehicule': {
                'id': vehicule.id,
                'immatriculation': vehicule.immatriculation,
                'marque': vehicule.marque,
                'modele': vehicule.modele,
                'etat_id': vehicule.etat_id
            }})
        return jsonify({'success': False, 'error': 'Vehicle not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@vehicules_bp.route('/vehicules/<int:vehicule_id>', methods=['DELETE'])
def delete_vehicule(vehicule_id):
    try:
        vehicule = Vehicule.query.get(vehicule_id)
        if vehicule:
            db.session.delete(vehicule)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Vehicle not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400 