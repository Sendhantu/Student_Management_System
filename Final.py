from tkinter import *
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import re
from tkinter import Tk, Label, Entry, Button

mydb = mysql.connector.connect(host='localhost',user='root',password='Sendhan@2005',database='app_project')

mycursor = mydb.cursor()

#STUDENT
def attendance(stuid):
    att = Tk()
    att.geometry('600x400')
    att.title('Attendance Page')
    att.configure(bg='ghost white')
    att.resizable(False, False)

    welcome_label = Label(att, text='Attendance Page', font=('Helvetica Neue', 24, 'bold'), bg='#f5f5f5', fg='#333')
    welcome_label.grid(row=0, column=0, columnspan=4, pady=(20, 10))

    try:
        query = f"SELECT subject, present, absent, od FROM attendance WHERE stu_id = '{stuid}'"
        mycursor.execute(query)
        data = mycursor.fetchall()

        if not data:
            Label(att, text=f"No attendance records found for Student ID: {stuid}",
                  font=('Helvetica Neue', 16), bg='snow', fg='red').grid(row=1, column=0, columnspan=4, pady=(10, 20))
        else:
            Label(att, text=f"Student ID: {stuid}", font=('Helvetica Neue', 20), bg='#f5f5f5', fg='#333').grid(row=1, column=0, columnspan=4, pady=(10, 20))

            headers = ["Subject", "Present", "Absent", "OD"]
            for col_num, header in enumerate(headers):
                header_label = Label(att, text=header, font=('Helvetica Neue', 16, 'bold'), fg='white', relief='flat', padx=10, pady=5)
                header_label.grid(row=2, column=col_num, sticky='nsew', padx=5, pady=5)

            row_num = 3
            for record in data:
                for col_num, value in enumerate(record):
                    Label(att, text=value, font=('Helvetica Neue', 16), bg='#f5f5f5', fg='#555', relief='flat').grid(row=row_num, column=col_num, padx=10, pady=5)
                row_num += 1

    except Exception as e:
        Label(att, text=f"Error fetching attendance data: {e}", font=('Helvetica Neue', 14), bg='#f5f5f5', fg='red').grid(row=1, column=0, columnspan=4, pady=(10, 20))

    close_button = Button(att, text="Close", command=att.destroy, font=('Helvetica Neue', 14), bg='#2196F3', fg='white', relief='flat', width=12, activebackground='#1976D2')
    close_button.grid(row=row_num, column=0, columnspan=4, pady=(20, 10))

def stumoreinfo(stu_id):
    STUINFO = Tk()
    STUINFO.title('Student Information')
    STUINFO.configure(bg='white')
    STUINFO.geometry('600x600')
    STUINFO.resizable(False, False)

    stumoreinfo_label = Label(STUINFO, text='Student Information', font=('Segoe UI', 24, 'bold'), bg='white', fg='#333')
    stumoreinfo_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    info_frame = Frame(STUINFO, bg='white', bd=2, relief='groove')
    info_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky='nsew')

    STUINFO.grid_columnconfigure(0, weight=1)
    STUINFO.grid_columnconfigure(1, weight=1)

    try:
        state = 'SELECT * FROM stu_details WHERE stu_id = %s'
        mycursor.execute(state, (stu_id,))
        data = mycursor.fetchone()

        if data:
            fields = ["ID", "Name", "Department", "Batch", "Date of Birth", "Gender", "Blood Group"]

            for i, field in enumerate(fields):
                Label(info_frame, text=f"{field}:", font=('Segoe UI', 14, 'bold'), bg='white', fg='#555').grid(row=i, column=0, sticky='e', padx=10, pady=10)
                Label(info_frame, text=data[i], font=('Segoe UI', 14), bg='white', fg='#333').grid(row=i, column=1, sticky='w', padx=10, pady=10)

            ttk.Separator(STUINFO, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=20)

        else:
            Label(STUINFO, text="No record found for the given Student ID.", font=('Segoe UI', 16), fg="#FF5722", bg='white').grid(row=2, column=0, columnspan=2, pady=20)

    except Exception as e:
        Label(STUINFO, text=f"Error fetching data: {e}", font=('Segoe UI', 16), fg="#FF5722", bg='white').grid(row=2, column=0, columnspan=2, padx=10, pady=20)

    close_button = Button(STUINFO, text="Close", command=STUINFO.destroy, font=('Segoe UI', 14), bg='#2196F3', fg='white', relief='flat', width=10)
    close_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))

    STUINFO.grid_rowconfigure(1, weight=1)
    STUINFO.grid_rowconfigure(3, weight=0)

def marksct1(stu_id):
    mark = tk.Tk()
    mark.title("Cycle Test 1 Marks")
    mark.geometry('600x600')
    mark.configure(background='ivory2')

    title_label = tk.Label(mark, text="CT 1 MARKS", font=("Segoe UI", 24, 'bold'), bg='ivory2')
    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    mark_frame = tk.Frame(mark, bg='white', bd=2, relief='groove')
    mark_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky='nsew')

    mark.grid_columnconfigure(0, weight=1)
    mark.grid_columnconfigure(1, weight=1)
    mark.grid_rowconfigure(1, weight=1)
    mark.grid_rowconfigure(3, weight=0)

    try:
        query = 'SELECT SUBJECT, MARKS FROM STU_MARKS_CT1 WHERE stu_id = %s'
        mycursor.execute(query, (stu_id,))
        data = mycursor.fetchall()

        if data:
            tk.Label(mark_frame, text="SUBJECT", font=('Segoe UI', 14, 'bold'), bg='white', fg='#555').grid(row=0, column=0, padx=10, pady=10)
            tk.Label(mark_frame, text="MARKS", font=('Segoe UI', 14, 'bold'), bg='white', fg='#555').grid(row=0, column=1, padx=10, pady=10)

            for i, (subject, marks) in enumerate(data, start=1):
                tk.Label(mark_frame, text=subject, font=('Segoe UI', 14), bg='white', fg='#333').grid(row=i, column=0, padx=10, pady=10)
                tk.Label(mark_frame, text=marks if marks is not None else 'N/A', font=('Segoe UI', 14), bg='white', fg='#333').grid(row=i, column=1, padx=10, pady=10)

            ttk.Separator(mark, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky="ew", padx=2, pady=20)

        else:
            tk.Label(mark, text="No marks found for the given Student ID.", font=('Segoe UI', 16), fg="#FF5722",
                     bg='white').grid(row=2, column=0, columnspan=2, pady=20)

    except Exception as e:
        tk.Label(mark, text=f"Error fetching data: {str(e)}", font=('Segoe UI', 16), fg="#FF5722", bg='white').grid(row=2, column=0, columnspan=2, padx=10, pady=20)
        logging.error(f"Error fetching data for student {stu_id}: {str(e)}")

    close_button = tk.Button(mark, text="Close", command=mark.destroy, font=('Segoe UI', 14), bg='#2196F3',
                             fg='white', relief='flat', width=10)
    close_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))

def marksct2(stu_id):
    mark = tk.Tk()
    mark.title("Cycle Test 2 Marks")
    mark.geometry('600x600')
    mark.configure(background='ivory2')

    title_label = tk.Label(mark, text="CT 2 MARKS", font=("Segoe UI", 24, 'bold'), bg='ivory2')
    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    mark_frame = tk.Frame(mark, bg='white', bd=2, relief='groove')
    mark_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky='nsew')

    mark.grid_columnconfigure(0, weight=1)
    mark.grid_columnconfigure(1, weight=1)
    mark.grid_rowconfigure(1, weight=1)
    mark.grid_rowconfigure(3, weight=0)

    try:
        query = 'SELECT SUBJECT, MARKS FROM STU_MARKS_CT2 WHERE stu_id = %s'
        mycursor.execute(query, (stu_id,))
        data = mycursor.fetchall()

        if data:
            tk.Label(mark_frame, text="SUBJECT", font=('Segoe UI', 14, 'bold'), bg='white', fg='#555').grid(row=0,column=0,padx=10,pady=10)
            tk.Label(mark_frame, text="MARKS", font=('Segoe UI', 14, 'bold'), bg='white', fg='#555').grid(row=0,column=1,padx=10,pady=10)

            for i, (subject, marks) in enumerate(data, start=1):
                tk.Label(mark_frame, text=subject, font=('Segoe UI', 14), bg='white', fg='#333').grid(row=i, column=0,padx=10, pady=10)
                tk.Label(mark_frame, text=marks if marks is not None else 'N/A', font=('Segoe UI', 14), bg='white',fg='#333').grid(row=i, column=1, padx=10, pady=10)

            ttk.Separator(mark, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky="ew", padx=2, pady=20)

        else:
            tk.Label(mark, text="No marks found for the given Student ID.", font=('Segoe UI', 16), fg="#FF5722",bg='white').grid(row=2, column=0, columnspan=2, pady=20)

    except Exception as e:
        tk.Label(mark, text=f"Error fetching data: {str(e)}", font=('Segoe UI', 16), fg="#FF5722", bg='white').grid(row=2, column=0, columnspan=2, padx=10, pady=20)
        logging.error(f"Error fetching data for student {stu_id}: {str(e)}")

    close_button = tk.Button(mark, text="Close", command=mark.destroy, font=('Segoe UI', 14), bg='#2196F3',fg='white', relief='flat', width=10)
    close_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))

def marksct3(stu_id):
    mark = tk.Tk()
    mark.title("Cycle Test 3 Marks")
    mark.geometry('600x600')
    mark.configure(background='ivory2')

    title_label = tk.Label(mark, text="CT 3 MARKS", font=("Segoe UI", 24, 'bold'), bg='ivory2')
    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    mark_frame = tk.Frame(mark, bg='white', bd=2, relief='groove')
    mark_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky='nsew')

    mark.grid_columnconfigure(0, weight=1)
    mark.grid_columnconfigure(1, weight=1)
    mark.grid_rowconfigure(1, weight=1)
    mark.grid_rowconfigure(3, weight=0)

    try:
        query = 'SELECT SUBJECT, MARKS FROM STU_MARKS_CT3 WHERE stu_id = %s'
        mycursor.execute(query, (stu_id,))
        data = mycursor.fetchall()

        if data:
            tk.Label(mark_frame, text="SUBJECT", font=('Segoe UI', 14, 'bold'), bg='white', fg='#555').grid(row=0,column=0,padx=10,pady=10)
            tk.Label(mark_frame, text="MARKS", font=('Segoe UI', 14, 'bold'), bg='white', fg='#555').grid(row=0,column=1,padx=10,pady=10)

            for i, (subject, marks) in enumerate(data, start=1):
                tk.Label(mark_frame, text=subject, font=('Segoe UI', 14), bg='white', fg='#333').grid(row=i, column=0,padx=10, pady=10)
                tk.Label(mark_frame, text=marks if marks is not None else 'N/A', font=('Segoe UI', 14), bg='white',fg='#333').grid(row=i, column=1, padx=10, pady=10)

            ttk.Separator(mark, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky="ew", padx=2, pady=20)

        else:
            tk.Label(mark, text="No marks found for the given Student ID.", font=('Segoe UI', 16), fg="#FF5722",
                     bg='white').grid(row=2, column=0, columnspan=2, pady=20)

    except Exception as e:
        tk.Label(mark, text=f"Error fetching data: {str(e)}", font=('Segoe UI', 16), fg="#FF5722", bg='white').grid(row=2, column=0, columnspan=2, padx=10, pady=20)
        logging.error(f"Error fetching data for student {stu_id}: {str(e)}")

    close_button = tk.Button(mark, text="Close", command=mark.destroy, font=('Segoe UI', 14), bg='#2196F3',fg='white', relief='flat', width=10)
    close_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))

def markssem(stu_id):
    mark = tk.Tk()
    mark.title("Cycle Test SEM Marks")
    mark.geometry('600x600')
    mark.configure(background='ivory2')

    title_label = tk.Label(mark, text="SEM MARKS", font=("Segoe UI", 24, 'bold'), bg='ivory2')
    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    mark_frame = tk.Frame(mark, bg='white', bd=2, relief='groove')
    mark_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky='nsew')

    mark.grid_columnconfigure(0, weight=1)
    mark.grid_columnconfigure(1, weight=1)
    mark.grid_rowconfigure(1, weight=1)
    mark.grid_rowconfigure(3, weight=0)

    try:
        query = 'SELECT SUBJECT, MARKS FROM STU_MARKS_SEM WHERE stu_id = %s'
        mycursor.execute(query, (stu_id,))
        data = mycursor.fetchall()

        if data:
            tk.Label(mark_frame, text="SUBJECT", font=('Segoe UI', 14, 'bold'), bg='white', fg='#555').grid(row=0,column=0,padx=10,pady=10)
            tk.Label(mark_frame, text="MARKS", font=('Segoe UI', 14, 'bold'), bg='white', fg='#555').grid(row=0,column=1,padx=10,pady=10)

            for i, (subject, marks) in enumerate(data, start=1):
                tk.Label(mark_frame, text=subject, font=('Segoe UI', 14), bg='white', fg='#333').grid(row=i, column=0,padx=10, pady=10)
                tk.Label(mark_frame, text=marks if marks is not None else 'N/A', font=('Segoe UI', 14), bg='white',fg='#333').grid(row=i, column=1, padx=10, pady=10)

            ttk.Separator(mark, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky="ew", padx=2, pady=20)

        else:
            tk.Label(mark, text="No marks found for the given Student ID.", font=('Segoe UI', 16), fg="#FF5722",bg='white').grid(row=2, column=0, columnspan=2, pady=20)

    except Exception as e:
        tk.Label(mark, text=f"Error fetching data: {str(e)}", font=('Segoe UI', 16), fg="#FF5722", bg='white').grid(row=2, column=0, columnspan=2, padx=10, pady=20)
        logging.error(f"Error fetching data for student {stu_id}: {str(e)}")

    close_button = tk.Button(mark, text="Close", command=mark.destroy, font=('Segoe UI', 14), bg='#2196F3',fg='white', relief='flat', width=10)
    close_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))

def process(username):
    mainpg = tk.Tk()
    mainpg.title('Main Page')
    mainpg.geometry('800x600')
    mainpg.configure(bg='ivory2')

    title_label = Label(mainpg, text='Student Information', font=('Arial', 24, 'bold', 'underline'), bg='ivory2', fg='darkblue')
    title_label.grid(row=0, column=0, columnspan=6, pady=(20, 10))

    try:
        mycursor.execute('SELECT stu_id FROM login_page WHERE username = %s', (username,))
        stu_id = mycursor.fetchone()

        if stu_id:
            stu_id = stu_id[0]
            mycursor.execute('SELECT * FROM STU_DETAILS WHERE stu_id = %s', (stu_id,))
            data = mycursor.fetchone()

            if data:
                table_frame = Frame(mainpg, bg='ivory2', relief='sunken', bd=2)
                table_frame.grid(row=1, column=0, padx=20, pady=10, columnspan=6, sticky='ew')

                fields = ['Student ID', 'Student Name', 'Department', 'Class Sec']
                values = list(data)

                for i, field in enumerate(fields):
                    Label(table_frame, text=f"{field}:", font=('Arial', 16, 'bold'), bg='ivory2', anchor='e', width=15).grid(row=i, column=0, padx=5, pady=5, sticky='e')
                    Label(table_frame, text=values[i], font=('Arial', 16), bg='ivory2', anchor='w', width=20).grid(row=i, column=1, padx=5, pady=5, sticky='w')

                more_info_label = Label(mainpg, text="For More Information", font=('Arial', 20, 'bold'), bg='ivory2', fg='darkgreen')
                more_info_label.grid(column=0, row=2, pady=10, columnspan=6)

                Button(mainpg, text="Attendance", font=('Arial', 18), command=lambda: attendance(stu_id), bg='lightblue', padx=20, relief='raised').grid(row=3, column=0, padx=10, pady=10, sticky='ew')
                Button(mainpg, text="Personal Information", font=('Arial', 18), command=lambda: stumoreinfo(stu_id), bg='lightgreen', padx=20, relief='raised').grid(row=3, column=1, padx=10, pady=10, sticky='ew')
                Button(mainpg, text="CT 1", font=('Arial', 18), command=lambda: marksct1(stu_id), bg='lightcoral', padx=20, relief='raised').grid(row=3, column=2, padx=10, pady=10, sticky='ew')
                Button(mainpg, text="CT 2", font=('Arial', 18), command=lambda: marksct2(stu_id), bg='lightcoral', padx=20, relief='raised').grid(row=3, column=3, padx=10, pady=10, sticky='ew')
                Button(mainpg, text="CT 3", font=('Arial', 18), command=lambda: marksct3(stu_id), bg='lightcoral', padx=20, relief='raised').grid(row=3, column=4, padx=10, pady=10, sticky='ew')
                Button(mainpg, text="SEM", font=('Arial', 18), command=lambda: markssem(stu_id), bg='lightcoral', padx=20, relief='raised').grid(row=3, column=5, padx=10, pady=10, sticky='ew')

            else:
                Label(mainpg, text="No student information found.", font=('Arial', 18), fg='red', bg='ivory2').grid(
                    row=1, column=0, columnspan=6, pady=10)
        else:
            Label(mainpg, text="No student ID found for the given username.", font=('Arial', 18), fg='red',
                  bg='ivory2').grid(row=1, column=0, columnspan=6, pady=10)

    except Exception as e:
        Label(mainpg, text=f"Error: {str(e)}", font=('Arial', 18), fg='red', bg='ivory2').grid(row=1, column=0, columnspan=6, pady=10)
        logging.error(f"Error fetching student data: {e}")

    mainpg.grid_rowconfigure(1, weight=1)
    mainpg.grid_columnconfigure(0, weight=1)
    for i in range(6):
        mainpg.grid_columnconfigure(i, weight=1)

def student_portal():
    ui = Tk()
    ui.title("Student Portal")
    ui.geometry("500x300")
    ui.configure(background='ivory2')

    welcome_label = Label(ui, text="Welcome to Student Portal", font=("Arial", 24, 'bold'), bg='ivory2')
    welcome_label.grid(column=0, row=0, columnspan=2, pady=20)

    table_frame = Frame(ui, bg='ivory2')
    table_frame.grid(row=1, column=0, padx=20, pady=10)

    username_label = Label(table_frame, text="Username:", font=("Arial", 15), bg='ivory2')
    username_label.grid(column=0, row=0, padx=10, pady=5, sticky='E')
    username_entry = Entry(table_frame, width=30)
    username_entry.grid(column=1, row=0, padx=10, pady=5, sticky='W')

    password_label = Label(table_frame, text="Password:", font=("Arial", 15), bg='ivory2')
    password_label.grid(column=0, row=1, padx=10, pady=5, sticky='E')
    password_entry = Entry(table_frame, width=30, show='*')
    password_entry.grid(column=1, row=1, padx=10, pady=5, sticky='W')

    invalid_label = Label(table_frame, text="", font=("Arial", 12), fg='red', bg='ivory2')
    invalid_label.grid(column=0, row=3, columnspan=2)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            invalid_label.config(text="Please enter both username and password.")
            return

        try:
            statement = 'SELECT PASSWORD FROM login_page WHERE username = %s'
            mycursor.execute(statement, (username,))
            data = mycursor.fetchone()

            if data:
                stored_password = data[0]
                if password == stored_password:
                    process(username)
                    ui.destroy()
                else:
                    invalid_label.config(text="Invalid username or password")
            else:
                invalid_label.config(text="Invalid username or password")
        except mysql.connector.Error as err:
            invalid_label.config(text=f"Database error: {err}")

    submit_button = Button(table_frame, text="Submit", font=("Helvetica", 13), command=login, bg='lightblue')
    submit_button.grid(column=1, row=2, pady=10, sticky='W')

    cancel_button = Button(table_frame, text="Cancel", font=("Helvetica", 13), command=ui.destroy, bg='lightcoral')
    cancel_button.grid(column=0, row=2, pady=10, sticky='E')

    ui.grid_rowconfigure(1, weight=1)
    ui.grid_columnconfigure(0, weight=1)

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

#ADMIN
#CREATE NEW STUDENT USER
def newuserstu():
    newuser = Tk()
    newuser.title("New User Registration")
    newuser.geometry("500x400")
    newuser.configure(background="#f8f9fa")

    frame = Frame(newuser, bg='#f8f9fa')
    frame.pack(pady=20)

    userentry = Label(frame, text="Create a New Account", font=('Segoe UI', 20, 'bold'), bg='#f8f9fa', fg="#343a40")
    userentry.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    labels = ["Username:", "Password:", "Student ID:"]
    for i, label in enumerate(labels):
        Label(frame, text=label, font=('Segoe UI', 14), bg='#f8f9fa', fg="#343a40").grid(row=i + 1, column=0, padx=10, pady=10, sticky='e')

    username_entry = ttk.Entry(frame, width=30, font=('Segoe UI', 12))
    password_entry = ttk.Entry(frame, width=30, show='•', font=('Segoe UI', 12))  # Mask password
    stu_id_entry = ttk.Entry(frame, width=30, font=('Segoe UI', 12))

    username_entry.grid(row=1, column=1, padx=10, pady=10)
    password_entry.grid(row=2, column=1, padx=10, pady=10)
    stu_id_entry.grid(row=3, column=1, padx=10, pady=10)

    feedback_var = StringVar()
    feedback_label = Label(frame, textvariable=feedback_var, font=('Segoe UI', 12), fg="red", bg='#f8f9fa')
    feedback_label.grid(row=5, column=0, columnspan=2)

    def insertuser():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        student_id = stu_id_entry.get().strip()

        feedback_var.set("")

        if not username or not password or not student_id:
            feedback_var.set("All fields are required.")
            return

        try:
            loginpagedetails = 'SELECT * FROM login_page WHERE USERNAME = %s OR STU_ID = %s'
            mycursor.execute(loginpagedetails, (username, student_id))
            userdata = mycursor.fetchall()

            if userdata:
                errors = []
                if userdata[0][0] == username:
                    errors.append("Username Already Exists")
                if userdata[0][2] == student_id:
                    errors.append("Student ID Already Exists")
                feedback_var.set(", ".join(errors))
            else:
                statement = 'INSERT INTO login_page (USERNAME, PASSWORD, STU_ID) VALUES (%s, %s, %s)'
                data = (username, password, student_id)

                mycursor.execute(statement, data)
                mydb.commit()
                feedback_var.set("User Created Successfully")

                username_entry.delete(0, END)
                password_entry.delete(0, END)
                stu_id_entry.delete(0, END)

        except mysql.connector.Error as err:
            feedback_var.set(f"Database error: {err}")
        except Exception as e:
            feedback_var.set(f"An unexpected error occurred: {e}")

    entry_button = Button(frame, text="Create Account", command=insertuser, bg='#007bff', fg='white', font=('Segoe UI', 14),
                          relief='flat', borderwidth=2, padx=10, pady=5)
    entry_button.grid(row=4, column=1, pady=20)

    for widget in frame.winfo_children():
        widget.configure(borderwidth=2, relief='flat')

#CREATE NEW STAFF USER
def newuserstaff():
    staffui = Tk()
    staffui.title("Staff Registration")
    staffui.geometry("500x400")
    staffui.configure(background="#f0f4f8")

    frame = Frame(staffui, bg='#f0f4f8')
    frame.pack(pady=20)

    staffuserentry = Label(frame, text="Create Staff Account", font=('Segoe UI', 24, 'bold'), bg='#f0f4f8', fg="#333")
    staffuserentry.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    labels = ["Username", "Password", "Staff ID"]
    for i, label in enumerate(labels):
        Label(frame, text=label, font=('Segoe UI', 14), bg='#f0f4f8', fg="#333").grid(row=i + 1, column=0, padx=10, pady=10, sticky='e')

    staffusername_entry = Entry(frame, width=30, font=('Segoe UI', 12), bd=2, relief='flat', highlightbackground="#ccc")
    staffpassword_entry = Entry(frame, width=30, show='•', font=('Segoe UI', 12), bd=2, relief='flat', highlightbackground="#ccc")  # Mask password
    staff_id_entry = Entry(frame, width=30, font=('Segoe UI', 12), bd=2, relief='flat', highlightbackground="#ccc")

    staffusername_entry.grid(row=1, column=1, padx=10, pady=10)
    staffpassword_entry.grid(row=2, column=1, padx=10, pady=10)
    staff_id_entry.grid(row=3, column=1, padx=10, pady=10)

    feedback_var = StringVar()
    feedback_label = Label(frame, textvariable=feedback_var, font=('Segoe UI', 12), bg='#f0f4f8')
    feedback_label.grid(row=5, column=0, columnspan=2, pady=10)

    def insertstaff():
        username = staffusername_entry.get().strip()
        password = staffpassword_entry.get().strip()
        staffid = staff_id_entry.get().strip()

        if not username or not password or not staffid:
            feedback_var.set("All fields are required.")
            feedback_label.config(fg="red")
            return

        loginpagedetails = 'SELECT * FROM STAFF_LOGIN WHERE USERNAME = %s OR STAFF_ID = %s'
        mycursor.execute(loginpagedetails, (username, staffid))
        userdata = mycursor.fetchall()

        if userdata:
            feedback_var.set("Username or Staff ID already exists.")
            feedback_label.config(fg="red")
        else:
            statestaff = "INSERT INTO STAFF_LOGIN(USERNAME, PASSWORD, STAFF_ID) VALUES(%s, %s, %s)"
            data = (username, password, staffid)
            mycursor.execute(statestaff, data)
            mydb.commit()
            feedback_var.set("User Created Successfully")
            feedback_label.config(fg="green")
            staffusername_entry.delete(0, END)
            staffpassword_entry.delete(0, END)
            staff_id_entry.delete(0, END)

    submit_button = Button(frame, text="Submit", command=insertstaff, bg='#007bff', fg='white', font=('Segoe UI', 14),
                           relief='flat', borderwidth=0, padx=10, pady=8)
    submit_button.grid(row=4, column=1, pady=20)

    def on_enter(event):
        submit_button['bg'] = '#0056b3'

    def on_leave(event):
        submit_button['bg'] = '#007bff'

    submit_button.bind("<Enter>", on_enter)
    submit_button.bind("<Leave>", on_leave)

def studetailupd():
    studetui = Tk()
    studetui.title("Student Information Update")
    studetui.geometry("500x300")
    studetui.configure(background="#f7f9fc")

    frame = Frame(studetui, bg='#f7f9fc')
    frame.pack(pady=20)

    Label(frame, text="Student ID", font=('Segoe UI', 14), bg='#f7f9fc', fg="#333").grid(row=0, column=0, padx=10, pady=10)
    studentid_entry = Entry(frame, width=30, font=('Segoe UI', 12), bd=2, relief='flat', highlightbackground="#ccc")
    studentid_entry.grid(row=0, column=1, padx=10, pady=10)

    def studeatilupdprocess(STUID):
        if not STUID:
            messagebox.showerror("Error", "Please enter a valid Student ID")
            return

        studet = Toplevel()
        studet.title("Update Student Information")
        studet.geometry("500x500")
        studet.configure(background="#f7f9fc")

        labels = {"NAME": "Student Name","DEPT": "Department","BATCH": "Batch","DOB": "Date of Birth","GENDER": "Gender","BLOOD_GROUP": "Blood Group"}

        entries = {}
        row = 1
        for db_column, label in labels.items():
            Label(studet, text=label, font=('Segoe UI', 14), bg='#f7f9fc', fg="#333").grid(row=row, column=0, padx=10, pady=5, sticky='e')
            entry = Entry(studet, width=30, font=('Segoe UI', 12), bd=2, relief='flat', highlightbackground="#ccc")
            entry.grid(row=row, column=1, padx=10, pady=5, sticky='w')
            entries[db_column] = entry
            row += 1

        try:
            mycursor = mydb.cursor()
            query = "SELECT NAME, DEPT, BATCH, DOB, GENDER, BLOOD_GROUP FROM stu_details WHERE STU_ID = %s"
            mycursor.execute(query, (STUID,))
            student_data = mycursor.fetchone()

            if not student_data:
                messagebox.showerror("Error", "Student ID not found.")
                studet.destroy()
                return

            for i, key in enumerate(labels.keys()):
                if student_data[i] is not None:
                    entries[key].insert(0, student_data[i])

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data: {err}")
            studet.destroy()
            return

        def update_student():
            for db_column, entry in entries.items():
                value = entry.get()

                if value.strip() == "":
                    messagebox.showerror("Error", f"{labels[db_column]} cannot be empty")
                    return

                try:
                    update_stmt = f"UPDATE stu_details SET {db_column} = %s WHERE STU_ID = %s"
                    mycursor.execute(update_stmt, (value, STUID))
                    mydb.commit()
                    messagebox.showinfo("Success", f"{labels[db_column]} updated successfully!")
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to update {labels[db_column]}: {err}")
                    return

        Button(studet, text="Update", font=('Segoe UI', 14), command=update_student, bg='#007bff', fg='white', relief='flat', borderwidth=0, padx=10, pady=8).grid(row=row, column=1, padx=10, pady=20)

    submit_button = Button(frame, text="Submit", font=('Segoe UI', 14), command=lambda: studeatilupdprocess(studentid_entry.get()), bg='#007bff', fg='white', relief='flat', borderwidth=0, padx=10, pady=8)
    submit_button.grid(row=1, column=1, padx=10, pady=20)

def staffdeatilupd():
    staffdetui = Tk()
    staffdetui.title("Staff Information Update")
    staffdetui.geometry("500x300")
    staffdetui.configure(bg='#f7f9fc')

    frame = Frame(staffdetui, bg='#f7f9fc')
    frame.pack(pady=20)

    Label(frame, text="Staff ID:", font=('Segoe UI', 14), bg='#f7f9fc', fg="#333").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    staffid_entry = Entry(frame, font=('Segoe UI', 12), bd=2, relief='flat', highlightbackground="#ccc")
    staffid_entry.grid(row=0, column=1, padx=10, pady=10)

    def staffdetailupdprocess(STAFFID):
        if not STAFFID:
            messagebox.showerror("Error", "Please enter a valid Staff ID")
            return

        staffdet = Toplevel()
        staffdet.title("Update Staff Information")
        staffdet.geometry("500x500")
        staffdet.configure(bg='#f7f9fc')

        detail_frame = Frame(staffdet, bg='#f7f9fc')
        detail_frame.pack(pady=20)

        labels = {"NAME": "Staff Name","DEPT": "Department","SUBJECT": "Subject","GENDER": "Gender","SALARY": "Salary","ADDRESS": "Address","DOB": "Date of Birth"}

        entries = {}
        row = 0
        for db_column, label in labels.items():
            Label(detail_frame, text=label, font=('Segoe UI', 14), bg='#f7f9fc', fg="#333").grid(row=row, column=0, padx=10, pady=10, sticky='e')
            if db_column == "GENDER":
                GENDER_OPTIONS = ["Male", "Female", "Other"]
                gender_var = StringVar()
                gender_var.set(GENDER_OPTIONS[0])
                gender_menu = OptionMenu(detail_frame, gender_var, *GENDER_OPTIONS)
                gender_menu.grid(row=row, column=1, padx=10, pady=10, sticky='w')
                entries[db_column] = gender_var
            else:
                entry = Entry(detail_frame, font=('Segoe UI', 12), bd=2, relief='flat', highlightbackground="#ccc")
                entry.grid(row=row, column=1, padx=10, pady=10, sticky='w')
                entries[db_column] = entry
            row += 1

        try:
            mycursor = mydb.cursor()
            query = "SELECT NAME, DEPT, SUBJECT, GENDER, SALARY, ADDRESS, DOB FROM STAFF_INFO WHERE STAFF_ID = %s"
            mycursor.execute(query, (STAFFID,))
            staff_data = mycursor.fetchone()

            if not staff_data:
                messagebox.showerror("Error", "Staff ID not found.")
                staffdet.destroy()
                return

            for i, key in enumerate(labels.keys()):
                if staff_data[i] is not None:
                    entries[key].set(staff_data[i])

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data: {err}")
            staffdet.destroy()
            return

        def update_staff():
            for db_column, entry in entries.items():
                value = entry.get()

                if value.strip() == "":
                    messagebox.showerror("Error", f"{labels[db_column]} cannot be empty")
                    return

                try:
                    update_stmt = f"UPDATE STAFF_INFO SET {db_column} = %s WHERE STAFF_ID = %s"
                    mycursor.execute(update_stmt, (value, STAFFID))
                    mydb.commit()
                    messagebox.showinfo("Success", f"{labels[db_column]} updated successfully!")
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to update {labels[db_column]}: {err}")
                    return

        update_button = Button(detail_frame, text="Update", font=('Segoe UI', 14), command=update_staff, bg='#007bff', fg='white', relief='flat', borderwidth=0, padx=10, pady=8)
        update_button.grid(row=row, column=1, padx=10, pady=20)

    submit_button = Button(frame, text="Submit", font=('Segoe UI', 14), command=lambda: staffdetailupdprocess(staffid_entry.get()), bg='#007bff', fg='white', relief='flat', borderwidth=0, padx=10, pady=8)
    submit_button.grid(row=1, column=1, padx=10, pady=20)

def studentnewuserdetails():
    studet = Tk()
    studet.geometry('500x600')
    studet.title('New Student Information')
    studet.configure(bg='#f7f9fc')

    frame = Frame(studet, bg='#f7f9fc')
    frame.pack(pady=20)

    labels = [("Student ID: ", "student_id"),("Name: ", "name"),("Dept: ", "dept"),("Batch: ", "batch"),("DOB (YYYY-MM-DD): ", "dob"),("Gender: ", "gender"),("Blood Group: ", "blood_group")]

    entries = {}

    for i, (text, var_name) in enumerate(labels):
        label = Label(frame, text=text, font=("Segoe UI", 12), bg='#f7f9fc', fg="#333")
        label.grid(column=0, row=i, padx=10, pady=10, sticky='e')

        if var_name == "gender":
            GENDER_OPTIONS = ["Male", "Female", "Other"]
            gender_var = StringVar()
            gender_var.set(GENDER_OPTIONS[0])
            gender_menu = OptionMenu(frame, gender_var, *GENDER_OPTIONS)
            gender_menu.grid(column=1, row=i, padx=10, pady=10, sticky='w')
            entries[var_name] = gender_var
        else:
            entry = Entry(frame, font=("Segoe UI", 12), bd=2, relief='flat', highlightbackground="#ccc")
            entry.grid(column=1, row=i, padx=10, pady=10)
            entries[var_name] = entry

    def validate_dob(dob):
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(pattern, dob)

    def validate_fields():
        for key, entry in entries.items():
            if key != "gender" and not entry.get():
                messagebox.showerror("Error", "All fields are required.")
                return False
        if not validate_dob(entries["dob"].get()):
            messagebox.showerror("Error", "Date of Birth must be in YYYY-MM-DD format.")
            return False
        return True

    def insert_student():
        if not validate_fields():
            return

        student_data = {key: entry.get() for key, entry in entries.items()}
        student_data['gender'] = entries['gender'].get()

        statement = "INSERT INTO stu_details (STU_ID, NAME, DEPT, BATCH, DOB, GENDER, BLOOD_GROUP) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        try:
            mycursor.execute(statement, (student_data['student_id'], student_data['name'],
                                         student_data['dept'], student_data['batch'],
                                         student_data['dob'], student_data['gender'],
                                         student_data['blood_group']))
            mydb.commit()
            messagebox.showinfo("Success", "New student information added successfully.")
            clear_entries()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add student information: {err}")

    def clear_entries():
        for entry in entries.values():
            if isinstance(entry, Entry):
                entry.delete(0, 'end')
            elif isinstance(entry, StringVar):
                entry.set("Male")

    submit_button = Button(frame, text="Submit", font=("Segoe UI", 14), command=insert_student,bg='#007bff', fg='white', relief='flat', borderwidth=0, padx=10, pady=10)
    submit_button.grid(column=1, row=len(labels), padx=10, pady=20)

def staffnewuserdetails():
    staffet = Tk()
    staffet.geometry('500x600')
    staffet.title('New Staff Information')
    staffet.configure(bg='#f7f9fc')

    frame = Frame(staffet, bg='#f7f9fc')
    frame.pack(pady=20)

    labels = [("Staff ID: ", "staff_id"), ("Name: ", "name"), ("Dept: ", "dept"),("Subject: ", "subject"), ("Gender: ", "gender"), ("Salary: ", "salary"),("Address: ", "address"), ("DOB (YYYY-MM-DD): ", "dob")]

    entries = {}

    for i, (text, var_name) in enumerate(labels):
        label = Label(frame, text=text, font=("Segoe UI", 12), bg='#f7f9fc', fg="#333")
        label.grid(column=0, row=i, padx=10, pady=10, sticky='e')

        if var_name == "gender":
            GENDER_OPTIONS = ["Male", "Female", "Other"]
            gender_var = StringVar()
            gender_var.set(GENDER_OPTIONS[0])
            gender_menu = OptionMenu(frame, gender_var, *GENDER_OPTIONS)
            gender_menu.grid(column=1, row=i, padx=10, pady=10, sticky='w')
            entries[var_name] = gender_var
        else:
            entry = Entry(frame, font=("Segoe UI", 12), bd=2, relief='flat', highlightbackground="#ccc")
            entry.grid(column=1, row=i, padx=10, pady=10)
            entries[var_name] = entry

    def validate_dob(dob):
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(pattern, dob)

    def validate_fields():
        for key, entry in entries.items():
            if key != "gender" and not entry.get():
                messagebox.showerror("Error", "All fields are required.")
                return False
        if not validate_dob(entries["dob"].get()):
            messagebox.showerror("Error", "Date of Birth must be in YYYY-MM-DD format.")
            return False
        if not entries["salary"].get().isdigit():
            messagebox.showerror("Error", "Salary must be a valid number.")
            return False
        return True

    def insert_staff():
        if not validate_fields():
            return

        staff_data = {key: entry.get() for key, entry in entries.items()}
        staff_data['gender'] = entries['gender'].get()

        statement = "INSERT INTO STAFF_INFO (STAFF_ID, NAME, DEPT, SUBJECT, GENDER, SALARY, ADDRESS, DOB) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        try:
            mycursor.execute(statement, (staff_data['staff_id'], staff_data['name'], staff_data['dept'],
                                         staff_data['subject'], staff_data['gender'], staff_data['salary'],
                                         staff_data['address'], staff_data['dob']))
            mydb.commit()
            messagebox.showinfo("Success", "New staff information added successfully.")
            clear_entries()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add staff information: {err}")

    def clear_entries():
        for entry in entries.values():
            if isinstance(entry, Entry):
                entry.delete(0, 'end')
            elif isinstance(entry, StringVar):
                entry.set("Male")

    submit_button = Button(frame, text="Submit", font=("Segoe UI", 14), command=insert_staff,bg='#007bff', fg='white', relief='flat', borderwidth=0, padx=10, pady=10)
    submit_button.grid(column=1, row=len(labels), padx=10, pady=20)

    staffet.mainloop()

def viewstaffatt():
    staffatt = Tk()
    staffatt.title("Staff Attendance")
    staffatt.geometry("600x400")
    staffatt.configure(bg='#F0F4F8')

    main_frame = Frame(staffatt, bg='#F0F4F8')
    main_frame.pack(pady=20)

    header = Label(main_frame, text="Staff Attendance Lookup", font=("Helvetica Neue", 20, 'bold'), bg='#F0F4F8', fg="#333")
    header.grid(column=0, row=0, columnspan=2, pady=10)

    staffid_label = Label(main_frame, text="Staff ID:", font=("Helvetica Neue", 14), bg='#F0F4F8', fg="#555")
    staffid_label.grid(column=0, row=1, padx=10, pady=10, sticky='e')

    staffid_entry = Entry(main_frame, font=("Helvetica Neue", 14), bd=2, relief='flat', highlightbackground="#CED4DA")
    staffid_entry.grid(column=1, row=1, padx=10, pady=10)

    error_label = None

    def clear_error():
        nonlocal error_label
        if error_label:
            error_label.destroy()
            error_label = None

    def validate_staff_id():
        staffid = staffid_entry.get().strip()
        if not staffid:
            return False, "Staff ID cannot be empty"

        query = "SELECT 1 FROM STAFF_ATTENDANCE_SUMMARY WHERE STAFF_ID = %s"
        mycursor.execute(query, (staffid,))
        if not mycursor.fetchone():
            return False, "Staff ID not found"

        return True, ""

    def open_summary_window(data):
        summary_window = Tk()
        summary_window.title("Staff Attendance Summary")
        summary_window.geometry("600x400")
        summary_window.configure(bg='#F0F4F8')

        Label(summary_window, text="Staff ID", font=("Helvetica Neue", 16, 'bold'), bg='#F0F4F8').grid(column=0, row=0,padx=10, pady=10)
        Label(summary_window, text="Present", font=("Helvetica Neue", 16, 'bold'), bg='#F0F4F8').grid(column=1, row=0,padx=10, pady=10)
        Label(summary_window, text="Absent", font=("Helvetica Neue", 16, 'bold'), bg='#F0F4F8').grid(column=2, row=0,padx=10, pady=10)

        if not data:
            Label(summary_window, text="No Summary Data Found", bg='#F0F4F8').grid(column=0, row=1, columnspan=3)
            return

        for i, row in enumerate(data, start=1):
            Label(summary_window, text=row[0], font=("Helvetica Neue", 14), bg='#F0F4F8').grid(column=0, row=i, padx=10,pady=5)
            Label(summary_window, text=row[1], font=("Helvetica Neue", 14), bg='#F0F4F8').grid(column=1, row=i, padx=10,pady=5)
            Label(summary_window, text=row[2], font=("Helvetica Neue", 14), bg='#F0F4F8').grid(column=2, row=i, padx=10,pady=5)

    def show_summary():
        clear_error()
        valid, message = validate_staff_id()
        if not valid:
            nonlocal error_label
            error_label = Label(main_frame, text=message, fg="red", bg='#F0F4F8', font=("Helvetica Neue", 12))
            error_label.grid(column=0, row=2, columnspan=2, pady=10)
            return

        staffid = staffid_entry.get()
        statement = 'SELECT * FROM STAFF_ATTENDANCE_SUMMARY WHERE STAFF_ID = %s'
        mycursor.execute(statement, (staffid,))
        data = mycursor.fetchall()
        open_summary_window(data)

    def open_details_window(data):
        details_window = Tk()
        details_window.title("Staff Attendance Details")
        details_window.geometry("600x400")
        details_window.configure(bg='#F0F4F8')

        Label(details_window, text="Staff ID", font=("Helvetica Neue", 16, 'bold'), bg='#F0F4F8').grid(column=0, row=0,padx=10, pady=10)
        Label(details_window, text="Date", font=("Helvetica Neue", 16, 'bold'), bg='#F0F4F8').grid(column=1, row=0,padx=10, pady=10)
        Label(details_window, text="Status", font=("Helvetica Neue", 16, 'bold'), bg='#F0F4F8').grid(column=2, row=0,padx=10, pady=10)

        if not data:
            Label(details_window, text="No Attendance Detail Data Found", bg='#F0F4F8').grid(column=0, row=1,columnspan=3)
            return

        for i, row in enumerate(data, start=1):
            Label(details_window, text=row[0], font=("Helvetica Neue", 14), bg='#F0F4F8').grid(column=0, row=i, padx=10,pady=5)
            Label(details_window, text=row[1], font=("Helvetica Neue", 14), bg='#F0F4F8').grid(column=1, row=i, padx=10,pady=5)
            Label(details_window, text=row[2], font=("Helvetica Neue", 14), bg='#F0F4F8').grid(column=2, row=i, padx=10,pady=5)

    def show_details():
        clear_error()
        valid, message = validate_staff_id()
        if not valid:
            nonlocal error_label
            error_label = Label(main_frame, text=message, fg="red", bg='#F0F4F8')
            error_label.grid(column=0, row=2, columnspan=2, pady=10)
            return

        staffid = staffid_entry.get()
        statement1 = "SELECT * FROM STAFF_ATTENDANCE_DETAIL WHERE STAFF_ID = %s"
        mycursor.execute(statement1, (staffid,))
        data = mycursor.fetchall()
        open_details_window(data)

    summary_button = Button(main_frame, text="Summary", command=show_summary, font=("Helvetica Neue", 14), bg='#007BFF', fg='white', relief='flat', padx=20, pady=5)
    summary_button.grid(column=0, row=3, padx=10, pady=10)

    details_button = Button(main_frame, text="Details", command=show_details, font=("Helvetica Neue", 14), bg='#28A745', fg='white', relief='flat', padx=20, pady=5)
    details_button.grid(column=1, row=3, padx=10, pady=10)

def staffatt():
    STAFFATT = Tk()
    STAFFATT.title("Staff Attendance")
    STAFFATT.geometry("500x400")
    STAFFATT.configure(bg='#E9ECEF')

    frame = Frame(STAFFATT, bg='#E9ECEF')
    frame.pack(pady=20)

    header = Label(frame, text="Staff Attendance Update", font=("Helvetica Neue", 16, 'bold'), bg='#E9ECEF', fg="#343a40")
    header.grid(row=0, column=0, columnspan=3, pady=10)

    labels = [("Staff ID: ", "staff_id"),("Date: ", "date")]

    entries = {}

    for i, (text, var_name) in enumerate(labels):
        label = Label(frame, text=text, font=("Helvetica Neue", 12), bg='#E9ECEF', fg="#495057")
        label.grid(column=0, row=i + 1, padx=10, pady=10, sticky='e')

        entry = Entry(frame, font=("Helvetica Neue", 12), bd=2, relief='flat', highlightbackground="#CED4DA")
        entry.grid(column=1, row=i + 1, padx=10, pady=10)
        entries[var_name] = entry

    STAFFID_ENTRY = entries['staff_id']
    DATE_ENTRY = entries['date']

    def getdate():
        today = datetime.today().strftime('%Y-%m-%d')
        DATE_ENTRY.delete(0, END)
        DATE_ENTRY.insert(0, today)

    DATE_BUTTON = Button(frame, text="Set Today's Date", font=("Helvetica Neue", 12), command=getdate,
                         bg='#007BFF', fg='white', relief='flat', padx=10)
    DATE_BUTTON.grid(column=2, row=1, padx=10, pady=10)

    def validate_date(date):
        pattern = r"\d{4}-\d{2}-\d{2}"
        return bool(re.match(pattern, date))

    def get_existing_counts(staffid):
        query = "SELECT PRESENT, ABSENT FROM STAFF_ATTENDANCE_SUMMARY WHERE STAFF_ID = %s"
        mycursor.execute(query, (staffid,))
        return mycursor.fetchone() or None

    def insert_into_summary(staffid, present_count, absent_count):
        insert_query = """INSERT INTO STAFF_ATTENDANCE_SUMMARY (STAFF_ID, PRESENT, ABSENT) VALUES (%s, %s, %s)"""
        mycursor.execute(insert_query, (staffid, present_count, absent_count))
        mydb.commit()

    def update_summary(staffid, present_count, absent_count):
        update_query = """UPDATE STAFF_ATTENDANCE_SUMMARY SET PRESENT = %s, ABSENT = %s WHERE STAFF_ID = %s"""
        mycursor.execute(update_query, (present_count, absent_count, staffid))
        mydb.commit()

    def insert_into_detail(staffid, date, status):
        detail_query = """INSERT INTO STAFF_ATTENDANCE_DETAIL (STAFF_ID, DATE, STATUS) VALUES (%s, %s, %s)"""
        mycursor.execute(detail_query, (staffid, date, status))
        mydb.commit()

    def mark_attendance(status):
        staffid = STAFFID_ENTRY.get().strip()
        date = DATE_ENTRY.get().strip()

        if not staffid or not date:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        if not validate_date(date):
            messagebox.showerror("Error", "Please enter the date in YYYY-MM-DD format.")
            return

        counts = get_existing_counts(staffid)

        if counts is None:
            messagebox.showinfo("Info", f"Staff ID {staffid} not found. Creating a new attendance summary entry.")
            present_count, absent_count = (1, 0) if status == "Present" else (0, 1)
            insert_into_summary(staffid, present_count, absent_count)
        else:
            present_count, absent_count = counts
            if status == "Present":
                present_count += 1
            else:
                absent_count += 1
            update_summary(staffid, present_count, absent_count)

        insert_into_detail(staffid, date, status)
        messagebox.showinfo("Success", f"Staff {staffid} marked as {status} for {date}.")

    button_frame = Frame(frame, bg='#E9ECEF')
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)

    PRESENT_BUTTON = Button(button_frame, text="Mark Present", font=("Helvetica Neue", 12), command=lambda: mark_attendance("Present"),bg='#28A745', fg='white', relief='flat', padx=20, pady=5)
    PRESENT_BUTTON.grid(row=0, column=0, padx=10)

    ABSENT_BUTTON = Button(button_frame, text="Mark Absent", font=("Helvetica Neue", 12), command=lambda: mark_attendance("Absent"),bg='#DC3545', fg='white', relief='flat', padx=20, pady=5)
    ABSENT_BUTTON.grid(row=0, column=1, padx=10)

def admin_portal():
    uiadmin = Tk()
    uiadmin.title("Admin Portal")
    uiadmin.geometry("600x600")
    uiadmin.configure(background='ivory3')

    wel_label = Label(uiadmin, text="Admin Portal", font=('Arial', 24, 'bold'), bg='ivory3', fg='darkblue')
    wel_label.grid(column=0, row=0, columnspan=2, pady=20)

    button_style = {'font': ('Arial', 14), 'bg': 'lightblue', 'fg': 'black', 'padx': 10, 'pady': 5}
    label_style = {'font': ('Arial', 16), 'bg': 'ivory3', 'fg': 'black', 'padx': 5, 'pady': 5, 'anchor': 'w'}

    stunewuser_label = Label(uiadmin, text="Student Registration", **label_style)
    stunewuser_label.grid(column=0, row=1, sticky='w')
    stunewuser_button = Button(uiadmin, text="New User", command=newuserstu, **button_style)
    stunewuser_button.grid(column=1, row=1, padx=10, pady=5)

    staffnewuser_label = Label(uiadmin, text="Staff Registration", **label_style)
    staffnewuser_label.grid(column=0, row=2, sticky='w')
    staffnewuser_button = Button(uiadmin, text="New User", command=newuserstaff, **button_style)
    staffnewuser_button.grid(column=1, row=2, padx=10, pady=5)

    newuserdetails_label = Label(uiadmin, text="New Student Details", **label_style)
    newuserdetails_label.grid(column=0, row=3, sticky='w')
    newuserdetails_button = Button(uiadmin, text="New Details", command=studentnewuserdetails, **button_style)
    newuserdetails_button.grid(column=1, row=3, padx=10, pady=5)

    newuserdetail_label = Label(uiadmin, text="New Staff Details", **label_style)
    newuserdetail_label.grid(column=0, row=4, sticky='w')
    newuserdetail_button = Button(uiadmin, text="New Details", command=staffnewuserdetails, **button_style)
    newuserdetail_button.grid(column=1, row=4, padx=10, pady=5)

    studentdetails_label = Label(uiadmin, text="Student Details Updation", **label_style)
    studentdetails_label.grid(column=0, row=5, sticky='w')
    studentdetails_button = Button(uiadmin, text="Details Updation", command=studetailupd, **button_style)
    studentdetails_button.grid(column=1, row=5, padx=10, pady=5)

    staffdetails_label = Label(uiadmin, text="Staff Details Updation", **label_style)
    staffdetails_label.grid(column=0, row=6, sticky='w')
    staffdetails_button = Button(uiadmin, text="Details Updation", command=staffdeatilupd, **button_style)
    staffdetails_button.grid(column=1, row=6, padx=10, pady=5)

    staffatt_label = Label(uiadmin, text="Staff Attendance", **label_style)
    staffatt_label.grid(column=0, row=7, sticky='w')
    staffatt_button = Button(uiadmin, text="Attendance", command=staffatt, **button_style)
    staffatt_button.grid(column=1, row=7, padx=10, pady=5)

    viewstaffatt_label = Label(uiadmin, text="View Staff Attendance", **label_style)
    viewstaffatt_label.grid(column=0, row=8, sticky='w')
    viewstaffatt_button = Button(uiadmin, text="View", command=viewstaffatt, **button_style)
    viewstaffatt_button.grid(column=1, row=8, padx=10, pady=5)

    for child in uiadmin.winfo_children():
        child.grid_configure(padx=10, pady=5)

def adminlogin():
    adminui = Tk()
    adminui.geometry('600x400')
    adminui.title("Admin Login")
    adminui.configure(bg='ivory2')

    # Updated font and spacing for better presentation
    welcome_label = Label(adminui, text="Admin Login", font=("Helvetica", 26, 'bold'), bg='ivory2', fg='midnight blue')
    welcome_label.grid(column=0, row=0, columnspan=2, pady=30)

    table_frame = Frame(adminui, bg='ivory2', highlightbackground="gray", highlightthickness=1, padx=20, pady=20)
    table_frame.grid(row=1, column=0, padx=20, pady=10)

    userlabel = Label(table_frame, text="Username:", font=("Helvetica", 16), bg='ivory2', fg='black')
    userlabel.grid(column=0, row=0, padx=10, pady=10, sticky='E')
    userentry = Entry(table_frame, width=30, font=("Helvetica", 14), bd=2, relief="groove")
    userentry.grid(column=1, row=0, padx=10, pady=10, sticky='W')

    passlabel = Label(table_frame, text="Password:", font=("Helvetica", 16), bg='ivory2', fg='black')
    passlabel.grid(column=0, row=1, padx=10, pady=10, sticky='E')
    passentry = Entry(table_frame, show="*", width=30, font=("Helvetica", 14), bd=2, relief="groove")
    passentry.grid(column=1, row=1, padx=10, pady=10, sticky='W')

    feedback_label = Label(table_frame, text="", font=("Helvetica", 14), fg="red", bg='ivory2')
    feedback_label.grid(column=0, row=3, columnspan=2, pady=10)

    def adminlog():
        useradmin = userentry.get().strip()
        passadmin = passentry.get().strip()

        if not useradmin or not passadmin:
            feedback_label.config(text="Please enter both username and password", fg="red")
            return

        try:
            state = 'SELECT * FROM ADMIN_LOGIN'
            mycursor.execute(state)
            data = mycursor.fetchall()

            for admin in data:
                if admin[0] == useradmin and admin[1] == passadmin:
                    feedback_label.config(text="Login successful", fg="green")
                    admin_portal()
                    adminui.destroy()
                    return

            if any(admin[0] == useradmin for admin in data):
                feedback_label.config(text="Invalid Password", fg="red")
            else:
                feedback_label.config(text="Invalid Username and Password", fg="red")

            userentry.delete(0, 'end')
            passentry.delete(0, 'end')

        except mysql.connector.Error as err:
            feedback_label.config(text=f"Database error: {err}", fg="red")

    submitbutton = Button(table_frame, text="Submit", font=("Helvetica", 16), command=adminlog,bg='midnight blue', fg='white', activebackground='lightblue', padx=10, pady=5)
    submitbutton.grid(column=1, row=2, pady=10, padx=5, sticky='W')

    close_button = Button(table_frame, text="Close", font=("Helvetica", 16), command=adminui.destroy,bg='firebrick3', fg='white', activebackground='salmon', padx=10, pady=5)
    close_button.grid(column=0, row=2, pady=10, padx=5, sticky='E')

    userentry.focus_set()

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