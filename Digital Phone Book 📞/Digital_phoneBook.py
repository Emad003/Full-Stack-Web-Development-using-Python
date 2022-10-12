import os
import datetime
import getpass
from termcolor import colored
from tabulate import tabulate
#DATABASE CONNECTION
try:
 import connect_db
except Exception as error:
    print("Connection File is Missing..")
    input("Press Any key to Exit...")
    exit(0)
#CLOSE DATABASE CONNECTION
def CLOSE_DATABASE():
    connect_db.conn.close()
                 # MIAN MENU
def main_menu():
    os.system('cls')
    print("1.Registration","2.Login","3.Exit",sep='\n')
    ch=int(input("Enter your choice: "))
    return ch
                 # SECOND MENU
def second_menu():
    print("1.Add Contact","2.Read all Contacts","3.Read any Specific Contact","4.Update any specific Contact","5.Delete any Specific Contact","6.Delete All Contacts","7.Logout",sep='\n')
    ch1=int(input("Enter your Choice: "))
    return ch1

#  PERFORM REGISTARTION
def perform_Registration(name,email,password):
        register_script="INSERT into accnt(name,email,password)values(%s,%s,%s)"
        val=(name,email,password)
        connect_db.cur.execute(register_script,val)
        connect_db.conn.commit()        
        print(colored("Account Registered Successfully!\n",'green'))
        input("\nPress any key to Continue...")
        start()
#PRINT Data and TIME
def printDate():
      get_date = datetime.datetime.now()
      print (get_date.strftime("%Y-%m-%d %H:%M:%S"))
      print("--------------------")

# Login AUTHENTICATION
def Login_Auth(email,passwrd):
    auth_script='''
        select name from accnt where email=%s and password=%s
    '''
    val=(email,passwrd)
    try:
        connect_db.cur.execute(auth_script,val)
        data=connect_db.cur.fetchone()       
    except Exception as error:
        print(colored("\nFailed to connect to the Database.!\n",'red'))
        input("Press any key to exist..")
        exit(0)
    else:
        if  not data:
            print(colored("\nInvalid Credential or Account Not Registered!\n",'red'))
            input("\nPress any key to Continue...")
            start()
        else:
            os.system('cls')
            print(colored('[{} logged in]','green').format(data[0]))
            printDate()
            start_CRUD(email,passwrd)
#check Existing user
def check_user(email):
    check_script="select name from accnt where email=%s"
    val=(email,)
    try:
        connect_db.cur.execute(check_script,val)
        data=connect_db.cur.fetchone()
        if not data:
         return True
        else:
            print(colored('{} is Already Registered with this Email..!','yellow').format(data[0]))
            input("press any Key to continue...")
            start() 
    except Exception as error:
        print(colored("Failed to connect to the Database!",'red')) 
        input()
        start() 
    
# Login Function
def Login():
    os.system('cls')
    while(True):
        email=input("Enter your Email: ")
        if email.count('@')==1 and email.count('.')==1:
            break
        else:
            print(colored("Invalid Email Format!\n",'red'))

    passwrd=getpass.getpass("Enter Password: ")
    Login_Auth(email.lower(),passwrd)
# Registration Function
def Registration():
    os.system('cls')
    name=input("Enter your Name: ")
    while(True):
        email=input("Enter your Email: ")
        if email.count('@')==1 and email.count('.')==1:
            break
        else:
            print(colored("Invalid Email Format!\n",'red'))
    while(True):
        passwrd,cpasswrd=getpass.getpass("Enter your password: "),input("Confirm your password: ")
        if(passwrd==cpasswrd):
            break
        else:
           print(colored("\nPassword must be Same!\n",'red'))
    if check_user(email):
        perform_Registration(name,email.lower(),passwrd)
                            #PERFROM UPDATION
def perfrom_updation(id,fname,lname,email,phone,temail,tpass):
    update_script='UPDATE contact set firstname=%s,lastname=%s,email=%s,phone_no=%s where contact_id=%s and a_mail=%s and a_pass=%s'
    # update_script='select * from contact'
    val=(fname,lname,email,phone,id,temail,tpass)
    connect_db.cur.execute(update_script,val)
    row=connect_db.cur.rowcount
    connect_db.conn.commit()
    if row>0:
        return True
    return False
    
                            #Fetch USER NAME
def fetch_username(temail,tpass):
    auth_script='''
        select name from accnt where email=%s and password=%s
    '''
    val=(temail,tpass)
    connect_db.cur.execute(auth_script,val)
    data=connect_db.cur.fetchone()
    return data[0]
                            # DELETE ALL CONTACTS
                            
def delete_all(temail,tpass):
    os.system('cls')
    temp_name=fetch_username(temail,tpass)
    print(colored('[{} logged in]','green').format(temp_name))
    printDate()
    print(colored("Warning! You will Lose All Contacts\n",'red'))
    choice=input((colored("Type'CONFIRM' to Agree OR Press Any key to Cancel\n",'red')))
    if choice=="CONFIRM":
        
        delete_script="DELETE from contact WHERE a_mail=%s and a_pass=%s"
        val=(temail,tpass)
        connect_db.cur.execute(delete_script,val)
        affected_row=connect_db.cur.rowcount
        connect_db.conn.commit()
        print(colored('{} Records Deleted\n','yellow').format(affected_row))
        input("Press Any key to Return..")
        start_CRUD(temail,tpass)
    else:
        start_CRUD(temail,tpass)
                             #GET ALL CONTACTS
def get_ALL(temail,tpass):
    os.system('cls')
    temp_name=fetch_username(temail,tpass)
    print(colored('[{} logged in]','green').format(temp_name))
    printDate()
    getALL_Script="SELECT contact_id,firstname,lastname,email,phone_no from contact where a_mail=%s and a_pass=%s"
    val=(temail,tpass)
    connect_db.cur.execute(getALL_Script,val)
    RAW_DATA=connect_db.cur.fetchall()
    row=connect_db.cur.rowcount
    headers="ContactID","FirstName","LastName","Email","PhoneNumber"
    print(colored('{} Contacts','green').format(row))
    print(tabulate(RAW_DATA,headers,tablefmt='fancy_grid'))
    input("Press any key to continue...")
    start_CRUD(temail,tpass)  
                             #UPDATE SPECIFIC CONTACT
def update_specific(temail,tpass):
    os.system('cls')
    temp_name=fetch_username(temail,tpass)
    print(colored('[{} logged in]','green').format(temp_name))
    printDate()
    id=input("Enter ContactID to Update: ")
    view_script="SELECT contact_id,firstname,lastname,email,phone_no from contact WHERE  contact_id=%s and a_mail=%s and a_pass=%s "
    val=(id,temail,tpass)
    connect_db.cur.execute(view_script,val)
    row=connect_db.cur.rowcount
    if row==0:
        print(colored("No Contact Found to Update:",'yellow'))  
        print("Press Any key to Return...")
        input()
        start_CRUD(temail,tpass)
    else:
        raw_data=connect_db.cur.fetchall()
        headers="ContactID","FirstName","LastName","Email","PhoneNumber"
        print(colored("{} Contact Found:",'green').format(row))
        print(tabulate(raw_data,headers,tablefmt='fancy_grid'))
        n=input(colored("Want to Update?[Type 'yes' or press any key..] ",'red')).lower()
        if n=='yes':

            fname,lname=input("Enter First Name: "),input("Enter Last Name: ")
            while(True):
                email=input("Enter Email: ")
                if email.count('@')==1 and email.count('.')==1:
                    break
                else:
                    print(colored("Invalid Email Format!\n",'red'))
            while(True):
                try:
                    phone=int(input("Enter Phone Number: "))

                except ValueError:
                        print(colored("\nPhone Number Must Be Digit!\n",'red'))
                else:
                    break
            if perfrom_updation(id,fname,lname,email,phone,temail,tpass):
                print(colored("Updation Successfull!",'green'))
                input("Press Any key to Return...")
                start_CRUD(temail,tpass)
            else:
                print(colored("Failed to Update",'red'))
                input("Press Any key to Return...")
                start_CRUD(temail,tpass)
        else:
            start_CRUD(temail,tpass)
                         #PERFORM ADDITION
def do_addition(firstname,lastname,email,phone,temail,tpss):
    add_script="insert into contact(firstname,lastname,email,phone_no,a_mail,a_pass)VALUES(%s,%s,%s,%s,%s,%s)"
    val=(firstname,lastname,email.lower(),phone,temail,tpss)
    connect_db.cur.execute(add_script,val)
    connect_db.conn.commit()
    print(colored("Contact Added Successfully!\n",'green'))
    input("Press any key to Continue...")
    start_CRUD(temail,tpss,email)
                           #PERFORM SPECIFIC DELETION
def perform_del_specific(id,temail,tpass):
    delete_script="DELETE from contact where contact_id=%s AND a_mail=%s and a_pass=%s"
    val=(id,temail,tpass)
    connect_db.cur.execute(delete_script,val)
    affected_row=connect_db.cur.rowcount
    connect_db.conn.commit()
    if affected_row==0:
        return False
    else:
        return True
#DELETE SPECIFIC
def del_specific(temail,tpass):
    os.system('cls')
    temp_name=fetch_username(temail,tpass)
    print(colored('[{} logged in]','green').format(temp_name))
    printDate()
    id=input("Enter Contact Id: ")
    view_script="SELECT contact_id,firstname,lastname,email,phone_no from contact WHERE  contact_id=%s and a_mail=%s and a_pass=%s "
    val=(id,temail,tpass)
    connect_db.cur.execute(view_script,val)
    raw_data=connect_db.cur.fetchall()
    headers="ContactID","FirstName","LastName","Email","PhoneNumber"
    print("Your Contacts")
    print(tabulate(raw_data,headers,tablefmt='fancy_grid'))
    if perform_del_specific(id,temail,tpass):
         print(colored("Deleted\n",'green')) 
         input("Enter Any key to Return..")
         start_CRUD(temail,tpass)
    else:
         print(colored("No Record Found!\n",'red'))
         input("Enter Any key to Return..")
         start_CRUD(temail,tpass)
#READING SPECIFIC CONTACT
def read_specific(temail,tpass):
    os.system('cls')
    temp_name=fetch_username(temail,tpass)
    print(colored('[{} logged in]','green').format(temp_name))
    printDate()
    while(True):
        email=input("Enter Email to Search: ")
        if email.count('@')==1 and email.count('.')==1:
            break
        else:
            print(colored("Invalid Email Format!\n",'red'))
    rs_script="SELECT contact_id,firstname,lastname,email,phone_no from contact WHERE email=%s and a_mail=%s and a_pass=%s"
    val=(email.lower(),temail,tpass)
    connect_db.cur.execute(rs_script,val)
    row=connect_db.cur.rowcount
    if row==0:
        print(colored("No Contact Found!",'red'))
        input("Press Any key to Return...")
        start_CRUD(temail,tpass)
    else:
        RAW_DATA=connect_db.cur.fetchall()
        print(colored("Contact Found",'green'))
        headers="ContactID","FirstName","LastName","Email","PhoneNumber"
        print(tabulate(RAW_DATA,headers,tablefmt='fancy_grid'))
        input("Press Any key to Continue...")
        start_CRUD(temail,tpass)
##ADDING NEW CONTACT###
def ADD(temail,tpss):
    os.system('cls')
    temp_name=fetch_username(temail,tpss)
    print(colored('[{} logged in]','green').format(temp_name))
    printDate()
    fname,lname=input("Enter First Name: "),input("Enter Last Name: ")
    while(True):
        email=input("Enter Email: ")
        if email.count('@')==1 and email.count('.')==1:
            break
        else:
            print(colored("Invalid Email Format!\n",'red'))
    while(True):
        try:
            phone=int(input("Enter Phone Number: "))

        except ValueError:
                 print(colored("\nPhone Number Must Be Digit!\n",'red'))
        else:
            break
    do_addition(fname,lname,email,phone,temail,tpss)
def start():
    try:
        match main_menu():
            case 1:
                Registration()
            case 2:
                Login()
            case 3:
                CLOSE_DATABASE()
                exit(0)
            case _:
                print("Invalid choice!")
                input()
                start()
    except ValueError:
        print(colored("Bad Input! press Any key...",'red'))
        input()
        start()
            #PERFORMING OPERATIONS
def start_CRUD(temail,tpass,email=None):
    os.system('cls')
    temp_name=fetch_username(temail,tpass)
    print(colored('[{} logged in]','green').format(temp_name))
    printDate()
    match second_menu():
        case 1:
            ADD(temail,tpass)
        case 2:
            get_ALL(temail,tpass)
        case 3:
            read_specific(temail,tpass)
        case 7:
            start()
        case 5:
            del_specific(temail,tpass)
        case 6:
            delete_all(temail,tpass)
        case 4:
            update_specific(temail,tpass)
#Start Program
start()
