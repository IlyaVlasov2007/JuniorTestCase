# Этот файл необходим для определения основных классов (таблиц) в БД
# Подключаем класс для работы с БД
from extensions import db
from datetime import datetime

from faker import Faker
from random import randint
from random import choice


fake = Faker('ru_RU')


# Реализуем основной класс - сотрудник
class Employee(db.Model):
    __tablename__: str = 'employees'
    

    # Определение необходимых полей каждого сотрудника
    id: int = db.Column(db.Integer, primary_key=True)
    full_name: str = db.Column(db.String(120), nullable=False)
    position: str = db.Column(db.String(100), nullable=False)
    hire_date: datetime = db.Column(db.Date, nullable=False)
    salary: float = db.Column(db.Float, nullable=False)


    # Связь с начальником
    boss_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    # Определяем рекурсивную связь таблицы с самой собой
    boss = db.relationship('Employee', remote_side=id,
                           backref=db.backref('subordinates', lazy='dynamic'))
    

    def to_dict(self) -> dict:
        """Метод возвращает словарь с данными о сотруднике"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'position': self.position,
            'hire_date': self.hire_date,
            'salary': self.salary,
            'boss_id': self.boss_id
        }


def generate_test_data() -> None:
    """Функция генерирует тестовые данные для проверки"""
    db.create_all()

    # Определение самого главного начальника - верхний уровень иерархии
    seo = Employee(
        full_name=fake.name(),
        position='Генеральный директор',
        hire_date=datetime.strptime(fake.date(), '%Y-%m-%d'),
        salary=500000,
        boss_id=None
        )

    db.session.add(seo)
    db.session.commit()


    # Группировка по уровням иерархии
    levels = {
        1: [seo],
        2: [],
        3: [],
        4: [],
        5: []
    }

    # Генерируем 50 000 сотрудников
    for lvl in range(2, 6):
        for i in range(12500):
            # Выбираем случайного начальника уровнем выше
            boss = choice(levels[lvl-1])

            employee = Employee(
                full_name=fake.name(),
                position=fake.job(),
                hire_date=datetime.strptime(fake.date(), '%Y-%m-%d'),
                salary=randint(30000, 200000),
                boss_id=boss.id
            )

            db.session.add(employee)

            levels[lvl].append(employee)

    db.session.commit()
