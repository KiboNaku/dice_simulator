import pickle
import sys
from os import path, makedirs
from random import randrange as rand

import math


class Die:

    """"
    Class used to simulate rolling of a die.

    :param values: values on the die (each value represents a "face").
    :type values: sequence of any
    :param name: value used to identify the die. If no value is specified, name is defaulted to "generic die",
    meaning all unnamed dice will have the same name (NOT recommended).
    :type name: str
    """

    def __init__(self, values, name="generic die"):
        self._values = values
        self.name = name

    def roll(self):
        """
        Simulates a single die roll.

        :returns: the value rolled.
        :rtype: type contained in self._values
        """
        return self._values[rand(len(self._values))]

    def roll_multiple(self, times):
        """
        Simulates a specified number of die rolls.

        :param times: number of times to roll the die.
        :type times: int

        :return: a list of the the roll results.
        :rtype: list of type contained in self._values
        """
        rolls = []
        for _ in range(times):
            rolls.append(self.roll())
        return rolls

    def get_values(self):
        """
        :return: a separate copy of the self._values.
        :rtype: list
        """
        return list(self._values)


class NumericalDie (Die):

    """"
    Class used to simulate numerical die. Allows for mathematical operations.

    :param num_values: numerical values on the die.
    :type num_values: sequence of int
    :param name: defaults to "numerical die"
    :type name: str
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
        Simulates a specified number of die rolls. Overrides the super().roll_multiple(self, times) method by
        also returning additional values (mathematical calculations).
        Additional Values: sum, average, max, min.

        :param times: number of times to roll the die.
        :type times: int

        :return: a list of the the roll results, additional numerical calculations.
        :rtype: tuple of (list, tuple of (float, float, float, float))
        """
        rolls = super().roll_multiple(times)
        return rolls, NumericalDie._additional_values(rolls)

    @staticmethod
    def _additional_values(rolls):
        """
        Returns additional mathematical calculations for the rolls passed: sum, average, max, min.

        :param rolls: a list of the rolls.
        :type rolls: list

        :return: additional mathematical calculations: (sum, average, max, min).
        :rtype: tuple
        """
        return NumericalDie._sum(rolls), NumericalDie._average(rolls), \
               NumericalDie._max(rolls), NumericalDie._min(rolls)

    @staticmethod
    def _sum(rolls):
        """
        :param rolls: list of the dice rolls.
        :type rolls: list

        :return: sum of the values.
        :rtype: int
        """
        return sum(rolls)

    @staticmethod
    def _average(rolls):
        """
        :param rolls: list of the dice rolls.
        :type rolls: list

        :return: average of the values.
        :rtype: double
        """
        return NumericalDie._sum(rolls) / len(rolls)

    @staticmethod
    def _max(rolls):
        """
        :param rolls: list of the dice rolls.
        :type rolls: list

        :return: max of the values.
        :rtype: int
        """
        return max(rolls)

    @staticmethod
    def _min(rolls):
        """
        :param rolls: list of the dice rolls.
        :type rolls: list

        :return: min of the values.
        :rtype: int
        """
        return min(rolls)


class ClassicDie (NumericalDie):
    """"
    Simplified version of NumericalDie with values ranging from 1 to the specified max.

    :param max_val: the max values on the die. Example: enter 6 to create a die with values from 1 to 6.
    :type max_val: int
    :param name: defaults to "classical die"
    :type name: str
    """

    def __init__(self, max_val, name="classical die"):
        super().__init__(range(0, max_val + 1), name)


# constants
_back = "back"
_user_dir = "userdata"
_dice_file = "custom_dice.pickle"
_file_path = path.join(_user_dir, _dice_file)

# holds all of the dice
_all_dice = [Die(ClassicDie(spots, "D{}".format(spots))) for spots in [4, 6, 8, 10, 12, 20]]


def _print_die_values(die_obj):
    """Prints out all of the potential values of the die in a table format with "Potential Value" heading."""
    print("Potential values:")
    _print_table(die_obj.get_values())


def _print_die_summary(die_obj):
    """
    Prints out simple summary of the die.
    Name:   (name)
    Potential Values:
    (values in table format)
    """
    print("Name:\t{}".format(die_obj.name))
    _print_die_values(die_obj)


def _print_table(values, columns=5, padding=4):
    """
    Prints a list of values in table format.

    :param values: values to print.
    :type values: list
    :param columns: number of columns. Defaults to 5.
    :type columns: int
    :param padding: padding for each column (padded on the left)
    :type padding: int
    """
    val_len = len(values)

    # width is padding + length of the longest value.
    i_width = padding + len(str(val_len))
    v_width = padding + max([len(str(val)) for val in values])

    # printing the values in rows
    for row in range(int(math.ceil(val_len/columns))):
        num_index = row + columns
        num_rolls = values[row:num_index]
        print(' '.join("{:{i_width}}.  {:{v_width}}\t"
                       .format(columns * row + roll_index + 1, num_rolls[roll_index], i_width=i_width, v_width=v_width)
                       for roll_index in range(len(num_rolls))))


def _print_rolls(die_obj, rolls_list, other_info=None):
    """
    Prints the dice rolls with additional information.

    :param die_obj: the die object that was rolled.
    :type die_obj: Die
    :param rolls_list: list of the rolls.
    :type rolls_list: list
    :param other_info: additional info to display (eg the mathematical calculations returned by NumericalDie).
    if not specified, nothing is printed for this.
    :type other_info: list or tuple
    """

    # the main info
    print()
    _print_die_values(die_obj)
    _print_table(rolls_list)

    # the mathematical info
    other_labels = ["sum", "avg", "max", "min"]
    if other_info is not None:
        print("\nsimple results:\n", "\n".join("\t{}:\t{}"
                                               .format(other_labels[i], other_info[i]) for i in range(len(other_info))))

    # the frequency at which each value was rolled
    print("\nfrequency of each value:")
    print("\n".join("\t{}:\t{}".format(val, rolls_list.count(val)) for val in die_obj.get_values()))

    _print_menu_die()


# below are the "menu methods" used to help users navigate and perform what they want.

def _menu_input(input_min, input_max):
    """
    Simple method used to request a numerical input or the back command which takes them back to the previous menu.

    :param input_min: the minimum integer that can be accepted.
    :type input_min: int
    :param input_max: the maximum integer that can be accepted.
    :type input_max: int

    :return: the numerical input or "back"
    :rtype: int or str
    """
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
    """
    Simple function used to print a basic menu.

    :param options: tuple arguments that contain the menu options.
    :type options: tuple of (str, any) where str is what will be displayed to the user as the option and any is what
    will be returned if the option is chosen.
    :param back_string: option printed for the "back command". If nothing is specified, "previous menu" will be used.
    :type back_string: str

    :return: the option chosen.
    :rtype: any (what is contained in the option tuple)
    """
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
    """"
    The first menu: choose die or exit.
    """
    print("\nDice Roll Simulator")
    main_menu_input = _print_menu(("choose die", _print_menu_die), back_string="exit app")

    if main_menu_input is None:
        return

    return main_menu_input()


def _print_menu_die():
    """
    Second menu: choose die or create custom die.
    """
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


def create_custom_die():
    """simple menu used to create a custom die and write to file."""
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
    """
    ask user to input values and create the custom die.

    :return: the custom die the user specified.
    :rtype: NumericalDie
    """
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


def _print_menu_roll(current_die):
    """
    User specifies the number of rolls to roll. If successful, the rolls are printed and they are brought back to
    the _print_menu_die().

    :param current_die: the die used to roll.
    :type current_die: Die
    """
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


# initialization methods

def run():
    """used to run the program from start to finish"""
    _create_user_dir_file()
    _load_saved_dice()
    _print_menu_main()
    print("closing app...")


def _create_user_dir_file():
    """creates the directory for storing the custom dice if doesn't already exist."""
    if not path.isfile(_file_path):
        try:
            open(_file_path, 'r')
        except IOError:
            open(_file_path, 'w')

    if not path.exists(_user_dir):
        makedirs(_user_dir)


def _load_saved_dice():
    """loads the custom die that have been saved and appends them to all_dice"""
    with open(_file_path, "rb") as dice_file:
        while True:
            try:
                _all_dice.append(pickle.load(dice_file))
            except EOFError:
                break


if __name__ == "__main__":
    run()
