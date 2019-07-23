
from random import randrange
import sys
import math


class Dice:

    def __init__(self, max_spots):
        self.max_spots = max_spots if max_spots >= 1 else 1

    def roll(self):
        return [randrange(self.max_spots) + 1]

    def roll_multiple(self, times):
        rolls = []
        for _ in range(times):
            rolls += self.roll()
        return rolls

    def get_max_spots(self):
        return self.max_spots


basic_die = {"D{}".format(spots): Dice(spots) for spots in [4, 6, 8, 10, 12, 20]}
back = 0


def integer_input(valid_min, valid_max):
    while True:
        try:
            int_input = int(input())
        except ValueError:
            print("enter a number please")
            continue
        else:
            if valid_min <= int_input <= valid_max:
                return int_input
            print("invalid number")


def print_dice_range(dice):
    print("\npotential values: 1-{}\n".format(dice.get_max_spots()))


def print_rolls(dice, rolls_list):
    padding = 4
    num_columns = 5
    length = len(rolls_list)

    print_dice_range(dice)

    for index in range(int(math.ceil(length/num_columns))):
        num_index = index + num_columns
        num_rolls = rolls_list[index:num_index]
        width = padding + len(str(length))
        print(' '.join("{:{width}}.  {}\t".format(num_columns * index + roll_index + 1, num_rolls[roll_index],
                                                  width=width) for roll_index in range(len(num_rolls))))
    print()
    total = sum(rolls_list)
    average = total / length
    largest = max(rolls_list)
    smallest = min(rolls_list)
    print("""
    simple results:
    
    sum:\t{}
    average:\t{}
    max:\t{}
    min:\t{}
    """.format(total, average, largest, smallest))

    print_menu_dice()


def print_menu(options):
    options_size = len(options)
    options_list = list(options)
    print()
    print("{}.\tBACK".format(back))
    for i in range(options_size):
        print("{}.\t{}".format(i+1, options_list[i]))
    print()
    menu_option = integer_input(0, options_size)
    option_chosen = None if menu_option == 0 else list(options.values())[menu_option - 1]
    return option_chosen


def print_menu_main():
    main_menu_input = print_menu({
        "choose dice":  print_menu_dice
    })

    if main_menu_input is None:
        return

    current_dice = main_menu_input()
    if current_dice is None:
        print("unknown error occurred...")
        return

    return print_menu_roll(current_dice)


def print_menu_dice():
    print()
    print("Please choose of the following dice:")
    dice = print_menu(basic_die)
    if dice is None:
        return print_menu_main()
    elif type(dice) is Dice:
        return dice
    print("Something unexpected happened...\n"
          "Please try again\n")
    return print_menu_dice()


def print_menu_roll(current_dice):
    print_dice_range(current_dice)
    num_rolls = print_menu({
        "roll once":        1,
        "roll multiple":    (-1),
    })

    rolls = None
    if num_rolls is None:
        return print_menu_dice()
    elif num_rolls == 1:
        rolls = current_dice.roll()
    elif num_rolls == -1:
        rolls = current_dice.roll_multiple(print_menu_roll_multiple())
    if rolls is None:
        print("sorry something unexpected happened with the rolls.\n"
              "please try again\n")
        return print_menu_roll(current_dice)
    return print_rolls(current_dice, rolls)


def print_menu_roll_multiple():
    global back
    min_rolls = 1
    back = min_rolls - 1
    print("how many times? ({} to {} times)\n"
          "enter {} to go back".format(min_rolls, sys.maxsize, back))
    return integer_input(back, sys.maxsize)


def run():
    print("\nDice Roll Simulator\n")
    print_menu_main()
    print("closing app...")


if __name__ == "__main__":
    run()
