import socketserver

customer_tuples = []

ERR_DOES_NOT_EXIST = "Customer does not exist!"
ERR_ALREADY_EXIST = "Customer already exists!"
ERR_NOT_FOUND = "Customer not found!" 

class RequestHandler(socketserver.BaseRequestHandler):
    # helper methods
    def serialize_and_migrate(self):
        data_file = open('data.txt','w')
        for customer in customer_tuples:
            data_file.write(self.disp_customer(customer))
        data_file.close()    

    def disp_customer(self, customer):
        return "{}|{}|{}|{}|".format(customer['first_name'], customer['age'], customer['address'], customer['phone_no'])

    def filtered_and_extract(self, c_name):
        delta_list = list(filter(lambda customer: customer['first_name'] != c_name, customer_tuples))
        customer_to_update_list = list(filter(lambda customer: customer['first_name'] == c_name, customer_tuples))
        return delta_list, customer_to_update_list

    def immutably_reset(self, updated_list):
        global customer_tuples
        customer_tuples = updated_list
        self.serialize_and_migrate()

    # processing methods
    def process_find(self, arg_list):
        found_list = list(filter(lambda customer: customer['first_name'] == arg_list[0], customer_tuples))
        found_list = list(map(self.disp_customer, found_list))
        if len(found_list) > 0:
            return '\n'.join(found_list)
        else:
            return ERR_NOT_FOUND  

    def process_add(self, arg_list):
        customer_to_add = {
            "first_name" : arg_list[0].strip(),
            "age": arg_list[1].strip(),
            "address": arg_list[2].strip(),
            "phone_no": arg_list[3].strip()
        }
        if customer_to_add not in customer_tuples:
            updated_list = customer_tuples
            updated_list.append(customer_to_add)
            self.immutably_reset(updated_list)
            return "Added tuple successfully -- {}".format(self.disp_customer(customer_to_add))
        else:
            return ERR_ALREADY_EXIST   
    
    def process_delete(self, arg_list):
        found_list = list(filter(lambda customer: customer['first_name'] != arg_list[0], customer_tuples))
        if len(found_list) < len(customer_tuples):
            self.immutably_reset(found_list)
            return "Successfully Deleted Customer with name -- {}".format(arg_list[0])    
        else:
            return ERR_DOES_NOT_EXIST 

    def process_update_age(self, arg_list):
        delta_list, customer_to_update_list = self.filtered_and_extract(arg_list[0])
        customer_to_update = customer_to_update_list[0]
        if customer_to_update:
            customer_to_update['age'] = arg_list[1]
            delta_list.append(customer_to_update)
            self.immutably_reset(delta_list)
            return "Successfully Updated Age to '{}' for Customer with Name -- {}".format(arg_list[1],arg_list[0])    
        else:
            return ERR_NOT_FOUND  

    def process_update_address(self, arg_list):
        delta_list, customer_to_update_list = self.filtered_and_extract(arg_list[0])
        customer_to_update = customer_to_update_list[0]
        if customer_to_update:
            customer_to_update['address'] = arg_list[1]
            delta_list.append(customer_to_update)
            self.immutably_reset(delta_list)
            return "Successfully Updated Address to '{}' for Customer with Name -- {}".format(arg_list[1],arg_list[0])    
        else:
            return ERR_NOT_FOUND 

    def process_update_phone(self, arg_list):
        delta_list, customer_to_update_list = self.filtered_and_extract(arg_list[0])
        customer_to_update = customer_to_update_list[0]
        if customer_to_update:
            customer_to_update['phone'] = arg_list[1]
            delta_list.append(customer_to_update)
            self.immutably_reset(delta_list)
            return "Successfully Updated Phone to '{}' for Customer with Name -- {}".format(arg_list[1],arg_list[0])    
        else:
            return ERR_NOT_FOUND 

    def process_print_report(self, arg_list):
        return "\n".join(list(map(self.disp_customer, customer_tuples)))

    def parse_and_process(self):
        req = self.data.split("|")
        op = req[0]
        arg_list = req[1].split(",")
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

    customer_tuples.append({
        "first_name" : c_tuple[0].strip(),
        "age": c_tuple[1].strip(),
        "address": c_tuple[2].strip(),
        "phone_no": c_tuple[3].strip()
    })

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