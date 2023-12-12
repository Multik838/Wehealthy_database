import os
import csv
from sqlalchemy import create_engine, Column, Integer, String, PrimaryKeyConstraint
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

# Define the structure of the Diary table
class Diary(Base):
    __tablename__ = 'diary_meal'
    __table_args__ = {'schema': 'stg'}

    unique_key = Column(Integer, primary_key=True)
    report_date = Column(String)
    mealtime_id = Column(Integer)
    user_id = Column(Integer)
    food_id = Column(Integer)
    food_category_ncode = Column(Integer)

# Read the CSV file and add records to the database
def read_csv_file():
    with open('diary_meal.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            report_date, mealtime_id, user_id, food_id, food_category_ncode = row
            # Check if a record with the same user_id exists
            unique_key = report_date + mealtime_id + user_id + food_id + food_category_ncode
            if unique_key is not None:
                diary = Diary(
                    unique_key=str(unique_key),
                    report_date=str(report_date),
                    mealtime_id=int(mealtime_id),
                    user_id=int(user_id),
                    food_id=int(food_id),
                    food_category_ncode=int(food_category_ncode)
                )
                session.add(diary)
            else:
                # If the record already exists, skip the current record
                print(f"{unique_key}Skipping the record.")
    session.commit()

read_csv_file()
