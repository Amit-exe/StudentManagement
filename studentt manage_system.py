#Student management system with database
star=100
from email.mime import application
import re
import mysql.connector as db
from prettytable import PrettyTable


class Student:
    def __init__(self):
        self.__adminid = 'admin'
        self.__adminpasswd = 'admin123'



        # create table for 
        mydb = db.connect(host = 'localhost', user = 'root' , passwd = 'root', database = 'StudentManagement')
        cur = mydb.cursor()
        query = '''create table if not exists RegisterStudent(
        id int primary key auto_increment,
        Name varchar(100) not null,
        contact bigint not null,
        email varchar(100) unique not null,
        password varchar(100));'''
        cur.execute(query)


        query = '''create table if not exists SApplication(
        id int primary key auto_increment,
        Name varchar(100) not null,
        Course varchar(100) not null,
        email varchar(100) unique not null, 
        Percentage int not null,
        Last_college_name varchar(100) not null,
        Application_status varchar(20));'''
        cur.execute(query) 


        query = '''create table if not exists Student(
            rollno int primary key auto_increment,
            Name varchar(100) not null,
            course varchar(100) not null,
            email varchar(100) unique not null,
            academic_year varchar(100));'''
        cur.execute(query)


        mydb.close()



    def connection(self):
        self.mydb = db.connect(host = 'localhost', user = 'root' , passwd = 'root', database = 'StudentManagement')
        self.cur = self.mydb.cursor()


#------------------------------------------------------------------Admin Section--------------------------------------------------------


    def AdminLogin(self,adminid,adminpasswd):
        if self.__adminid == adminid:
            if self.__adminpasswd == adminpasswd:
                
                return True
            else:
                return ' Invalid password '

                
        else:
            return ' Invalid Id ' 


    def addNewStudent(self,Sname,Scourse,Semail,Syear):
        try:
            self.connection()
            data=(Semail,)
            query='''select Name from student where email=%s; '''
            self.cur.execute(query,data)

            res=self.cur.fetchone()
            print(res)
            if res==None:
                
                data=(Sname,Scourse,Semail,Syear)
                query='''insert into student(Name,course,email,academic_year) values(%s,%s,%s,%s)'''
                self.cur.execute(query,data)
                return 'Student Added Successfully..'
            else:
                return f'This email is already enrolled with name {res[0]}'    

        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()    

    def showPendingApplication(self):
        try:
            self.connection()
            query='''select * from sapplication;'''
            self.cur.execute(query)

            res=self.cur.fetchall()
            t = PrettyTable(['Application ID','Name', 'Course','Email', 'Pecentage' ,'Last college name' , 'Application_status'])
            for app in res:
                if app[6]=='pending':
                    t.add_row([app[0],app[1] ,app[2],app[3],app[4],app[5],app[6]])

            
            print(t)
            #print(res)
            if res==None:
                print('No Pending Applications as of Now')

        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()

    def addStudentFromPending(self,studentToAdd,AcademicYear):
        try:
            self.connection()
            data=(studentToAdd,)
            query='''select * from sapplication where id=%s; '''
            self.cur.execute(query,data)

            res=self.cur.fetchone()
            # print(res)
            if res==None:
                return f'This Application Id doesn\'t exist'
            else:
                if res[6]=='confirmed':
                    return 'This Application Id is already Confirmed'
                else:
                    self.addNewStudent(res[1],res[2],res[3],AcademicYear)
                    self.connection()
                    data=(studentToAdd,)
                    query='''update sapplication set Application_status='confirmed' where id=%s; '''
                    self.cur.execute(query,data)
                    return 'Student  Enrolled Successfully..'
                    
        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()   
        




#------------------------------------------------------------------Validation Functions--------------------------------------------------------



    def validateUsername(self,name):
        name_length = len(name)
        x = re.findall('[A-Za-z]+',name)
        
        if len(x[0]) == name_length:
            return True 
        else:
            return False




    #check valid contact no
    def validateContact(self,contact):
        contact=str(contact)
        ptr=r"[6-9]\d{9}" 
        x=re.findall(ptr,contact)
        if len(x) > 0:
            return True
        else:
            return False  


    #check valid email id
    def validateEmail(self,email):
        ptr=r"^[a-zA-Z0-9\.]+@[a-z]+\.[a-z]+" 
        x=re.findall(ptr,email)
        if len(x) > 0:
            return True
        else:
            return False   

#------------------------------------------------------------------Student Section--------------------------------------------------------

    #Register Student function
    def StudentRegister(self,name,contact,email,passwd,confirm_pass):
        self.userName_flag = self.validateUsername(name)
        if not self.userName_flag:
            return "Username is not valid try only with alphabets"
        
        self.userContact_flag = self.validateContact(contact)
        if not self.userContact_flag:
            return "Contact Number is not valid"

        
        self.userEmail_flag = self.validateEmail(email)
        if not self.userEmail_flag:
            return "Email Id is not valid" 
      
        if passwd == confirm_pass :
            self.password_flag = True
        else:
            return "Password MisMatch Plz try again"
        
        if self.userName_flag == True and self.userContact_flag == True and self.userEmail_flag == True and self.password_flag == True:
            self.connection()

            try:
                data = (name,contact,email,passwd)
                query = '''insert into  registerstudent(Name,contact,email,password) values(%s,%s,%s,%s);'''

                self.cur.execute(query,data)

                self.cur.execute("commit;")
                self.mydb.close()
            except Exception as e:
                print(e)
                self.mydb.close()
                return 'Email or contact Already Exists....'
            return f"Student {name} is Successfully Registered" 

    def StudentLogin(self,StudentEmailId,StudentPwd): 
        try:
            self.connection()
            data=(StudentEmailId,)
            query='''select password from registerstudent where email=%s; '''
            self.cur.execute(query,data)

            res=self.cur.fetchone()
            #print(res)
            if res==None:
                return 'Email does not exist please register First..'
            elif res[0] == StudentPwd:      
                return True
            else:
                return 'Password is incorrect.'            

        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()    

    def SubmitApplication(self,Name,Course,Email,Percentage,Last_college):
        try:
            self.connection()
            data=(Email,)
            query='''select Name from sapplication where email=%s; '''
            self.cur.execute(query,data)

            res=self.cur.fetchone()
            print(res)
            if res==None:
                
                data=(Name,Course,Email,Percentage,Last_college,"Pending")
                query='''insert into sapplication(Name,Course,email,Percentage,Last_college_name,Application_status) values(%s,%s,%s,%s,%s,%s)'''
                self.cur.execute(query,data)
                return 'Application submitted Successfully..'
            else:
                return f'This Email is already registered with name {res[0]}'    

        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()    

    def ViewApplication(self,email):
        try:
            self.connection()
            data=(email,)
            query='''select * from sapplication where email=%s; '''
            self.cur.execute(query,data)

            res=self.cur.fetchone()
            #print(res)
            if res==None:
                return f'No application has been submitted for this {email}'
                
                
            else:
                return f'Name:{res[1]}\nCourse:{res[2]}\nEmail:{res[3]}\nPecentage:{res[4]}\nLast college name:{res[5]}\nApplication_status:{res[6]}\n'
  

        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()    


            
#------------------------------------------------------------------application start from here--------------------------------------------------------


app=Student()

print(" STUDENT MANAGEMENT SYSTEM ".center(star, '*'))

while True: 
    print('1-Admin login\n2-Student Corner\n3-Exit ') 
    ch=int(input('Enter your Choice:')) 


    #choice @1admin
    if ch == 1:
        print('Admin Login Section'.center(star,"*"))

        adminId=input("Enter Admin Id:")
        adminPwd=input("Enter Admin Password:")

        LoginStatus=app.AdminLogin(adminId,adminPwd)

        if LoginStatus==True:
            print(' Admin Login Succefull  '.center(star,"*"))

            #Admin choice
            while True:  
                print('1-Add Student\n2-Remove Student\n3-List Student\n4-View Pending Applications\n5-Logout') 

                Adch=int(input('Enter your Choice:')) 

                if Adch == 1:
                    print(' Add Student Section '.center(star,"*"))
                    while True:
                        print('1-Add Student from submitted Application\n2-Enroll and Add new student\n3-Exit')
                        addStudentCh=int(input('Enter your choice:'))


                        if addStudentCh ==1:
                            print(' Add Student From Submitted Applications'.center(star,"*"))
                            print()
                            app.showPendingApplication()
                            studentToAdd = input('Enter Application Id of student you want to add:')
                            Syear=input('Enter the academic year in format YYYY-YY:')
                            addStudentStatus=app.addStudentFromPending(studentToAdd,Syear)
                            if addStudentStatus == True:
                                print(' Student Added Sucessfully '.center(star,"*"))
                            else:
                                print(f' {addStudentStatus} '.center(star,"*"))


                        elif addStudentCh==2:
                            Sname=input('Enter Student Name:')
                            Scourse=input('Enter student Course:')
                            Semail=input('Enter Student Email:')
                            Syear=input('Enter the academic year in format YYYY-YY:')

                            addNewStudentStatus=app.addNewStudent(Sname,Scourse,Semail,Syear)

                            if addNewStudentStatus==True:
                                print(' Student Added Sucessfully '.center(star,"*"))
                            else:
                                print(f' {addNewStudentStatus} '.center(star,"*"))


                        elif addStudentCh==3:
                            print(' Exiting Add student section '.center(star,'*'))
                            break
                        else:
                            print(' Invalid Choice '.center(star,'*'))










                elif Adch == 2:
                    print(' Remove Student Section'.center(star,"*"))

                    
                    




                elif Adch == 3:
                    print(' List Student Section'.center(star,"*"))

                    



                elif Adch == 4:
                    print(' View Pending Applications Section'.center(star,"*"))

                    




                elif Adch == 5:
                    print(' Logged Out '.center(star,"*"))
                    break


                else:
                    print(' Invalid Choice '.center(star,"*"))


        else:
            print(f'{LoginStatus}'.center(star,"*"))

            
                              

    #choice @2student section
    elif ch == 2:
        print('Student Section'.center(star,"*"))

        #student Choice
        while True:
            print('1-Register Student\n2-Student Login\n3-Exit') 

            stuch=int(input('Enter your Choice:')) 
            
            #student Choice @1 Register Student
            if stuch == 1:
                print(' Register Student Section '.center(star,"*"))

                SName=input("Enter your name:").strip()
                SPhone=int(input("Enter your Phone no:").strip())

                SEmail=input("Enter your Email:").strip()
                SPassword=input("Enter your Password:").strip()
                SCPassword=input("Confirm Password:").strip()

                regStatus=app.StudentRegister(SName,SPhone,SEmail,SPassword,SCPassword)

                print(f' {regStatus} '.center(star,"*"))



            #student Choice @2 Student Login
            elif stuch == 2:
                print(' Student Login '.center(star,"*"))

                StudentId=input("Enter Student Id:")
                StudentPwd=input("Enter Student Password:")

                LoginStatus=app.StudentLogin(StudentId,StudentPwd)

                if LoginStatus==True:
                    print(' Student Login Succefull  '.center(star,"*"))



                    #student choice After Login
                    while True:
                
                        print('1-Submit Application\n2-View Applications status\n3-Logout') 

                        log_st_ch=int(input('Enter your Choice:'))  

                        if log_st_ch == 1:
                            print(' Submit Application Section '.center(star,"*"))
                            Name=input("Enter your name:").strip()

                            Course=input("Enter your Course Appying for:").strip()
                            Email=input("Enter your Email:").strip()
                            Percentage=int(input("Enter your Percentage:").strip())
                            Last_college=input("Enter your Last Attended College Name:").strip()

                            Submit_Status=app.SubmitApplication(Name,Course,Email,Percentage,Last_college)

                            if Submit_Status==True:
                                print(' Application Submited Successfully..'.center(star,"*"))

                            else:
                                print(f' {Submit_Status} '.center(star,"*"))    












                        elif log_st_ch == 2:
                            print(' Applications status '.center(star,"*"))

                            email=input("Enter your Email filled in application form :")
                            viewStatus=app.ViewApplication(email)

                            print(f' {viewStatus} '.center(star,"*"))



                        elif log_st_ch == 3:
                            print(' logout '.center(star,"*")) 
                            break

                        else :
                            print(' Invalid choice '.center(star,"*"))        

                else:
                    print(f' {LoginStatus} '.center(star,"*"))        


                    
                    



            #student Choice @3 Exit
            elif stuch == 3:
                print(' Exiting Student Section'.center(star,"*"))
                break

            #student Choice @ Invalid option
            else:
                print(' Invalid Choice '.center(star,"*"))



        
        
    #Choice @3-Exit
    elif ch == 3:
        print(' Exiting Application '.center(star,"*"))
        break

        
    #Choice @Invlid choice    
    else:
        print(' Invalid Choice '.center(star,"*"))
        
        
