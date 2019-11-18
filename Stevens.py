'''
@author: Gianna Fazio
SSW 810B HW 12: Stevens Data Repository Web Page with Flask 
11/17/2019
'''
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/instructor_summary') # add this forward slash to the URL generated when the program is run
def instructor_summary():
    '''
    Queries an SQLite db and uses flask and Jinja2 to create a table of courses taught in the web
    '''
    # EDIT path to the database! 
    dbpath = r"C:\Users\Test\Desktop\Scripts\HW12\810_startup.db"

    try:
        db = sqlite3.connect(dbpath)
    except sqlite3.OperationalError:
        return f"Error: Unable to open the database at {dbpath}"
    else:
        query = """ select i.cwid, i.name, i.dept, g.course, count(*) as students 
                        from instructors i join grades g on i.cwid=g.instructorcwid group by i.cwid, g.course""" 
    
        data = [{'cwid': cwid, 'name': name, 'dept': dept, 'course': course, 'students': students}
                for cwid, name, dept, course, students in db.execute(query)]

        db.close()

        return render_template( #fills in the fields defined in instructor_summary.html
                'instructor_summary.html',
                title ='Stevens Repository',
                table_title='Number of students by course and instructor',
                instructors=data)

app.run(debug=True)


