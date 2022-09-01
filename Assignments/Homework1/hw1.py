# Homework1: Text Processing with Python

 
import sys  # to get the system parameter
import os # to process the filepath


class Person:

    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("\n Employee id: ", self.id)
        print("\t", self.first, self.mi, self.last)
        print("\t", self.phone)


def text_processing(raw_text):
    lines = raw_text.splitlines(True)
    data = [lines[i] for i in range(1, len(lines))]
    employee_list = []
    for person in data:
        last, first, mi, id, phone = person.split(',')
        employee = Person(last, first, mi, id, phone)
        employee_list.append(employee)

    print('\nTest text_processing: \n')
    for e in employee_list:
        e.display()


def main():
    # Method to handle the filepath in both Window and Mac
    def method1(filepath):
        print("\nUsing method 1")

        with open(os.path.join(os.getcwd(), filepath), 'r') as f:
            text_in = f.read()
        print(text_in)
        text_processing(text_in)

    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        method1(fp)


if __name__ == "__main__":
    main()

# Some commentary:
# the Python interpreter sets the __name__ variable to __main__ if it is a standalone program
# otherwise it sets __name__ to the name of the module
# so if you run this script like this: python3 main_example.py
#    then all of the code at indentation level 0 gets executed,
#    including the above 'if' which calls main()