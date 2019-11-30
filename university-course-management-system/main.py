import os
import pickle

class User:

    def __init__(self,userType,username,password):
        self.userType=userType   # -> STUDENT, INSTRUCTOR, ADMIN
        self.username=username.lower()
        self.password=password

    def __str__(self):
        return "User Type: %-12s Username: %-15s Password: %-12s" %(self.userType,self.username,self.password)

class AdminUser(User):
  
    def __init__(self,username,password):
        User.__init__(self,'ADMIN',username,password)

class InstructorUser(User):

    def __init__(self,username,password,name,surname,department):
        User.__init__(self,'INSTRUCTOR',username,password)
        self.name=name
        self.surname=surname
        self.department=department.upper()

    def __str__(self):
        return super().__str__()+"Name: %-10s Surname: %-12s Department: %-4s" %(self.name,self.surname,self.department)

class StudentUser(User):
    
    def __init__(self,username,password,student_id,name,surname,semester,department):
        User.__init__(self,'STUDENT',username,password)
        self.id=student_id
        self.name=name
        self.surname=surname
        self.semester=semester.upper()
        self.department=department.upper()
        self.courses=[]
        self.reg_status=None   # -> NONE, REGISTERED, APPROVED
        self.instructor_message="" 
        self.grades={}

    def __str__(self):
        return "ID: %-15s Name: %-10s Surname: %-12s Department: %-4s Semester: %-s" %(self.id, self.name,self.surname,self.department,self.semester)

class Course:
    
    def __init__(self,code,department,title,semester,credit,section_amount,hours,prerequiste=None):
        self.code=code.upper()
        self.department=department.upper()
        self.title=title
        self.semester=semester.upper()
        self.credit=credit
        self.section_amount=section_amount
        self.hours=hours
        self.prerequiste=prerequiste.upper()

    def __repr__(self):
        return "Code: %-8s Department: %-10s Semester: %-3s Credit: %-2s Hours: %-7s" %(self.code,self.department,self.semester,self.credit,self.hours)

class CourseManagementSystem:
    users=[]
    courses={"F":[],"S":[]}
    loggedUser=None


    def __init__(self,cms_name):
        self.cms_name = cms_name
        if os.path.isfile("users.data"):
            self.readUsers()
        else:
            defaultUser = AdminUser('admin','1234')
            self.users.append( defaultUser )
            self.users.append(StudentUser("username1","password1","userID-1","name1","surname1","semester1","department1"))
            self.users.append(StudentUser("username2","password2","userID-2","name2","surname2","semester2","department2"))
            self.users.append(StudentUser("username3","password3","userID-3","name3","surname3","semester3","department3"))
            self.users.append(StudentUser("username4","password4","userID-4","name4","surname4","semester4","department4"))
            self.users.append(StudentUser("username5","password5","userID-5","name5","surname5","semester5","department5"))
            self.saveUsers()
        if os.path.isfile("courses.data"):
            self.readCourses()

    def Login(self):
        print("\nWelcome to %s Course Management System\n" % self.cms_name)
        while self.loggedUser is None:
            username=input("Enter username: ")
            password=input("Enter password: ")
            for user in self.users:
                if (user.username==username and user.password==password):
                    self.loggedUser=user
                    print("You are logged in as %s [%s]" % (self.loggedUser.username, self.loggedUser.userType))
            if self.loggedUser is None:
                print("\nWrong username or password. Please try again.\n")

    @staticmethod    
    def AdminMenu():
        print("\nChoose an action:\n",
              "1) Create course\n",
              "2) List courses\n",
              "3) Define instructor\n",
              "4) List all users\n",
              "0) Logout")
        return input()
    
    @staticmethod
    def InstructorMenu():
        print("\nChoose an action:\n",
              "1) Enter grades\n",
              "2) Approve registration\n",
              "0) Logout")
        return input()

    @staticmethod
    def StudentMenu1():
        print("\nChoose an action:\n",
              "1) See transcript\n",
              "2) Manage courses\n",
              "0) Logout")
        return input()

    @staticmethod
    def StudentMenu2():
        print("\nChoose an action:\n",
              "1) Add course\n",
              "2) Remove course\n",
              "3) Register (You can't add/remove course after registration)\n",
              "4) Go back to main menu")
        return input()

    def saveUsers(self):
        with open("users.data",'wb') as userfile:
            pickle.dump(self.users,userfile)

    def readUsers(self):
        try:
            with open("users.data",'rb') as userfile:
                self.users=pickle.load(userfile)
        except FileNotFoundError:
            print("File does not exist!")

    def saveCourses(self):
        with open("courses.data",'wb') as coursefile:
            pickle.dump(self.courses,coursefile)

    def readCourses(self):
        try:
            with open("courses.data",'rb') as coursefile:
                self.courses=pickle.load(coursefile)
        except FileNotFoundError:
            print("File does not exist!")

    def __isAdmin(self):
        if self.loggedUser.userType=='ADMIN':
            return True
        else:
            print("Access denied!")
            return False

    def __getUsername(self,userType):
        while True:
            username=input(userType+" username: ")            
            if any(user.username==username for user in self.users):
                print("\nUsername already exists!\n")
            else:
                return username
                
    def __getCourseCode(self):
        while True:
            code=input("Course code: ")
            for semester in self.courses:          
                if any(course.code==code for course in self.courses[semester]):
                    print("\nCourse already exists!\n")
                    break
            else:
                return code

    def __getPrerequisteCourseCode(self):
        while True:
            code=input("Prerequiste course code (Press ENTER if none) : ")
            if code=="":
                return code
            else:    
                if not any(course.code==code for course in self.courses["F"]):
                    print("\nCourse doesn't exist!\n")
                else:
                    return code

    def CreateAdminUser(self):
        if self.__isAdmin:
            username=self.__getUsername("Admin")
            password=input("Admin password: ")
            self.users.append(AdminUser(username,password))
            self.saveUsers()          
            print("User '%s' has been created as ADMIN\n" %username)

    def CreateInstructorUser(self):
        if self.__isAdmin:
            username=self.__getUsername("Instructor")
            password=input("Instructor password: ")
            name=input("Instructor name: ")
            surname=input("Instructor surname: ")
            department=input("Instructor department: ")
            self.users.append(InstructorUser(username,password,name,surname,department))
            self.saveUsers()
            print("User '%s %s' has been created as INSTRUCTOR\n" %(name,surname))

    def CreateStudentUser(self):
        if self.__isAdmin:
            username=self.__getUsername("Student")
            password=input("Student password: ")
            student_id=input("Student id: ")
            name=input("Student name: ")
            surname=input("Student surname: ")
            semester=input("Student semester (F/S): ")
            department=input("Student department: ")
            self.users.append(StudentUser(username,password,student_id,name,surname,semester,department))
            self.saveUsers()
            print("User '%s %s' has been created as STUDENT\n" %(name,surname))

    def CreateCourse(self):
        if self.__isAdmin:
            code=self.__getCourseCode()
            prerequiste=self.__getPrerequisteCourseCode()
            department=input("Course department: ")
            title=input("Course title: ")
            semester=input("Course semester (F/S): ").upper()
            credit=input("Course credit: ")
            section_amount=input("Course section amount: ")
            start_time=input("Course start time: ")
            end_time=input("Course end time: ")
            hours=(start_time,end_time)
            if semester=="F" or semester=="S":
                self.courses[semester].append( Course(code,department,title,semester,credit,section_amount,hours,prerequiste) )
                self.saveCourses()
                print("Course %s has been created" % (title))
            else:
                print("Semester can only be F or S")
    
    def __getLoggedUserIndex(self):
        return [i for i,user in enumerate(self.users) if user.username==self.loggedUser.username][0]
    
    def displayStudentCourses(self):
        index = self.__getLoggedUserIndex()
        print("----- YOUR COURSE LIST -----")
        for course in self.users[index].courses:
            print(course)        

    def StudentAddCourse(self):
        # find loggedUser's index in cms.users (list) in order to be able to change student user's courses
        index = self.__getLoggedUserIndex()
        available_courses = self.courses[self.users[index].semester]
        selected_course_count = len(self.users[index].courses)
        if self.users[index].reg_status!=None:
            print("You cannot add courses. Because your registeration status is: %s" %self.users[index].reg_status)
        else:
            while True:
                if len(available_courses)==0 or selected_course_count>=len(available_courses):
                    print("There is no available course left, please contact with student relations")
                    break
                else:
                    print("\n----- AVAILABLE COURSE LIST -----")
                    for course in available_courses:
                        print(course)
                choice3=input("\nEnter course code (Press 0 to exit): ").upper()
                if choice3=='0':
                    break
                elif not any(course.code==choice3 for course in available_courses):
                    print("Course does not exist!\n")
                else:
                    selected_course = [i for i,course in enumerate(available_courses) if course.code==choice3][0]
                    self.users[index].courses.append(available_courses[selected_course])
                    available_courses.pop(selected_course)
                    self.saveUsers()
                    print("Course %s added to your list\n" %choice3)
                    self.displayStudentCourses()

    def StudentRemoveCourse(self):
        # find loggedUser's index in cms.users (list) in order to be able to change student user's courses
        index = self.__getLoggedUserIndex()
        selected_course_count = len(self.users[index].courses)
        if self.users[index].reg_status!=None:
            print("You cannot remove courses. Because your registeration status is: %s" %self.users[index].reg_status)
        else:
            while True:
                if selected_course_count==0:
                    print("You have not selected any course")
                    break
                else:
                    print("----- YOUR COURSE LIST -----")
                    for course in self.users[index].courses:
                        print(course)
                choice3=input("\nEnter course code (Press 0 to exit): ")
                if choice3=='0':
                    break
                elif not any(course.code==choice3 for course in self.users[index].courses):
                    print("Course does not exist in your list!\n")
                else:
                    selected_course = [i for i,course in enumerate(self.users[index].courses) if course.code==choice3][0]
                    self.users[index].courses.pop(selected_course)
                    self.saveUsers()
                    print("Course %s removed from your list\n" %choice3)

    def StudentRegister(self):
        index = self.__getLoggedUserIndex()
        if self.users[index].reg_status=="REGISTERED":
            print("You are already registered") 
        elif self.users[index].reg_status=='APPROVED':
            print("Your registration have already been approved")
        else:
            self.displayStudentCourses()
            answer=input("\nAre you sure? (Y/N): ").upper()
            if answer=='Y':
                self.users[index].reg_status="REGISTERED"
                print("You have successfully registered")
                self.saveUsers()
        
    def __checkCredit(self,student_index):
        total_credit=0
        for course in self.users[student_index].courses:
            total_credit+=int(course.credit)
        if total_credit<=30:
            return True
        else:
            return False
            
    def __checkDepartment(self,student_index):
        for course in self.users[student_index].courses:
            if self.users[student_index].department != course.department:
                return False
        return True
    
    def __checkHours(self,student_index):
        all_hours=[]
        for course in self.users[student_index].courses:
            all_hours.append(course.hours)
        all_hours_set=set(all_hours)
        if len(all_hours_set)==len(all_hours):
            return True
        else:
            return False
    
    def __getStudentsByRegStatus(self,reg_status):
        student_indices = [i for i,student in enumerate(self.users) if student.userType=='STUDENT' and student.reg_status==reg_status]
        students=[]
        for student_index in student_indices:
            students.append(self.users[student_index])
        return students

    def ApproveRegistration(self):
        reg_students=self.__getStudentsByRegStatus('REGISTERED')
        while True:
            for student in reg_students:
                print(student,'\n')            
            student_id = input("Enter student id (Press 0 to exit): ")
            if student_id=='0':
                break
            elif not any(student.id==student_id for student in reg_students):
                print("Student is not in the list")
            else:
                student_index = [i for i,user in enumerate(self.users) if user.userType=='STUDENT' and user.id==student_id][0]
                c = self.__checkCredit(student_index)
                d = self.__checkDepartment(student_index)
                h = self.__checkHours(student_index)      
                if c and d and h:
                    self.users[student_index].reg_status='APPROVED'
                    print("Registration is approved\n")
                    self.__saveTranscript(student_index)

                else:
                    self.users[student_index].reg_status=None
                    message=""
                    if not c:
                        message+="Total course credits cannot be more than 35\n"
                    if not d:
                        message+="Courses' and student's department must be the same\n"
                    if not h:
                        message+="Course hours cannot overlap\n"
                    print("Registratiration cannot be approved. Because:")
                    print(message)
                    self.users[student_index].instructor_message=message
                self.saveUsers()

    def EnterGrades(self):
        approved_students=self.__getStudentsByRegStatus('APPROVED')     
        while True:
            for student in approved_students:
                print(student,'\n') 
            student_id = input("Enter student id (Press 0 to exit): ")
            if student_id=='0':
                break
            elif not any(student.id==student_id for student in approved_students):
                print("Student is not in the list")       
            else:
                student_index = [i for i,student in enumerate(self.users) if student.userType=='STUDENT' and student.id==student_id][0]
                for course in self.users[student_index].courses:
                    print(course, self.users[student_index].grades.get(course.code))
                code=input("Enter course code (Press 0 to exit): ").upper()
                if code=='0':
                    break
                elif not any(course.code==code for course in self.users[student_index].courses):
                    print("Course does not exist")
                else:
                    if self.users[self.__getLoggedUserIndex()].department==self.users[student_index].department:
                        while True:
                            grade = float(input("Enter grade: "))
                            if grade>=0 and grade<=100:
                                self.users[student_index].grades[code] = grade
                                print("Grade updated\n")
                                self.__saveTranscript(student_index)
                                break
                            else:
                                print("Enter a grade between 0 and 100")
                        self.saveUsers()
                    else:
                        print("Course's department is different than yours. You cannot enter grades")
    
    def __saveTranscript(self,student_index):
        student=self.users[student_index]
        file_name="transcript_"+self.users[student_index].id+".txt"
        transcript=open(file_name,"w")
        if student.semester=='F':
            transcript.write("FALL SEMESTER \n")
        elif student.semester=='S':
            transcript.write("SPRING SEMESTER \n")
        transcript.write("ID\t\t\t\tNAME\t\tDEPARTMENT\n")
        transcript.write(student.id+"\t\t\t\t"+student.name+"\t\t"+student.department+"\n")
        transcript.write("COURSE ID\tCOURSE TITLE\t\t\t\t\tGRADE\tCREDIT\n")
        for course in student.courses:
            transcript.write(course.code+"\t\t"+course.title+"\t\t\t\t\t"+str(student.grades.get(course.code))+"\t"+course.credit+"\n")
        transcript.write('-'*80)
        transcript.close()

    def SeeTranscript(self):
        student=self.users[self.__getLoggedUserIndex()]
        try:
            file_name="transcript_"+student.id+".txt"
            transcript=open(file_name,"r")
            for line in transcript:
                print(line,end="")
            transcript.close()
        except FileNotFoundError:
            print("File does not exist!")

cms = CourseManagementSystem("Yasar University")
cms.Login()

if cms.loggedUser.userType=='ADMIN':
    choice=None
    while True:
        choice=cms.AdminMenu()
        if choice=='1':
            cms.CreateCourse()
        elif choice=='2':
            for semester in cms.courses:
                for course in cms.courses[semester]:
                    print(course)
        elif choice=='3':
            cms.CreateInstructorUser()
        elif choice=='4':
            for user in cms.users:
                print(user)
        elif choice=='0':
            print("Logging out...")
            break
        else:
            print("Choose an action from the menu")
elif cms.loggedUser.userType=='INSTRUCTOR':
    choice=None
    while True:
        choice=cms.InstructorMenu()
        if choice=='1':
            cms.EnterGrades()
        elif choice=='2':
            cms.ApproveRegistration()
        elif choice=='0':
            print("Logging out...")
            break
        else:
            print("Choose an action from the menu")
elif cms.loggedUser.userType=='STUDENT':

    choice=None
    while True:
        choice=cms.StudentMenu1()
        if choice=='1':
            cms.SeeTranscript()
        elif choice=='2':
            choice2=None
            while True:
                choice2=cms.StudentMenu2()
                if choice2=='1':
                    cms.StudentAddCourse()
                elif choice2=='2':
                    cms.StudentRemoveCourse()
                elif choice2=='3':
                    cms.StudentRegister()
                elif choice2=='4':
                    break
        elif choice=='0':
            print("Logging out...")
            break
        else:
            print("Choose an action from the menu")
