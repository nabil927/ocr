import cv2
import numpy as np
import pytesseract
import utlis

import sqlite3
import data

import tkinter as tk
from tkinter import ttk
# from tkinter import filedialog
from tkinter import messagebox as msg

########################################################################

pathImage = "yes/orig_3_.jpg"        # the path of the image

heightImg = 480                 # new dimensions to resize the image
widthImg = 640

########################################################################

data.create_table()             # create the table in the database if it doesn't exist

win = tk.Tk()                   # the tkinter window
win.title("main")
win.geometry("1000x500")
win.resizable(False, False)


def show_all():
    """
    this function shows all the users in the database in a treeview
    """
    # First, it connects to the database then it pulls all the data from the table
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people ORDER BY ID ASC")
    # put the data in a variable
    table = cursor.fetchall()
    # create Treeview with 6 columns
    cols = ('ID', 'Name', 'City', 'Country', 'Email', 'Tel')
    tree = ttk.Treeview(win, columns=cols, show='headings')
    tree.column('ID', width=150)
    tree.column('Name', width=150)
    tree.column('City', width=150)
    tree.column('Country', width=150)
    tree.column('Email', width=150)
    tree.column('Tel', width=150)
    # set column headings
    for col in cols:
        tree.heading(col, text=col)
    # INSERTING ELEMENTS IN THE LIST BOX
    for user in table:
        tree.insert("", "end", values=(user[0], user[1], user[2], user[3], user[4], user[5]))
    # POSITIONING THE LIST BOX
    tree.grid(row=1, column=0, columnspan=5)
    # CLOSE THE DATABASE CONNECTION
    conn.commit()
    conn.close()


def add():
    """
    this function adds a new user to the database and the treeview
    """
    data.add(id_value, name_value, city_value, country_value, email_value, tel_value)
    show_all()
    msg.showinfo('', 'A new person is added :)')


def delete():
    """
    this function deletes the selected user from the database and the treeview
    """
    data.delete(id_value)
    show_all()
    msg.showinfo('', 'This person is deleted :)')


def delete_all():
    """
    this function deletes all the users from the database and the treeview
    """
    answer = msg.askquestion("Delete All", "All records will be deleted ")
    if answer == "yes":
        data.delete_all()
        show_all()
        msg.showinfo('', 'Everyone is deleted :)')


def save():
    """
    this function adds a scanned version of the image to 'Scanned' directory
    """
    file = open("count_of_images.txt", "r")
    count = file.read()
    file.close()

    cv2.imwrite("Scanned/scan_" + str(count) + "_.jpg", imgWarpColored)
    msg.showinfo('', 'This picture is scanned and saved :)')

    file = open("count_of_images.txt", "w")
    count = str(int(count) + 1)
    file.write(str(count))
    file.close()


def check():
    """
    this function takes the value of the ID from the check entry and checks the table in the database
    to see if this user is registered or not.
    If the user is registered, this function displays his personal data.
    """
    user_exists = data.check(check_entry.get())
    if user_exists:
        ID, name, city, country, email, tel = user_exists
        # user_data = ''
        str_id = "ID           :   " + str(ID) + "\n\n"
        str_name = "Name       :   " + name + "\n\n"
        str_city = "City       :   " + city + "\n\n"
        str_country = "Country :   " + country + "\n\n"
        str_email = "Email     :   " + email + "\n\n"
        str_tel = "Phone       :   " + tel + "\n\n"
        user_data = str_id + str_name + str_city + str_country + str_email + str_tel
        present_data = ttk.Label(win, text=user_data)
        present_data.grid(row=4, column=0)
    else:
        msg.showinfo('', 'This person is not registered :)')


# THIS BUTTON IS FOR DISPLAYING AL THE PEOPLE IN THE DATABASE
show_btn = ttk.Button(win, text="show all", command=show_all)
show_btn.grid(row=0, column=0, ipadx=50)

# THIS BUTTON IS FOR ADDING A NEW USER
add_btn = ttk.Button(win, text="add", command=add)
add_btn.grid(row=0, column=1, ipadx=50)

# THIS BUTTON IS FOR DELETING A SELECTED USER
delete_btn = ttk.Button(win, text="delete", command=delete)
delete_btn.grid(row=0, column=2, ipadx=50)

# THIS BUTTON IS FOR DELETING ALL THE USERS
delete_all_btn = ttk.Button(win, text="delete all", command=delete_all)
delete_all_btn.grid(row=0, column=3, ipadx=50)

# THIS BUTTON IS FOR SAVING THE SCANNED VERSION OF THE IMAGE
save_image_btn = ttk.Button(win, text="save image", command=save)
save_image_btn.grid(row=0, column=4, ipadx=50)

# THIS LABEL IS FOR THE CHECKING
check_label = ttk.Label(win, text='Enter the ID to see if the user is registered :')
check_label.grid(row=2, column=0)

# THIS ENTRY IS FOR ENTERING THE ID OF THE USER WE ARE SEARCHING FOR
check_entry = ttk.Entry(win)
# check_entry.insert(0, 'Enter ID ...')
check_entry.grid(row=3, column=0)

# THIS BUTTON IS FOR STARTING THE SEARCH PROCESS
check_btn = ttk.Button(win, text="Check", command=check)
check_btn.grid(row=3, column=1)

"""
THIS IS WHERE THE OCR PART BEGINS
"""

img = cv2.imread(pathImage)  # READING THE IMAGE
img = cv2.resize(img, (widthImg, heightImg))  # RESIZE THE IMAGE
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
imgThreshold = cv2.Canny(imgBlur, 100, 40)  # APPLY CANNY BLUR
kernel = np.ones((5, 5))  # DEFINING THE KERNEL
imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)  # APPLY DILATION
imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION

# FIND ALL CONTOURS
imgContours = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
imgBigContour = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)  # DRAW ALL DETECTED CONTOURS

# FIND THE BIGGEST CONTOUR
biggest, maxArea = utlis.biggestContour(contours)  # FIND THE BIGGEST CONTOUR
if biggest.size != 0:
    biggest = utlis.reorder(biggest)
    # DRAW THE BIGGEST CONTOUR
    cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)
    imgBigContour = utlis.drawRectangle(imgBigContour, biggest, 2)
    pts1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))  # GETTING THE BIRD VIEW (WARP)

    # REMOVE 20 PIXELS FORM LEFT AND BOTTOM AND 100 PIXELS FROM TOP AND RIGHT
    imgWarpColored = imgWarpColored[100:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 100]
    imgWarpColored = cv2.resize(imgWarpColored, (widthImg, heightImg))

    # APPLY ADAPTIVE THRESHOLD
    imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)  # CONVERT WARPED IMAGE TO GRAY SCALE
    imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)  # APPLY ADAPTIVE THRESHOLD
    imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)  # BLACK TEXT ON WHITE BACKGROUND
    imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 5)  # APPLY BLUR TO REDUCE NOISE

    """
    SELECTING CERTAIN REGIONS OF INTEREST(ROI) AND CROPPING THEM TO START THE PYTESSERACT PROCESS 
    """
    id_roi = imgAdaptiveThre[0:80, 170:370]  # SELECT THE ID REGION OF INTEREST
    conf = r'--oem 3 --psm 6 outputbase digits'  # BETTER IDENTIFYING NUMBERS
    id_value = pytesseract.image_to_string(id_roi, config=conf)    # SELECT THE ID REGION OF INTEREST

    name_roi = imgAdaptiveThre[80:160, 170:imgAdaptiveThre.shape[1]]  # SELECT THE NAME REGION OF INTEREST
    name_value = pytesseract.image_to_string(name_roi)  # SELECT THE NAME REGION OF INTEREST

    city_roi = imgAdaptiveThre[160:240, 170:imgAdaptiveThre.shape[1]]  # SELECT THE CITY REGION OF INTEREST
    city_value = pytesseract.image_to_string(city_roi)  # SELECT THE CITY REGION OF INTEREST

    country_roi = imgAdaptiveThre[240:320, 170:imgAdaptiveThre.shape[1]]  # SELECT THE COUNTRY REGION OF INTEREST
    country_value = pytesseract.image_to_string(country_roi)  # SELECT THE COUNTRY REGION OF INTEREST

    email_roi = imgAdaptiveThre[320:400, 170:imgAdaptiveThre.shape[1]]  # SELECT THE EMAIL REGION OF INTEREST
    email_value = pytesseract.image_to_string(email_roi)  # SELECT THE EMAIL REGION OF INTEREST

    tel_roi = imgAdaptiveThre[400:480, 170:imgAdaptiveThre.shape[1]]  # SELECT THE PHONE REGION OF INTEREST
    tel_value = pytesseract.image_to_string(tel_roi)  # SELECT THE PHONE REGION OF INTEREST

"""
THIS IS WHERE THE OCR PART ENDS
"""

win.mainloop()
