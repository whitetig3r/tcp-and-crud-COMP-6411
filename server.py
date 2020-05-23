import socketserver
import os
import sys

DATA_FILE = 'data.txt'
SEP = "$%^#"

customer_tuples = {}

ERR_DOES_NOT_EXIST = "Customer does not exist!"
ERR_ALREADY_EXIST = "Customer already exists!"
ERR_NOT_FOUND = "Customer not found!" 

class RequestHandler(socketserver.BaseRequestHandler):
    # helper methods  
    def disp_customer_pretty(self, customer):
        try:
            return "Name: {} || Age:  {} || Addr.: {} || Ph.No.: {}".format(customer['first_name'], customer['age'], customer['address'], customer['phone_no'])
        except:
            print("ERROR: FAILED TO RENDER CUSTOMER TUPLE AS UTF-8 STRING")           

    # processing methods
    def process_find(self, arg_list):
        try:
            if arg_list[0] in customer_tuples.keys():
                return self.disp_customer_pretty(customer_tuples[arg_list[0]])
            else:
                return ERR_NOT_FOUND  
        except:
            print("ERROR: FAILED TO PROCESS FIND OPERATION")        

    def process_add(self, arg_list):
        try:
            customer_to_add = {
                "first_name" : arg_list[0],
                "age": arg_list[1].strip(),
                "address": arg_list[2].strip(),
                "phone_no": arg_list[3].strip()
            }
            if arg_list[0].lower() not in customer_tuples.keys():
                customer_tuples[arg_list[0]] = customer_to_add
                return "Added tuple successfully -- {}".format(self.disp_customer_pretty(customer_to_add))
            else:
                return ERR_ALREADY_EXIST   
        except:
            print("ERROR: FAILED TO PROCESS INSERT OPERATION")        
    
    def process_delete(self, arg_list):
        try:
            if arg_list[0] in customer_tuples.keys():
                customer_tuples.pop(arg_list[0])
                return "Successfully Deleted Customer with name -- {}".format(arg_list[0])    
            else:
                return ERR_DOES_NOT_EXIST 
        except:
            print("ERROR: FAILED TO PROCESS DELETE OPERATION")        

    def process_update_age(self, arg_list):
        try:
            if arg_list[0] in customer_tuples.keys():
                customer_tuples[arg_list[0]]['age'] = arg_list[1].strip()
                return "Successfully Updated Age to '{}' for Customer with Name -- {}".format(arg_list[1].strip(),arg_list[0])    
            else:
                return ERR_NOT_FOUND  
        except:
            print("ERROR: FAILED TO PROCESS UPDATE_AGE OPERATION")        

    def process_update_address(self, arg_list):
        try:
            if arg_list[0] in customer_tuples.keys():
                customer_tuples[arg_list[0]]['address'] = arg_list[1].strip() 
                return "Successfully Updated Address to '{}' for Customer with Name -- {}".format(arg_list[1].strip(),arg_list[0])    
            else:
                return ERR_NOT_FOUND  
        except:
            print("ERROR: FAILED TO PROCESS UPDATE_ADDRESS OPERATION")        

    def process_update_phone(self, arg_list):
        try:
            if arg_list[0] in customer_tuples.keys():
                customer_tuples[arg_list[0]]['phone_no'] = arg_list[1].strip() 
                return "Successfully Updated Phone Number to '{}' for Customer with Name -- {}".format(arg_list[1].strip(),arg_list[0])    
            else:
                return ERR_NOT_FOUND  
        except:
            print("ERROR: FAILED TO PROCESS UPDATE_PHONE OPERATION")        

    def process_print_report(self, arg_list):
        try:
            customer_list = list(map(self.disp_customer_pretty, customer_tuples.values()))
            return "\n".join(sorted(customer_list))
        except:
            print("ERROR: FAILED TO PROCESS PRINT_REPORT OPERATION")    

    def parse_and_process(self):
        try:
            req = self.data.split("|")
            op = req[0]
            arg_list = req[1].split(SEP)
            arg_list[0] = arg_list[0].strip().lower()
            if (op != "print_report") and (not arg_list[0]):
                 return "ERROR: NAME CANNOT BE BLANK"
            if op == "find":
                return self.process_find(arg_list)
            elif op == "add":
                return self.process_add(arg_list)
            elif op == "delete":      
                return self.process_delete(arg_list)
            elif op == "update_age":
                return self.process_update_age(arg_list)
            elif op == "update_address":
                return self.process_update_address(arg_list)      
            elif op == "update_phone":
                return self.process_update_phone(arg_list)  
            elif op == "print_report":
                return self.process_print_report(arg_list)
            else:
                return "ERROR: UNRECOGNIZED OPERATION!"   
        except: 
            print("ERROR: BAD REQUEST MADE BY CLIENT")         

    def handle(self):
        try:
            self.data = self.request.recv(1024).strip()
            print("{} made a request!".format(self.client_address[0]))
            self.data = self.data.decode("utf-8")
            ret_message = self.parse_and_process()
            self.request.sendall(ret_message.encode("utf-8"))
        except:
            print("ERROR: FAILED TO HANDLE THE REQUEST!")    

def store_value_in_hash(c_tuple):
    try:   
        c_tuple = c_tuple.split("|")  
    
        if len(c_tuple) != 4:
            print("ERROR: BAD FORMAT FOR TUPLE! MOVING TO NEXT TUPLE...")
            return
        
        if not c_tuple[0].strip(): 
            return

        customer_tuples[c_tuple[0].strip().lower()] = {
            "first_name" : c_tuple[0].strip().lower(),
            "age": c_tuple[1].strip(),
            "address": c_tuple[2].strip(),
            "phone_no": c_tuple[3].strip()
        }
    except:
        print("ERROR: FAILED TO STORE TUPLE IN MEMORY HASH")    

def load_db():
    with open(DATA_FILE, 'r') as data_file: 
        try:
            c_tuples = data_file.readlines()
            for c_tuple in c_tuples: 
                store_value_in_hash(c_tuple.strip())  
            data_file.close()
        except OSError:
            print("ERROR: COULD NOT OPEN 'data.txt'. Ensure it exists in your path")    
            sys.exit()
        except:
            print("ERROR: UNRECOGNIZED ERROR")            

def init_server():
    HOST, PORT = "localhost", 9999

    load_db()

    try:
        with socketserver.TCPServer((HOST, PORT), RequestHandler) as server:
            print("Server is active on port 9999 ...")
            server.serve_forever()
    except KeyboardInterrupt:
        print("\nSuccessfully shutdown server!")            
    except:
        print("ERROR: INTERNAL SERVER ERROR (UNABLE TO SERVE)")        


init_server()        