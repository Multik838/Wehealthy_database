import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, VARCHAR, String
from dotenv import load_dotenv, dotenv_values

load_dotenv()

# Создаем подключение к базе данных
engine = create_engine(f'postgresql://{os.getenv("PS_USER")}:{os.getenv("PS_PASSWORD")}@{os.getenv("PS_HOST")}:{os.getenv("PS_PORT")}/{os.getenv("PS_DB")}')
# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Создаем базовый класс для определения моделей таблиц базы данных
Base = declarative_base()

# Определяем модель таблицы
class Ingredients(Base):
    __tablename__ = 'ingredients'
    __table_args__ = {'schema': 'stg'}

    meal_key = Column(String, primary_key=True)
    meal_name = Column(String)
    meal_ingredient = Column(String)
    meal_quantity = Column(String)
    meal_link = Column(String)

    def init(self, meal_key, meal_name, meal_ingredient, meal_quantity, meal_link):
        self.meal_key = meal_key
        self.meal_name = meal_name
        self.meal_ingredient = meal_ingredient
        self.meal_quantity = meal_quantity
        self.meal_link = meal_link

# Открываем папку
folder_path = 'recipe'
folder = os.scandir(folder_path)

# Проходимся по файлам
for file in folder:
    # Проверяем, что файл имеет расширение .json
    if file.name.endswith('.json'):
        json_file_path = os.path.join(folder_path,file.name)
        print(file.name)

        with open(json_file_path, 'r', encoding='UTF-8') as file:
            json_data = json.load(file)
            print(json_data)

            # Создаем объекты моделей и сохраняем их в базе данных
            for row in json_data['ingredients']:
                meal = Ingredients(
                    meal_key=row['key'],
                    meal_name=row['dish'],
                    meal_ingredient=row['ingredient'],
                    meal_quantity=row['quantity'],
                    meal_link=row['link']
                )
                session.add(meal)

# Выполняем сохранение изменений в базе данных
session.commit()
