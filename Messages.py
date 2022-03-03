# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000

# Audrey Nguyen
# audrehn3@uci.edu
# 50253773

# ui.py
# Contains UI elements, specifically messages.

class Message:
    '''
    Contains the program's menus. 
    AUTHOR: Audrey Nguyen's ui.py module. 
    '''
    # message1
    main_menu: str = ("How would you like to start?\n\n"
                    "   C: Create a new Profile\n"
                    "   O: Open an existing Profile\n"
    )
    # message2
    home: str = ("What would you like to do next?\n\n"
                    "   C: Create a new Profile\n"
                    "   O: Open an existing Profile\n"
                    "   E: Edit an existing Profile\n"
                    "   A: Add a post\n"
                    "   D: Delete a post\n"
                    "   P: Print\n"
                    "   X: Post\n"
                    "   Q: Quit\n"
    )
    # message3
    edit: str = ("What would you like to edit?\n\n"
                    "   U: Username\n"
                    "   P: Password\n"
                    "   B: Bio\n"
                    "   S: Server\n"
    )
    # message4
    print: str = ("What would you like to print?\n\n"
                    "   S: Server\n"
                    "   U: Username\n"
                    "   P: Password\n"
                    "   B: Bio\n"
                    "   X: All posts\n"
                    "   Y: One post\n"
                    "   A: All content\n"
    )