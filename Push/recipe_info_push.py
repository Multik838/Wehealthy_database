import os
import csv
from sqlalchemy import create_engine, Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.util import deprecations
from sqlalchemy import exc
deprecations.SILENCE_UBER_WARNING = True

load_dotenv()

# Define the database connection
engine = create_engine(f'postgresql://{os.getenv("PS_USER")}:{os.getenv("PS_PASSWORD")}@{os.getenv("PS_HOST")}:{os.getenv("PS_PORT")}/{os.getenv("PS_DB")}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the structure of the Diary table
class RecipeInfo(Base):
    __tablename__ = 'recipe_info'
    __table_args__ = {'schema': 'stg'}

    unique_key = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    meal_name = Column(String)
    report_date = Column(String)

# Read the CSV file and add records to the database
def read_csv_file(unique_key=None):
    with open('recipe_info.csv', 'r', newline='', encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            user_id, meal_name, report_date = row
            # Check if a record with the same user_id exists
            if user_id is not None:
                recipe_info = RecipeInfo(
                    unique_key=unique_key,
                    user_id=int(user_id),
                    meal_name=str(meal_name),
                    report_date=str(report_date)
                )
                session.add(recipe_info)
            else:
                # If the record already exists, skip the current record
                print(f"{user_id}Skipping the record.")
    session.commit()

read_csv_file()
