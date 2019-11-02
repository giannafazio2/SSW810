from HW09_Gianna_Fazio import Repository, Student, Instructor
from collections import defaultdict
import unittest

class RepositoryTest(unittest.TestCase):
    ''' contains all test cases for HW09 '''
    def test_instances(self):
        ''' Tests if data is read correctly from the files  ''' 
        repo = Repository(r"C:\Users\Test\Desktop\Scripts\Repository")
        repo.read_files()

        # tests the number of students and instructors read from each file is correct
        self.assertEqual(len(repo._students), 10)
        self.assertEqual(len(repo._instructors), 6)
        
        # tests that the first student object was created correctly from reading the files
        student = Student()
        student._cwid = "10103"
        student._name = "Baldwin, C"
        student._major = "SFEN"
        student._course = defaultdict(str)
        student._course['SSW 567'] = 'A'
        student._course['SSW 564'] = 'A-'
        student._course['SSW 687'] = 'B'
        student._course['CS 501'] = 'B'
        self.assertEqual(str(repo._students[student._cwid]), str(student))
        
        # test that the first instructor object was created correctly from reading the files
        instructor = Instructor()
        instructor._cwid = "98763"
        instructor._name = "Newton, I"
        instructor._dept = "SFEN"
        instructor._course = defaultdict(int)
        instructor._course['SSW 555'] = 1
        instructor._course['SSW 689'] = 1
        self.assertEqual(str(repo._instructors[instructor._cwid]), str(instructor))
    
    def test_student_summary(self):
        ''' tests the creation of the student Pretty Table '''
        repo = Repository(r"C:\Users\Test\Desktop\Scripts\Repository")
        print('/n')
        repo.read_files()
     
        expect = [('10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']), 
                  ('10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']), 
                  ('10172', 'Forbes, I', ['SSW 555', 'SSW 567']), 
                  ('10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']), 
                  ('10183', 'Chapman, O', ['SSW 689']), 
                  ('11399', 'Cordova, I', ['SSW 540']), 
                  ('11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']), 
                  ('11658', 'Kelly, P', ['SSW 540']), 
                  ('11714', 'Morton, A', ['SYS 611', 'SYS 645']), 
                  ('11788', 'Fuller, E', ['SSW 540'])]       
        
        self.assertEqual(repo.student_summary(),expect)

    def test_instructor_summary(self):
        ''' tests the creation of the instructor Pretty Table '''
        repo = Repository(r"C:\Users\Test\Desktop\Scripts\Repository")
        print('/n')
        repo.read_files()

        expect = [('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1), 
                  ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1), 
                  ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2), 
                  ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1), 
                  ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1), 
                  ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1), 
                  ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3), 
                  ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3), 
                  ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1), 
                  ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1), 
                  ('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4), 
                  ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3)]
        
        self.assertEqual(repo.instructor_summary(),expect)
    
if __name__ == '__main__':
    unittest.main(exit=True,verbosity=2)