from CourseScraperTest6 import TeacherSurveyScraper
import pyodbc


mainSurvey = TeacherSurveyScraper("CITA 180 - Spring 2023.html") # why isn't this new page forming correctly
mainComments = TeacherSurveyScraper("CYBR180 OpenTExt.html")

Sproceedures = mainSurvey.SPnames
Cproceedures = mainSurvey.SPCnames

mainSurveyName = mainSurvey.surveyName
mainCommentsName = mainSurvey.surveyName2

scrapedProduct = mainSurvey.scrapeSurveyInfomration(['SUNYID', 'LastName', 'FirstName','Course','Section','Title', 'Students', 'Term', 'Question', 'Category', 'Rating', 'CourseRating', 'SchoolRating', 'CollegeRating'])
scrapedProductComments = mainComments.scrapeSurveyInfomration(['SUNYID', 'LastName', 'FirstName','Course','Section','Title', 'Students', 'Term','QuestionNo', 'Response'])

masterDataSurvey = mainSurvey.masterDatabase
masterDataComments = mainComments.masterDatabase

#o(2^n)
def runSurveyUpsert(parameters = []): # parameter's should be a list
    connect = pyodbc.connect('DRIVER=SQL Server;Server=citasql02;Database=patrick;UID=patrick;PWD=PineApple;')
    primariesFormed = []
    cursor = connect.cursor()  
    for j in range(len(masterDataSurvey)):
        for i in range(len(parameters)):
            value = (masterDataSurvey[j][parameters[i]]).strip() # this promopts the user to input what each value should be populated with.
            primariesFormed.append(f"@{parameters[i]} = '{value}'") # this puts the paramters needed for this inside a container fully formed
        queryString = "exec {} {}".format("SurveyUpsert", ", ".join(primariesFormed)) # this code completes the sequence
        print(queryString)
        cursor.execute(queryString)
        connect.commit()
        primariesFormed = [] # this sets the primaries back to zero, the error of Too many arguments, ws stackign as these arent setup as keys for the parameters they are 
    cursor.close()


def runSurveySelect(): # parameter's should be a list
    connect = pyodbc.connect('DRIVER=SQL Server;Server=citasql02;Database=patrick;UID=patrick;PWD=PineApple;')
    cursor = connect.cursor()
    queryString = f"SELECT * FROM {mainSurveyName};"
    print(queryString)
    cursor.execute(queryString)
    connect.commit()
    cursor.close()

def runSurveyDelete(pks = []):
    connect = pyodbc.connect('DRIVER=SQL Server;Server=citasql02;Database=patrick;UID=patrick;PWD=PineApple;')
    cursor = connect.cursor()
    queryString = "exec {} {}".format(Sproceedures[2], ",".join(pks))
    print(queryString)
    cursor.execute(queryString)
    connect.commit()
    cursor.close()


def runCommentUpsert(parameters = []): # parameter's should be a list
    connect = pyodbc.connect('DRIVER=SQL Server;Server=citasql02;Database=patrick;UID=patrick;PWD=PineApple;')
    primariesFormed = []
    cursor = connect.cursor()  
    for j in range(len(masterDataComments)):
        for i in range(len(parameters)):
            value = (masterDataComments[j][parameters[i]]).strip() # this promopts the user to input what each value should be populated with.
            primariesFormed.append(f"@{parameters[i]} = '{value}'") # this puts the paramters needed for this inside a container fully formed
        queryString = "exec {} {}".format("CommentsUpsert", ", ".join(primariesFormed)) # this code completes the sequence
        print(queryString)
        cursor.execute(queryString)
        connect.commit()
        primariesFormed = [] # this sets the primaries back to zero, the error of Too many arguments, ws stackign as these arent setup as keys for the parameters they are 
    cursor.close()


def runCommentSelect(): # parameter's should be a list
    connect = pyodbc.connect('DRIVER=SQL Server;Server=citasql02;Database=patrick;UID=patrick;PWD=PineApple;')
    cursor = connect.cursor()
    queryString = f"SELECT * FROM {mainCommentsName};"
    print(queryString)
    cursor.execute(queryString)
    connect.commit()
    cursor.close()

def runCommentDelete(value):
    connect = pyodbc.connect('DRIVER=SQL Server;Server=citasql02;Database=patrick;UID=patrick;PWD=PineApple;')
    cursor = connect.cursor()
    queryString = f"exec {Cproceedures[2]} {value}"
    print(queryString)
    cursor.execute(queryString)
    connect.commit()
    cursor.close()

def tester():
    connect = pyodbc.connect('DRIVER=SQL Server;Server=citasql02;Database=patrick;UID=patrick;PWD=PineApple;')
    cursor = connect.cursor()
    queryString = "exec SurveyUpsert @SUNYID = '803582138', @LastName = 'Burl', @FirstName = 'Thomas', @Course = 'CYBR180', @Section = '0W1', @Title = 'INTRO TO PROGRAMMING', @Students = '13', @Term = '202309', @Question = 'I am:', @Category = 'Under 20 years old', @Rating = '0', @CourseRating = '0', @SchoolRating = '28.29', @CollegeRating = '29.95'"
    print(queryString)
    cursor.execute(queryString)
    connect.commit()
    cursor.close()

#tester()
#runSurveySelect()
#runSurveyUpsert(['SUNYID', 'LastName', 'FirstName','Course','Section','Title', 'Students', 'Term', 'Question', 'Category', 'Rating', 'CourseRating', 'SchoolRating', 'CollegeRating'])
runCommentUpsert(['SUNYID', 'LastName', 'FirstName','Course','Section','Title', 'Students', 'Term','QuestionNo', 'Response'])