# ICS 32 Winter 2022
# Final Exam: Chatting with Friends

Audrey Nguyen
audrehn3@uci.edu
50253773

John Daniel Norombaba
jnoromba@uci.edu
91483000

### Welcome!

The Anteaters Networking through Technology Messenger, or antMessenger! for short, allows users to communicate over the internet through supported DSU (Distributed Social) server.

### How to Use:
Launch the **antMessenger.py** file!

Upon running the program, users should be greeted with the antMessenger! window. The message viewing box (top right) contains a short welcome message and quick instructions on how to navigate the program. The status in the footer (bottom left) currently reads "Ready."

To begin, open an existing Profile or create a new Profile from the File menu bar. The footer status should promptly change to "Welcome back." At the moment, the Send and New Conversation buttons in the footer are disabled. Loading a Profile will activate these buttons.

The Toggle Appearance button in the footer stays active throughout the entire program. Pressing this button allows the user to switch between dark and light mode.

Upon loading a Profile, existing recipients should appear in the treeview (left box). Clicking on a recipient brings forth all messages into the message viewing box. Messages aligned to the right are sent by the user. Messages aligned to the left are sent by the recipient and received by the user.

To send a message, type an entry into the bottom right box and then press the Send button. The message should appear in the viewing box as a result of this action, and the footer status changes to "Message sent!"

Users also have the option to start a new conversation by pressing the New Conversation button in the footer. This opens up a new window, where the user will be prompted to enter the username of a new recipient. Users will now be able to converse with this new person!

While the program is running, it will be on the constant lookout for any new messages sent to the user. Once the message is detected by the program, the footer status will alert the user with the message "New message from recipient" and it will automatically show up in the message viewing box.

To discontinue messaging, users can navigate to the File menu bar and close the program.

### Important Notes:
* On Windows, the window must be expanded to view the footer. This is a Windows/Tk issue out of the developer's control.
* On Windows, you may need to add '.dsu' to the filename when creating/opening a profile.
* The ability to toggle between dark and light mode is independent of operating system's setting. Try it!
* Creating a new profile will automatically give you the profile: dsuserver='168.235.86.101', username='notjohndaniel', password='zotzot9148'
* However, you are free to edit these settings using a UTF-8 compatible text editor.
* You will only recieve messages from contacts you've added. Once they are added, you can accept messages from that user.
* You will recieve messages from all added contacts. Keep an eye on the footer, messages come by quick.

### References/Sources:
* https://tkdocs.com/tutorial/windows.html
* https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/text-methods.html
* https://docs.huihoo.com/tkinter/an-introduction-to-tkinter-1997/
* https://www.delftstack.com/howto/python-tkinter/how-to-create-a-new-window-with-a-button-in-tkinter/
* https://stackoverflow.com/questions/35977238/tagging-in-a-text-widget-tkinter
* https://pythonexamples.org/python-tkinter-window-background-color/
* https://www.pythontutorial.net/tkinter/ttk-style/
* https://github.com/ThomasPericoi/ASCIIPrinter