import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, VARCHAR, String
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

# Определяем модель таблицы
class Dicts(Base):
    __tablename__ = 'category_food'
    __table_args__ = {'schema': 'stg'}

    food_category_ncode = Column(Integer, primary_key=True)
    food_category_name = Column(VARCHAR(255))

    def __init__(self, food_category_ncode, food_category_name):
        self.food_category_ncode = food_category_ncode
        self.food_category_name = food_category_name

def category(category_number, category_name):
    category_number = category_number
    category_name = category_name
    try:
        category_number = int(category_number)
    except ValueError:
        category_number = None
    return category_name, category_number

# Открываем папку

folder_path = 'data'

folder = os.scandir(folder_path)

# Проходимся по файлам
for file in folder:
    # Проверяем, что файл имеет расширение .csv
    if file.name.endswith('.json') and file.name != 'all_categories_dict.json':
        json_file_path = os.path.join(folder_path, file.name)
        print(json_file_path)
        # Очищаем имя файла
        file_name = os.path.basename(json_file_path)
        category_number, category_name = file_name.split('_', 1)
        category_number = category_number.replace(' ', '')
        category_name = category_name.replace('_', ' ').replace('.json', '').replace('  ', ' ')
        # Выводим номер категории и имя категории
        print("Номер категории:", category_number)
        print("Имя категории:", category_name)
        # Читаем данные из CSV-файла
        # codecs = ["cp1252", "cp437", "utf-16be", "utf-16", "UTF-8", "cp1251"]
        with open(json_file_path, 'r', encoding='UTF-8') as file:
            json_data = json.load(file)
            # print(json_data)

            # Создаем объекты моделей и сохраняем их в базе данных
            for row in json_data:
                if len(row) == 0:
                    continue
                try:
                    category_number = int(category_number)
                except ValueError:
                    category_number = -1

                existing_dict = session.query(Dicts).filter_by(food_category_ncode=category_number,
                                                               food_category_name=category_name).first()
                if existing_dict:
                    continue

                dicts = Dicts(
                    food_category_ncode=category_number,
                    food_category_name=category_name)
                session.add(dicts)

# Выполняем сохранение изменений в базе данных
session.commit()
