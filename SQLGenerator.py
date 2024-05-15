from CourseScraperTest6 import TeacherSurveyScraper


mainObject = TeacherSurveyScraper("CYBR180 OpenTExt.html")
mainSurvey = TeacherSurveyScraper("canton_survey_fac_eval.p_disp_main.html")
#scrapedSurvey = mainSurvey.scrapeSurveyInfomration(['SUNYID', 'LastName', 'FirstName','Course','Section','Title', 'Students', 'Term', 'Question', 'Category', 'Rating', 'CourseRating', 'SchoolRating', 'CollegeRating'])
#2scrapedProduct = mainObject.scrapeCommentsInfomration(['SUNYID', 'LastName', 'FirstName','Course','Section','Title', 'Students', 'Term', "QuestionNo", "Response"])
controls = 0 # 1 is for Survey and 2 is for Comments

# For Testing
#print(scrapedProduct[:])
while True:
    print("Would you like to generate proceedures for the 1)Servey or the 2)Comments ?\nEnter the number that corresponds to the option below")
    controls = int(input())
    if controls == 1:
        scrapedSurvey = mainSurvey.scrapeSurveyInfomration(['SUNYID', 'LastName', 'FirstName','Course','Section','Title', 'Students', 'Term', 'Question', 'Category', 'Rating', 'CourseRating', 'SchoolRating', 'CollegeRating'])
        break
    elif controls == 2:
        scrapedProduct = mainObject.scrapeCommentsInfomration(['SUNYID', 'LastName', 'FirstName','Course','Section','Title', 'Students', 'Term', "QuestionNo", "Response"])
        break  
    else:
        print("You've entered a bad input please try again")

while controls == 1:
    print("What would you like to do with the database?\n1.Select All\n2.Select Based on Collumn\n3.Delete\n4.Upsert\n5.Exit\nEnter the number corresponding to the option below:\n")
    entry = input("Enter your Choice Here:").strip()
    # Why doesn't python have Switch-Case >:(
    if len(entry) > 1:
        print("\nInvalid Entry Please Try Again\n")
    elif "1" in entry:
        mainSurvey.selectAllData()
    elif "2" in entry:
        selectedCol = input("Enter The name of Collumn here:").strip()
        dataType = input("What is the datatype:").strip()
        mainSurvey.selectDataBasedOnCollumn(selectedCol,dataType)
    elif "3" in entry:
        mainSurvey.deleteAllData()
    elif "4" in entry:  
        mainSurvey.upsertData()
    elif "5" in entry:
        break
    else:
        print("\nInvalid Entry Please Try Again\n")

while controls == 2:
    print("What would you like to do with the database?\n1.Select All\n2.Delete\n3.Upsert\n4.Exit\nEnter the number corresponding to the option below:\n")
    entry = input("Enter your Choice Here:").strip()

    # Why doesn't python have Switch-Case >:(
    if len(entry) > 1:
        print("\nInvalid Entry Please Try Again\n")
    elif "1" in entry:
        mainObject.selectAllComments()
    elif "2" in entry:
        mainObject.deleteOneComment()
    elif "3" in entry:  
        mainObject.upsertComments()
    elif "4" in entry:
        break
    else:
        print("\nInvalid Entry Please Try Again\n")