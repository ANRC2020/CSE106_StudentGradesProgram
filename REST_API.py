import json
import time
from flask import Flask, request, jsonify
import sqlalchemy as db
import os
import pandas as pd
from TableSetup import Reset_Database

try:
    os.system("cls")
except:
    pass

# Returned Access Points for each of the Tables
departments, teachers, classes, students, enrollments, admins = Reset_Database()

engine = db.create_engine('sqlite:///SchoolDataBase.sqlite?check_same_thread=False')
conn = engine.connect()
metadata = db.MetaData()

global ID
ID = ""

global viewCourse
viewCourse = ""

app = Flask(__name__)

@app.route('/<user_ID>', methods=['GET'])

def func(user_ID):
    
    global ID

    ID = user_ID

    if(request.method == "GET"):
        print(request.method)

        HT = {}

        results = conn.execute(db.select([students])).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()

        for i in range(df.shape[0]):
            HT[df.loc[i]['student_ID']] = df.loc[i]['password']

        results = conn.execute(db.select([teachers])).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()

        for i in range(df.shape[0]):
            HT[df.loc[i]['teacher_ID']] = df.loc[i]['password']

        results = conn.execute(db.select([admins])).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()

        for i in range(df.shape[0]):
            HT[df.loc[i]['admin_ID']] = df.loc[i]['password']

        return json.dumps(HT)

@app.route('/Student', methods=['GET'])

def Student_func():

    global ID

    if(request.method == "GET"):
        print(f"Student: {request.method}")

        HT = {}

        results = conn.execute(db.select([students])).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()

        for i in range(df.shape[0]):
            if df.iloc[i][0] == ID:
                HT[df.loc[i][0]] = df.loc[i][1]

        results = conn.execute(db.select([enrollments])).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()

        results2 = conn.execute(db.select([classes])).fetchall()
        df2 = pd.DataFrame(results2)
        df2.columns = results2[0].keys()

        results3 = conn.execute(db.select([teachers])).fetchall()
        df3 = pd.DataFrame(results3)
        df3.columns = results3[0].keys()

        for i in range(df.shape[0]):
            if df.iloc[i][0] == ID:
                
                teacher_ID = ""
                course_Des = ""
                num_students_enrolled = 0
                limit_student_enrolled = 0
                course_time = ""

                for j in range(df2.shape[0]):
                    # print(f"Index: {j} Data: {df2.iloc[j]}")
                    if df2.iloc[j]['course_ID'] == df.iloc[i]['course_ID']:
                        teacher_ID = df2.iloc[j]['teacher_ID']
                        course_Des = df2.iloc[j]['course_Des']
                        limit_student_enrolled = df2.iloc[j]['capacity']
                        num_students_enrolled = df2.iloc[j]['num_students_enrolled']
                        course_time = df2.iloc[j]['times']
                        break
                
                teacher_name = ""

                for j in range(df3.shape[0]):
                    if df3.iloc[j]['teacher_ID'] == teacher_ID:
                        teacher_name = df3.iloc[j]['name']

                HT[course_Des] = teacher_name + " " + course_time + " " +  str(df.iloc[i][2]) + " " + str(num_students_enrolled) + " " + str(limit_student_enrolled)

        return json.dumps(HT)

@app.route('/Student/ManageEnrollment', methods=['GET'])
def Manage_Enrollment():
        
    # Save the courses the student is in and their times
    student_courses = []
    student_course_times = []
    
    for i in range(1):
        results = conn.execute(db.select([enrollments])).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()

        results2 = conn.execute(db.select([classes])).fetchall()
        df2 = pd.DataFrame(results2)
        df2.columns = results2[0].keys()

        results3 = conn.execute(db.select([teachers])).fetchall()
        df3 = pd.DataFrame(results3)
        df3.columns = results3[0].keys()

        for i in range(df.shape[0]):
            if df.iloc[i][0] == ID:
                
                teacher_ID = ""
                course_Des = ""
                num_students_enrolled = 0
                limit_student_enrolled = 0
                course_time = ""

                for j in range(df2.shape[0]):
                    # print(f"Index: {j} Data: {df2.iloc[j]}")
                    if df2.iloc[j]['course_ID'] == df.iloc[i]['course_ID']:
                        teacher_ID = df2.iloc[j]['teacher_ID']
                        course_Des = df2.iloc[j]['course_Des']
                        limit_student_enrolled = df2.iloc[j]['capacity']
                        num_students_enrolled = df2.iloc[j]['num_students_enrolled']
                        course_time = df2.iloc[j]['times']
                        break
                
                teacher_name = ""

                for j in range(df3.shape[0]):
                    if df3.iloc[j]['teacher_ID'] == teacher_ID:
                        teacher_name = df3.iloc[j]['name']

                student_courses.append(course_Des)
                student_course_times.append(course_time)

    # print(f"stud courses = {student_courses}, stud times = {student_course_times}")

    if(request.method == "GET"):
        print(f"Student: {request.method}")

        HT = {}

        results2 = conn.execute(db.select([classes])).fetchall()
        df2 = pd.DataFrame(results2)
        df2.columns = results2[0].keys()

        results3 = conn.execute(db.select([teachers])).fetchall()
        df3 = pd.DataFrame(results3)
        df3.columns = results3[0].keys()

        for i in range(df2.shape[0]):
            
            teacher_ID = df2.iloc[i]['teacher_ID']

            teacher_name = ""

            for j in range(df3.shape[0]):
                if df3.iloc[j]['teacher_ID'] == teacher_ID:
                    teacher_name = df3.iloc[j]['name']
                    break
            
            type = "Add"

            if df2.iloc[i]['times'] in student_course_times:
                type = "T/C"

            if str(df2.iloc[i]['num_students_enrolled']) == str(df2.iloc[i]['capacity']):
                type = "Full"

            if df2.iloc[i]['course_Des'] in student_courses:
                type = "Drop"


            # Course Name	Instructor	Time	Students Enrolled	Add Class   Button Type(Add/Drop)
            HT[df2.iloc[i]['course_Des']] = teacher_name + " " + df2.iloc[i]['times'] + " " + str(df2.iloc[i]['num_students_enrolled']) + " " + str(df2.iloc[i]['capacity']) + " " + type

        # print(HT)

        return HT

@app.route('/Student/ManageEnrollment/Add', methods=['POST'])
def Manage_Enrollment_Add():

    if(request.method == "POST"):

        # print(request.json['course'])

        # Get the course ID of the course passed in
        results2 = conn.execute(db.select([classes])).fetchall()
        df2 = pd.DataFrame(results2)
        df2.columns = results2[0].keys()

        course_ID = ""
        num_students_enrolled = 0

        for i in range(df2.shape[0]):
            if df2.iloc[i]['course_Des'] == request.json['course']:
                course_ID = df2.iloc[i]['course_ID']
                num_students_enrolled = df2.iloc[i]['num_students_enrolled'] + 1

        query = db.insert(enrollments).values(student_ID = ID, course_ID = course_ID, grade=-1)
        conn.execute(query)

        # Increment the number of students enrolled in the class by 1

        # print(num_students_enrolled)

        query = db.update(classes).values(num_students_enrolled = int.from_bytes(num_students_enrolled, "little"))
        query = query.where(classes.columns.course_ID == course_ID)
        conn.execute(query)

    return {0:0}

@app.route('/Student/ManageEnrollment/Drop', methods=['DELETE'])
def Manage_Enrollment_Drop():

    if(request.method == "DELETE"):

        # print(request.json['course'], request.json['num_students'])

        # Delete the row corresponding to the course ID in enrollments
        results = conn.execute(db.select([enrollments])).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()

        # Get the course ID of the course passed in
        results2 = conn.execute(db.select([classes])).fetchall()
        df2 = pd.DataFrame(results2)
        df2.columns = results2[0].keys()

        course_ID = ""

        for i in range(df2.shape[0]):
            if df2.iloc[i]['course_Des'] == request.json['course']:
                course_ID = df2.iloc[i]['course_ID']

        query = db.delete(enrollments)
        query = query.where(enrollments.columns.student_ID == ID, enrollments.columns.course_ID == course_ID)
        conn.execute(query)

        temp = int(request.json['num_students']) - 1

        query = db.update(classes).values(num_students_enrolled = temp)
        query = query.where(classes.columns.course_ID == course_ID)
        conn.execute(query)

    return {0:0}

@app.route('/Teacher', methods=['GET'])
def Teacher_func():

    global ID

    if(request.method == "GET"):
        print(f"Teacher: {request.method}")

        HT = {}
        teacher_name = ""

        results = conn.execute(db.select([teachers])).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()

        for i in range(df.shape[0]):
            if df.iloc[i]["teacher_ID"] == ID:
                HT[df.iloc[i]["name"]] = ID
                teacher_name = df.iloc[i]["name"]
                break
        
        results2 = conn.execute(db.select([classes])).fetchall()
        df2 = pd.DataFrame(results2)
        df2.columns = results2[0].keys()

        for i in range(df2.shape[0]):
            if df2.iloc[i]["teacher_ID"] == ID:
                HT[df2.iloc[i]["course_ID"]] = df2.iloc[i]["course_Des"] + "|" + teacher_name + "|" + df2.iloc[i]["times"] + "|" + str(df2.iloc[i]["num_students_enrolled"]) + "|" + str(df2.iloc[i]["capacity"])

        return HT

@app.route('/Teacher/SetCourse/<course_ID>', methods=['GET'])
def Teacher_Set_Course(course_ID):

    global viewCourse

    viewCourse = course_ID

    print(viewCourse)

    HT = {"Placeholder":0}

    return HT

@app.route('/Teacher/GetCourse', methods=['GET'])
def Teacher_Course_Info():

    global viewCourse

    course_ID = viewCourse

    if(request.method == 'GET'):

        HT = {}

        results2 = conn.execute(db.select([teachers])).fetchall()
        df2 = pd.DataFrame(results2)
        df2.columns = results2[0].keys()

        for i in range(df2.shape[0]):
            if df2.iloc[i]['teacher_ID'] == ID:
                HT[df2.iloc[i]['name']] = ID
                break
        
        HT[viewCourse] = -1

        results = conn.execute(db.select([enrollments])).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()


        for i in range(df.shape[0]):
            if df.iloc[i]['course_ID'] == course_ID:

                grade = df.iloc[i]['grade']

                results1 = conn.execute(db.select([students])).fetchall()
                df1 = pd.DataFrame(results1)
                df1.columns = results1[0].keys()

                student_name = ""

                for j in range(df1.shape[0]):
                    if df.iloc[i]['student_ID'] == df1.iloc[j]['student_ID']:
                        student_name = df1.iloc[j]['name']

                HT[student_name] = str(grade)

        return HT

@app.route('/Teacher/UpdateGrade', methods=['PUT'])
def Teacher_Update_Grade():

    global viewCourse

    course_ID = viewCourse

    if(request.method == 'PUT'):

        results = conn.execute(db.select([students])).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()

        student_ID = ""

        for i in range(df.shape[0]):
            if df.iloc[i]["name"] == request.json['StudentName']:
                student_ID = df.iloc[i]['student_ID']

        query = db.update(enrollments).values(grade=request.json['newGrade'])
        query = query.where(enrollments.columns.student_ID == student_ID, enrollments.columns.course_ID == course_ID)
        conn.execute(query)

        return {"0": 0}

app.run()
