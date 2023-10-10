import pandas as pd
import random
from datetime import datetime, timedelta

def generate_input_data():

    category_list = ['blue', 'red', 'green']

    data = []
    for category in category_list:
        date = datetime(2020,1,1)
        value = random.randint(0,1000)
        while date < datetime.now():
            data.append(
                [category, date, value]
            )
            date = date + timedelta(days = 1)
            value = value + random.randint(-10,10)

    data = pd.DataFrame(data, columns=['category', 'date', 'value'])
    data.to_csv('input_data/input_data.csv', index=False)

if __name__ == "__main__":
    generate_input_data()