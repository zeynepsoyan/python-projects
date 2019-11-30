from random import sample, shuffle

def myshuffle(str):
    l = list(str)
    shuffle(l)
    result = ''.join(l)
    return result

print("Welcome to The Game of Guesses!")
print("The purpose of the game is to guess the number I'm thinking. There are a few rules to play this game:")
print("1- The number in my mind will be a 4-digit one with different digits.")
print("2- You will see a - sign for every digit you guess correcly and a + sign if the digit is in the correct place.")
print("3- You only have 10 attempts.")
print("4- You will not lose an attempt if you enter any other value than a 4-digit one.")
print("Good luck! \n")
input("Press any key to begin. \n")

while True:
    r = sample(range(10), 4)
    if r[0] > 0:
        break

remaining = 10
while remaining > 0:
    while True:
        try:
            g = [int(i) for i in input("Guess:")]
            break
        except ValueError:
            print("Please enter a numerical value!")
            print("Remaining Attempts: %d \n" % remaining)

    a = int(''.join(str(n) for n in g))
    if a > 9999 or a < 1000:
        print("Please enter a 4-digit value!")
        print("Remaining Attempts: %d \n" % remaining)
        continue

    #print(r)
    result = ""
    for x, i in enumerate(r):
        for y, j in enumerate(g):
            if x == y and i == j:
                result += "+"
            elif x != y and i == j:
                result += "-"

    print("Result: [%s]" % myshuffle(result))
    if result == "++++":
        print("Congratulations! You have guessed the number correctly. You must be a mind-reader. \n")
        input("Press any key to exit.")
        break

    remaining -= 1
    print("Remaining Attempts: %d \n" % remaining)
else:
    print("Sorry, you couldn't guess the number correctly! The number was: %s \n" % ''.join(str(m) for m in r))
    input("Press any key to exit")