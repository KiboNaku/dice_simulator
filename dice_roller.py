
from random import randrange as rand
import sys
import math


class Die:

    """"
    Class used to simulate rolling of a die.

    :param values: values on the die (each value represents a "face").
    :type values: sequence of any.
    """
    def __init__(self, values):
        self._values = values

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
    def __init__(self, num_values):
        """
        :raises: "ValueError": a value in the sequence passed is not of int type.
        """
        for num in num_values:
            if type(num) is not int:
                raise ValueError("Each of the value passed to the NumericalDie must be an integer value.")
        super().__init__(num_values)

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

    def __init__(self, max_val):
        super().__init__(range(0, max_val+1))


_all_dice = {"D{}".format(spots): ClassicDie(spots) for spots in [4, 6, 8, 10, 12, 20]}
_back = "back"


def _print_die_values(die):
    print("Potential values:")
    print(", ".join(str(val) for val in die.get_values()))


def _print_table(values, columns=5, padding=4):
    val_len = len(values)
    width = padding + len(str(val_len))
    for row in range(int(math.ceil(val_len/columns))):
        num_index = row + columns
        num_rolls = values[row:num_index]
        print(' '.join("{:{width}}.  {}\t".format(columns * row + roll_index + 1, num_rolls[roll_index],
                                                  width=width) for roll_index in range(len(num_rolls))))


def _print_rolls(die, rolls_list, other_info):
    print()
    _print_die_values(die)

    print()
    _print_table(rolls_list)

    other_labels = ["sum", "avg", "max", "min"]
    print("\nsimple results:\n", "\n".join("\t{}:\t{}"
                                           .format(other_labels[i], other_info[i]) for i in range(len(other_info))))

    print("\nfrequency of each value:")
    print("\n".join("\t{}:\t{}".format(val, rolls_list.count(val)) for val in die.get_values()))

    _print_menu_die()


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


def _print_menu(options, back_string="previous menu"):
    option_format = "{:<8}{}"
    options_size = len(options)
    options_list = list(options)

    print(option_format.format("INPUT", "OPTION") + "\n")

    print("\n".join(option_format.format(i+1, options_list[i]) for i in range(options_size)))
    print(option_format.format(_back, back_string))
    print("\n")

    menu_option = _menu_input(1, options_size)
    return None if menu_option == _back else list(options.values())[menu_option - 1]


def _print_menu_main():
    print("\nDice Roll Simulator")
    main_menu_input = _print_menu({
        "choose die":  _print_menu_die
    }, "exit app")

    if main_menu_input is None:
        return

    return main_menu_input()


def _print_menu_die():
    print("\n")
    print("Please choose of the following dice:")
    die = _print_menu(_all_dice)
    if die is None:
        return _print_menu_main()
    elif isinstance(die, Die):
        return _print_menu_roll(die)
    else:
        print("Something unexpected happened...unable to choose die\nPlease try again\n")
    return _print_menu_die()


def _print_menu_roll(current_die):
    _print_die_values(current_die)
    while True:
        try:
            num_rolls = int(_print_menu_roll_multiple())
            break
        except TypeError:
            print("Invalid value.")
    rolls = current_die.roll_multiple(num_rolls)
    if rolls is None:
        print("sorry something unexpected happened with the rolls.\n"
              "please try again\n")
        return _print_menu_roll(current_die)
    return _print_rolls(current_die, rolls[0], rolls[1])


def _print_menu_roll_multiple():
    global _back
    min_rolls = 1
    print("how many times? ({} to {} times)\n"
          "enter {} to go back".format(min_rolls, sys.maxsize, _back))

    num_input = _menu_input(1, sys.maxsize)
    return _print_menu_die() if num_input == _back else num_input


def run():
    _print_menu_main()
    print("closing app...")


def custom_numerical_die():
    print("Please enter a list of values separated by commas.")
    print("Example: '1,2,3,4,5,6,7' --> ['1','2','3','4','5','6','7']")
    values_input = input().split(',')
    num_values = []
    invalid_values = []
    for val in values_input:
        try:
            num_values.append(int(val))
        except ValueError:
            invalid_values.append(val)
    print("Values added to die: {}".format(num_values))
    print("Invalid values that failed to add: {}".format(invalid_values))
    name = input("Please enter a name for the die:\n")
    return name, num_values


if __name__ == "__main__":
    run()