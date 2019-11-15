from HW11_Gianna_Fazio import Repository, Student, Instructor, Major
from collections import defaultdict
import unittest

class RepositoryTest(unittest.TestCase):
    ''' contains all test cases for HW09, HW10
    HW 11: Add a new automated test to verify that the data retrieved from the database matches the expected rows.'''

    def test_prettytables(self):
        ''' Tests if data is read correctly from the files into the 3 Pretty Tables ''' 
        repo = Repository(r"C:\Users\Test\Desktop\Scripts\Repository11")

        print('\n')
        
        # test the creation of the database- based pretty table 
        expected_db_instructor_pt = [
            ('98762', 'Hawking, S', 'CS', 'CS 501', 1),
            ('98764', 'Cohen, R', 'SFEN', 'CS 546', 2),
            ('98762', 'Hawking, S', 'CS', 'CS 570', 1),
            ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1), 
            ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),
            ]
        self.assertEqual(repo.instructor_table_db(r"C:\Users\Test\Desktop\Scripts\Repository11\810_startup.db"), expected_db_instructor_pt)

        # test creation of new student summary with courses
        expected_student_pt = [
            ('10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], None),
            ('10115', 'Bezos, J', 'SFEN', ['CS 546', 'SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546']), 
            ('10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546']), 
            ('11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], [], None), 
            ('11717', 'Kernighan, B', 'CS', [], ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']), 
        ]
        self.assertEqual(repo.student_summary(), expected_student_pt)  
        
        # test creation of instructor summary
        expected_instructor_pt = [
        ("98762", "Hawking, S", "CS", "CS 501", 1),
        ("98762", "Hawking, S", "CS", "CS 546", 1),
        ("98762", "Hawking, S", "CS", "CS 570", 1),
        ("98763", "Rowland, J", "SFEN", "SSW 810", 4),
        ("98763", "Rowland, J", "SFEN", "SSW 555", 1),
        ("98764", "Cohen, R", "SFEN", "CS 546", 1),
        ]
        self.assertEqual(repo.instructor_summary(), expected_instructor_pt)
       
        # test creation of majors summary
        expected_majors_pt = [
            ('CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']), 
            ('SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']),
            ]
        self.assertEqual(repo.major_summary(), expected_majors_pt)           

    
if __name__ == '__main__':
    unittest.main(exit=True,verbosity=2)