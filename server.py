import socketserver
import os

customer_tuples = {}

ERR_DOES_NOT_EXIST = "Customer does not exist!"
ERR_ALREADY_EXIST = "Customer already exists!"
ERR_NOT_FOUND = "Customer not found!" 

class RequestHandler(socketserver.BaseRequestHandler):
    # helper methods
    def serialize_and_migrate(self):
        data_file = open('data.txt','w')
        for index, customer in enumerate(customer_tuples.values(), start=1):
            data_file.write(self.disp_customer(customer))
            if index != len(customer_tuples): 
                data_file.write(os.linesep)
        data_file.close()    

    def disp_customer(self, customer):
        return "{}|{}|{}|{}".format(customer['first_name'], customer['age'], customer['address'], customer['phone_no'])

    # processing methods
    def process_find(self, arg_list):
        print(customer_tuples.keys())
        if arg_list[0].strip() in customer_tuples.keys():
            return self.disp_customer(customer_tuples[arg_list[0].strip()])
        else:
            return ERR_NOT_FOUND  

    def process_add(self, arg_list):
        customer_to_add = {
            "first_name" : arg_list[0].strip(),
            "age": arg_list[1].strip(),
            "address": arg_list[2].strip(),
            "phone_no": arg_list[3].strip()
        }
        if customer_to_add['first_name'] not in customer_tuples.keys():
            customer_tuples[arg_list[0].strip()] = customer_to_add
            self.serialize_and_migrate()
            return "Added tuple successfully -- {}".format(self.disp_customer(customer_to_add))
        else:
            return ERR_ALREADY_EXIST   
    
    def process_delete(self, arg_list):
        if arg_list[0].strip() in customer_tuples.keys():
            customer_tuples.pop(arg_list[0].strip())
            self.serialize_and_migrate()
            return "Successfully Deleted Customer with name -- {}".format(arg_list[0].strip())    
        else:
            return ERR_DOES_NOT_EXIST 

    def process_update_age(self, arg_list):
        if arg_list[0].strip() in customer_tuples.keys():
            customer_tuples[arg_list[0].strip()]['age'] = arg_list[1].strip() 
            self.serialize_and_migrate()
            return "Successfully Updated Age to '{}' for Customer with Name -- {}".format(arg_list[1].strip(),arg_list[0].strip())    
        else:
            return ERR_NOT_FOUND  

    def process_update_address(self, arg_list):
        if arg_list[0].strip() in customer_tuples.keys():
            customer_tuples[arg_list[0].strip()]['address'] = arg_list[1].strip() 
            self.serialize_and_migrate()
            return "Successfully Updated Address to '{}' for Customer with Name -- {}".format(arg_list[1].strip(),arg_list[0].strip())    
        else:
            return ERR_NOT_FOUND  

    def process_update_phone(self, arg_list):
        if arg_list[0].strip() in customer_tuples.keys():
            customer_tuples[arg_list[0].strip()]['phone_no'] = arg_list[1].strip() 
            self.serialize_and_migrate()
            return "Successfully Updated Phone Number to '{}' for Customer with Name -- {}".format(arg_list[1].strip(),arg_list[0].strip())    
        else:
            return ERR_NOT_FOUND  

    def process_print_report(self, arg_list):
        return "\n".join(list(map(self.disp_customer, customer_tuples.values())))

    def parse_and_process(self):
        req = self.data.split("|")
        op = req[0]
        arg_list = req[1].split("$%^#")
        # names should be case insensitive
        arg_list[0] = arg_list[0].lower()
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
            return "ERROR: BAD OP!"    

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} requested -- :".format(self.client_address[0]))
        self.data = self.data.decode("utf-8")
        print("{}".format(self.data))
        ret_message = self.parse_and_process()
        self.request.sendall(ret_message.encode("utf-8"))

def store_value_in_hash(c_tuple):   
    c_tuple = c_tuple.split("|")  

    if not c_tuple[0].strip(): 
        return

    customer_tuples[c_tuple[0].strip().lower()] = {
        "first_name" : c_tuple[0].strip(),
        "age": c_tuple[1].strip(),
        "address": c_tuple[2].strip(),
        "phone_no": c_tuple[3].strip()
    }

def load_db():
    data_file = open('data.txt','r')
    c_tuples = data_file.readlines()
    for c_tuple in c_tuples: 
        store_value_in_hash(c_tuple.strip())  
    data_file.close()    

def init_server():
    HOST, PORT = "localhost", 9999

    load_db()

    with socketserver.TCPServer((HOST, PORT), RequestHandler) as server:
        print("Server is active on port 9999 ...")
        server.serve_forever()


init_server()        