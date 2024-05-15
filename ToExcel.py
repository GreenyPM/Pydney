import pandas as pd
import CourseScraperTest6 as cs6
from openpyxl import load_workbook
import logging

class exportToExcel:
    def __init__(self, array):

        self.Sscrapper = cs6.TeacherSurveyScraper("canton_survey_fac_eval.p_disp_main.html")
        self.Cscrapper = cs6.TeacherSurveyScraper("CYBR180 OpenTExt.html")

        self.collumns = array 

        self._ID = []
        self._lastName = []
        self._firstName = []
        self._course = []
        self._section = []
        self._title = []
        self._students = []
        self._term = []
        self._question = []
        self._questionNo = []
        self._response = []
        self._category = []
        self._rating = []
        self._cRating = []
        self._sRating = []
        self._collRating = []
        

    def _exportSurvey(self):
        self.Sscraper = self.Sscrapper.scrapeSurveyInfomration(self.collumns)
        for i in self.Sscrapper.masterDatabase:
            self._ID.append(i['SUNYID'])
            self._lastName.append(i['LastName'])
            self._firstName.append(i['FirstName'])
            self._course.append(i['Course'])
            self._section.append(i['Section'])
            self._title.append(i['Title'])
            self._students.append(i['Students'])
            self._term.append(i['Term'])
            self._question.append(i['Question'])
            self._category.append(i['Category'])
            self._rating.append(i['Rating'])
            self._cRating.append(i['CourseRating'])
            self._sRating.append(i['SchoolRating'])
            self._collRating.append(i['CollegeRating'])
        try:
            df = pd.DataFrame({self.collumns[0]:self._ID,
                      self.collumns[1]:self._lastName,
                      self.collumns[2]:self._firstName,
                      self.collumns[3]:self._course,
                      self.collumns[4]:self._section,
                      self.collumns[5]:self._title,
                      self.collumns[6]:self._students,
                      self.collumns[7]:self._term,
                      self.collumns[8]:self._question,
                      self.collumns[9]:self._category,
                      self.collumns[10]:self._rating,
                      self.collumns[11]:self._cRating,
                      self.collumns[12]:self._sRating,
                      self.collumns[13]:self._collRating
                      })
            with pd.ExcelWriter("export.xlsx", engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:            
                df.to_excel(writer, sheet_name="Sheet1", index=False, header=True)   
        except Exception as e:
            logging.error('Error at %s', 'division', exc_info=e)
    
    def _exportComments(self):
        self.Cscraper = self.Cscrapper.scrapeCommentsInfomration(self.collumns)
        for i in self.Cscrapper.masterDatabase:
            print(i)
            self._ID.append(i['SUNYID'])
            self._lastName.append(i['LastName'])
            self._firstName.append(i['FirstName'])
            self._course.append(i['Course'])
            self._section.append(i['Section'])
            self._title.append(i['Title'])
            self._students.append(i['Students'])
            self._term.append(i['Term'])
            self._question.append(i['QuestionNo'])
            self._category.append(i['Response'])

        try:
            df = pd.DataFrame({self.collumns[0]:self._ID,
                      self.collumns[1]:self._lastName,
                      self.collumns[2]:self._firstName,
                      self.collumns[3]:self._course,
                      self.collumns[4]:self._section,
                      self.collumns[5]:self._title,
                      self.collumns[6]:self._students,
                      self.collumns[7]:self._term,
                      self.collumns[8]:self._question,
                      self.collumns[9]:self._category,
                      })
            with pd.ExcelWriter("export.xlsx", engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:            
                df.to_excel(writer, sheet_name="Sheet2", index=False, header=True)        
        except Exception as e:
            logging.error('Error at %s', 'division', exc_info=e)

v = exportToExcel(['SUNYID', 'LastName', 'FirstName','Course','Section','Title', 'Students', 'Term', 'Question', 'Category', 'Rating', 'CourseRating', 'SchoolRating', 'CollegeRating'])
v._exportSurvey()

y = exportToExcel(['SUNYID', 'LastName', 'FirstName','Course','Section','Title', 'Students', 'Term','QuestionNo', 'Response'])
y._exportComments()