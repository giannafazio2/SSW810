from HW10_Gianna_Fazio import Repository, Student, Instructor, Major
from collections import defaultdict
import unittest

class RepositoryTest(unittest.TestCase):
    ''' contains all test cases for HW09 '''
    
    def test_prettytables(self):
        ''' Tests if data is read correctly from the files into the 3 Pretty Tables ''' 
        repo = Repository(r"C:\Users\Test\Desktop\Scripts\Repository10")
        print('\n')
        
        # test creation of new student summary with courses
        expected_student_pt = [
            ('10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], None),
            ('10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], None), 
            ('10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'], ['CS 501', 'CS 513', 'CS 545']), 
            ('10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 513', 'CS 545']), 
            ('10183', 'Chapman, O', 'SFEN', ['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']), 
            ('11399', 'Cordova, I', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], None), 
            ('11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 612', 'SYS 671'], ['SSW 540', 'SSW 565', 'SSW 810']), 
            ('11658', 'Kelly, P', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']), 
            ('11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']), 
            ('11788', 'Fuller, E', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], None)
        ]
        self.assertEqual(repo.student_summary(), expected_student_pt)  
        
        # test creation of instructor summary
        expected_instructor_pt = [
            ("98765", "Einstein, A", "SFEN", "SSW 567", 4),
            ("98765", "Einstein, A", "SFEN", "SSW 540", 3),
            ("98764", "Feynman, R", "SFEN", "SSW 564", 3),
            ("98764", "Feynman, R", "SFEN", "SSW 687", 3),
            ("98764", "Feynman, R", "SFEN", "CS 501", 1),
            ("98764", "Feynman, R", "SFEN", "CS 545", 1),
            ("98763", "Newton, I", "SFEN", "SSW 555", 1),
            ("98763", "Newton, I", "SFEN", "SSW 689", 1),
            ("98760", "Darwin, C", "SYEN", "SYS 800", 1),
            ("98760", "Darwin, C", "SYEN", "SYS 750", 1),
            ("98760", "Darwin, C", "SYEN", "SYS 611", 2),
            ("98760", "Darwin, C", "SYEN", "SYS 645", 1),
            ]
        instructors = [row for instructor in repo._instructors.values() for row in instructor.pt_row()] # it is a list
        self.assertEqual(instructors, expected_instructor_pt)  
        
       
        # test creation of majors summary
        expected_majors_pt = [('SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']), 
                           ('SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'])]
        self.assertEqual(repo.major_summary(), expected_majors_pt)           

    
if __name__ == '__main__':
    unittest.main(exit=True,verbosity=2)