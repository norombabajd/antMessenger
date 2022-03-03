# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000

# Audrey Nguyen
# audrehn3@uci.edu
# 50253773

# a3.py
# A3: Publishing Online, allows users to post from their DSU profiles to a DSU Server.

from pathlib import Path
from Profile import DsuFileError, Profile, Post
from Journal import Journal
from Messages import Message
from ds_client import send

profile_path = ''
IP = ''
port = 3021

def run():
    """ Run interacts with the user, encapsulates main program functions. """
    global profile_path, IP, port
    
    user = input()
    if user == 'C':
        # Collect user information.
        print("Enter new profile information:\n")
        username = input("Username: ")
        password = input("Password: ")
        bio = input("Bio: ")
        print()
        path = input("Where would you like to store your profile? ")
        profile = input("What should your profile be called? ")
        print()
        
        try:
            # Create profile.
            IP, p = Journal.create_dsu(path, profile, username, password, bio)
            profile_path = p
            print()
            print("Profile successfully created!\n")
            print(Message.home)
            run()
        except FileNotFoundError:
            # If the file is not found, restart program.
            print("ERROR: Not a valid path. Try again.\n")
            print(Message.home)
            run()

    elif user == 'O':
        # Open existing profile.
        profile = input("What profile would you like to open?\n")
        try:
            profile_path = profile
            IP, user, pw, bio = Journal.open_dsu(profile)
            print()
            print("Profile successfully opened!\n")
            print("   Server:", IP)
            print("   Username:", user)
            print("   Password:", pw)
            print("   Bio:", bio)
            print()
            print(Message.home)
            run()
        except Exception:
            # If the profile does not exist, restart program.
            print()                                       
            print("ERROR: Profile not found. Try again.\n")
            print(Message.main_menu)
            run()

    elif user == 'E':
        # Edit existing profile.
        try:
            # Load profile.
            prf = Profile()
            prf.load_profile(profile_path)
        except:
            print()
            print("ERROR: Profile not found. Try again.\n")
            print(Message.home)
            run()
        print()
        print(Message.edit)

        # Interpret user choice.
        option = input()
        if option not in ['U', 'P', 'B', 'S']:
            print("ERROR: Not a valid choice. Try again.\n")
            print(Message.home)
            run()
        
        # Retrieve user choice.
        value = input("Enter new edit: ")
        try:
            boolean = Journal.edit_dsu(prf, profile_path, option, value)
            print()
            print("Edit saved!\n")
            # If biography was updated to server.
            if boolean == True:
                print("Bio published to server, or IP\n")
            elif boolean == None:
                pass
            else:
                print("An error has occurred.\n"
                      "Please check your Profile's IP and/or internet connection, and try again.\n")
            print(Message.home)
            run()
        except Exception:
            # Handle all errors.
            print()
            print("ERROR: An error has occurred. Try again. \n")
            print(Message.home)
            run()                                          

    elif user == 'A':
        # Add post to user profile.
        entry = input("What would you like to post?\n")
        try:
            # Load profile.
            prf = Profile()
            prf.load_profile(profile_path)
        except:
            print()
            print("ERROR: Profile not found. Try again.\n")
            print(Message.home)
            run()
        Journal.post_locally(prf, profile_path, entry)
        print()
        print("Post added!\n")
        
        # Ask if user wants to post to the server.
        choice = input("Would you like to post to the server? (Y or N) ") 
        if choice == 'Y':
            message = prf.get_posts()[-1]['entry']
            status = Journal.post_online(prf, IP, port, message)
            if status == True:
                print("Post successfully published!\n")
                print(Message.home)
                run()
            else:
                # Handle posting errors.
                print(  "An error has occurred.\n"
                        "Please check your Profile's IP and/or internet connection, and try again.\n")
                print(Message.home)
                run()
        elif choice == 'N':
            print()
            print(Message.home)
            run()
        else:
            print("Not a valid choice. Try again.\n")
            print(Message.home)
            run()

    elif user == 'D':
        # Delete posts from user profile.
        try:
            id = int(input("What would you like to delete? (Enter an id)\n"))
        except:
            print("ERROR: Not an integer. Try again.\n")
            print(Message.home)
            run()
        try:
            prf = Profile()
            prf.load_profile(profile_path)
        except:
            print()
            print("ERROR: Profile not found. Try again.\n")
            print(Message.home)
            run()
        try:
            Journal.del_post(prf, profile_path, id)
            print()
            print("Post deleted!\n")
            print(Message.home)
            run()
        except IndexError:
            print("ERROR: Not a valid id. Try again.\n")
            print(Message.home)
            run()
        except:
            print("ERROR: An error has occurred. Try again.\n")
            print(Message.home)
            run()
        
    elif user == 'P':
        # Print from user profile.
        print(Message.print)
        choice = input()
        if choice not in ['S', 'U', 'P', 'B', 'X', 'Y', 'A']:
            print("ERROR: Not a valid choice. Try again.\n")
            print(Message.home)
            run()
        try:
            prf = Profile()
            prf.load_profile(profile_path)

        except:
            print()
            print("ERROR: Profile not found. Try again.\n")
            print(Message.home)
            run()
        try:
            Journal.print_dsu(prf, choice)
            print()
            print(Message.home)
            run()
        except IndexError:
            # If id is not an integer or out of range, fail.
            print("ERROR: Not a valid id. Try again.\n")
            print(Message.home)
            run()
        except:
            print("ERROR: An error has occurred. Try again.\n")
            print(Message.home)
            run()
    
    elif user == 'X':
        # Post to DSU server.
        print("What would you like to post?\n")
        try:
            prf = Profile()
            prf.load_profile(profile_path)
        except:
            print()
            print("ERROR: An error has occurred. Try again.\n")
            print(Message.home)
            run()
        lst = prf.get_posts()
        for index, post in enumerate(lst):
            print(f"   {index}: {post.entry}")
        print()
        id = input()
        try:
            message = prf.get_posts()[int(id)]['entry']
        except IndexError:
            print("ERROR: Not a valid id. Try again.\n")
            print(Message.home)
            run()
        try:
            bio = None
            boolean = Journal.post_online(prf, IP, port, message, bio)
        except:
            print("ERROR: An error has occurred. Try again.\n")
            print(Message.home)
            run()
        if boolean == True:
            print("Post successfully published!\n")
            print(Message.home)
            run()
        else:
            print()
            print("An error has occurred.\n"
                  "Please check your Profile's IP and/or internet connection, and try again.\n")
            print(Message.home)
            run()
    
    elif user == 'Q':
        # Quit on 'Q'.
        quit()

    else:
        # Invalid menu choices.
        print()
        print("ERROR: Not a valid choice. Try again.\n")
        print(Message.main_menu)
        run()

if __name__ == "__main__":
    print("Welcome to ICS 32 Journal!\n")
    print(Message.main_menu)

    try:
        run()
    except ValueError or DsuFileError or SystemExit:
        pass
