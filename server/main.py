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
def get_employees() -> tuple[Response, int]:
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
    ...


@app.route('/create_employee', methods=['POST'])
def create_employee() -> Response:
    """Endpoint создает нового сотрудника"""
    ...


@app.route('/update_employee', methods=['PUT'])
def update_employee() -> Response:
    """Endpoint обновляет информацию о сотруднике"""
    ...


@app.route('/delete_employee', methods=['DELETE'])
def delete_employee() -> Response:
    """Endpoint удаляет сотрудника"""
    ...


if __name__ == '__main__':
    db_manager.init_database(test_data=False)
    app.run(debug=True)
