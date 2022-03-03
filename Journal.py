# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000

# Audrey Nguyen
# audrehn3@uci.edu
# 50253773

# Journal.py
# Journal contains program features from A2, involving DSU profiles.

from pathlib import Path
from Profile import Profile, Post
from ds_client import send

class Journal:
    '''
    Contains the program's main commands and functions. 
    Structured similarly to John Daniel's 'Program' object in his A2.py module. 
    Functions included are modified from Audrey Nguyen's A2.py module. 
    '''

    IP = ''
    port = 3021

    def create_dsu(path:str, profile:str, username:str, password:str, bio:str) -> None:
        '''
        Creates a profile using the Profile module, collects user information.
        
        :param path: The location of the user's '.dsu' file.
        :param profile: The file name of the user's profifle.
        :param username: Username
        :param password: Password
        :param bio: Biography
        '''
        
        # Create file.
        new_file = f'{profile}.dsu'
        p = Path(path)
        p = p / new_file
        if not p.exists():
            p.touch()
        else:
            # If the profile exists, load the command.
            Journal.open_dsu(p)

        # Populate and save Profile.
        Journal.IP = input("What server would you like this profile to be stored on? ")
        prf = Profile()
        prf.dsuserver = Journal.IP
        prf.username = username
        prf.password = password
        prf.bio = bio
        prf.save_profile(p)

        return Journal.IP, p

    def open_dsu(profile:str) -> tuple:                    
        ''' 
        Opens a profile using the Profile module.
        :param profile: profile path collected from user
        '''
        # Initalize user profile.
        prf = Profile()
        prf.load_profile(profile)
        
        # Check if IP 
        if prf.dsuserver == None:
            Journal.IP = input("What server would you like this profile to be posted to? ")
        else:
            Journal.IP = prf.dsuserver
        
        prf.save_profile(profile)

        return Journal.IP, prf.username, prf.password, prf.bio

    def edit_dsu(prf:Profile, profile:str, option:str, value:str) -> None:
        '''
        Edit updates the values within a profile.
        
        :param prf: Profile() object
        :param profile: User directory of '.dsu' file.
        :param option: Edit option collected from user.
        :param value: New value to be edited to.
        '''

        boolean = None

        # Updates a user's profile, based on an option.
        if option == 'U':
            prf.username = value
        elif option == 'P':
            prf.password = value
        elif option == 'B':
            prf.bio = value
            # If user wants to post after editing bio
            choice = input("Would you like to post to the server? (Y or N) ")
            if choice == 'Y':
                username = prf.username
                password = prf.password
                bio = prf.bio
                message = None
                boolean = send(Journal.IP, Journal.port, username, password, message, bio)
            elif choice == 'N':
                pass
            else:
                raise Exception
        elif option == 'S':
            prf.dsuserver = value
            Journal.IP = value
        else:
            raise Exception
            
        prf.save_profile(profile)

        return boolean


    def print_dsu(prf:Profile, choice:str) -> None:
        '''
        Print prints items from a user's profile. 
        
        :param prf: Profile() object.
        :param choice: Print choice collected from user.
        
        '''
        if choice == 'S':
            print()
            print("Server:", prf.dsuserver)
        elif choice == 'U':
            print()
            print("Username:", prf.username)
        elif choice == 'P':
            print()
            print("Password:", prf.password)
        elif choice == 'B':
            print()
            print("Bio:", prf.bio)
        elif choice == 'X':
            lst = prf.get_posts()
            print()
            print("Here are your posts:\n")
            for index, post in enumerate(lst):
                print(f"   {index}: {post.entry}")
        elif choice == 'Y':
            lst = prf.get_posts()
            print("Here are your posts:\n")
            for index, post in enumerate(lst):
                print(f"   {index}: {post.entry}")
            print()
            id = int(input("What would you like to print? (Enter an id)\n"))
            lst = prf.get_posts()
            print()
            try:
                print("Post:", lst[id].entry)
            except:
                raise IndexError
        elif choice == 'A':
            print()
            print("Server: ", prf.dsuserver)
            print("Username:", prf.username)
            print("Password:", prf.password)
            print("Bio:", prf.bio)

            lst = prf.get_posts()
            print()
            print("Here are your posts:\n")
            for index, post in enumerate(lst):
                print(f"   {index}: {post.entry}")
        else:
            raise Exception

    def del_post(prf:Profile, profile:str, id:int) -> None:
        '''
        Delete removes a post locally to a user's profile.

        :param prf: Profile() object.
        :param profile: profile path
        :param id: ID of post to be deleted collected from user.
        '''
        prf.del_post(id)
        prf.save_profile(profile)

    def post_locally(prf:Profile, profile:str, entry:str) -> None:
        '''
        Adds a post locally to a user's profile. 
        
        :param prf: Profile() object
        :param profile: The location of the user's '.dsu' file.
        :param entry: Post message collected from user.
        '''
        
        post = Post()
        post._timestamp = 0
        post.set_entry(entry)

        prf.add_post(post)
        prf.save_profile(profile)

    def post_online(prf:Profile, IP:str, port:int, message:str=None, bio=None) -> bool:
        '''
        Post online passes a user's local information to the ds_client module.
        :param prf: Profile() object.
        :param IP: Server IP address collected from user.
        :param port: Server port.
        :param message: Message to be sent collected from user.
        '''
        username = prf.username
        password = prf.password
        bio = prf.bio

        status = send(Journal.IP, Journal.port, username, password, message, bio)
        return status