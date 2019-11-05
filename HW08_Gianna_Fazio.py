'''
@author: Gianna Fazio
SSW 810B HW 08
10/21/2019
'''

from datetime import timedelta, datetime
from  prettytable import PrettyTable
import os 

def date_arithmetic():
    ''' Part 1: uses the datetime module to complete calendar date arithmetic '''
    three_days_after_02272000 = datetime(2000, 2, 27) + timedelta(days = 3)
    # calculates the date three days after Feb 27 2000 
    three_days_after_02272017 = datetime(2017, 2, 27) + timedelta(days = 3)
    # calculates the date three days after Feb 27 2017 
    days_passed_01012017_10312017 = (datetime(2017, 10, 31) - datetime(2017, 1, 1)).days
    # calculates the number of days between Jan 1 & Oc 31, 2017 
    return three_days_after_02272000, three_days_after_02272017, days_passed_01012017_10312017

def file_reading_gen(path, num_fields, sep=',', header=False):
    try:
        fp = open(path, "r", encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Can't open '{path}' for reading")
    else:
        with fp:
            for n, line in enumerate(fp, 1):
                fields = line.rstrip('\n').split(sep)
                if len(fields) != num_fields:
                    raise ValueError(f"{path} line {n} read {len(fields)} but expected {num_fields}")
                elif n == 1 and header:
                    continue
                else:
                    yield tuple(fields)

'''def file_reading_gen(path, fields, sep=',', header=False):
   
    file_name = path
    try:
        fp = open(file_name, 'r')
    except FileNotFoundError:
        print(f'there is no file with the given path for {file_name}')
    else:
        with fp: 
            for offset, line in enumerate(fp):
                if header == True:
                    header = False
                    continue
                sep_line = line.rstrip('\n').split(sep)
                if len(sep_line) != fields:
                    raise ValueError(f"{file_name} in line {offset} has {len(sep_line)} but it should have {fields}")
                yield tuple(sep_line)'''
'''
def file_reading_gen(path, fields ,sep = ',', header='False'):
    
    try:
        fp = open(path,'r')
    except FileNotFoundError:
        print("Cannot open ", path)
    else:
        with fp:5
            line_number = 1 
            
            if header == True: 
                next(fp) 
                line_number += 1          
            
            for line in fp:
                sep_line = line.rstrip('\r\n').split(sep)
                if len(sep_line) != fields:
                    raise ValueError(f"{path} has {len(sep_line)} fields on line {line_number} but expected {fields} fields")
                
                yield sep_line
                line_number += 1
'''
class FileAnalyzer:
    '''Part 3: searches a given directory for all Python files and creates a summary of each'''
    def __init__(self, directory):
        ''' contains the python dict to store the summarized data for a file path '''
        self.directory = directory
        self.files_summary = dict()

        self.analyze_files()
             
    def analyze_files(self):
        ''' populates the summarized data into self.files_summary, argument passed to self.directory''' 
        os.chdir(self.directory)       
        for file_name in os.listdir(path='.'): 
            if file_name.endswith('.py'):
                try:
                    fp = open(file_name, 'r') 
                except FileNotFoundError:
                    print(f'Cant open {file_name} !')
                else:
                    with fp:
                        attribute_dict = {'class': 0, 'function': 0, 'line': 0, 'char': 0}                   
                        for line in enumerate(fp):
                            attribute_dict['line'] += 1
                            attribute_dict['char'] += len(str(line).split()) 
                            if str(line).strip().startswith('class '):
                                attribute_dict['class'] += 1
                            if str(line).strip().startswith('def '):
                                attribute_dict['function'] +=1   
                        self.files_summary[file_name] = attribute_dict
    '''
    def pretty_print(self):
        
        pt = PrettyTable(field_names = ['File', 'Classes', 'Functions', 'Lines', 'Characters'])
        for file_name, attribute_dict in self.files_summary:
            pt.add_row([file_name, str(item.class), str(item.function), str(item.line), str(item.char)])
            print('\n')
            print(pt)
    '''    
    
    def pretty_print(self):
        
        pt = PrettyTable(field_names = ['File', 'Classes', 'Functions', 'Lines', 'Characters'])
        for file_name in self.files_summary:
            attribute = self.files_summary[file_name].values()
            row = [file_name] + list(attribute)
            pt.add_row(row)
        print('\n')
        print(pt)
        