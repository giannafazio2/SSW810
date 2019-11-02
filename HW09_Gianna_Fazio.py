'''
@author: Gianna Fazio
SSW 810B HW 09: Stevens Data Repository 
11/03/2019
'''

from collections import defaultdict
from prettytable import PrettyTable
from HW08_Gianna_Fazio import file_reading_gen
import os

class Repository:
    ''' Container to store all data structures for students, instructors and grades '''
    def __init__(self, path):
        ''' takes the path to the Repository as the argument and creates dictionaries for students and instructors'''
        self._students = dict() # key=CWID, value = instance of class Student()
        self._instructors = dict() # key=CWID, value = instance of class Instructor()
        self._path = path # path to repository passed in 
    
    def read_files(self):
        ''' Quick way to call to read the student, instructor and grades txt files'''
        self.read_students()
        self.read_instructors()
        self.read_grades()
    
    def read_students(self): 
        ''' Read the students file line by line to get all of their info and build their class instance '''
        for line in file_reading_gen(os.path.join(self._path,'students.txt'), 3, '\t', False):
            student = Student() # create a new instance of class Student()
            student._cwid = line[0].strip() # identify CWID
            
            if not student._cwid.isdigit():
                raise ValueError("Incorrect student CWID in the students file: " + student._cwid)
            
            if student._cwid in self._students.keys():
                raise ValueError("Duplicate student CWID in the students file: " + student._cwid)
            
            student._name = line[1].strip() # identify Name 
            student._major = line[2].strip() # identify Major 
            self._students[student._cwid] = student # add the identified info to the resvective CWID key in student dict

    def read_instructors(self):
        ''' Read the instructor file and create an instance of an instructor with the data '''
        for line in file_reading_gen(os.path.join(self._path,'instructors.txt'), 3, '\t', False):
            instructor = Instructor() # create a new instance of class Student()
            instructor._cwid = line[0].strip() # identify CWID
            
            if not instructor._cwid.isdigit():
                raise ValueError("Incorrect instructor CWID int the instructors file: " + instructor._cwid)
            
            if instructor._cwid in self._instructors.keys():
                raise ValueError("Duplicate instructor CWID in the instructors file: " + instructor._cwid)
            
            instructor._name = line[1].strip() # identify  Name 
            instructor._dept = line[2].strip() # identify dept 
            self._instructors[instructor._cwid] = instructor # add this info to the respective CWID key in instructor dict
    
    def read_grades(self):
        ''' Reads the grades file line by line to update:
            Courses taken and grades received by each student 
            Courses taught by each instuructor and the number of students in the class '''
        for line in file_reading_gen(os.path.join(self._path, 'grades.txt'), 4, '\t', False):
            student_cwid = line[0].strip() # identify student CWID 
            if not student_cwid.isdigit():
                raise ValueError("Incorrect student CWID in the grades file: " + str(line))
            
            if student_cwid not in self._students.keys():
                raise ValueError("Unfamiliar student CWID: " + str(line))
            
            instructor_cwid = line[3].strip() # identify instructor CWID
            
            if not instructor_cwid.isdigit():
                raise ValueError("Incorrect instructor CWID in the grades file: " + str(line))
            if instructor_cwid not in self._instructors.keys():
                raise ValueError("Unfamiliar instructor CWID: " + str(line))
        
            course = line[1].strip() # identify the course taken 
            grade = line[2].strip() # identify the grade received 
        
            if course in self._students[student_cwid]._course.keys():
                raise ValueError("Duplicate grade in the grades file: " + str(line))

            self._instructors[instructor_cwid]._course[course] += 1 # add another student to the course to the instructors data 
            self._students[student_cwid]._course[course] = grade # add the grade the student got to the student's data 

    def student_summary(self):
        ''' generates a pretty table of all students w/ their CWID, name, and a sorted list of courses '''
        pt = PrettyTable()
        pt.field_names = ["CWID", "Name", "Completed Courses"]

        test_ = list()

        for student in sorted(self._students.values(), key=lambda student: student._cwid):
            row = (student._cwid, student._name, sorted([name for name in student._course.keys()]))
            test_.append(row)
            pt.add_row(row)

        print(pt)

        return test_
    
    def instructor_summary(self):
        ''' generates a pretty table of all instructors w/ their CWID, name, dept, courses taught, and # of students per class '''
        pt = PrettyTable()
        pt.field_names = ["CWID", "Name", "Dept", "Course", "Students"]

        test_ = list()

        for instructor in sorted(self._instructors.values(), key=lambda ins: ins._cwid):
            for course, students in instructor._course.items():
                row = (instructor._cwid, instructor._name, instructor._dept, course, students)
                test_.append(row)
                pt.add_row(row)

        print(pt)
        print(test_)

        return test_

class Student:
    ''' holds all details of a student '''
    def __init__(self):
        self._cwid = ''
        self._name = ''
        self._major = ''
        self._course = defaultdict(str) # key=course, value=grade
    
    def __repr__(self):
        return ' '.join([self._cwid, self._name, self._major, " ".join(self._course.keys())])

class Instructor:
    ''' holds all details of an instructor '''
    def __init__(self):
        self._cwid = ''
        self._name = ''
        self._dept = ''
        self._course = defaultdict(int) # key=course value=number of students
    
    def __repr__(self):
        return ' '.join([self._cwid, self._name, self._dept, " ".join(self._course.keys())])

def main():
    ''' run the whole thing '''
    repo = Repository(r"C:\Users\Test\Desktop\Scripts\Repository") # EDIT path to repository
    repo.read_files() # read the grades, students and intructors files 
    repo.student_summary() # generate a student summary PT from the data 
    repo.instructor_summary() # generate an instructor summary PT from the data 

if __name__ == "__main__":
    main()
