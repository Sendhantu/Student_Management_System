from tkinter import *
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
from tkinter import Tk, Label, Entry, Button

mydb = mysql.connector.connect(host='localhost',username='root',password='Sendhan@2005',database='app_project')

mycursor = mydb.cursor()

#STAFF
def staff_personal_info(STAFF_ID):
    staffper = Tk()
    staffper.title("Staff Personal Information")
    staffper.geometry("750x450")
    staffper.configure(background='ivory')

    header_label = Label(staffper, text="Staff Personal Information", font=("Arial", 24, 'bold'), bg='darkslategray', fg='white', relief="solid", borderwidth=2)
    header_label.grid(column=0, row=0, columnspan=2, pady=20, padx=20, sticky='ew')

    separator = Frame(staffper, height=2, bd=1, relief="sunken", bg='lightgray')
    separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

    try:
        print(f"STAFF_ID passed: {STAFF_ID}")

        Statestaff = 'SELECT * FROM STAFF_INFO WHERE STAFF_ID = %s'
        mycursor.execute(Statestaff, (STAFF_ID,))
        data = mycursor.fetchall()

        print("Fetched data: ", data)

        if not data:
            error_label = Label(staffper, text="No record found for the given Staff ID.", font=("Arial", 14, 'bold'), fg='red', bg='ivory')
            error_label.grid(row=2, column=0, columnspan=2, pady=20)
        else:
            fields = [("Staff ID:", data[0][0]),("Staff Name:", data[0][1]),("Department:", data[0][2]),("Subject:", data[0][3]),("Gender:", data[0][4]),("Salary:", f"₹{data[0][5]:,.2f}"),("Address:", data[0][6]),("Date of Birth:", data[0][7])]

            info_section_label = Label(staffper, text="Personal Information", font=("Arial", 18, 'underline'), bg='ivory', fg='darkblue')
            info_section_label.grid(row=2, column=0, columnspan=2, pady=10)

            for row_num, (label_text, value) in enumerate(fields, start=3):
                Label(staffper, text=label_text, font=("Arial", 14, 'bold'), bg='ivory', fg='darkslategray').grid(column=0, row=row_num, padx=20, pady=10, sticky=W)
                Label(staffper, text=value, font=("Arial", 14), bg='ivory', fg='black').grid(column=1, row=row_num, padx=20, pady=10, sticky=W)

    except Exception as e:
        print(f"Error: {str(e)}")
        error_label = Label(staffper, text=f"Error fetching data: {str(e)}", font=("Arial", 14, 'bold'), fg='red', bg='ivory')
        error_label.grid(row=2, column=0, columnspan=2, pady=20)

    for i in range(1, 10):
        staffper.grid_rowconfigure(i, weight=1)
    staffper.grid_columnconfigure(0, weight=1)
    staffper.grid_columnconfigure(1, weight=2)

def staffstudentattendence():
    stastuatt = Tk()
    stastuatt.title("Students Attendance")
    stastuatt.geometry("600x400")
    stastuatt.configure(background='ivory2')

    def stuattendance():
        stuui = Toplevel(stastuatt)
        stuui.title("Students Attendance")
        stuui.geometry("600x400")
        stuui.configure(background='ivory2')

        headers = ["Student ID", "Subject", "Present", "Absent", "OD"]
        for col_num, header in enumerate(headers):
            header_label = Label(stuui, text=header, font=("Arial", 12, "bold"), bg="lightblue")
            header_label.grid(row=0, column=col_num, padx=10, pady=10)

        statement = 'SELECT * FROM attendance WHERE SUBJECT = "DS"'
        mycursor.execute(statement)
        data = mycursor.fetchall()

        if data:
            for row_num, row_data in enumerate(data, start=1):
                for col_num, cell_data in enumerate(row_data):
                    data_label = Label(stuui, text=cell_data, font=("Arial", 12), bg="ivory2")
                    data_label.grid(row=row_num, column=col_num, padx=10, pady=5)
        else:
            messagebox.showinfo("Information", "No attendance records found for the specified subject.")

    def update():
        updui = Toplevel(stastuatt)
        updui.title("Attendance Update")
        updui.geometry("400x200")
        updui.configure(background='ivory2')

        stuid_label = Label(updui, text="Student ID:", font=("Arial", 12), bg='ivory2')
        stuid_label.grid(column=0, row=0, padx=10, pady=5, sticky=W)

        stuid_entry = Entry(updui, font=("Arial", 12))
        stuid_entry.grid(column=1, row=0, padx=10, pady=5)

        def updatepage(stuid):
            if not stuid.strip():
                messagebox.showerror("Error", "Please enter a valid Student ID")
                return

            upui = Toplevel(updui)
            upui.title("Attendance Update Options")
            upui.geometry("400x200")
            upui.configure(background='ivory2')

            def update_attendance(status):
                STATEMENT = f"UPDATE attendance SET {status} = {status} + 1 WHERE stu_id = %s AND subject = 'DS'"
                try:
                    mycursor.execute(STATEMENT, (stuid,))
                    mydb.commit()
                    messagebox.showinfo("Success", f"{status.capitalize()} updated successfully!")
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to update attendance: {err}")

            present_button = Button(upui, text="Present", font=("Arial", 12), command=lambda: update_attendance('present'), bg='lightgreen', activebackground='mediumseagreen')
            present_button.grid(column=0, row=0, padx=10, pady=5)

            absent_button = Button(upui, text="Absent", font=("Arial", 12), command=lambda: update_attendance('absent'), bg='lightcoral', activebackground='red')
            absent_button.grid(column=1, row=0, padx=10, pady=5)

        submit_button = Button(updui, text="Submit", font=("Arial", 12), command=lambda: updatepage(stuid_entry.get()), bg='lightblue', activebackground='deepskyblue')
        submit_button.grid(column=1, row=1, padx=10, pady=5)

    main_frame = Frame(stastuatt, bg='ivory2')
    main_frame.pack(pady=20)

    attendance_label = Label(main_frame, text="Student Attendance", font=("Arial", 16, "bold"), bg='ivory2')
    attendance_label.grid(column=0, row=0, pady=10)

    stuatt_button = Button(main_frame, text="View Attendance", font=("Arial", 16), command=stuattendance, bg="lightblue", activebackground="deepskyblue")
    stuatt_button.grid(column=1, row=0, pady=10, padx=10)

    update_label = Label(main_frame, text="To Update", font=("Arial", 16, "bold"), bg='ivory2')
    update_label.grid(column=0, row=1, pady=10, sticky=W)

    update_button = Button(main_frame, text="Update", font=("Arial", 16), command=update, bg="lightblue", activebackground="deepskyblue")
    update_button.grid(column=1, row=1, pady=10, padx=10)

def staffattendanceview(staff_id):
    staffattview = Toplevel()
    staffattview.title("Staff Attendance Overview")
    staffattview.geometry("550x550")
    staffattview.configure(bg='#f7f7f7')

    STAFF_ID = staff_id

    statement1 = "SELECT DATE, STATUS FROM STAFF_ATTENDANCE_DETAIL WHERE STAFF_ID = %s"
    statement2 = "SELECT PRESENT, ABSENT FROM STAFF_ATTENDANCE_SUMMARY WHERE STAFF_ID = %s"

    try:
        mycursor.execute(statement1, (STAFF_ID,))
        data = mycursor.fetchall()

        mycursor.execute(statement2, (STAFF_ID,))
        data1 = mycursor.fetchone()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
        return

    SUMMARY_LABEL = Label(staffattview, text="Attendance Summary", font=("Arial", 16, "bold"), bg='#f7f7f7', fg='#0056b3')
    SUMMARY_LABEL.grid(column=0, row=0, padx=20, pady=20, columnspan=2)

    STAFFID_LABEL = Label(staffattview, text=f"Staff ID: {STAFF_ID}", font=("Arial", 13), bg='#f7f7f7')
    STAFFID_LABEL.grid(column=0, row=1, padx=20, pady=5, columnspan=2)

    PRESENT_LABEL = Label(staffattview, text="Present:", font=("Arial", 13), bg='#f7f7f7')
    PRESENT_LABEL.grid(column=0, row=2, padx=20, pady=5, sticky='e')

    ABSENT_LABEL = Label(staffattview, text="Absent:", font=("Arial", 13), bg='#f7f7f7')
    ABSENT_LABEL.grid(column=1, row=2, padx=20, pady=5, sticky='w')

    if data1:
        PRESENT_COUNT = Label(staffattview, text=data1[0], font=("Arial", 13, "bold"), bg='#f7f7f7', fg='green')  # Present count
        PRESENT_COUNT.grid(column=0, row=3, padx=20, pady=5, sticky='e')

        ABSENT_COUNT = Label(staffattview, text=data1[1], font=("Arial", 13, "bold"), bg='#f7f7f7', fg='red')  # Absent count
        ABSENT_COUNT.grid(column=1, row=3, padx=20, pady=5, sticky='w')
    else:
        NO_DATA_LABEL = Label(staffattview, text="No summary data available.", font=("Arial", 13), fg="red", bg='#f7f7f7')
        NO_DATA_LABEL.grid(column=0, row=3, columnspan=2, padx=20, pady=5)

    canvas_divider = Canvas(staffattview, width=450, height=2, bg='#0056b3', bd=0, highlightthickness=0)
    canvas_divider.grid(column=0, row=4, pady=20, columnspan=2)

    DETAIL_LABEL = Label(staffattview, text="Attendance Details", font=("Arial", 16, "bold"), bg='#f7f7f7', fg='#0056b3')
    DETAIL_LABEL.grid(column=0, row=5, padx=20, pady=10, columnspan=2)

    DATE_LABEL = Label(staffattview, text="Date", font=("Arial", 13), bg='#f7f7f7')
    DATE_LABEL.grid(column=0, row=6, padx=20, pady=5, sticky='e')

    STATUS_LABEL = Label(staffattview, text="Status", font=("Arial", 13), bg='#f7f7f7')
    STATUS_LABEL.grid(column=1, row=6, padx=20, pady=5, sticky='w')

    details_frame = Frame(staffattview, bg='#f7f7f7')
    details_frame.grid(row=7, column=0, columnspan=2, pady=10)

    canvas = Canvas(details_frame, bg='#f7f7f7', height=200)
    scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='#f7f7f7')

    scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    if data:
        for i, (attendance_date, status) in enumerate(data, start=1):
            DATE_VALUE = Label(scrollable_frame, text=attendance_date, font=("Arial", 13), bg='#f7f7f7')
            DATE_VALUE.grid(column=0, row=i, padx=20, pady=5, sticky='e')

            status_color = 'green' if status == 'Present' else 'red'
            STATUS_VALUE = Label(scrollable_frame, text=status, font=("Arial", 13, "bold"), bg='#f7f7f7', fg=status_color)
            STATUS_VALUE.grid(column=1, row=i, padx=20, pady=5, sticky='w')
    else:
        NO_DETAILS_LABEL = Label(scrollable_frame, text="No attendance details available.", font=("Arial", 13), fg="red", bg='#f7f7f7')
        NO_DETAILS_LABEL.grid(column=0, row=1, columnspan=2, padx=20, pady=5)

def STUCT1(stu_id):
    if not stu_id:
        messagebox.showerror("Input Error", "Student ID is required!")
        return

    CT1UI = Tk()
    CT1UI.geometry("400x400")
    CT1UI.title("CT 1 MARKS")
    CT1UI.configure(background='#f7f7f7')

    try:
        STATEMENT = "SELECT subject, marks FROM STU_MARKS_CT1 WHERE STU_ID = %s"
        mycursor.execute(STATEMENT, (stu_id,))
        records = mycursor.fetchall()

        if not records:
            messagebox.showinfo("No Records", f"No marks found for Student ID {stu_id}")
            CT1UI.destroy()
            return

        subject_label = Label(CT1UI, text="Subject", font=("Arial", 13), bg='#f7f7f7')
        subject_label.grid(column=0, row=0, padx=20, pady=10)

        marks_label = Label(CT1UI, text="Marks", font=("Arial", 13), bg='#f7f7f7')
        marks_label.grid(column=1, row=0, padx=20, pady=10)

        for i, (subject, marks) in enumerate(records, start=1):
            Label(CT1UI, text=subject, font=("Arial", 12), bg='#f7f7f7').grid(column=0, row=i, padx=20, pady=5)
            Label(CT1UI, text=str(marks), font=("Arial", 12), bg='#f7f7f7').grid(column=1, row=i, padx=20, pady=5)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    Button(CT1UI, text="Close", font=("Arial", 15), bg='#f44336', fg='white', command=CT1UI.destroy).grid(column=0,row=i + 1,columnspan=2,pady=20)

def STUCT2(stu_id):
    if not stu_id:
        messagebox.showerror("Input Error", "Student ID is required!")
        return

    CT2UI = Tk()
    CT2UI.geometry("400x400")
    CT2UI.title("CT 2 MARKS")
    CT2UI.configure(background='#f7f7f7')

    try:
        STATEMENT = "SELECT subject, marks FROM STU_MARKS_CT2 WHERE STU_ID = %s"
        mycursor.execute(STATEMENT, (stu_id,))
        records = mycursor.fetchall()

        if not records:
            messagebox.showinfo("No Records", f"No marks found for Student ID {stu_id}")
            CT2UI.destroy()
            return

        subject_label = Label(CT2UI, text="Subject", font=("Arial", 13), bg='#f7f7f7')
        subject_label.grid(column=0, row=0, padx=20, pady=10)

        marks_label = Label(CT2UI, text="Marks", font=("Arial", 13), bg='#f7f7f7')
        marks_label.grid(column=1, row=0, padx=20, pady=10)

        for i, (subject, marks) in enumerate(records, start=1):
            Label(CT2UI, text=subject, font=("Arial", 12), bg='#f7f7f7').grid(column=0, row=i, padx=20, pady=5)
            Label(CT2UI, text=str(marks), font=("Arial", 12), bg='#f7f7f7').grid(column=1, row=i, padx=20, pady=5)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    Button(CT2UI, text="Close", font=("Arial", 15), bg='#f44336', fg='white', command=CT2UI.destroy).grid(column=0,row=i + 1,columnspan=2,pady=20)

def STUCT3(stu_id):
    if not stu_id:
        messagebox.showerror("Input Error", "Student ID is required!")
        return

    CT3UI = Tk()
    CT3UI.geometry("400x400")
    CT3UI.title("CT 3 MARKS")
    CT3UI.configure(background='#f7f7f7')

    try:
        STATEMENT = "SELECT subject, marks FROM STU_MARKS_CT3 WHERE STU_ID = %s"
        mycursor.execute(STATEMENT, (stu_id,))
        records = mycursor.fetchall()

        if not records:
            messagebox.showinfo("No Records", f"No marks found for Student ID {stu_id}")
            CT3UI.destroy()
            return

        subject_label = Label(CT3UI, text="Subject", font=("Arial", 13), bg='#f7f7f7')
        subject_label.grid(column=0, row=0, padx=20, pady=10)

        marks_label = Label(CT3UI, text="Marks", font=("Arial", 13), bg='#f7f7f7')
        marks_label.grid(column=1, row=0, padx=20, pady=10)

        for i, (subject, marks) in enumerate(records, start=1):
            Label(CT3UI, text=subject, font=("Arial", 12), bg='#f7f7f7').grid(column=0, row=i, padx=20, pady=5)
            Label(CT3UI, text=str(marks), font=("Arial", 12), bg='#f7f7f7').grid(column=1, row=i, padx=20, pady=5)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    Button(CT3UI, text="Close", font=("Arial", 15), bg='#f44336', fg='white', command=CT3UI.destroy).grid(column=0,row=i + 1,columnspan=2,pady=20)


def STUSEM(stu_id):
    if not stu_id:
        messagebox.showerror("Input Error", "Student ID is required!")
        return

    SEMUI = Tk()
    SEMUI.geometry("400x400")
    SEMUI.title("CT 1 MARKS")
    SEMUI.configure(background='#f7f7f7')

    try:
        STATEMENT = "SELECT subject, marks FROM STU_MARKS_SEM WHERE STU_ID = %s"
        mycursor.execute(STATEMENT, (stu_id,))
        records = mycursor.fetchall()

        if not records:
            messagebox.showinfo("No Records", f"No marks found for Student ID {stu_id}")
            SEMUI.destroy()
            return

        subject_label = Label(SEMUI, text="Subject", font=("Arial", 13), bg='#f7f7f7')
        subject_label.grid(column=0, row=0, padx=20, pady=10)

        marks_label = Label(SEMUI, text="Marks", font=("Arial", 13), bg='#f7f7f7')
        marks_label.grid(column=1, row=0, padx=20, pady=10)

        for i, (subject, marks) in enumerate(records, start=1):
            Label(SEMUI, text=subject, font=("Arial", 12), bg='#f7f7f7').grid(column=0, row=i, padx=20, pady=5)
            Label(SEMUI, text=str(marks), font=("Arial", 12), bg='#f7f7f7').grid(column=1, row=i, padx=20, pady=5)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    Button(SEMUI, text="Close", font=("Arial", 15), bg='#f44336', fg='white', command=SEMUI.destroy).grid(column=0,row=i + 1,columnspan=2,pady=20)

def CT1UPD(stu_id):
    CT1UPD = Tk()
    CT1UPD.title("CT 1 UPDATION")
    CT1UPD.geometry("400x400")
    CT1UPD.configure(background='#f7f7f7')

    try:
        subject_query = "SELECT subject FROM STU_MARKS_CT1 WHERE STU_ID = %s"
        mycursor.execute(subject_query, (stu_id,))
        subjects = mycursor.fetchall()
        subject_list = [subject[0] for subject in subjects]
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        CT1UPD.destroy()
        return

    if not subject_list:
        messagebox.showinfo("No Subjects", f"No subjects found for Student ID {stu_id}")
        CT1UPD.destroy()
        return

    subject_label = Label(CT1UPD, text="Subject", font=("Arial", 13))
    subject_label.grid(column=0, row=0, padx=20, pady=10)

    subject_combobox = ttk.Combobox(CT1UPD, values=subject_list, font=("Arial", 12), state="readonly")
    subject_combobox.grid(column=1, row=0, padx=20, pady=10)
    subject_combobox.set(subject_list[0])

    marks_label = Label(CT1UPD, text="Marks", font=("Arial", 13))
    marks_label.grid(column=0, row=1, padx=20, pady=10)

    marks_entry = Entry(CT1UPD)
    marks_entry.grid(column=1, row=1, padx=20, pady=10)

    def update_marks():
        subject = subject_combobox.get()
        marks = marks_entry.get()

        if not marks:
            messagebox.showerror("Input Error", "Marks field is required!")
            return

        try:
            STATEMENT = "UPDATE STU_MARKS_CT1 SET MARKS = %s WHERE STU_ID = %s AND subject = %s"
            mycursor.execute(STATEMENT, (marks, stu_id, subject))
            mydb.commit()
            messagebox.showinfo("Success", "Marks updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    update_button = Button(CT1UPD, text="Update Marks", font=("Arial", 13), bg="lightgreen", command=update_marks)
    update_button.grid(column=0, row=2, columnspan=2, pady=20)

    close_button = Button(CT1UPD, text="Close", font=("Arial", 13), bg="red", fg="white", command=CT1UPD.destroy)
    close_button.grid(column=0, row=3, columnspan=2, pady=10)

def CT2UPD(stu_id):
    CT2UPD = Tk()
    CT2UPD.geometry("400x400")
    CT2UPD.title("CT 2 UPDATION")
    CT2UPD.configure(background='#f7f7f7')

    try:
        subject_query = "SELECT subject FROM STU_MARKS_CT2 WHERE STU_ID = %s"
        mycursor.execute(subject_query, (stu_id,))
        subjects = mycursor.fetchall()
        subject_list = [subject[0] for subject in subjects]
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        CT2UPD.destroy()
        return

    if not subject_list:
        messagebox.showinfo("No Subjects", f"No subjects found for Student ID {stu_id}")
        CT2UPD.destroy()
        return

    subject_label = Label(CT2UPD, text="Subject", font=("Arial", 13))
    subject_label.grid(column=0, row=0, padx=20, pady=10)

    subject_combobox = ttk.Combobox(CT2UPD, values=subject_list, font=("Arial", 12), state="readonly")
    subject_combobox.grid(column=1, row=0, padx=20, pady=10)
    subject_combobox.set(subject_list[0])

    marks_label = Label(CT2UPD, text="Marks", font=("Arial", 13))
    marks_label.grid(column=0, row=1, padx=20, pady=10)

    marks_entry = Entry(CT2UPD)
    marks_entry.grid(column=1, row=1, padx=20, pady=10)

    def update_marks():
        subject = subject_combobox.get()
        marks = marks_entry.get()

        if not marks:
            messagebox.showerror("Input Error", "Marks field is required!")
            return

        try:
            STATEMENT = "UPDATE STU_MARKS_CT2 SET MARKS = %s WHERE STU_ID = %s AND subject = %s"
            mycursor.execute(STATEMENT, (marks, stu_id, subject))
            mydb.commit()
            messagebox.showinfo("Success", "Marks updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    update_button = Button(CT2UPD, text="Update Marks", font=("Arial", 13), bg="lightgreen", command=update_marks)
    update_button.grid(column=0, row=2, columnspan=2, pady=20)

    close_button = Button(CT2UPD, text="Close", font=("Arial", 13), bg="red", fg="white", command=CT2UPD.destroy)
    close_button.grid(column=0, row=3, columnspan=2, pady=10)

def CT3UPD(stu_id):
    CT3UPD = Tk()
    CT3UPD.geometry("400x400")
    CT3UPD.title("CT 3 UPDATION")
    CT3UPD.configure(background='#f7f7f7')

    try:
        subject_query = "SELECT subject FROM STU_MARKS_CT3 WHERE STU_ID = %s"
        mycursor.execute(subject_query, (stu_id,))
        subjects = mycursor.fetchall()
        subject_list = [subject[0] for subject in subjects]
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        CT3UPD.destroy()
        return

    if not subject_list:
        messagebox.showinfo("No Subjects", f"No subjects found for Student ID {stu_id}")
        CT3UPD.destroy()
        return

    subject_label = Label(CT3UPD, text="Subject", font=("Arial", 13))
    subject_label.grid(column=0, row=0, padx=20, pady=10)

    subject_combobox = ttk.Combobox(CT3UPD, values=subject_list, font=("Arial", 12), state="readonly")
    subject_combobox.grid(column=1, row=0, padx=20, pady=10)
    subject_combobox.set(subject_list[0])

    marks_label = Label(CT3UPD, text="Marks", font=("Arial", 13))
    marks_label.grid(column=0, row=1, padx=20, pady=10)

    marks_entry = Entry(CT3UPD)
    marks_entry.grid(column=1, row=1, padx=20, pady=10)

    def update_marks():
        subject = subject_combobox.get()
        marks = marks_entry.get()

        if not marks:
            messagebox.showerror("Input Error", "Marks field is required!")
            return

        try:
            STATEMENT = "UPDATE STU_MARKS_CT3 SET MARKS = %s WHERE STU_ID = %s AND subject = %s"
            mycursor.execute(STATEMENT, (marks, stu_id, subject))
            mydb.commit()
            messagebox.showinfo("Success", "Marks updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    update_button = Button(CT3UPD, text="Update Marks", font=("Arial", 13), bg="lightgreen", command=update_marks)
    update_button.grid(column=0, row=2, columnspan=2, pady=20)

    close_button = Button(CT3UPD, text="Close", font=("Arial", 13), bg="red", fg="white", command=CT3UPD.destroy)
    close_button.grid(column=0, row=3, columnspan=2, pady=10)

def SEMUPD(stu_id):
    SEMUPD = Tk()
    SEMUPD.geometry("400x400")
    SEMUPD.title("SEM UPDATION")
    SEMUPD.configure(background='#f7f7f7')

    try:
        subject_query = "SELECT subject FROM STU_MARKS_SEM WHERE STU_ID = %s"
        mycursor.execute(subject_query, (stu_id,))
        subjects = mycursor.fetchall()
        subject_list = [subject[0] for subject in subjects]
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        SEMUPD.destroy()
        return

    if not subject_list:
        messagebox.showinfo("No Subjects", f"No subjects found for Student ID {stu_id}")
        SEMUPD.destroy()
        return

    subject_label = Label(SEMUPD, text="Subject", font=("Arial", 13))
    subject_label.grid(column=0, row=0, padx=20, pady=10)

    subject_combobox = ttk.Combobox(SEMUPD, values=subject_list, font=("Arial", 12), state="readonly")
    subject_combobox.grid(column=1, row=0, padx=20, pady=10)
    subject_combobox.set(subject_list[0])

    marks_label = Label(SEMUPD, text="Marks", font=("Arial", 13))
    marks_label.grid(column=0, row=1, padx=20, pady=10)

    marks_entry = Entry(SEMUPD)
    marks_entry.grid(column=1, row=1, padx=20, pady=10)

    def update_marks():
        subject = subject_combobox.get()
        marks = marks_entry.get()

        if not marks:
            messagebox.showerror("Input Error", "Marks field is required!")
            return

        try:
            STATEMENT = "UPDATE STU_MARKS_SEM SET MARKS = %s WHERE STU_ID = %s AND subject = %s"
            mycursor.execute(STATEMENT, (marks, stu_id, subject))
            mydb.commit()
            messagebox.showinfo("Success", "Marks updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    update_button = Button(SEMUPD, text="Update Marks", font=("Arial", 13), bg="lightgreen", command=update_marks)
    update_button.grid(column=0, row=2, columnspan=2, pady=20)

    close_button = Button(SEMUPD, text="Close", font=("Arial", 13), bg="red", fg="white", command=SEMUPD.destroy)
    close_button.grid(column=0, row=3, columnspan=2, pady=10)

def stumarks():
    marks = Tk()
    marks.title("Student's Marks")
    marks.configure(background='#f7f7f7')
    marks.geometry("500x500")

    title_label = Label(marks, text="Staff Page", font=("Arial", 24, "bold"), fg='darkblue')
    title_label.grid(column=0, row=0, columnspan=2, pady=20)

    stuid_label = Label(marks, text="Student ID", font=('Arial', 13), fg='darkblue')
    stuid_label.grid(column=0, row=1, padx=20, pady=10, sticky='e')

    stu_id = Entry(marks)
    stu_id.grid(column=1, row=1, padx=20, pady=10, sticky='w')

    Label(marks, text="CT 1 MARKS", font=("Arial", 13), bg='#f7f7f7').grid(column=0, row=2, padx=20, pady=5, sticky='e')
    Button(marks, text='CT 1', font=("Arial", 13), bg='tomato', command=lambda: STUCT1(stu_id.get())).grid(column=1, row=2, padx=20, pady=5, sticky='w')
    Button(marks, text='UPDATE', font=("Arial", 13), bg='orangered2', command=lambda: CT1UPD(stu_id.get())).grid(column=2,row=2,padx=20,pady=5,sticky='w')

    Label(marks, text="CT 2 MARKS", font=("Arial", 13), bg='#f7f7f7').grid(column=0, row=3, padx=20, pady=5, sticky='e')
    Button(marks, text="CT 2", font=("Arial", 13), bg='lightgreen', command=lambda: STUCT2(stu_id.get())).grid(column=1, row=3, padx=20, pady=5, sticky='w')
    Button(marks, text='UPDATE', font=("Arial", 13), bg='red', command=lambda: CT2UPD(stu_id.get())).grid(column=2,row=3,padx=20,pady=5,sticky='w')

    Label(marks, text="CT 3 MARKS", font=("Arial", 13), bg='#f7f7f7').grid(column=0, row=4, padx=20, pady=5, sticky='e')
    Button(marks, text="CT 3", font=("Arial", 13), bg='lightblue', command=lambda: STUCT3(stu_id.get())).grid(column=1, row=4, padx=20, pady=5, sticky='w')
    Button(marks, text='UPDATE', font=("Arial", 13), bg='coral', command=lambda: CT3UPD(stu_id.get())).grid(column=2,row=4,padx=20,pady=5,sticky='w')

    Label(marks, text="SEM MARKS", font=("Arial", 13), bg='#f7f7f7').grid(column=0, row=5, padx=20, pady=5, sticky='e')
    Button(marks, text="SEM", font=("Arial", 13), bg='lightyellow', command=lambda: STUSEM(stu_id.get())).grid(column=1, row=5, padx=20, pady=5, sticky='w')
    Button(marks, text='UPDATE', font=("Arial", 13), bg='orange', command=lambda: SEMUPD(stu_id.get())).grid(column=2,row=5,padx=20,pady=5,sticky='w')

    close_button = Button(marks, text="Close", font=("Arial", 15), bg='#f44336', fg='white', command=marks.destroy)
    close_button.grid(column=0, row=6, columnspan=2, pady=30)

def staff_process(staff_id):
    staffpg = Toplevel()
    staffpg.title('Staff Page')
    staffpg.geometry('600x600')
    staffpg.configure(bg='ivory2')

    title_label = Label(staffpg, text="Staff Page", font=("Arial", 24, "bold"), bg='ivory2', fg='darkblue')
    title_label.grid(column=0, row=0, columnspan=2, pady=20)

    table_frame = Frame(staffpg, bg='ivory2')
    table_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

    Label(table_frame, text="Staff ID:", font=('Arial', 15), bg='ivory2').grid(row=1, column=0, sticky='e', padx=10, pady=5)
    Label(table_frame, text=f"{staff_id}", font=('Arial', 15), bg='ivory2').grid(row=1, column=1, sticky='w', padx=10, pady=5)

    try:
        STATEMENT = 'SELECT NAME, DEPT, SUBJECT FROM STAFF_INFO WHERE STAFF_ID = %s'
        mycursor.execute(STATEMENT, (staff_id,))
        data = mycursor.fetchone()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
        return

    name, dept, subject = data if data else ("N/A", "N/A", "N/A")

    Label(table_frame, text="Name:", font=('Arial', 15), bg='ivory2').grid(row=2, column=0, sticky='e', padx=10, pady=5)
    Label(table_frame, text=name, font=('Arial', 15), bg='ivory2').grid(row=2, column=1, sticky='w', padx=10, pady=5)

    Label(table_frame, text="Department:", font=('Arial', 15), bg='ivory2').grid(row=3, column=0, sticky='e', padx=10, pady=5)
    Label(table_frame, text=dept, font=('Arial', 15), bg='ivory2').grid(row=3, column=1, sticky='w', padx=10, pady=5)

    Label(table_frame, text="Subject:", font=('Arial', 15), bg='ivory2').grid(row=4, column=0, sticky='e', padx=10, pady=5)
    Label(table_frame, text=subject, font=('Arial', 15), bg='ivory2').grid(row=4, column=1, sticky='w', padx=10, pady=5)

    Label(table_frame, text="Personal Information:", font=('Arial', 15), bg='ivory2').grid(row=5, column=0, sticky='e', padx=10, pady=5)
    Button(table_frame, text="View Personal Info", font=('Arial', 15), bg='#4CAF50', fg='white', command=lambda: staff_personal_info(staff_id)).grid(row=5, column=1, sticky='w', padx=10, pady=5)

    Label(table_frame, text="Staff Attendance:", font=('Arial', 15), bg='ivory2').grid(row=6, column=0, sticky='e', padx=10, pady=5)
    Button(table_frame, text="Attendance", font=('Arial', 15), bg='#4CAF50', fg='white', command=lambda: staffattendanceview(staff_id)).grid(row=6, column=1, sticky='w', padx=10, pady=5)

    Label(table_frame, text="Student Attendance:", font=('Arial', 15), bg='ivory2').grid(row=7, column=0, sticky='e', padx=10, pady=5)
    Button(table_frame, text="Attendance", font=('Arial', 15), bg='#4CAF50', fg='white', command=staffstudentattendence).grid(row=7, column=1, sticky='w', padx=10, pady=5)

    Label(table_frame, text="Student Mark", font=('Arial', 15), bg='ivory2').grid(row=8, column=0, sticky='e', padx=10, pady=5)
    Button(table_frame, text="Marks", font=('Arial', 15), bg='#4CAF50', fg='white', command=stumarks).grid(row=8, column=1, sticky='w', padx=10, pady=5)

    close_button = Button(staffpg, text="Close", font=("Arial", 15), bg='#f44336', fg='white', command=staffpg.destroy)
    close_button.grid(column=0, row=9, columnspan=2, pady=30)

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)
    table_frame.grid_columnconfigure(1, weight=1)

    def on_enter(e, btn):
        btn['background'] = '#5fba7d'

    def on_leave(e, btn):
        btn['background'] = '#4CAF50'

    def on_close_hover(e, btn):
        btn['background'] = '#d9534f'

    def on_close_leave(e, btn):
        btn['background'] = '#f44336'

    for btn in [table_frame.grid_slaves(row=i, column=1)[0] for i in range(5, 9)]:
        btn.bind("<Enter>", lambda e, b=btn: on_enter(e, b))
        btn.bind("<Leave>", lambda e, b=btn: on_leave(e, b))

    close_button.bind("<Enter>", lambda e: on_close_hover(e, close_button))
    close_button.bind("<Leave>", lambda e: on_close_leave(e, close_button))


def staff_portal():
    ui = Toplevel()
    ui.title("Staff Portal")
    ui.geometry("500x350")
    ui.configure(background='ivory3')

    label = Label(ui, text="Welcome to Staff Portal", font=("Arial", 24, 'bold'), bg='ivory3', fg='darkblue')
    label.grid(column=0, row=0, columnspan=2, pady=20)

    table_frame = Frame(ui, bg='ivory3')
    table_frame.grid(row=1, column=0, padx=20, pady=10)

    username_label = Label(table_frame, text="Username:", font=("Arial", 15), bg='ivory3', fg='black')
    username_label.grid(column=0, row=0, padx=10, pady=5, sticky='E')
    username_entry = Entry(table_frame, width=30)
    username_entry.grid(column=1, row=0, padx=10, pady=5, sticky='W')

    password_label = Label(table_frame, text="Password:", font=("Arial", 15), bg='ivory3', fg='black')
    password_label.grid(column=0, row=1, padx=10, pady=5, sticky='E')
    password_entry = Entry(table_frame, width=30, show='*')
    password_entry.grid(column=1, row=1, padx=10, pady=5, sticky='W')

    invalid_label = Label(table_frame, text="", font=("Arial", 12), fg='red', bg='ivory3')
    invalid_label.grid(column=0, row=3, columnspan=2, pady=5)

    def validate_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            invalid_label.config(text="Please enter both username and password.")
            return

        try:
            mycursor.execute("SELECT * FROM STAFF_LOGIN WHERE username = %s AND password = %s", (username, password))
            user = mycursor.fetchone()

            if user:
                ui.destroy()
                staff_process(user[2])
            else:
                invalid_label.config(text="Invalid username or password.")
                username_entry.delete(0, END)
                password_entry.delete(0, END)
        except mysql.connector.Error as err:
            invalid_label.config(text="Database error occurred.")
            print("Error:", err)

    button_style = {'font': ("Helvetica", 13), 'bg': 'lightblue', 'padx': 10, 'pady': 5}

    submit_button = Button(table_frame, text="Submit", command=validate_login, **button_style)
    submit_button.grid(column=1, row=2, pady=10, sticky='W')

    cancel_button = Button(table_frame, text="Cancel", command=ui.destroy, font=("Helvetica", 13), bg='lightcoral', padx=10, pady=5)
    cancel_button.grid(column=0, row=2, pady=10, sticky='E')

    ui.grid_rowconfigure(1, weight=1)
    ui.grid_columnconfigure(0, weight=1)

ui = tk.Tk()
ui.title("Main")
ui.configure(background='skyblue')

welcome_label = Label(ui, text="Welcome to the Management System", font=("Arial", 24, 'bold'), bg='skyblue', fg='navy')
welcome_label.grid(row=0, column=0, padx=10, pady=20)

frame = Frame(ui, width=500, height=400, bg='lightcyan', bd=2, relief='raised')
frame.grid(row=1, column=0, padx=10, pady=5)
frame.grid_propagate(False)

student_button = Button(frame, text="Student Portal", font=("Arial", 18), command=student_portal, padx=20, pady=15, bg='deepskyblue', fg='white')
student_button.grid(column=0, row=0, padx=10, pady=15, sticky='ew')

staff_button = Button(frame, text="Staff Portal", font=("Arial", 18), command=staff_portal, padx=20, pady=15, bg='dodgerblue', fg='white')
staff_button.grid(column=0, row=1, padx=10, pady=15, sticky='ew')

admin_button = Button(frame, text="Admin Portal", font=("Arial", 18), command=adminlogin, padx=20, pady=15, bg='steelblue', fg='white')
admin_button.grid(column=0, row=2, padx=10, pady=15, sticky='ew')

frame.columnconfigure(0, weight=1)

ui.mainloop()