import socket

HOST = "localhost"
PORT = 9999
SEP = "$%^#"

def make_request(params = "print_report|"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(params + "\n", "utf-8"))
        received = str(sock.recv(1024), "utf-8")
        print("Received:")
        print(received)

def c_find():
    c_name = input("Enter name of customer to find:").strip()
    make_request("find|"+c_name)

def c_add():
    c_name = input("Enter first name:").strip()
    c_age = input("Enter age:").strip()
    c_address = input("Enter address:").strip()
    c_phone = input("Enter phone:").strip()
    make_request("add|"+SEP.join([c_name,c_age,c_address,c_phone]))

def c_delete():
    c_name = input("Enter name of customer to delete:").strip()
    make_request("delete|"+c_name)

def c_update_age():
    c_name = input("Enter name of customer to update:").strip()
    c_age = input("Enter updated age:").strip()
    make_request("update_age|"+SEP.join([c_name,c_age]))

def c_update_address():
    c_name = input("Enter name of customer to update:").strip()
    c_address = input("Enter updated address:").strip()
    make_request("update_address|"+SEP.join([c_name,c_address]))

def c_update_phone():
    c_name = input("Enter name of customer to update:").strip()
    c_phone = input("Enter updated phone:").strip()
    make_request("update_phone|"+SEP.join([c_name,c_phone]))

def c_print_report():
    make_request()
               
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

while(True):
    print(MENU_STRING)
    selected_option = int(input("Select:").strip())
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