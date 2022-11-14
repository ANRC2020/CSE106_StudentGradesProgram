import sqlalchemy as db
from sqlalchemy import select
import random
from random import randrange, randint
import pandas as pd
import time

try:
    import os
    os.system('cls')
except:
    pass

# Define Information that will be used to populate the tables
dep = ['Language', 'Natural Sciences', 'Engineering']

dep_subjects = {'Language': {'WRI', 'HIST', 'ENGLISH', 'JAPANESE', 'SPANISH', 'GASP'}, 'Natural Sciences': {
    'BIO', 'MATH', 'CHEM', 'PHYS', 'PSYCH', 'COGS'}, 'Engineering': {'CSE', 'ENGR'}}

course_dic = {0: 'MATH', 1: 'PHYS', 2: 'CSE', 3: 'PSYCH', 4: 'WRI', 5: 'SPANISH',
              6: 'ENGLISH', 7: 'JAPANESE', 8: 'ENGR', 9: 'COGS', 10: 'HIST', 11: 'GASP', 12: 'CHEM',
              13: 'BIO'}

course_des = [['Pre-Calculus', 'Calculus', 'Discrete Math', 'Linear Algebra', 'Optimization', 'ODEs/PDEs', 'Statistics'],
              ['Intro to Physics', 'Optics', 'Chaotic Systems', 'Physics Group Study',
                  'Intermediate Physics', 'Nuclear Physics', 'Quantum Physics'],
              ['Intro to CSE', 'Data Structures', 'Computer Organization', 'Algorithims',
                  'Computer Architecture', 'Machine Learning', 'Intro to Data Bases'],
              ['Intro to Psychology', 'Intermediate Human Psychology', 'Child Development', 'Criminal Psychology',
               'Family/House Functions', 'Psychology Group Study', 'Advanced Psychology Theory'],
              ['Intro to Essay Writing', 'Classic Literature', 'Post-Modern Era Writing', 'Court House Writing',
               'Current World Issues', 'Writing in Discipline', 'Professional Writing Seminar'],
              ['Spanish 001', 'Spanish 010', 'Spanish 020', 'Spanish 030',
                  'Spanish 110', 'Spanish 120', 'Spanish 132'],
              ['English 001', 'English 010', 'English 020', 'English 030',
                  'English 110', 'English 120', 'English 132'],
              ['Japanese 001', 'Japanese 010', 'Japanese 020', 'Japanese 030',
               'Japanese 110', 'Japanese 120', 'Japanese 132'],
              ['Intro to Engineeing', 'Protyping Methods', 'Material Science', 'Structural Integrity Analysis',
               'Therodynamics', 'Enginerring Professional Seminar', 'CAD based Designing'],
              ['Intro to Cog Sci', 'Intro to Lang and Linguistics', 'Cog Sci Research Methods', 'Modeling Social Behavior',
               'Neuroscience with ML Application', 'Cog Sci and Emotions', 'Complex Adaptive Systems'],
              ['US History', 'Colonial Period', 'Silk Road', 'Policing and Race',
               'History of Korea', 'Latin American Revolutions', 'Ancient Rome'],
              ['Intro to Media', 'Writing Love Songs', 'Music Studies',
               'Theater and Cinema', 'Drawing 001', 'Drawing 005', 'Video 001'],
              ['Intro to Chem', 'General Chem 1', 'Organic Chem', 'Organic Synth and Mech',
               'Biochemistry', 'Chem Thermo and Kinetics', 'Inorganic Chem'],
              ['Contemp. Bio', 'Molecular Bio', 'Biology Today', 'The Cell', 'Nutrition', 'Microbiology', 'Virology']]

meets = [['Mon-Wed', '7:30 AM', '8:50 AM', '10:30 AM', '11:50 AM'],
         ['Tue-Thur', '7:30 AM', '8:50 AM', '10:30 AM', '11:50 AM'],
         ['Mon-Wed', '7:30 AM', '8:50 AM', '12:00 PM', '1:20 PM'],
         ['Tue-Thur', '9:00 AM', '10:20 AM', '9:00 PM', '10:20 PM'],
         ['Tue-Thur', '6:00 PM', '7:20 PM'],
         ['Mon-Wed', '9:00 AM', '10:20 AM', '1:30 PM', '2:50 PM'],
         ['Tue-Thur', '1:30 PM', '2:50 PM', '4:30 PM', '5:50 PM'],
         ['Tue-Thur', '7:30 PM', '8:50 PM'],
         ['Mon-Wed', '9:00 PM', '10:20 PM'],
         ['Fri', '7:30 AM', '8:50 AM', '9:00 AM', '10:20 AM'],
         ['Fri', '10:30 AM', '11:50 AM', '12:00 PM', '1:20 PM'],
         ['Fri', '1:30 PM', '2:50 PM', '3:00 PM', '4:20 PM'],
         ['Fri', '4:30 PM', '5:50 PM', '6:00 PM', '7:20 PM'],
         ['Fri', '7:30 PM', '8:50 PM', '9:00 PM', '10:20 PM']]

# Routine for dropping all tables


def Drop_Tables():

    tables = ['departments', 'classes', 'teachers',
              'students', 'enrollments', 'admins']

    for table in tables:
        sql = f'DROP TABLE IF EXISTS {table};'
        engine.execute(sql)

# Auxillary Routines


def generate_password():
    password = ""

    for j in range(randrange(8, 15)):

        x = 0

        while (True):
            x = randrange(33, 122)

            if (x == 34 or (x >= 36 and x <= 47) or (x >= 58 and x <= 63) or (x >= 91 and x <= 96)):
                continue

            break

        password += chr(x)

    return password


def generate_DOB(type):
    birthday = ""

    year = 0

    if type == 'student':
        year = randint(1999, 2004)

    if type == 'teacher':
        year = randint(1960, 1990)

    month = randint(1, 12)

    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)

    day = randint(1, 30)

    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)

    birth_day = [str(year), '-', month,
                 '-', day]

    for j in range(len(birth_day)):
        birthday += birth_day[j]

    return birthday


def assign_teacher(dep_name, teachers):
    # Gets all teachers from teachers table

    i = 0
    teacher_ID = 0

    while (True):
        s = select(teachers).where(teachers.c.department ==
                                   dep_name, teachers.c.num_classes == i)
        try:
            teacher_ID = list(conn.execute(s).first())[0]
            # print(dep_name, teacher_ID)
            break
        except:
            i += 1

    # Update the teacher's class count
    query = db.update(teachers).values(num_classes=i + 1)
    query = query.where(teachers.columns.teacher_ID ==
                        list(conn.execute(s).first())[0])
    conn.execute(query)

    return teacher_ID

# Routines for defining each table


def Initialize_Departments():

    global dep
    global subjects

    # Define and Create the Department Table
    departments = db.Table('departments', metadata,
                           db.Column('dep_ID', db.Integer(),
                                     primary_key=True, nullable=False),
                           db.Column('dep_name', db.String(
                               255), nullable=False)
                           )

    metadata.create_all(engine)  # Creates the table

    # Populate the Department Table

    for i, department in enumerate(dep_subjects):
        query = db.insert(departments).values(
            dep_ID=i + 1, dep_name=department)
        conn.execute(query)

    return departments


def Initialize_Teachers():
    # Define and Create the teachers Table
    teachers = db.Table('teachers', metadata,
                        db.Column('teacher_ID', db.String(
                            255), primary_key=True, nullable=False),
                        db.Column('name', db.String(255), nullable=False),
                        db.Column('password', db.String(255), nullable=False),
                        db.Column('date_of_birth', db.String(
                            255), nullable=False),
                        db.Column('department', db.String(
                            255), nullable=False),
                        db.Column('num_classes', db.Integer(), nullable=False)
                        )

    metadata.create_all(engine)  # Creates the table

    # Populate the teachers Table
    with open("Instructor.txt") as file_in:
        instructors = []
        for line in file_in:
            instructors.append(line[0:len(line) - 1])

    for i, teacher in enumerate(instructors):

        assignment = randint(1, 13)
        dep_choice = ""

        if assignment <= 5:
            dep_choice = 'Language'
        elif assignment >= 6 and assignment <= 11:
            dep_choice = 'Natural Sciences'
        else:
            dep_choice = 'Engineering'

        query = db.insert(teachers).values(teacher_ID=str(9000 + i), name=teacher, password=generate_password(),
                                           date_of_birth=generate_DOB('teacher'), department=dep_choice, num_classes=0)
        conn.execute(query)

    return teachers


def Initialize_Classes(teachers):

    global course_des
    global meets

    # Define and Create the Classes Table
    classes = db.Table('classes', metadata,
                       db.Column('course_ID', db.String(255),
                                 primary_key=True, nullable=False),
                       db.Column('course_Des', db.String(255), nullable=False),
                       db.Column('dep_name', db.String(255), nullable=False),
                       db.Column('teacher_ID', db.String(255)),
                       db.Column('num_students_enrolled',
                                 db.Integer(), nullable=False),
                       db.Column('capacity', db.Integer(), nullable=False),
                       db.Column('times', db.String(255), nullable=False)
                       )

    metadata.create_all(engine)  # Creates the table

    # Populate the classes Table
    # k = 0

    for i in range(len(course_dic)):
        for j, course in enumerate(course_des[i]):
            dep_name = ''
            for key in dep_subjects:
                if course_dic[i] in dep_subjects[key]:
                    dep_name = key
                    break

            # Assign teachers to each course

            teacher_ID = assign_teacher(dep_name, teachers)

            temp = random.randint(0, len(meets) - 1)
            query = db.insert(classes).values(course_ID=str(course_dic[i] + "_" + str((j*10))), course_Des=course, dep_name=dep_name, teacher_ID=teacher_ID,
                                              num_students_enrolled=0, capacity=random.randint(4, 10) * 5, times=str(meets[temp][0] + " " + meets[temp][random.randint(1, len(meets[temp]) - 1)]))
            conn.execute(query)

            # k += 1
            # print(f"Created Class #{k}\n")

    return classes


def Initialize_Students():
    # Define and Create the students Table
    students = db.Table('students', metadata,
                        db.Column('student_ID', db.String(
                            255), primary_key=True, nullable=False),
                        db.Column('name', db.String(255), nullable=False),
                        db.Column('password', db.String(255), nullable=False),
                        db.Column('date_of_birth', db.String(
                            255), nullable=False)
                        )

    metadata.create_all(engine)  # Creates the table

    # Populate the students Table
    with open("students_names.txt") as file_in:
        student = []
        for line in file_in:
            student.append(line[0:len(line) - 1])

    for i, stud_name in enumerate(student):
        query = db.insert(students).values(student_ID=str(1000 + i), name=stud_name,
                                           password=generate_password(), date_of_birth=generate_DOB('student'))
        conn.execute(query)

    return students


def Initalize_Enrollments(students, classes):
    # Define and Create the enrollments Table
    enrollments = db.Table('enrollments', metadata,
                           db.Column('student_ID', db.String(
                               255), nullable=False),
                           db.Column('course_ID', db.String(
                               255), nullable=False),
                           db.Column('grade', db.Float(10), nullable=False)
                           # , UniqueConstraint('student_ID', 'course_ID')
                           )

    metadata.create_all(engine)  # Creates the table

    # Gets all classes from classes table
    results = conn.execute(db.select([classes])).fetchall()
    df = pd.DataFrame(results)
    df.columns = results[0].keys()

    courses = []
    course_limit = {}
    course_count = {}
    course_date = {}

    for i in range(df.shape[0]):
        courses.append(df.iloc[i][0])
        course_limit[df.iloc[i][0]] = df.iloc[i][5]
        course_count[df.iloc[i][0]] = 0
        course_date[df.iloc[i][0]] = df.iloc[i][6]

    # Gets all students from students table
    results = conn.execute(db.select([students])).fetchall()
    df = pd.DataFrame(results)
    df.columns = results[0].keys()

    for i in range(df.shape[0]):
        # Student's name
        stud_ID = df.iloc[i][0]
        # print(stud_ID)

        # Number of classes student is taking
        num_classes = randint(3, 5)

        stud_courses = []
        stud_times = []

        for i in range(num_classes):
            # print(f"Num {i + 1} of {num_classes}\n")

            while True:

                potential_course = courses[randint(0, len(courses)-1)]

                # print(potential_course)

                if potential_course not in stud_courses and course_count[potential_course] < course_limit[potential_course] and course_date[potential_course] not in stud_times:

                    # Add row into enrollment about the student and current class
                    query = db.insert(enrollments).values(
                        student_ID=stud_ID, course_ID=potential_course, grade=randint(60, 100))
                    conn.execute(query)

                    course_count[potential_course] += 1

                    # Update the Student Count in the class
                    query = db.update(classes).values(
                        num_students_enrolled=course_count[potential_course])
                    query = query.where(
                        classes.columns.course_ID == potential_course)
                    conn.execute(query)

                    stud_courses.append(potential_course)

                    break

    return enrollments


def Initalize_Admins():
    # Define and Create the admins Table
    admins = db.Table('admins', metadata,
                      db.Column('admin_ID', db.String(255),
                                primary_key=True, nullable=False),
                      db.Column('name', db.String(255), nullable=False),
                      db.Column('password', db.String(255), nullable=False),
                      db.Column('date_of_birth', db.String(
                          255), nullable=False)
                      )

    metadata.create_all(engine)  # Creates the table

    # Populate the admins Table
    admin_names = ['Abbas Siddiqui']

    for i, admin in enumerate(admin_names):

        query = db.insert(admins).values(admin_ID=str(10000 + i), name=admin,
                                         password=generate_password(), date_of_birth=generate_DOB('teacher'))
        conn.execute(query)

    return admins


# Connect to the database
engine = db.create_engine(
    'sqlite:///SchoolDataBase.sqlite?check_same_thread=False')
conn = engine.connect()
metadata = db.MetaData()

# Reset the database


def Reset_Database():

    Drop_Tables()
    departments = Initialize_Departments()
    teachers = Initialize_Teachers()
    classes = Initialize_Classes(teachers)
    students = Initialize_Students()
    enrollments = Initalize_Enrollments(students, classes)
    admins = Initalize_Admins()

    print("Database Reset!\n")

    return departments, teachers, classes, students, enrollments, admins
