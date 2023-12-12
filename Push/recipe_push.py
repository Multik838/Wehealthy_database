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
class Recipe(Base):
    __tablename__ = 'recipe'
    __table_args__ = {'schema': 'stg'}

    meal_key = Column(String, primary_key=True)
    recipe_description = Column(String)

    def init(self, meal_key, recipe_description):
        self.meal_key = meal_key
        self.recipe_description = recipe_description


# Открываем папку
folder_path = 'recipe_manual'
folder = os.scandir(folder_path)

# Проходимся по файлам
for file in folder:
    # Проверяем, что файл имеет расширение .json
    if file.name.endswith('.json'):
        json_file_path = os.path.join(folder_path, file.name)
        print(file.name)

        with open(json_file_path, 'r', encoding='UTF-8') as file:
            json_data = json.load(file)
            # Создаем пары ключ и значение(сам рецепт). Запишем их в базу данных
            for key, value in json_data.items():
                meal = Recipe(
                    meal_key=key,
                    recipe_description=value
                )
                session.add(meal)

# Выполняем сохранение изменений в базе данных
session.commit()
