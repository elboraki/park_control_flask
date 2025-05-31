from models.employee import Employee, db

class EmployeeRepository:
    @staticmethod
    def get_search_query(query):
        return Employee.query.filter(Employee.nom.ilike(f"%{query}%")).all()
    
    @staticmethod
    def get_paginated(page, per_page=5):
        return Employee.query.paginate(page=page, per_page=per_page)
    
    @staticmethod
    def get_all():
        return Employee.query.all()