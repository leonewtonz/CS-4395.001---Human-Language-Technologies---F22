# Homework1: Text Processing with Python


import sys
import os
import re
import pickle

class Person:

    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("\nEmployee id: ", self.id)
        print("\t", self.first, self.mi, self.last)
        print("\t", self.phone)


def text_processing(raw_text):
    lines = raw_text.splitlines(True)
    data = [lines[i] for i in range(1, len(lines))]
    employee_list = {}  # create a dict of employees
    for person in data:
        last, first, mi, id, phone = person.split(',')

        last = last.capitalize()

        first = first.capitalize()

        if mi != '':
            mi = mi.capitalize()
        else:
            mi = 'X'

        while True:
            if len(id) == 6 and id[:2].isalpha() and id[2:].isnumeric():
                break
            else:
                print('ID invalid: ', id)
                print('ID is two letters followed by 4 digits')
                id = input('Please enter a valid id: ')
                id = id[:2].upper() + id[2:]  # auto convert first 2 characters to upper case

        ## might need to work on force user to input correct phone format

        phone = re.sub(r'\D', '', phone)  # get rid of non-digit chars
        assert (len(phone) == 10)
        phone = f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"

        employee = Person(last, first, mi, id, phone)
        id_list = employee_list.keys()
        # print('ID List: ', id_list)  #debug
        if id in id_list:
            print('ID:', id, 'is duplicate')
        else:
            employee_list.update({id: employee})
    return employee_list


def main():
    # Method to handle the filepath in both Window and Mac
    def read_file(filepath):
        with open(os.path.join(os.getcwd(), filepath), 'r') as f:
            input_file = f.read()
        # print(text_in) #debug
        return input_file

    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        text_in = read_file(fp)
        employees = text_processing(text_in)

        # save the pickle file
        pickle.dump(employees, open('employees.p', 'wb'))  # write binary

        # read the pickle file
        employees = pickle.load(open('employees.p', 'rb'))  # read binary

        print('\nEmployee list: ')
        for e in employees.values():
            e.display()



if __name__ == "__main__":
    main()

# Some commentary:
# the Python interpreter sets the __name__ variable to __main__ if it is a standalone program
# otherwise it sets __name__ to the name of the module
# so if you run this script like this: python3 main_example.py
#    then all of the code at indentation level 0 gets executed,
#    including the above 'if' which calls main()
