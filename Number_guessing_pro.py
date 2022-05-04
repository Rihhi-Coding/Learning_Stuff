import random

score = 0       # Points scored
total_score = 0     # Total score in this session
attempts = 0        # the ammount of needed attempts
number_choice = 0       # the random number chosen
max_attempts = 0        # the max attempts, the player gets before losing
even_hint = False       # determining if player already got an hint if the number is even or not even
not_even_hint = False


def start():
    global max_attempts
    print("Tell me in which difficulty you want to play.")
    difficulty = input("Type in the number: [1] = Easy, [2] = Medium, [3] = Hard, [4] Help:")
    if int(difficulty) == 1:        # Sets number of max attempts, and the range of the randomized number
        randomize(1, 10)
        max_attempts = 3
    elif int(difficulty) == 2:
        randomize(1, 100)
        max_attempts = 5
    elif int(difficulty) == 3:
        randomize(1, 1000)
        max_attempts = 10
    elif int(difficulty) == 4:
        print("Easy is numbers between 1-10 with 3 hints"
              "Medium is numbers between 1-100 with 5 hints"
              "Hard is numbers between 1-1000 with 10 hints")
        start()
    elif int(difficulty) >= 5:
        print("There is no difficulty", difficulty, ", try again bud.")
        start()
    else:
        print("What the hell did you type?")
        start()
    play()


def randomize(num1, num2):      # randomizes between 2 numbers, depending on difficulty settings
    global number_choice
    number = int(random.randint(num1, num2))
    number_choice = number


def hint(guess):        # Gives hints to players depending on their choice
    global number_choice
    global even_hint
    global not_even_hint
    global attempts
    if number_choice % 2 == 0 and not even_hint:
        print("Its an even number")
        even_hint = True
        attempts += 1
        play()
    if number_choice % 2 != 0 and not not_even_hint:
        print("The number is not even")
        not_even_hint = True
        attempts += 1
        play()
    if guess <= number_choice:
        print("We seek for a higer number")
        attempts += 1
        play()
    elif guess >= number_choice:
        print("We seek for a lower number")
        attempts += 1
        play()


def reset_hints():      # resets even / Not even hints
    global even_hint
    global not_even_hint
    even_hint = False
    not_even_hint = False


def play():
    global attempts
    global number_choice
    global score
    global total_score
    global max_attempts
    if attempts == 0:
        guess = input("Okay! I have a number in mind. Can you guess which one?: ")
    elif attempts == max_attempts:
        print("Sadly you lost.")
        restart_question()
    else:
        guess = input("Next try! Your guess is?: ")
    if int(guess) == number_choice:
        print("Congrats! You already won!")
        attempts += 1
        print("You only needed", attempts, "attempts")
        score = 100 / attempts + 1
        score = round(score, 0)
        total_score += score
        print("Your score was increased by " + str(score) + ". You got a total score of " + str(total_score)
              + " in this seassion")
        restart_question()
    else:
        hint(int(guess))


def restart_question():         # Asking if the player wants to play again
    global attempts
    attempts = 0
    print("Do you want to play again?")
    restart = input("Write [y] = Yes : [n] = No ")
    if restart == "y":
        reset_hints()
        start()
    elif restart == "n":
        exit()
    else:
        print("You like to be different huh?")
        reset_hints()
        start()


print("Welcome friend, i heard you wanna have some guesses?")
start()
