from bs4 import BeautifulSoup
import codecs 
import re

class TeacherSurveyScraper:
    def __init__(self, file):

        self.file = file

        self.masterDatabase = [] 
        self.courseInformation = {}
        self.serveyQuestions = []
        self.serveyQuestionCategoryLength = [3,2,5,5,5,5,5,5,5,5,5]
        self.surveyData = []
        self.countr = []
        self.professorInfo = []

        self.lengthAccurateQuestions = []

        self.indexesToRemove = [15,16,17,18,29,30,31,32,58,59,60,61,87,88,89,90,116,117,118,119,145,146,147,148,174,175,176,177,203,204,205,206,232,233,234,235,261,262,263,264,290,291,292,293]
        self.startcnt = 1

        self.surveyName = "Survey"

        self.SPnames = ["SurveySelect","SelectBasedOn","SurveyDelete","SurveyUpsert"]

        self.dbSurvey = { # first value of the first value of the first value .self.dbSurvey["SUNYID"][1] should = Primarykey = False
            "SUNYID":["char(9)","PrimaryKey = False"],
            "LastName":["varchar(100)","PrimaryKey = False"],
            "FirstName":["varchar(100)","PrimaryKey = False"],
            "Course":["char(10)","PrimaryKey = True"],
            "Section":["char(3)","PrimaryKey = True"],
            "Title":["varchar(100)","PrimaryKey = False"],
            "Students":["int","PrimaryKey = False"],
            "Term":["char(6)","PrimaryKey = True"],
            "Question":["varchar(200)","PrimaryKey = True"],
            "Category":["varchar(100)","PrimaryKey = True"],
            "Rating":["int","PrimaryKey = False"],
            "CourseRating":["decimal(6,2)","PrimaryKey = False"],
            "SchoolRating":["decimal(6,2)","PrimaryKey = False"],
            "CollegeRating":["decimal(6,2)","PrimaryKey = False"]
        }


        self.primaries = []

        #for serveyQuestions

        self.dbSurveyComments = {
            "SUNYID":["char(9)","PrimaryKey = False"],
            "LastName":["varchar(100)","PrimaryKey = False"],
            "FirstName":["varchar(100)","PrimaryKey = False"],
            "Course":["char(10)","PrimaryKey = False"],
            "Section":["char(3)","PrimaryKey = False"],
            "Title":["varchar(100)","PrimaryKey = False"],
            "Students":["int","PrimaryKey = False"],
            "Term":["char(6)","PrimaryKey = False"],
            "QuestionNo":["int","PrimaryKey = True"],
            "Response":["varchar(max)","PrimaryKey = False"]
        }

        self.SPCnames = ["CommentsSelect","SelectBasedOn","CommentsDelete","CommentsUpsert"]

        self.surveyName2 = "SurveyComments"

        self.primaryKeyCom = "QuestionNo"


        

        # the above code is where the Course Information will be stored and the Contents of the Servey will be stored.
        webpageFile = codecs.open(self.file, 'r') 
        # The code above allows us to read in the html as a codecs.StreamReaderWritter object, we then will convert it to a string with the following code.
        webpageToString = webpageFile.read()

        self.soup = BeautifulSoup(webpageToString, 'html.parser')
        # this instanciates a BeautifulSoup object with two arguments (webpage information as a string and the parser you're using.


    def selectAllData(self):
        with open('database.txt', 'a') as db:
            db.write("\ngo\n")
            db.write(f"Create Procedure {self.SPnames[0]}\n")
            db.write("as\n")
            db.write(f"SELECT * FROM {self.surveyName}\n")

    def selectDataBasedOnCollumn(self, Col, Datatype):
        try:
            with open('database.txt', 'a') as db:
                db.write("\ngo\n")
                db.write(f"Create Procedure {self.SPnames[1]} @{Col} {Datatype}\n")
                db.write("as\n")
                db.write(f"SELECT * FROM {self.surveyName} WHERE {Col} = @{Col}\n")
        except:
            print("Something went wrong, please check the Collumn Name or Datatype and try again.")

    def deleteAllData(self):
        comCount = 1
        andCount = 1
        with open('database.txt', 'a') as db:
            db.write("\ngo\n")
            db.write(f"Create Procedure {self.SPnames[2]}\n")
            for l in self.primaries:
                db.write(f"@{l} {self.dbSurvey[l][0]}")
                if comCount < len(self.primaries):
                    db.write(", ")
                    comCount+=1
            db.write("\nas\n")
            db.write(f"DELETE FROM {self.surveyName} Where ")
            for l in self.primaries:
                db.write(f"{l} = @{l}")
                if andCount < len(self.primaries):
                    db.write(" and ")
                    andCount+=1
            db.write(";\n")


    def upsertData(self):
        comCount = 1
        andCount  = 1
        with open('database.txt', 'a') as db:
            db.write("\ngo")
            db.write(f"\nCreate Procedure {self.SPnames[3]}\n")
            for i in self.dbSurvey.keys():
                    temp = str(i)
                    db.write(f"@{temp}  {self.dbSurvey[i][0]}")
                    if comCount < len(self.dbSurvey.keys()):
                        db.write(", ")
                        comCount+=1
            db.write("\nas\n")
            db.write("With Source (")
            comCount = 1 # resets the comCount to be used with other sets
            for j in self.dbSurvey.keys():
                    temp = str(j)
                    db.write(f"{temp}")
                    if comCount < len(self.dbSurvey.keys()):
                        db.write(", ")
                        comCount+=1
            db.write(") as (Select ")
            comCount = 1
            for k in self.dbSurvey.keys():
                    temp = str(k)
                    db.write(f"@{temp}")
                    if comCount < len(self.dbSurvey.keys()):
                        db.write(", ")
                        comCount+=1
            db.write(")\n")
            db.write(f"Merge {self.surveyName} m using Source s on ")
            for l in self.primaries:
                db.write(f"m.{l} = s.{l}")
                if andCount < len(self.primaries):
                    db.write(" and ")
                    andCount+=1
            db.write(f"\nwhen not Matched then\n")
            db.write("      insert(")
            comCount = 1
            for m in self.dbSurvey.keys():
                    temp = str(m)
                    db.write(f"{temp}")
                    if comCount < len(self.dbSurvey.keys()):
                        db.write(", ")
                        comCount+=1
            db.write(")\n")
            db.write("      values(")
            comCount = 1
            for n in self.dbSurvey.keys():
                    temp = str(n)
                    db.write(f"s.{temp}")
                    if comCount < len(self.dbSurvey.keys()):
                        db.write(", ")
                        comCount+=1
            db.write(")\n")
            db.write("when Matched then\n")
            db.write("      update set ")
            comCount = 1
            for o in self.dbSurvey.keys():
                    temp = str(o)
                    db.write(f"{temp} = s.{temp}")
                    if comCount < len(self.dbSurvey.keys()):
                        db.write(", ")
                        comCount+=1


    def selectAllComments(self):
        with open('database.txt', 'a') as db:
            db.write("\ngo\n")
            db.write(f"Create Procedure {self.SPCnames[0]}\n")
            db.write("as\n")
            db.write(f"SELECT * FROM {self.surveyName2}\n")

    def deleteOneComment(self):
        comCount = 1
        andCount = 1
        with open('database.txt', 'a') as db:
            db.write("\ngo\n")
            db.write(f"Create Procedure {self.SPCnames[2]}\n")
            db.write(f"@{self.primaryKeyCom} {self.dbSurveyComments[self.primaryKeyCom][0]}")
            if comCount < len(self.primaries):
                db.write(", ")
                comCount+=1
            db.write("\nas\n")
            db.write(f"DELETE FROM {self.surveyName2} Where ")
            db.write(f"{self.primaryKeyCom} = @{self.primaryKeyCom}")
            andCount+=1
            db.write(";\n")


    def upsertComments(self):
        comCount = 1
        andCount  = 1
        with open('database.txt', 'a') as db:
            db.write("\ngo")
            db.write(f"\nCreate Procedure {self.SPCnames[3]}\n")
            for i in self.dbSurveyComments.keys():
                    temp = str(i)
                    db.write(f"@{temp}  {self.dbSurveyComments[i][0]}")
                    if comCount < len(self.dbSurveyComments.keys()):
                        db.write(", ")
                        comCount+=1
            db.write("\nas\n")
            db.write("With Source (")
            comCount = 1 # resets the comCount to be used with other sets
            for j in self.dbSurveyComments.keys():
                    temp = str(j)
                    db.write(f"{temp}")
                    if comCount < len(self.dbSurveyComments.keys()):
                        db.write(", ")
                        comCount+=1
            db.write(") as (Select ")
            comCount = 1
            for k in self.dbSurveyComments.keys():
                    temp = str(k)
                    db.write(f"@{temp}")
                    if comCount < len(self.dbSurveyComments.keys()):
                        db.write(", ")
                        comCount+=1
            db.write(")\n")
            db.write(f"Merge {self.surveyName2} m using Source s on ")
            db.write(f"m.{self.primaryKeyCom} = s.{self.primaryKeyCom}")
            db.write(f"\nwhen not Matched then\n")
            db.write("      insert(")
            comCount = 1
            for m in self.dbSurveyComments.keys():
                    temp = str(m)
                    db.write(f"{temp}")
                    if comCount < len(self.dbSurveyComments.keys()):
                        db.write(", ")
                        comCount+=1
            db.write(")\n")
            db.write("      values(")
            comCount = 1
            for n in self.dbSurveyComments.keys():
                    temp = str(n)
                    db.write(f"s.{temp}")
                    if comCount < len(self.dbSurveyComments.keys()):
                        db.write(", ")
                        comCount+=1
            db.write(")\n")
            db.write("when Matched then\n")
            db.write("      update set ")
            comCount = 1
            for o in self.dbSurveyComments.keys():
                    temp = str(o)
                    db.write(f"{temp} = s.{temp}")
                    if comCount < len(self.dbSurveyComments.keys()):
                        db.write(", ")
                        comCount+=1




    def scrapeSurveyInfomration(self, tableCategories= ['']):
        tdValue = self.soup.find_all('table', class_='plaintable')
        # the above code stores the objects in the html that have the tag "td"

        professorBox = tdValue[4]
        pInfo = professorBox.find_all('td')

        for item in pInfo:
            if item.string == "\n":
                continue
            else:
                self.professorInfo.append(item.string)

        for value in range(len(self.professorInfo)):
            if "," in self.professorInfo[value]:
                newValue = re.split(r",",self.professorInfo[value])
                self.professorInfo[value] = newValue

        self.courseInformation.update({
            tableCategories[0]: self.professorInfo[0],
            tableCategories[1] : self.professorInfo[1][0],
            tableCategories[2] : self.professorInfo[1][1]})


        # ^This portion finds and stores the Professor's Information

        courseBox = tdValue[6]
        courseInfo = courseBox.find_all('td')

        for course in courseInfo:
            temp = course.string
            if temp == "\n" or temp == "\xa0":
                continue
            else:
                coursesplit = re.split(":|-", temp)
                self.professorInfo.append(coursesplit)
            
        self.courseInformation.update({tableCategories[3] : self.professorInfo[2][0],
                                       tableCategories[4]: self.professorInfo[2][1],
                                       tableCategories[5] : self.professorInfo[2][2],
                                       tableCategories[6]: self.professorInfo[3][1],
                                       tableCategories[7] : self.professorInfo[4][1]})

        # The above code places the course information, section information, section ID, and, professor infomration  

        questionBox = tdValue[7]
        questionInfo = questionBox.find_all('b')
        categoryAndValues = questionBox.find_all('td')
        c = []
        sortedC = []
        indexcount = 0 # I'm adding this due to the inbility of the system to have one variable with the same value to have different index ex(16 100, 16 100)

        for question in questionInfo:
            tempQ = question.string
            for nextQ in range(1,len(questionInfo)):
                if (questionInfo[nextQ].string).isnumeric == False:
                    print()
            if tempQ != "COUNT" and tempQ != "CRS %" and tempQ != "DIV %" and tempQ != 'INST %':
                self.serveyQuestions.append(tempQ)

        countCopy = self.countr.copy()
        for cav in categoryAndValues:
            if cav.string != "COUNT" and cav.string!= "CRS %" and cav.string != "DIV %" and cav.string != 'INST %' and cav.string != "______": # this takes out the filler crap, like categories
                if str(cav.string).isdigit() or len(str(cav.string)) > 1 or "." in str(cav.string) or str(cav.string).isalpha(): #this makes sure only values are numbers or strings
                    if str(cav.string) != "None":
                        c.append(cav.string)
        for par in c:
            if indexcount in self.indexesToRemove:
                pass
            else:
                sortedC.append(par)
            indexcount += 1


        for val in sortedC:
            if self.startcnt <= 5:
                countCopy.append(val)
                self.startcnt += 1
            else:
                if '\n' in countCopy[0]:
                    countCopy[0] = countCopy[0].replace('\n', ' ')
                self.surveyData.append(countCopy)
                countCopy = self.countr.copy()
                countCopy.append(val)
                self.startcnt = 2
        # the above code handles indexing the values of the servey into a matrix inside of a matrix
        
        entryCopy = self.courseInformation.copy()
        # this makes a shallow copy of the dictionary, meaning it won't effect the original

        d = -1  
        oldC = 0
        # These are important counters that allow us ot parse through the list
        try:
            for c in self.serveyQuestionCategoryLength:
                d+=1
                for x in range(oldC, c+oldC):
                    entryCopy.update({tableCategories[8] : self.serveyQuestions[d],
                            tableCategories[9] : self.surveyData[x][0],
                            tableCategories[10] : self.surveyData[x][1],
                            tableCategories[11] : self.surveyData[x][2],
                            tableCategories[12] : self.surveyData[x][3],
                            tableCategories[13] : self.surveyData[x][4]})
                    self.masterDatabase.append(entryCopy.copy())
                oldC += c
                    
        except:
            print()        # This reahces the end of the list

            oldC += c # DO NOT CHANGE THE INDENTATION
                # the dexCount allows the dictionary to have a new unique copy to place into it's database
        
        # Rememebr GARBAGE COLLECTION it's key to understadning why the above example works

        #For Debugging         
        #print(self.masterDatabase[0])
        #print(self.masterDatabase[1])
        #print(self.masterDatabase[2])
        #print(self.masterDatabase[3])
        #print(self.masterDatabase[4])
        #print(self.masterDatabase[5])

        #print(self.masterDatabase[6])
        #print(self.masterDatabase[7])
        #print(self.masterDatabase[8])
        #print(self.masterDatabase[9])
        #print(self.masterDatabase[10])
        
        #try:
            with open("database.txt", 'w') as db:
                comCount = 0
                primary = []
                db.write(f"drop table if exists {self.surveyName}\n")
                for x in self.SPnames:
                    db.write(f"drop proc if exists {x}\n")
                db.write("\nCreate table Survey(\n")
                for i in self.dbSurvey.keys():
                    temp = str(i)
                    if comCount < len(self.dbSurvey.keys()) and comCount >= 1:
                        db.write(f"    ,")
                        db.write(f"{temp}   {self.dbSurvey[i][0]}\n")
                        comCount += 1
                    else:
                        db.write(f"    ")
                        db.write(f"{temp}   {self.dbSurvey[i][0]}\n")
                        comCount += 1
                    if self.dbSurvey[i][1] == "PrimaryKey = True":
                        primary.append(temp)
                db.write("    ,constraint PK_Survey Primary Key(")
                comCount = 1
                for cols in primary:
                    db.write(f"{cols}")
                    if comCount < len(primary):
                        db.write(",")
                        comCount+=1
                db.write(")\n")    
                db.write("\n)\n")
                self.primaries = primary

                    


        #except:
         #   print("Error: Please Review Code")

        #return self.masterDatabase

    def scrapeCommentsInfomration(self, tableCategories= ['']):
        tdValue = self.soup.find_all('table', class_='plaintable')
        # the above code stores the objects in the html that have the tag "td"

        professorBox = tdValue[4]
        pInfo = professorBox.find_all('td')

        for item in pInfo:
            if item.string == "\n":
                continue
            else:
                self.professorInfo.append(item.string)

        for value in range(len(self.professorInfo)):
            if "," in self.professorInfo[value]:
                newValue = re.split(r",",self.professorInfo[value])
                self.professorInfo[value] = newValue

        self.courseInformation.update({
            tableCategories[0]: self.professorInfo[0],
            tableCategories[1] : self.professorInfo[1][0],
            tableCategories[2] : self.professorInfo[1][1]})


        # ^This portion finds and stores the Professor's Information

        courseBox = tdValue[6]
        courseInfo = courseBox.find_all('td')

        for course in courseInfo:
            temp = course.string
            if temp == "\n" or temp == "\xa0":
                continue
            else:
                coursesplit = re.split(":|-", temp)
                self.professorInfo.append(coursesplit)
            
        self.courseInformation.update({tableCategories[3] : self.professorInfo[2][0],
                                       tableCategories[4]: self.professorInfo[2][1],
                                       tableCategories[5] : self.professorInfo[2][2],
                                       tableCategories[6]: self.professorInfo[3][1],
                                       tableCategories[7] : self.professorInfo[4][1]})

        # The above code places the course information, section information, section ID, and, professor infomration  

        questionBox = tdValue[7]
        categoryAndValues = questionBox.find_all('td')
        c = []
        sortedC = []
        indexcount = 0 # I'm adding this due to the inbility of the system to have one variable with the same value to have different index ex(16 100, 16 100)

        for val in categoryAndValues:
             c.append(str(val.string))
        for strVals in c:
             if strVals == "None" or strVals == '\n' or strVals == '\xa0':
                  continue
             else:
                  sortedC.append(strVals)

        entryCopy = self.courseInformation.copy()
        # this makes a shallow copy of the dictionary, meaning it won't effect the original




        # These are important counters that allow us ot parse through the list

    # This reahces the end of the list

        try:
                for x in range(len(sortedC)):
                    entryCopy.update({tableCategories[8] : x,
                            tableCategories[9] : sortedC[x]})
                    self.masterDatabase.append(entryCopy.copy())
                    
        except:
            print()  
       
        with open("database.txt", 'w') as db:
                comCount = 0
                primary = []
                db.write(f"drop table if exists {self.surveyName2}\n")
                for x in self.SPCnames:
                    db.write(f"drop proc if exists {x}\n")
                db.write(f"\nCreate table {self.surveyName2}(\n")
                for i in self.dbSurveyComments.keys():
                    temp = str(i)
                    if comCount < len(self.dbSurveyComments.keys()) and comCount >= 1:
                        db.write(f"    ,")
                        db.write(f"{temp}   {self.dbSurveyComments[i][0]}\n")
                        comCount += 1
                    else:
                        db.write(f"    ")
                        db.write(f"{temp}   {self.dbSurveyComments[i][0]}\n")
                        comCount += 1
                    if self.dbSurveyComments[i][1] == "PrimaryKey = True":
                        primary.append(temp)
                db.write("    ,constraint PK_Survey Primary Key(")
                comCount = 1
                for cols in primary:
                    db.write(f"{cols}")
                    if comCount < len(primary):
                        db.write(",")
                        comCount+=1
                db.write(")\n")    
                db.write("\n)\n")
                self.primaries = primary
        
        #return self.masterDatabase


test = TeacherSurveyScraper("CYBR180 OpenTExt.html")
test = test.scrapeCommentsInfomration(['SUNYID', 'LastName', 'FirstName','Course','Section','Title', 'Students', 'Term','QuestionNo', 'Response'])
print(test)