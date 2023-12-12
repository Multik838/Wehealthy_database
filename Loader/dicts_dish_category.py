import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
# Создаем подключение к базе данных
engine = create_engine(f'postgresql://{os.getenv("PS_USER")}:{os.getenv("PS_PASSWORD")}@{os.getenv("PS_HOST")}:{os.getenv("PS_PORT")}/{os.getenv("PS_DB")}')
# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Создаем базовый класс для определения моделей таблиц базы данных
Base = declarative_base()
class Dicts(Base):
    __tablename__ = 'meals'
    __table_args__ = {'schema': 'stg'}

    meals_category_ncode = Column(Integer, primary_key=True)
    meals_category_name = Column(VARCHAR(255))

    def __init__(self, meals_category_ncode, meals_category_name):
        self.meals_category_ncode = meals_category_ncode
        self.meals_category_name = meals_category_name

# Открываем папку
folder_path = 'meals'

folder = os.scandir(folder_path)

# Проходимся по файлам
for file in folder:
    # Проверяем, что файл имеет расширение .json
    if file.name.endswith('.json'):
        json_file_path = os.path.join(folder_path, file.name)
        print(json_file_path)
        # Очищаем имя файла
        file_name = os.path.basename(json_file_path)
        meals_category_name = file_name.replace('_ingridients_dict.json', '').replace('_', ' ')
        # Выводим номер категории и имя категории
        print("Номер категории:", meals_category_ncode)
        print("Имя категории:", meals_category_name)
        with open(json_file_path, 'r', encoding='UTF-8') as file:
            try:
                json_data = json.load(file)
                for row in json_data:
                    if len(row) == 0:
                        continue
                    meals_category_ncode = -1
                    try:
                        meals_category_ncode = int(meals_category_ncode)
                    except ValueError:
                        pass
                    meals = Dicts(
                        meals_category_ncode=meals_category_ncode,
                        meals_category_name=meals_category_name
                    )
                    session.add(meals)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error processing JSON file: {json_file_path}")
                print(e)

# Выполняем сохранение изменений в базе данных
session.commit()
# Закрываем соединение с базой данных
session.close()
