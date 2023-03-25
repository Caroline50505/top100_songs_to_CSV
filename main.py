from bs4 import BeautifulSoup
import requests
import csv
from tkinter import *
import datetime

BG = "#F9DBBB"
FG = "#2E3840"
BTN = "#4E6E81"
FONT = "Calibri"


def find_song():
    year = year_var.get()

    month_num = int(month_var.get())
    if month_num < 9:
        month = f"0{month_num}"
    else:
        month = str(month_num)

    day_num = int(day_var.get())
    if day_num < 9:
        day = f"0{day_num}"
    else:
        day = str(day_num)

    date = f"{year}-{month}-{day}"

    response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
    soup = BeautifulSoup(response.text, 'html.parser')

    music_title = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
    song_names = [music.getText().strip("\n\t") for music in music_title]

    artist_titles = soup.find_all(name="span", class_="a-no-trucate")
    artist_names = [artist.getText().strip("\n\t") for artist in artist_titles]

    positions = [*range(1, 101, 1)]

    new_list = [list(a) for a in zip(positions, song_names, artist_names)]

    if new_list == []:
        success.config(text="Date could not be found. Please try again.")
    else:
        fields = ["Position", "Song Name", "Artist"]
        filename = f"Billboard Hot 100 for {date}.csv"

        with open(filename, "w") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(new_list)

        success.config(text="Success")


window = Tk()
window.geometry("360x320")
window.config(bg=BG)
window.title("Hot 100 Finder")

current_year = datetime.datetime.now().year
year_list = [*range(1958, current_year + 1, 1)]
month_list = [*range(1, 13, 1)]
day_list = [*range(1, 32, 1)]

year_var = StringVar()
year_var.set(year_list[0])
month_var = StringVar()
month_var.set(month_list[0])
day_var = StringVar()
day_var.set(day_list[0])

label_welcome = Label(text="Type in the date to extract a CSV file with the top 100 songs of that date according to "
                           "Billboard.", wraplength=350, padx=25, pady=10, font=(FONT, 15, "bold"), bg=BG, fg=FG)
label_welcome.grid(row=0, column=0, columnspan=2)

label_year = Label(text="Year", font=(FONT, 12, "normal"), bg=BG, fg=FG, pady=10)
label_year.grid(row=1, column=0)

label_month = Label(text="Month", font=(FONT, 12, "normal"), bg=BG, fg=FG, pady=10)
label_month.grid(row=2, column=0)

label_day = Label(text="Day", font=(FONT, 12, "normal"), bg=BG, fg=FG, pady=10)
label_day.grid(row=3, column=0)

drop_year = OptionMenu(window, year_var, *year_list)
drop_year.config(width=10, bg=BTN, fg=BG, highlightthickness=0)
drop_year.grid(row=1, column=1)

drop_month = OptionMenu(window, month_var, *month_list)
drop_month.config(width=10, bg=BTN, fg=BG, highlightthickness=0)
drop_month.grid(row=2, column=1)

drop_day = OptionMenu(window, day_var, *day_list)
drop_day.config(width=10, bg=BTN, fg=BG, highlightthickness=0)
drop_day.grid(row=3, column=1)

submit = Button(text="Submit", command=find_song, width=10, font=(FONT, 13, "bold"), bg=BTN, fg=BG)
submit.grid(row=4, column=0, columnspan=2)

success = Label(text="", font=(FONT, 14, "italic"), bg=BG, fg=FG)
success.grid(row=5, column=0, columnspan=2)

window.mainloop()
