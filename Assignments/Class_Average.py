import os
accepted_grades = ["a", "b", "c", "d", "f"]
classes_list = []


def menu():
    print("\nClass Manager:\n"
          "Create New Class:----------|1\n"
          "Add Student to Class:------|2\n"
          "Change Student's Grade:----|3\n"
          "Remove Student:------------|4\n"
          "Calculate Class Average:---|5\n"
          "Print Grades:--------------|6\n"
          "Exit Program:--------------|7\n")


def print_classes(class_list):
    print("Classes:")
    for classes in class_list:
        print(f"{classes.class_name}")


def check_for_number(question, response):
    while True:
        try:
            number = int(input(f"{question}\n"))
            return number
        except ValueError:
            print(response)


def get_task():
    while True:
        try:
            task = int(input("What do you want to do?\n"))
            if task in range(1, 8):
                return task
            else:
                continue
        except ValueError:
            print("Please use a number.\n")


def ask_for_grade(new=""):
    while True:
        catch = input(f"{new}Grade:\n").lower()
        if catch in accepted_grades:
            return catch
        else:
            print("Please input A, B, C, D, or F\n")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class ClassRoster:
    def __init__(self, class_name):
        self.class_name = class_name
        self.student = []
        self.grade = []

    def add_grades(self):
        if len(self.student) > 0:
            while True:
                name = str(input("\nStudents Name:\n"))
                if name in self.student:
                    print("This student is already in the class.\n")
                    continue
                else:
                    self.student.append(name)
                    self.grade.append(ask_for_grade())
                    break
        else:
            self.student.append(str(input("\nStudents Name:\n")))
            self.grade.append(ask_for_grade())

    def change_grades(self):
        if len(self.student) < 1:
            print("There are no students in this class.\n")
            return
        else:
            clear()
            print("Students:")
            for students in self.student:
                print(students)
            print("")
            while True:
                student = input("What is the student's name?\n")
                if student in self.student:
                    clear()
                    self.grade[self.student.index(student)] = ask_for_grade(new="New ")
                    break
                else:
                    print("That student is not in this class.\n")

    def remove_student(self):
        if len(self.student) < 1:
            print("There are no students in this class.\n")
        else:
            print("\nStudents:")
            for students in self.student:
                print(students)
            while True:
                student = input("What is the student's name?\n")
                if student in self.student:
                    clear()
                    del self.grade[self.student.index(student)]
                    del self.student[self.student.index(student)]
                    break
                else:
                    print("That student is not in this class.\n")

    def calculate_class_average(self):
        grade_sum = 0
        if len(self.grade) < 1:
            print("There are no students in this class.")
            return
        for j in self.grade:
            if j == "a":
                grade_sum += 4
            elif j == "b":
                grade_sum += 3
            elif j == "c":
                grade_sum += 2
            elif j == "d":
                grade_sum += 1
            elif j == "f":
                grade_sum += 0
        clear()
        print(f"\nGPA: {grade_sum/len(self.grade)}")

    def print_grades(self):
        clear()
        print(f"{self.class_name} Grades")
        for students in self.student:
            print(f"{students}: {self.grade[self.student.index(students)].upper()}")


if __name__ == "__main__":

    while True:
        menu()

        option = get_task()

        if option == 1:
            while True:
                exists = False
                clear()
                current_class = ClassRoster(input("Class Name:\n"))
                for i in classes_list:
                    if i.class_name == current_class.class_name:
                        print("That class already exists.")
                        exists = True
                if exists:
                    continue
                else:
                    break
            if len(classes_list) > 1:
                for i in classes_list:
                    if i.class_name == current_class.class_name:
                        pass
                    else:
                        classes_list.append(current_class)
                        num_students = check_for_number("How many students are there:", "Please use a number.")
                        for _ in range(num_students):
                            current_class.add_grades()
            else:
                classes_list.append(current_class)
                num_students = check_for_number("How many students are there:", "Please use a number.")
                for _ in range(num_students):
                    current_class.add_grades()
            clear()

        elif option == 2:
            if len(classes_list) > 0:
                clear()
                print_classes(classes_list)
                print("")
                current_class = input("Class Name:\n")
                for i in classes_list:
                    if i.class_name == current_class:
                        i.add_grades()
                    else:
                        print("There is no class with that name.")
                        pass
                clear()
            else:
                clear()
                print("There are no classes yet.")

        elif option == 3:
            if len(classes_list) > 0:
                clear()
                print_classes(classes_list)
                print("")
                current_class = input("Class Name:\n")
                for i in classes_list:
                    if i.class_name == current_class:
                        i.change_grades()
                    else:
                        print("There is no class with that name.")
                clear()
            else:
                clear()
                print("There are no classes yet.")

        elif option == 4:
            if len(classes_list) > 0:
                clear()
                print_classes(classes_list)
                print("")
                current_class = input("Class Name:\n")
                for i in classes_list:
                    if i.class_name == current_class:
                        i.remove_student()
                    else:
                        clear()
                        print("There is no class with that name.")
            else:
                clear()
                print("There are no classes yet.")

        elif option == 5:
            if len(classes_list) > 0:
                clear()
                print_classes(classes_list)
                print("")
                current_class = input("Class Name:\n")
                for i in classes_list:
                    if i.class_name == current_class:
                        i.calculate_class_average()
                    else:
                        clear()
                        print("There is no class with that name.")
            else:
                clear()
                print("There are no classes yet.")

        elif option == 6:
            print_classes(classes_list)
            print("")
            if len(classes_list) > 0:
                current_class = input("Class Name:\n")
                for i in classes_list:
                    if i.class_name == current_class:
                        i.print_grades()
                    else:
                        print("There is no class with that name.")
            else:
                print("There are no classes yet.")

        elif option == 7:
            quit()
