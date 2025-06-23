# Этот модуль реализует методы для простого взаимодествия с базой данных
# В соотвествии с ТЗ
from flask import Flask

from extensions import db

from models import Employee
from models import generate_test_data


class DataBaseManager:
    """Класс для простого взаимодействия с БД\n
    Данный класс реализует в себе фукционал работы только через 1 интерфейс"""
    
    def __init__(self, app: Flask) -> None:
        """Инициализирует объект сервера"""
        self.app = app
    
    
    def init_database(self, test_data: bool = True) -> None:
        """Метод инициализирует базу данных на сервере\n
        Параметры:
            - test_data: bool по умолчанию True - заполнение БД тестовыми данными\n
        Также создает все необходимые таблицы из базового класса Employee, если таковых нет,
        а также заполняет БД тестовыми данными на 50 000 сотрудников
        """
        
        db.init_app(self.app)

        with self.app.app_context():
            if test_data:
                generate_test_data()

            db.create_all()
