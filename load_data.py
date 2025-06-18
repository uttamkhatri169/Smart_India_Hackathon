import pandas as pd
from datetime import datetime
from app import app, db
from models import RawData

def load_data_from_csv(file_path):
    data = pd.read_csv(file_path)

    # Convert the datetime column to strings
    data['datetime'] = data['datetime'].astype(str)

    for _, row in data.iterrows():
        try:
            # Skip rows with invalid datetime values
            datetime_value = datetime.strptime(row['datetime'], '%d-%m-%Y %H:%M')
        except ValueError:
            continue

        raw_data = RawData(
            datetime=datetime_value,
            weekday=row['weekday'],
            delhi=row['DELHI'],
            bypl=row['BYPL'],
            mes=row['MES'],
            brpl=row['BRPL'],
            ndmc=row['NDMC'],
            temperature=row['temperature'],
            humidity=row['humidity'],
            wind_speed=row['wind_speed'],
            precipitation=row['precipitation']
        )
        db.session.add(raw_data)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        load_data_from_csv('final_data.csv')
