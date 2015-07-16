"""Menu and input utilities."""

from types import FunctionType


def repeat_input(prompt='? ', in_type=str, num_retries=-1):
    """
    Get input of a specific type, repeating on failure.

    Prompt for a specific type of input.  If the input cannot be converted to
    that type, retry the input for the specified amount of retries.  If the
    retry amount is negative, the function will retry indefinitely.  If the
    parameter is omitted, it will be supplied as -1.  If the user enters a
    blank string, this is considered a cancel sequence, and None is returned.
    Similarly, if the number of retries is exceeded, None is returned.

    :param str prompt: prompt to display each time input is requested
    :param type in_type: type or function to use to cast the input.  Should
                         raise :class:`ValueError` if input is invalid.
    :param num_retries: number of times to retry before returning.  -1 for
                        infinite.
    :returns: Input casted to ``in_type``
    """
    rv_str = input(str(prompt))  # Ask for input the first time
    rv = None
    if rv_str == '':
        return None  # Blank strings mean return None
    try:
        rv = in_type(rv_str)  # Succeeds if the input was the right type
    except ValueError:
        while rv is None and num_retries != 0:
            try:
                # Continue retrying until we get a successful conversion
                num_retries -= 1
                rv_str = input('Bad Input.  ' + str(prompt))
                if rv_str == '':
                    return None
                rv = in_type(rv_str)
            except ValueError:
                pass
    return rv


class Menu:
    """
    A class that represents command line numeric menus.

    This Menu class offers a simple menu formulation that allows programmers to
    simply define an arbitrarily large or complex sequence of menus, simply by
    supplying, the title, options+actions, and any customization options they
    wish.  Actions may be instances of the Menu class, or they may be
    functions.  Additionally, the Menu class allows you to create menus that
    re-appear after using an action.
    """

    def __init__(self, title='Main Menu', options=(), reentrant=False,
                 exit_text='Enter a blank string to exit.'):
        """
        *Constructor*

        :param title: The title to be displayed
        :param options: A list of (string, action) tuples.
        :param reentrant: Return to the menu after executing an action?
        :param exit_text: The text to display for the exit option.
        """
        self.title = str(title)
        self.options = list(options)
        self.reentrant = reentrant
        self.exit_text = str(exit_text)

    def pre_menu(self):
        """A pre-menu action for the menu."""
        print()

    def display(self):
        """Run the menu."""
        running = True
        while running:
            running = self.reentrant  # only run once if not re-entrant

            # Display the menu title and options
            self.pre_menu()
            print(self.title)
            for number, option in enumerate(self.options, start=1):
                print('  %d. %s' % (number, option[0]))
            if self.exit_text is not None:
                print(self.exit_text)
            print('')

            selection = repeat_input('Selection: ', int)
            print()

            # If they enter a blank line, we assume they want to exit
            if selection is None:
                running = False
                continue

            # Check that the input is correct.  If not, run again.
            try:
                text, action = self.options[selection - 1]
            except IndexError:
                print('The option you selected is invalid.')
                running = True
                continue

            # Perform the action!
            if type(action) is Menu:
                action.display()
            elif type(action) is FunctionType:
                action()

    def add(self, name, action):
        """
        Add an item to the menu.

        :param str name: Text to display for menu item.
        :param action: Action to perform (function or menu).
        """
        self.options.append((name, action))

    def function(self, name):
        """
        Function decorator to add directly to a menu.

        Put ``@menu.add_function('<text>')`` above a function to insert it right
        into the menu.

        :param name: The text to appear for the menu item.
        :return: A decorator that takes a function and adds it to the menu.
        """
        def decorator(f):
            self.add(name, f)
            return f
        return decorator
