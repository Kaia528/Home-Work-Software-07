Домашнє завдання №7

Робота з базою даних (SQLite / PostgreSQL), ORM SQLAlchemy, Alembic, Faker.
Структура проєкту
HW7/
├── alembic/         # міграції
│   └── versions/    
├── alembic.ini      # конфіг alembic
├── db.py            # підключення до БД
├── models.py        # моделі ORM
├── seed.py          # наповнення даними
├── my_select.py     # 10 запитів
├── requirements.txt # залежності
└── .env             # DATABASE_URL

Запуск
pip install -r requirements.txt
alembic upgrade head
python seed.py
python my_select.py

