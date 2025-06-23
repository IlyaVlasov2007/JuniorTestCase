# Junior Employee Manager

> Данный проект — это реализация тестового задания для собеседования на позицию Junior Python разработчика. Приложение демонстрирует навыки работы с Flask, базой данных, а также современным фронтендом с AJAX-подгрузкой.

Веб-приложение для управления сотрудниками с поддержкой AJAX-подгрузки и пагинации.

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий и перейдите в папку проекта
```bash
git clone https://github.com/IlyaVlasov2007/JuniorTestCase.git
cd JuniorTestCase
```

### 2. Установите зависимости backend
```bash
cd server
pip install -r requirements.txt
```

### 3. Запустите backend (Flask)
```bash
python main.py
```

### 4. Откройте frontend

Откройте файл `front-end/index.html` в браузере.

---

## 🗂️ Структура проекта

```
Junior/
  front-end/         # Фронтенд (HTML, CSS, JS)
  server/            # Бэкенд (Flask, Python)
  instance/          # База данных SQLite
  test/              # Тесты
```

- **front-end/index.html** — главная страница
- **front-end/index.js** — логика AJAX-подгрузки сотрудников
- **server/main.py** — основной файл Flask-приложения
- **server/models.py** — модели данных
- **instance/empl.db** — база данных сотрудников

---

## 🌟 Возможности
- Просмотр сотрудников с пагинацией
- AJAX-подгрузка при прокрутке страницы
- Современный интерфейс

---

## 📦 Пример API-ответа
```json
{
  "employees": [
    {
      "full_name": "Иванов Иван Иванович",
      "position": "Менеджер",
      "hire_date": "2020-01-01",
      "salary": 50000,
      "boss_name": "Петров Петр Петрович"
    }
  ]
}
```

---

## 🛠️ Требования
- Python 3.8+
- Flask
- Любой современный браузер

---

## 🤝 Авторы
- Vladislav Zavyalov