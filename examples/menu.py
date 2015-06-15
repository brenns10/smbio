from smbio.util.menu import Menu

# "Declare" your menus.
main_menu = Menu('Welcome to the show!', reentrant=True)
sub_menu = Menu('The cool submenu.')
# Add menus as submenus easily.
main_menu.add('Cool stuff', sub_menu)


# Annotate which menu a function belongs to, and what its text should be.
@main_menu.function('An option')
def pzip_test():
    print('An option')


@main_menu.function('A better option')
def something_else():
    print('A better option')


@sub_menu.function('A cool option')
def cool1():
    print('being cool')


@sub_menu.function('A cooler option')
def cool2():
    print('being cooler')


# Then, just have the menu display when you'd like.
if __name__ == '__main__':
    main_menu.display()
