import pickle
import sys
from os import path, makedirs
from random import randrange as rand

import math


class Die:

    """"
    Class used to simulate rolling of a die.

    :param values: values on the die (each value represents a "face").
    :type values: sequence of any.
    """

    def __init__(self, values, name="generic die"):
        self._values = values
        self.name = name

    def roll(self):
        """
        Simulates a single die roll.

        :returns: the value rolled.
        :rtype: type contained in self._values.
        """
        return self._values[rand(len(self._values))]

    def roll_multiple(self, times):
        """
        Simulates a specified number of die rolls.

        :param times: number of times to roll the die.
        :type times: int

        :return: a list of the the roll results.
        :rtype: list of type contained in self._values.
        """
        rolls = []
        for _ in range(times):
            rolls.append(self.roll())
        return rolls

    def get_values(self):
        return list(self._values)


class NumericalDie (Die):

    """"
    Class used to simulate numerical die. Allows for mathematical operations.

    :param num_values: numerical values on the die.
    :type num_values: sequence of int.
    """

    def __init__(self, num_values, name="numerical die"):
        """
        :raises: "ValueError": a value in the sequence passed is not of int type.
        """
        for num in num_values:
            if type(num) is not int:
                raise ValueError("Each of the value passed to the NumericalDie must be an integer value.")
        super().__init__(num_values, name)

    def roll_multiple(self, times):
        """
        Simulates a specified number of die rolls.

        :param times: number of times to roll the die.
        :type times: int

        :return: a list of the the roll results, additional numerical calculations
        :rtype: tuple of (list, tuple of (float, float, float, float))
        """
        rolls = super().roll_multiple(times)
        return rolls, NumericalDie._additional_values(rolls)

    @staticmethod
    def _additional_values(rolls):
        """
        Returns additional mathematical calculations for the rolls passed
        :param rolls: a list of the rolls
        :return:
        """
        return NumericalDie._sum(rolls), NumericalDie._average(rolls), \
               NumericalDie._max(rolls), NumericalDie._min(rolls)

    @staticmethod
    def _sum(rolls):
        """"returns"""
        val_sum = 0
        for num in rolls:
            val_sum += num
        return val_sum

    @staticmethod
    def _average(rolls):
        return NumericalDie._sum(rolls) / len(rolls)

    @staticmethod
    def _max(rolls):
        return max(rolls)

    @staticmethod
    def _min(rolls):
        return min(rolls)


class ClassicDie (NumericalDie):

    def __init__(self, max_val, name="classical dice"):
        super().__init__(range(0, max_val + 1), name)


_all_dice = [ClassicDie(spots, "D{}".format(spots)) for spots in [4, 6, 8, 10, 12, 20]]
_back = "back"
_user_dir = "userdata"
_dice_file = "custom_dice.pickle"
_file_path = path.join(_user_dir, _dice_file)


def _print_die_summary(die_obj):
    print("Name:\t{}".format(die_obj.name))
    _print_die_values(die_obj)


def _print_die_values(die_obj):
    print("Potential values:")
    print(", ".join(str(val) for val in die_obj.get_values()))


def _print_table(values, columns=5, padding=4):
    val_len = len(values)
    index_width = padding + len(str(val_len))
    value_width = padding + max([len(str(val)) for val in values])
    for row in range(int(math.ceil(val_len/columns))):
        num_index = row + columns
        num_rolls = values[row:num_index]
        print(' '.join("{:{i_width}}.  {:{v_width}}\t".format(columns * row + roll_index + 1, num_rolls[roll_index],
                                                              i_width=index_width, v_width=value_width)
                       for roll_index in range(len(num_rolls))))


def _print_rolls(die_obj, rolls_list, other_info):
    print()
    _print_die_values(die_obj)

    _print_table(rolls_list)

    other_labels = ["sum", "avg", "max", "min"]
    print("\nsimple results:\n", "\n".join("\t{}:\t{}"
                                           .format(other_labels[i], other_info[i]) for i in range(len(other_info))))

    print("\nfrequency of each value:")
    print("\n".join("\t{}:\t{}".format(val, rolls_list.count(val)) for val in die_obj.get_values()))

    _print_menu_die()


# menu methods

def _menu_input(input_min, input_max):
    input_error = "Integer Input Error:"
    input_val = input()
    try:
        input_int = int(input_val)
    except ValueError:
        if input_val.lower() == _back:
            return _back
    else:
        if input_min <= input_int <= input_max:
            return input_int
        print(input_error, "invalid input.")
        return _menu_input(input_min, input_max)


def _print_menu(*options, back_string="previous menu"):
    option_format = "{:<8}{}"
    options_size = len(options)

    # prints heading: "INPUT    OPTION"
    print(option_format.format("INPUT", "OPTION") + "\n")

    # prints the options for the menu
    print("\n".join(option_format.format(i + 1, options[i][0]) for i in range(options_size)))
    print(option_format.format(_back, back_string))
    print("\n")

    menu_option = _menu_input(1, options_size)
    return None if menu_option == _back else options[menu_option - 1][1]


def _print_menu_main():
    print("\nDice Roll Simulator")
    main_menu_input = _print_menu(("choose die", _print_menu_die), back_string="exit app")

    if main_menu_input is None:
        return

    return main_menu_input()


def _print_menu_die():
    print("\n")
    print("Please choose of the following dice:")
    selected_die = _print_menu(*[(dice.name, dice) for dice in _all_dice], ("create custom die", create_custom_die))
    if selected_die is None:
        return _print_menu_main()
    elif isinstance(selected_die, Die):
        return _print_menu_roll(selected_die)
    else:
        create_custom_die()
    return _print_menu_die()


def _print_menu_roll(current_die):
    _print_die_values(current_die)

    while True:
        print("how many times? ({} to {} times)\n"
              "enter {} to go back".format(1, sys.maxsize, _back))

        num_input = _menu_input(1, sys.maxsize)
        try:
            num_rolls = int(num_input)
            break
        except TypeError:
            if num_input == _back:
                return _print_menu_die()
            print("Invalid value.")

    rolls = current_die.roll_multiple(num_rolls)
    if rolls is None:
        print("sorry something unexpected happened with the rolls.\n"
              "please try again\n")
        return _print_menu_roll(current_die)
    return _print_rolls(current_die, rolls[0], rolls[1])


def run():
    _create_user_dir_file()
    _load_saved_dice()
    _print_menu_main()
    print("closing app...")


def create_custom_die():
    custom_die = custom_numerical_die()
    _print_die_summary(custom_die)
    while True:
        verify_die = input("\n\ncontinue with these values? y or n\n").lower()
        if verify_die == "n":
            return create_custom_die()
        elif verify_die == "y":
            break
        print("Please enter y or n")
    with open(_file_path, "ab") as dice_file:
        pickle.dump(custom_die, dice_file)
    _all_dice.append(custom_die)


def custom_numerical_die():
    print("Please enter a list of numerical values separated by commas (spaces ok).")
    print("Example 1: '1,2,3,4,5,6,7' --> [1,2,3,4,5,6,7]")
    print("Example 2: '1, 2 , 3, 4, 5, 6, 7' --> [1,2,3,4,5,6,7]\n")
    values_input = input().replace(" ", "").split(',')
    num_values = []
    invalid_values = []
    for val in values_input:
        try:
            num_values.append(int(val))
        except ValueError:
            invalid_values.append(val)
    if len(num_values) > 0:
        print("Values added to die: ")
        _print_table(num_values)
    else:
        print("No values was added to die.\nTry again")
        return custom_numerical_die()
    if len(invalid_values) > 0:
        print("Invalid values that failed to add: ")
        _print_table(invalid_values)
    else:
        print("All values was added properly")
    name = input("Please enter a name for the die:\n")
    return NumericalDie(num_values, name)


def _create_user_dir_file():
    if not path.isfile(_file_path):
        try:
            open(_file_path, 'r')
        except IOError:
            open(_file_path, 'w')

    if not path.exists(_user_dir):
        makedirs(_user_dir)


def _load_saved_dice():
    with open(_file_path, "rb") as dice_file:
        while True:
            try:
                _all_dice.append(pickle.load(dice_file))
            except EOFError:
                break


if __name__ == "__main__":
    run()
