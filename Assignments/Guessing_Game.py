from random import randint


def ask_for_num():
    while True:
        try:
            choice = int(input("Pick an integer between 1 and 100:\n"))
            if choice < 1 or choice > 100:
                print(f"{choice} is not between 1 and 100\n")
                continue
            else:
                return choice
        except ValueError:
            print("That is not an integer.\n")


def play_game():
    random_num = randint(1, 100)
    tries = 0
    while True:
        tries += 1

        if tries > 5:
            print(f"You lose. ☹\nThe correct number was {random_num}\n")
            break
        else:
            guess = ask_for_num()

        if guess == random_num:
            print("You win. ☺\n")
            break
        elif guess < random_num:
            print(f"{guess} was too low.\n")
        elif guess > random_num:
            print(f"{guess} was too high.\n")


if __name__ == "__main__":
    print("Welcome to my guessing game.\n")
    play_game()

    while True:
        play_again = input("Would you like to play again?\nY/n\n")

        if play_again not in ["y", "n", ""]:
            print("Please enter a valid input.\n")
            continue
        elif play_again == "y" or play_again == "":
            play_game()
        elif play_again == "n":
            quit()


