# Colton Hendricks
# 5/11/2022
# chore_database_reset.py

import sqlite3
from datetime import date
from calendar import monthrange

# connect to the database
try:
    conn = sqlite3.connect("chores_db.db")

    cursor = conn.cursor()
except OSError:
    print("ERROR: File not found")

# check the days within the current month
date = date.today()
today = date.strftime("%d")

month = date.month
year = date.year
days_in_month = monthrange(year, month)[1]


def database_reset():
    reset_month()


# replaces everything in the table with the correct dates and 0s for the completion data
def generate_dates():
    global month, year, days_in_month
    day_of_month = 0
    for day in range(days_in_month):
        day_of_month += 1
        print(day_of_month)
        cursor.execute("""INSERT INTO chore_completion (DATE) VALUES (?)""", ([str(day_of_month)]))
        cursor.execute("""UPDATE chore_completion SET (Colton_completion, Maddelyn_completion, Emilia_completion,
         Audrey_completion, Victoria_completion)=(?,?,?,?,?) WHERE date is not null""", (0, 0, 0, 0, 0))
        conn.commit()


# deletes everything in the table if the date is the first
def reset_month():
    if today == 1:
        cursor.execute("DELETE FROM chore_completion WHERE Date is not null ")
        conn.commit()
        generate_dates()


if __name__ == "__main__":
    database_reset()
