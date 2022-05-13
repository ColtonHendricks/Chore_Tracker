# Colton Hendricks
# 5/12/2022
# chore_tracker_GUI.py

# imports
import tkinter
from tkinter import *
from datetime import date
from calendar import monthrange
import sqlite3
from database import database_reset

# figure out the day and month
date = date.today()
today = date.strftime("%d")

month = date.month
year = date.year
days_in_month = monthrange(year, month)[1]


# define main
def main():
    database_reset()
    gui = GUI()


# define the GUI class
class GUI:
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.main_window.title("Family Chore Tracker")

        self.top_window = tkinter.Frame(self.main_window)
        self.bottom_window = tkinter.Frame(self.main_window)

        # determine which chore each child is on
        try:
            conn = sqlite3.connect("chores_db.db")
            cursor = conn.cursor()
        except OSError:
            print("ERROR: File not found")

        cursor.execute(f"""SELECT Colton_chore FROM chore_assignment WHERE month= {month}""")
        colton_chore = cursor.fetchone()[0]
        cursor.execute(f"""SELECT Maddelyn_chore FROM chore_assignment WHERE month= {month}""")
        maddelyn_chore = cursor.fetchone()[0]
        cursor.execute(f"""SELECT Emilia_chore FROM chore_assignment WHERE month= {month}""")
        emilia_chore = cursor.fetchone()[0]
        cursor.execute(f"""SELECT Audrey_chore FROM chore_assignment WHERE month= {month}""")
        audrey_chore = cursor.fetchone()[0]
        cursor.execute(f"""SELECT Victoria_chore FROM chore_assignment WHERE month= {month}""")
        victoria_chore = cursor.fetchone()[0]

        # buttons that bring you to different calendar pages
        self.Colton_button = tkinter.Button(self.top_window, text=f"Colton \nChore: {colton_chore}", height=10, width=20,
                                            bg="lightblue", command=lambda: self.open_calendar("Colton", "Colton_completion"), relief=RAISED)
        self.Maddelyn_button = tkinter.Button(self.top_window, text=f"Maddelyn \nChore: {maddelyn_chore}", height=10, width=20,
                                            bg="darkorange", command=lambda: self.open_calendar("Maddelyn", "Maddelyn_completion"), relief=RAISED)
        self.Emilia_button = tkinter.Button(self.top_window, text=f"Emilia \nChore: {emilia_chore}", height=10, width=20,
                                            bg="green2", command=lambda: self.open_calendar("Emilia", "Emilia_completion"), relief=RAISED)
        self.Audrey_button = tkinter.Button(self.top_window, text=f"Audrey \nChore: {audrey_chore}", height=10, width=20,
                                            bg="yellow", command=lambda: self.open_calendar("Audrey", "Audrey_completion"), relief=RAISED)
        self.Victoria_button = tkinter.Button(self.top_window, text=f"Victoria \nChore: {victoria_chore}", height=10, width=20,
                                            bg="pink", command=lambda: self.open_calendar("Victoria", "Victoria_completion"), relief=RAISED)

        # quit button
        self.quit_button = tkinter.Button(self.bottom_window, text="Quit", bg="red", command=self.main_window.destroy,
                                          relief=RAISED)

        # stats button
        self.stats_button = tkinter.Button(self.bottom_window, text="Statistics", command=lambda: self.statistics_page()
                                           , relief=RAISED, bg="gray")

        # pack the buttons
        self.Colton_button.pack(side="left")
        self.Maddelyn_button.pack(side="left")
        self.Emilia_button.pack(side="left")
        self.Audrey_button.pack(side="left")
        self.Victoria_button.pack(side="left")
        self.quit_button.pack(side="right")
        self.stats_button.pack(side="left")

        self.top_window.pack()
        # text box for the date and explains what to do
        text = f"The date is {date.today()}.\n Select one of the names above to log chore completion."
        date_and_instructions = tkinter.Text(self.bottom_window, height=5, width=30,)
        date_and_instructions.pack()

        date_and_instructions.insert(tkinter.END, text)

        self.bottom_window.pack()

        tkinter.mainloop()

# opens the calendar editor page
    def open_calendar(self, name, column):
        # creates the window and frames it
        calendar_window = Toplevel(self.main_window)
        self.top_calendar_window = tkinter.Frame(calendar_window)
        self.bottom_calendar_window = tkinter.Frame(calendar_window)
        calendar_window.title(name + " Calendar")

        try:
            conn = sqlite3.connect("chores_db.db")

            cursor = conn.cursor()
        except OSError:
            print("ERROR: File not found")

        # creates the checkboxes
        self.day_checkboxes = []
        self.check_var = []
        for day in range(days_in_month):
            cursor.execute(f"""SELECT {column} FROM chore_completion WHERE date = {day+1}""")
            i = cursor.fetchone()[0]
            self.check_var.append(day)
            self.check_var[day] = tkinter.IntVar()

            self.check_var[day].set(i)
            self.day_checkboxes.append(Checkbutton(self.top_calendar_window, text="Day "+str(day+1), variable=self.check_var[day]))
            self.day_checkboxes[day].grid(column=1, row=day+1, sticky=W)

        # save button
        self.save = tkinter.Button(self.bottom_calendar_window, text="Save", command=lambda: self.save_button(column),
                                   relief=RAISED)
        self.save.pack(side="left")
        # quit button
        self.quit_button_calendar = tkinter.Button(self.bottom_calendar_window, text="Quit",
                                                   command=calendar_window.destroy, relief=RAISED)
        self.quit_button_calendar.pack(side="left")
        self.top_calendar_window.pack()
        self.bottom_calendar_window.pack()
        tkinter.mainloop()

# save button function
    def save_button(self, column):
        try:
            conn = sqlite3.connect("chores_db.db")
            cursor = conn.cursor()
        except OSError:
            print("ERROR: File not found")

        # cycles the data and saves it
        for day in range(days_in_month):
            if self.check_var[day].get() == 1:
                cursor.execute(f"""UPDATE chore_completion SET {column} = 1 WHERE date = {day+1}""")
                conn.commit()
            if self.check_var[day].get() == 0:
                cursor.execute(f"""UPDATE chore_completion SET {column} = 0 WHERE date = {day + 1}""")
                conn.commit()

# open the statistics page
    def statistics_page(self):
        # create frames for the text widgets
        statistics_window = Toplevel(self.main_window)
        stats_top_window = tkinter.Frame(statistics_window)
        stats_middle_window = tkinter.Frame(statistics_window)
        stats_bottom_window = tkinter.Frame(statistics_window)

        # generate statistics about the chore completion rates
        try:
            conn = sqlite3.connect("chores_db.db")
            cursor = conn.cursor()
        except OSError:
            print("ERROR: File not found")

        # colton stats
        cursor.execute("""SELECT COUNT(Colton_completion) FROM chore_completion
         WHERE Colton_completion = 1""")

        colton_total_completion = int(cursor.fetchall()[-1][-1])
        colton_completion_so_far = float((colton_total_completion / int(today) * 100))
        colton_month_completion = float((colton_total_completion / int(days_in_month) * 100))

        colton_stats = f"Colton has done his chore {colton_total_completion} times this month." \
                       f" He has completed his chore {colton_completion_so_far:.2f}% of the days so far this month" \
                       f" and he has completed {colton_month_completion:.2f}% of his total monthly chores."
        colton_text_box = tkinter.Text(stats_top_window, width=30, height=7, bd=True, bg="lightblue", relief=RAISED,
                                       wrap=WORD)
        colton_text_box.pack(side="left")
        colton_text_box.insert(tkinter.END, colton_stats)

        # maddelyn stats
        cursor.execute("""SELECT COUNT(Maddelyn_completion) FROM chore_completion
         WHERE Maddelyn_completion = 1""")

        maddelyn_total_completion = int(cursor.fetchall()[-1][-1])
        maddelyn_completion_so_far = float((maddelyn_total_completion / int(today) * 100))
        maddelyn_month_completion = float((maddelyn_total_completion / int(days_in_month) * 100))

        maddelyn_stats = f"Maddelyn has done her chore {maddelyn_total_completion} times this month." \
                       f" She has completed her chore {maddelyn_completion_so_far:.2f}% of the days so far this month" \
                       f" and she has completed {maddelyn_month_completion:.2f}% of her total monthly chores."
        maddelyn_text_box = tkinter.Text(stats_top_window, width=30, height=7, bd=True, bg="darkorange", relief=RAISED,
                                       wrap=WORD)
        maddelyn_text_box.pack(side="left")
        maddelyn_text_box.insert(tkinter.END, maddelyn_stats)

        # emilia stats
        cursor.execute("""SELECT COUNT(Emilia_completion) FROM chore_completion
         WHERE Emilia_completion = 1""")

        emilia_total_completion = int(cursor.fetchall()[-1][-1])
        emilia_completion_so_far = float((emilia_total_completion / int(today) * 100))
        emilia_month_completion = float((emilia_total_completion / int(days_in_month) * 100))

        emilia_stats = f"Emilia has done her chore {emilia_total_completion} times this month." \
                       f" She has completed her chore {emilia_completion_so_far:.2f}% of the days so far this month" \
                       f" and she has completed {emilia_month_completion:.2f}% of her total monthly chores."
        emilia_text_box = tkinter.Text(stats_top_window, width=30, height=7, bd=True, bg="green2", relief=RAISED,
                                       wrap=WORD)
        emilia_text_box.pack(side="left")
        emilia_text_box.insert(tkinter.END, emilia_stats)

        # audrey stats
        cursor.execute("""SELECT COUNT(Audrey_completion) FROM chore_completion
         WHERE Audrey_completion = 1""")

        audrey_total_completion = int(cursor.fetchall()[-1][-1])
        audrey_completion_so_far = float((audrey_total_completion / int(today) * 100))
        audrey_month_completion = float((audrey_total_completion / int(days_in_month) * 100))

        audrey_stats = f"Audrey has done her chore {audrey_total_completion} times this month." \
                       f" She has completed her chore {audrey_completion_so_far:.2f}% of the days so far this month" \
                       f" and she has completed {audrey_month_completion:.2f}% of her total monthly chores."
        audrey_text_box = tkinter.Text(stats_middle_window, width=30, height=7, bd=True, bg="yellow", relief=RAISED,
                                       wrap=WORD)
        audrey_text_box.pack(side="left")
        audrey_text_box.insert(tkinter.END, audrey_stats)

        # victoria stats
        cursor.execute("""SELECT COUNT(Victoria_completion) FROM chore_completion
         WHERE Victoria_completion = 1""")

        victoria_total_completion = int(cursor.fetchall()[-1][-1])
        victoria_completion_so_far = float((victoria_total_completion / int(today) * 100))
        victoria_month_completion = float((victoria_total_completion / int(days_in_month) * 100))

        victoria_stats = f"Victoria has done her chore {victoria_total_completion} times this month." \
                       f" She has completed her chore {victoria_completion_so_far:.2f}% of the days so far this month" \
                       f" and she has completed {victoria_month_completion:.2f}% of her total monthly chores."
        victoria_text_box = tkinter.Text(stats_middle_window, width=30, height=7, bd=True, bg="pink", relief=RAISED,
                                       wrap=WORD)
        victoria_text_box.pack(side="left")
        victoria_text_box.insert(tkinter.END, victoria_stats)

        # quit button
        self.quit_button = tkinter.Button(stats_bottom_window, text="Quit", bg="red", command=statistics_window.destroy,
                                          relief=RAISED)
        # pack everything
        self.quit_button.pack()
        stats_top_window.pack()
        stats_middle_window.pack()
        stats_bottom_window.pack()

        tkinter.mainloop()


if __name__ == "__main__":
    main()
