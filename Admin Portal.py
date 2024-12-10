from tkinter import *
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import re
from tkinter import Tk, Label, Entry, Button

mydb = mysql.connector.connect(host='localhost',username='root',password='Sendhan@2005',database='app_project')

mycursor = mydb.cursor()

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