# Основной файл сервера
# Реализованные эндпоинты:
# 1. /get_employees - возвращает список сотрудников с пагинацией
# 2. /get_employee_by_id - возвращает сотрудника по id
# 3. /create_employee - создает нового сотрудника
# 4. /update_employee - обновляет информацию о сотруднике
# 5. /delete_employee - удаляет сотрудника

from flask import Flask
from flask import jsonify
from flask import Response
from flask import request

from flask_cors import CORS

from database import DataBaseManager
from models import Employee


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empl.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_manager = DataBaseManager(app=app)


@app.route('/get_employees', methods=['GET'])
def get_employees() -> Response:
    """Endpoint возвращает список сотрудников с пагинацией"""

    # Получаем параметры пагинации из запроса
    page = request.args.get('page', 1, type=int)
    # Получаем количество сотрудников на странице
    per_page = request.args.get('per_page', 100, type=int)
    # Получаем данные с пагинацией
    paginated_data = Employee.query.paginate(page=page, per_page=per_page)

    # Формируем ответ
    data: dict = {
        'employees': [employee.to_dict() for employee in paginated_data.items],
        'total': paginated_data.total,
        'pages': paginated_data.pages,
        'current_page': paginated_data.page,
        'per_page': paginated_data.per_page
    }

    return jsonify(data), 200


@app.route('/get_employee_by_id', methods=['GET'])
def get_employee_by_id() -> Response:
    """Endpoint возвращает сотрудника по id"""
    id = request.args.get('id', type=int)
    employee = Employee.query.get(id)

    if employee:
        return jsonify(employee.to_dict()), 200
    else:
        return jsonify({'error': 'Сотрудник не найден'}), 404


@app.route('/create_employee', methods=['POST'])
def create_employee() -> Response:
    """Endpoint создает нового сотрудника"""
    data = request.json

    if not data:
        return jsonify({'error': 'Некорректные данные'}), 400

    employee = Employee(
        full_name=data['full_name'],
        position=data['position'],
        salary=data['salary'],
        hire_date=data['hire_date'],
    )

    db_manager.session.add(employee)
    db_manager.session.commit()

    return jsonify({'message': 'Сотрудник успешно создан'}), 201


@app.route('/update_employee', methods=['PUT'])
def update_employee() -> Response:
    """Endpoint обновляет информацию о сотруднике"""
    data = request.json
    id = request.args.get('id', type=int)
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'error': 'Сотрудник не найден'}), 404

    employee.full_name = data.get('full_name', employee.full_name)
    employee.position = data.get('position', employee.position)
    employee.salary = data.get('salary', employee.salary)
    employee.hire_date = data.get('hire_date', employee.hire_date)

    db_manager.session.commit()

    return jsonify({'message': 'Сотрудник успешно обновлен'}), 200


@app.route('/delete_employee', methods=['DELETE'])
def delete_employee() -> Response:
    """Endpoint удаляет сотрудника"""
    id = request.args.get('id', type=int)
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'error': 'Сотрудник не найден'}), 404

    db_manager.session.delete(employee)
    db_manager.session.commit()

    return jsonify({'message': 'Сотрудник успешно удален'}), 200


if __name__ == '__main__':
    db_manager.init_database(test_data=False)
    app.run(debug=True)
