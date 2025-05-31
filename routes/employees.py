from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from services.employee_service import EmployeeService
from forms.employee_form import EmployeeForm
from services.poste_service import PosteService

employees_bp = Blueprint('employees_bp', __name__, url_prefix='/employees')

@employees_bp.route('/')
def list_employees():
    page = request.args.get('page', 1, type=int)
    pagination = EmployeeService.get_employees_page(page, per_page=5)
    form = EmployeeForm()
    form.poste_id.choices = [(p.id, p.titre) for p in PosteService.get_all()]
    
    if request.args.get("query"):
        query = request.args.get("query")
        records = EmployeeService.search_employees(query)
        return render_template('employees/employees.html', 
                             employees=records,
                             pagination=pagination,
                             form=form)
    else:
        return render_template('employees/employees.html', 
                             employees=pagination.items, 
                             pagination=pagination,
                             form=form)

@employees_bp.route('/search')
def search_employees():
    query = request.args.get('query', '')
    employees = EmployeeService.search_employees(query)
    return jsonify([{
        'id': emp.id,
        'nom': emp.nom,
        'prenom': emp.prenom,
        'date_hire': emp.date_hire.strftime('%d/%m/%Y'),
        'poste': emp.poste.titre if emp.poste else ''
    } for emp in employees])

@employees_bp.route('/add', methods=['POST'])
def add_employee():
    form = EmployeeForm()
    form.poste_id.choices = [(p.id, p.titre) for p in PosteService.get_all()]
    
    if form.validate_on_submit():
        EmployeeService.create_employee(
            nom=form.nom.data,
            prenom=form.prenom.data,
            date_hire=form.date_hire.data,
            poste_id=form.poste_id.data
        )
        flash('Employé ajouté avec succès!', 'success')
        return redirect(url_for('employees_bp.list_employees'))
    
    flash('Erreur lors de l\'ajout de l\'employé.', 'error')
    return redirect(url_for('employees_bp.list_employees'))

@employees_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    if request.method == 'GET':
        employee = EmployeeService.get_employee_by_id(id)
        return jsonify({
            'id': employee.id,
            'nom': employee.nom,
            'prenom': employee.prenom,
            'date_hire': employee.date_hire.strftime('%Y-%m-%d'),
            'poste_id': employee.poste_id
        })
    
    # Handle POST request
    data = request.get_json()
    try:
        EmployeeService.update_employee(
            id=id,
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            date_hire=data.get('date_hire'),
            poste_id=data.get('poste_id')
        )
        return jsonify({'success': True, 'message': 'Employé modifié avec succès!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@employees_bp.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    try:
        EmployeeService.delete_employee(id)
        flash('Employé supprimé avec succès!', 'success')
        return jsonify({'success': True})
    except Exception as e:
        flash('Erreur lors de la suppression de l\'employé.', 'error')
        return jsonify({'success': False, 'error': str(e)}), 400