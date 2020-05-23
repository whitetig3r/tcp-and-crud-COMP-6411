import socket

HOST = "localhost"
PORT = 9999
SEP = "$%^#"

# network helper
def make_request(params = "print_report|"):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(bytes(params + "\n", "utf-8"))
            received = str(sock.recv(1024), "utf-8")
            print("\n-- Server Replied with -- \n")
            print(received)
            print("\n-- END OF RESPONSE --")
    except:
        print("ERROR: NETWORK ERROR! FAILED TO MAKE REQUEST.")        

# input helpers
def safe_input(prompt):
    try:
        while(True):
            inp = input(prompt)       
            if (SEP in inp) or ('|' in inp):
                print('ERROR: Input cannot contain the special characters %s or | as a substring'%(SEP))
            else:
                return inp
    except:
        print("ERROR: FAILED TO TAKE INPUT!")        

def get_age_input():
    try: 
        while(True):
            c_age = safe_input("Enter a valid age:").strip()
            if (not c_age) or (c_age.isdigit() and int(c_age) < 150):
                return c_age
            else:
                print("ERROR: Age is not a number OR age is too large")
    except:
        print("ERROR: FAILED TO TAKE AGE INPUT!")       

def get_name_input(op):
    try: 
        while(True):
            c_name = safe_input("Enter name of customer to %s:"%(op)).strip() 
            if c_name:
                return c_name
            else:
                print("ERROR: Name cannot be blank")
    except:
        print("ERROR: FAILED TO TAKE NAME INPUT!")            

# core processing methods
def c_find():
    try:
        c_name = get_name_input("find")
        make_request("find|"+c_name)
    except:
        print("ERROR: FAILED TO PROCESS FIND")        

def c_add():
    try:
        c_name = get_name_input("add")
        c_age = get_age_input()
        c_address = safe_input("Enter address:").strip()
        c_phone = safe_input("Enter phone:").strip()
        make_request("add|"+SEP.join([c_name,c_age,c_address,c_phone]))
    except:
        print("ERROR: FAILED TO PROCESS INSERT")        

def c_delete():
    try:
        c_name = get_name_input("delete")
        make_request("delete|"+c_name)
    except:
        print("ERROR: FAILED TO PROCESS DELETE")        

def c_update_age():
    try:
        c_name = get_name_input("update")
        c_age = get_age_input()
        make_request("update_age|"+SEP.join([c_name,c_age]))
    except:
        print("ERROR: FAILED TO PROCESS UPDATE AGE")        

def c_update_address():
    try:
        c_name = get_name_input("update")
        c_address = safe_input("Enter updated address:").strip()
        make_request("update_address|"+SEP.join([c_name,c_address]))
    except:
        print("ERROR: FAILED TO PROCESS UPDATE ADDRESS")        

def c_update_phone():
    try:
        c_name = get_name_input("update")
        c_phone = safe_input("Enter updated phone:").strip()
        make_request("update_phone|"+SEP.join([c_name,c_phone]))
    except:
        print("ERROR: FAILED TO PROCESS UPDATE PHONE")

def c_print_report():
    try:
        make_request()
    except:
        print("ERROR: FAILED TO PROCESS PRINT REPORT")        
               
# main loop and vars
MENU_STRING = """

1. Find customer 
2. Add customer
3. Delete customer 
4. Update customer age
5. Update customer address
6. Update customer phone
7. Print report 
8. Exit

"""

print ("Python DB Menu")

try:
    while(True):
        print(MENU_STRING)
        selected_option = input("Select:").strip()
        
        if not selected_option.isdigit():
            print("ERROR: INVALID OPTION ENTERED!")
            continue
        else:
            selected_option = int(selected_option)

        if selected_option == 1:
            c_find()
        elif selected_option == 2:
            c_add()  
        elif selected_option == 3:
            c_delete() 
        elif selected_option == 4:
            c_update_age()
        elif selected_option == 5:
            c_update_address()
        elif selected_option == 6:
            c_update_phone()
        elif selected_option == 7:
            c_print_report()
        elif selected_option == 8:
            print("Good bye!")
            break 
        else:
            print("Please Enter a valid option!")                           
except:                        
    print("ERROR: UNRECOGNIZED ERROR!")