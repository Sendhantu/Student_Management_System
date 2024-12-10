from tkinter import *
import tkinter as tk
import mysql.connector
from tkinter import ttk
from tkinter import Tk, Label, Entry, Button

mydb = mysql.connector.connect(host='localhost',username='root',password='Sendhan@2005',database='app_project')

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