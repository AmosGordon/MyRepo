print("Advanced Calculator Time")

# global flag for whether the user has completed on full operation
# used to determine if the user can use the previous output
flag_for_if_the_user_has_done_an_operation = False


# asks for a number
def ask_for_num(donut_worry_about_it, number):
    while True:
        try:
            return int(input(f"{donut_worry_about_it}Number {number}:\n"))
        except ValueError:
            print("\nTry again silly >:)\n")


# asks for an operator
def ask_for_operator():
    global flag_for_if_the_user_has_done_an_operation

    # adds a fifth option to the operators menu if the user has completed an operation
    if flag_for_if_the_user_has_done_an_operation:
        another_input = "Use last input: 5"
    else:
        another_input = ""

    while True:
        try:
            # prints the operations menu
            print(f"\nAddition: 1\nSubtraction: 2\nMultiplication: 3\nDivision: 4\n{another_input}")

            # takes the users operator
            value = int(input("What operator are we using today?\n"))

            # only returns 5 if on operation has already been completed
            if value == 5 and flag_for_if_the_user_has_done_an_operation:
                return value
            elif 0 < value < 5:
                return value

            # error checking
            else:
                print("Try that one again.")
        except ValueError:
            print("Try that one again.")


# uses the operators on the given numbers
def use_that_funky_boi(operator, num_one, num_two):
    if operator == 1:  # adds
        return add(num_one, num_two)
    elif operator == 2:  # subtracts
        return subtract(num_one, num_two)
    elif operator == 3:  # multiplies
        return multiply(num_one, num_two)
    elif operator == 4:  # divides
        return division(num_one, num_two)


# adds numbers
def add(a, b):
    return a + b


# subtracts numbers
def subtract(a, b):
    return a - b


# multiplies numbers
def multiply(a, b):
    return a * b


# divides numbers
def division(a, b):
    global flag_for_if_the_user_has_done_an_operation
    try:
        return a / b

    # checks for division by zero
    except ZeroDivisionError:
        print("You cannot divide by zero try again you silly goose :P")
        flag_for_if_the_user_has_done_an_operation = False
        main()


# main loop
def main():
    global flag_for_if_the_user_has_done_an_operation

    # initializes the output value
    last_output = 0

    # asks for the first operator
    operator = ask_for_operator()

    while True:
        # if the user has chosen to use the previous output, this will prompt them for a second number to use against it
        if operator == 5:
            last_output = use_that_funky_boi(ask_for_operator(), last_output, ask_for_num("New ", ""))
            print(last_output)

        # otherwise they will be asked for two new values
        else:
            num_uno = ask_for_num("", "one")
            num_dos = ask_for_num("", "two")
            last_output = use_that_funky_boi(operator, num_uno, num_dos)
            print(last_output)

        # sets the global flag to True after one operation
        flag_for_if_the_user_has_done_an_operation = True
        operator = ask_for_operator()


# checks if this is the main file
if __name__ == "__main__":

    # calls the main function
    main()
