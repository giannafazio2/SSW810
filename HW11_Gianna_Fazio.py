'''
@author: Gianna Fazio
SSW 810B HW 11: Stevens Data Repository 
11/17/2019
'''

from collections import defaultdict
from prettytable import PrettyTable
from HW08_Gianna_Fazio import file_reading_gen
import os
import sqlite3


'''FOR HW 11: Update your code to use the new data files that use '\t' and a header row
Add a new instructor_table_db(self, db_path) method to your Repository class to create a new 
instructor PrettyTable that retrieves the data for the table from the database you created 
above using 'db_path' to specify the path of your SQLite database file.  Use Python calls to 
execute the instructor summary query you defined above and use the data from executing the query
 to generate and display a second instructor PrettyTable with the results.
'''
class Repository:
    ''' Container to store all data structures for students, instructors, majors and grades '''
   
    def __init__(self, path):
        ''' Takes the path to the Repository as the argument and creates dictionaries for students, instructors, and majors'''
        self._students = dict() # key=CWID, value = instance of class Student()
        self._instructors = dict() # key=CWID, value = instance of class Instructor()
        self._majors = dict() #key=major, value = instance of class Major()
        self._path = path # path to repository passed in 
        self.instructor_table_db(r"C:\Users\Test\Desktop\Scripts\Repository11\810_startup.db") # EDIT path to database file 
        try:
            self._read_students(os.path.join(path, 'students.txt'))
            self._read_instructors(os.path.join(path, 'instructors.txt'))
            self._read_grades(os.path.join(path, 'grades.txt'))
            self._read_majors(os.path.join(path, 'majors.txt'))
        
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)
    
    def instructor_table_db(self, db_path):
        '''create a new instructor PrettyTable that retrieves the data for the table from the database you created using 'db_path' 
        Use Python calls to execute the instructor summary query you defined above and use the data from executing the query to generate 
        and display a second instructor PrettyTable with the results.'''
        try: 
            db = sqlite3.connect(db_path)
        except sqlite3.OperationalError:
            print(f"There was an error opening the database file ")
        
        else:
            sql_command = "select cwid, name, dept, course, count(*) as num_students from instructors join grades on instructors.cwid = grades.InstructorCWID group by course"
            pt = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])
            test_ = list()
            for row in db.execute(sql_command):
                pt.add_row(row)
                test_.append(row)
            print(f"Instructor Summary from Database")
            print(pt)
            return test_
        
    def print_summaries(self):
        ''' Quick way to print the summary PT's for students, instructors, and majors '''  
        print("\nStudent Summary")
        self.student_summary()
        print("\nInstructor Summary")
        self.instructor_summary()
        print("\nMajor Summary")
        self.major_summary()

    def _read_students(self, path): 
        ''' Read the students file line by line and create an instance of a Student '''
        try:
            for cwid, name, major in file_reading_gen(path, 3, sep='\t', header='True'):
                # Validate cwid being read             
                if cwid in self._students.keys():
                    raise ValueError(f"{cwid} in the students file is a duplicate student CWID ")
               
               # If the cwid is ok, create new instance of Student w this cwid (key)
                self._students[cwid] = Student(cwid, name, major) 

                # If the major is not recognized, throw an exception 
        except ValueError as e:
            print(e)

    def _read_instructors(self, path):
        ''' Read the instructor file and create an instance of an Instructor '''
        try:   
            for cwid, name, dept in file_reading_gen(path, 3, sep='\t', header='True'):
                # validate cwid being read              
                if cwid in self._instructors.keys():
                    raise ValueError(f" {cwid} in the instructors file is a duplicate instructor CWID ")
                
                # If the cwid is ok, create a new instance of Instructor w this cwid (key)
                self._instructors[cwid] = Instructor(cwid, name, dept) 
        
        except ValueError as e:
            print(e)

    def _read_grades(self, path):
        ''' Reads the grades file line by line and update:
            Courses taken and grades received by each student 
            Courses taught by each instructor and the number of students in the class 
        '''
        try:
            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path, 4, sep='\t', header='True'):
                # if the student cwid is already in the students dict...
                if student_cwid in self._students.keys():
                    # see if grade already exists for the student 
                    if course in self._students[student_cwid]._course.keys():
                        raise ValueError(f"Student {student_cwid} already has a grade for {course}")
                    # if the course wasn't listed for them, add it with their grade
                    else:
                        self._students[student_cwid].add_course(course, grade)
                else:
                    print(f"A grade for {course} was posted for unknown student ID ({student_cwid}) in the grades file")
                    
                # if the instructor cwid is known, increase that class count by 1 
                if instructor_cwid in self._instructors.keys():
                    self._instructors[instructor_cwid].add_student(course)
                else:
                    print(f"Unknown instructor ID ({instructor_cwid}) associated with {course} in the grades file")
                # if the major is unknown, throw an exception
                 
        except ValueError as e:
            print(e)

    def _read_majors(self, path):
        ''' Read the majors file and create instances of each Major (dept) '''
        try:
            for dept, flag, course in file_reading_gen(path, 3, sep='\t', header='True'):
                # Create a new Major instance or add a course and flag to an existing major
                if dept not in self._majors.keys():
                    self._majors[dept] = Major(dept)
                self._majors[dept].add_course(flag, course)
        
        except ValueError as e:
            print(e)

    def student_summary(self):
        ''' Generate a pretty table of all students with their info, courses taken, and remaining core courses and electives '''

        pt = PrettyTable()
        pt.field_names = ["CWID", "Name", "Major", "Completed Courses", "Remaining Core Courses", "Remaining Electives"]

        test_ = list()

        for student in sorted(self._students.values(), key=lambda student: student._cwid):
            
            courses_taken = sorted(set(student._course.keys()))
            passed_courses = {course for course, grade in student._course.items() if grade in self._majors[student._major]._passing_grades}
           
            # calculate the remaining core courses (must take all)
            remaining_cores = sorted(self._majors[student._major]._required - passed_courses)
            
            # calculate the remaining electives (they only need to take one from their major)
            if self._majors[student._major]._electives.intersection(passed_courses):
                remaining_electives = None
            else:
                remaining_electives = sorted(self._majors[student._major]._electives)
            # student cwid, student name, student's major, all classes taken, cores remaining, electives remaining
            row = student._cwid, student._name, student._major, courses_taken, remaining_cores, remaining_electives 
            test_.append(row)
            pt.add_row(row)

        print(pt)

        return test_
    
    def instructor_summary(self):
        ''' Generate a pretty table of all instructor info, including the number of students per class taught '''
        pt = PrettyTable()
        pt.field_names = ["CWID", "Name", "Dept", "Course", "Students"]

        test_ = list()

        for instructor in sorted(self._instructors.values(), key=lambda ins: ins._cwid):
            for row in instructor.pt_row():
                test_.append(row)
                pt.add_row(row)

        print(pt)

        return test_

    def major_summary(self):
        ''' Generate a pretty table of all majors, including the core and elective course options '''
        pt = PrettyTable()
        pt.field_names = ["Dept", "Required Courses", "Elective Courses"]

        test_ = list()

        for major in sorted(self._majors.values(), key=lambda major: major._dept):
            test_.append(major.pt_row())
            pt.add_row(major.pt_row())

        print(pt)

        return test_
 
class Student:
    ''' holds all details of a student '''
    def __init__(self, cwid, name, major):
        self._cwid = cwid
        self._name = name
        self._major = major
        self._course = defaultdict(str) # key=course, value=grade
    
    def __repr__(self):
        return ' '.join([self._cwid, self._name, self._major, " ".join(self._course.keys())])

    def add_course(self, course, grade):
        self._course[course] = grade

class Instructor:
    ''' holds all details of an instructor '''
    def __init__(self, cwid, name, major):
        self._cwid = cwid
        self._name = name
        self._dept = major
        self._course = defaultdict(int) # key=course value=number of students
    
    def __repr__(self):
        return ' '.join([self._cwid, self._name, self._dept, " ".join(self._course.keys())])

    def add_student(self, course):
        self._course[course] +=1

    def pt_row(self):
        course_list = list()
        for course in self._course.keys():
            # Instructor CWID, Instructor name, Major, Course, Num Students in class
            row = (self._cwid, self._name, self._dept, course, self._course[course])
            course_list.append(row)
        
        return course_list

class Major: 
    ''' hold the details (required and elective courses) for each major '''
    def __init__(self, dept):
        self._dept = dept
        self._required = set()
        self._electives = set()
        self._passing_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}

    def add_course(self, flag, course):
        if flag  == 'E':
            self._electives.add(course)
        elif flag == 'R':
            self._required.add(course)
        else:
            raise ValueError(f"Course {course} not marked as required or elective correctly (R/E)")

    def pt_row(self):
        # Major, Required Courses, Elective Courses
        return self._dept, sorted(list(self._required)), sorted(list(self._electives))

def main():
    ''' run the whole thing '''
    repo = Repository(r"C:\Users\Test\Desktop\Scripts\Repository11") # EDIT path to repository 
    repo.print_summaries()
    

if __name__ == "__main__":
    main()
