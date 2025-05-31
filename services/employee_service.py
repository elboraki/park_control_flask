from repositories.employee_repository import EmployeeRepository
from models.employee import Employee
from models.database import db
from sqlalchemy import or_

class EmployeeService:

    @staticmethod
    def list_employees():
        return EmployeeRepository.get_all()
    
    @staticmethod
    def search_employee_name(query):
        return EmployeeRepository.get_search_query(query)
    
    @staticmethod
    def get_employees_page(page, per_page=5):
        return EmployeeRepository.get_paginated(page, per_page)
    
    @staticmethod
    def create_employee(nom, prenom, date_hire, poste_id):
        employee = Employee(
            nom=nom,
            prenom=prenom,
            date_hire=date_hire,
            poste_id=poste_id
        )
        db.session.add(employee)
        db.session.commit()
        return employee
    
    @staticmethod
    def search_employees(query):
        if not query:
            return Employee.query.all()
        
        search_term = f"%{query}%"
        return Employee.query.join(Employee.poste).filter(
            or_(
                Employee.nom.ilike(search_term),
                Employee.prenom.ilike(search_term),
                Employee.poste.has(titre=search_term)
            )
        ).all()
    
    @staticmethod
    def get_employee_by_id(id):
        return Employee.query.get_or_404(id)
    
    @staticmethod
    def update_employee(id, nom, prenom, date_hire, poste_id):
        employee = EmployeeService.get_employee_by_id(id)
        employee.nom = nom
        employee.prenom = prenom
        employee.date_hire = date_hire
        employee.poste_id = poste_id
        db.session.commit()
        return employee
    
    @staticmethod
    def delete_employee(id):
        employee = EmployeeService.get_employee_by_id(id)
        db.session.delete(employee)
        db.session.commit()
        return True
