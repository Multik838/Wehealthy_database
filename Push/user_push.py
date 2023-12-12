import os
import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.util import deprecations
deprecations.SILENCE_UBER_WARNING = True

load_dotenv()

# Define the database connection
engine = create_engine(f'postgresql://{os.getenv("PS_USER")}:{os.getenv("PS_PASSWORD")}@{os.getenv("PS_HOST")}:{os.getenv("PS_PORT")}/{os.getenv("PS_DB")}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Передаём структуру Users table
class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'stg'}

    user_id = Column(Integer, primary_key=True)
    gender = Column(String)
    user_age = Column(Integer)
    weight_kg = Column(Integer)
    height_cm = Column(Integer)

# Читаем csv и добавляем записи в базу данных
def read_csv_file():
    with open('Users.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            user_id, gender, user_age, weight_kg, height_cm = row
            # Проверяем, существует ли запись с таким user_id
            existing_user = session.query(Users).filter_by(user_id=int(user_id)).first()

            # Если запись не найдена, сохраняем текущую запись в базе данных
            if existing_user is None:
                users = Users(
                    user_id=int(user_id),
                    gender=str(gender),
                    user_age=int(user_age),
                    weight_kg=int(weight_kg),
                    height_cm=int(height_cm)
                )
                session.add(users)
            else:
                # Если запись уже существует, пропускаем текущую запись
                print(f"Запись с user_id={user_id} уже существует. Пропуск записи.")
    session.commit()

read_csv_file()
