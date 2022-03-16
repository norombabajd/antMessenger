# Audrey Nguyen
# audrehn3@uci.edu
# 50253773
# 
# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000
#
# zotMessenger.py
# Constructs messenging window and sends and receives messages. 

# TODO: 
#   - Fix light and dark mode elements (start on light mode and not default), repetitive code
#   - Figure out a better way to handle new messages / notifications (maybe a yellow footer?)
#   - Continue to annotate code for pddoc
#   - Error handling in the footer (and console?), except errors into footer.
#   - Change variable names (PUSH THEN DO LAST TO PREVENT BREAKING CODE)
#   - CREATE TEST_... (or recreate)
#   - README, sources

import tkinter as tk
from tkinter import TclError, ttk, filedialog
from Profile import Profile, Message, DsuFileError, DsuProfileError
from ds_messenger import DirectMessenger, DirectMessengerError

class Body(tk.Frame):
    """A subclass of tk.Frame that draws widgets in the body portion of the root frame."""
    def __init__(self, root, select_callback=None):
        """Initializes the root and select_callback class attributes."""
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self._username: str = ""
        """Create the username variable to store the username in self._current_profile."""
        self._contact: str  = ""
        """Create the contact variable to store the current conversation thread."""
        self._threads: dict = {}
        """Create the storage container to hold all conversations from the self._current_profile."""
        self._draw()
    
    def node_select(self, event):
        """Update the messages_view with the full post entry when the corresponding node in the posts_tree is selected."""
        # Clear the message view, set the current contact from the selected node, and populate the thread.
        self.clear_message_view()
        self._contact = self.posts_tree.item(self.posts_tree.selection()[0], option='text')
        self.populate_thread(self._threads[self._contact])

    def get_text_entry(self) -> str:
        """Returns the text that is currently displayed in the messages_view widget."""
        self.messages_view.configure(state=tk.NORMAL)
        return self.messages_view.get('1.0', 'end').rstrip()
        
    def clear_text_entry(self):
        """Clears the text displayed in the entry_editor widget."""
        self.entry_editor.delete('0.0', 'end')

    def clear_message_view(self):
        """Clears the text in the messages_view widget."""
        # Enabling messages_view is required to perform changes to the widget.
        self.messages_view.configure(state=tk.NORMAL)
        self.messages_view.delete('0.0', 'end')
        self.messages_view.configure(state=tk.DISABLED)

    def insert_msg(self, text:str, tag:str):
        """ 
        Insert a sent or recieved message in message_view.
        
        :text: Text to be inserted, derived from a Message or dict.
        :tag: 'sent' or 'recieved', respectivly aligns text left or right.
        """
        # Enabling messages_view is required to perform changes to the widget.
        self.messages_view.configure(state=tk.NORMAL)
        self.messages_view.insert('end', text, (tag))
        self.messages_view.insert('end', "\n")
        self.messages_view.configure(state=tk.DISABLED)

    def populate_thread(self, thread:list):
        """
        Populates thread with entries and messages.
        
        :thread: A list that contains conversations exchanged between two users.
        """
        # Iterate through a list (thread) containing messages. 
        for msg in thread:
            if 'recipient' in msg:
                # Align text to the right.
                self.insert_msg(msg['entry'], 'sent')
            if 'from' in msg:
                # Align text to the left.
                self.insert_msg(msg['message'], 'recieved')
        self.messages_view.update()
    
    def populate_thread_tree(self, username, threads:dict):
        """Populates self._posts with conversations from the active Profile."""
        self._username:str = username
        """INSERT DESCRIPTION HERE."""
        self._threads:dict = threads
        """INSERT DESCRIPTION HERE."""
        for id, user in enumerate(self._threads):
            """INSERT DESCRIPTION HERE."""
            self.posts_tree.insert('', id, id, text=user)    

    def reset_ui(self):
        """Resets all UI widgets to their default state."""
        self.clear_message_view()
        self.clear_text_entry()
        self.messages_view.configure(state=tk.NORMAL)
        self._threads = {}
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)
    
    def _draw(self):
        """ Add widgets to the frame upon initialization, call only once."""
        self.posts_frame:tk.Frame = tk.Frame(master=self, width=250)
        """Create the frame that will hold a Treeview widget."""
        self.posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        
        self.posts_tree = ttk.Treeview(self.posts_frame, show=('tree'))
        """Create a Treeview widget that will store a user's contacts."""
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.tag_configure('new', foreground='red')
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        self.style:ttk.Style = ttk.Style()
        """Establish the Treeview widget's style."""
        self.style.theme_use('clam')

        self.entry_frame:tk.Frame = tk.Frame(master=self, bg="")
        """INSERT DESCRIPTION HERE."""
        self.entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.editor_frame:tk.Frame = tk.Frame(master=self.entry_frame, bg="white")
        """INSERT DESCRIPTION HERE."""
        self.editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        self.entry_editor:tk.Text = tk.Text(self.editor_frame, width=0, height=3, state=tk.DISABLED)
        """INSERT DESCRIPTION HERE."""
        self.entry_editor.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False, padx=5, pady=5)
        
        self.scroll_frame:tk.Frame = tk.Frame(master=self.entry_frame, bg="", width=10)
        """INSERT DESCRIPTION HERE."""
        self.scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.messages_view:tk.Text = tk.Text(self.editor_frame, width=0, state=tk.DISABLED)
        """INSERT DESCRIPTION HERE."""
        self.messages_view.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)
        
        self.messages_view.tag_configure(tagName='sent', justify='right')
        self.messages_view.tag_configure(tagName='recieved', justify='left')
        self.messages_view.tag_configure(tagName='heading', justify='center')
        
        self.insert_msg("\nWelcome! Let's get started.\nOpen or create a profile by navigating to File in the menu bar.", 'heading')

        self.messages_view_scrollbar:tk.Scrollbar = tk.Scrollbar(master=self.scroll_frame, command=self.messages_view.yview)
        """INSERT DESCRIPTION HERE."""
        self.messages_view['yscrollcommand'] = self.messages_view_scrollbar.set
        self.messages_view_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

class Footer(tk.Frame):
    """A subclass of tk.Frame that draws widgets in the footer portion of the root frame."""
    def __init__(self, root, send_callback=None, add_callback=None, mode_callback=None):
        """ Initializes root, send_callback, add_callback, mode_callback, is_online, and is_light class attributes. """
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_callback = add_callback
        self._mode_callback = mode_callback
        self.is_online:tk.IntVar = tk.IntVar()
        """INSERT DESCRIPTION HERE."""
        self.is_light:tk.IntVar = tk.IntVar()
        """INSERT DESCRIPTION HERE."""
        self._draw()
        
    def send_click(self):
        """Calls the send_message function when the send_btn is clicked."""
        if self._send_callback is not None:
            self._send_callback()
    
    def add_click(self):
        """Calls the new_conversation function when the new_btn is clicked."""
        if self._add_callback is not None:
            self._add_callback()
    
    def mode_click(self):
        """Calls the change_mode function when the mode_btn is clicked."""
        if self._mode_callback is not None:
            self._mode_callback()

    def set_status(self, message):
        """Updates the text that is displayed in the footer_label widget."""
        self.footer_label.configure(text=message)        

    def _draw(self):
        """ Add widgets to the footer upon initialization, call only once."""
        self.send_btn = tk.Button(master=self, text="Send", width=10, command=self.send_click, state=tk.DISABLED)
        self.send_btn.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.new_btn = tk.Button(master=self, text="New Conversation", width=15, command=self.add_click, state=tk.DISABLED)
        self.new_btn.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.mode_btn = tk.Button(master=self, text="Change Mode", width=15, command=self.mode_click, state=tk.DISABLED)
        self.mode_btn.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

class antMessenger(tk.Frame):
    """A subclass of tk.Frame that draws widgets in the main portion of the root frame, also manages Profile functions."""
    def __init__(self, root):
        """Initializes root class attribute."""
        tk.Frame.__init__(self, root)
        self.root = root
        self._is_online:bool = False
        """INSERT DESCRIPTION HERE."""
        self._is_light:bool = True
        """INSERT DESCRIPTION HERE."""
        self._profile_filename:str = None
        """INSERT DESCRIPTION HERE."""

        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile:Profile = Profile()
        """INSERT DESCRIPTION HERE."""
        
        self._messenger:DirectMessenger = DirectMessenger()
        """INSERT DESCRIPTION HERE."""

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    def new_profile(self):
        """Create a new DSU file when the 'New' menu item is clicked."""
        try:
            filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
            self.profile_filename = filename.name
            self._current_profile = Profile()
            self._current_profile.save_profile(self.profile_filename)
            self.body.reset_ui()
            self.footer.set_status("Ready.")
        except AttributeError:
            # Inform the user when they cancel profile creation.
            self.footer.set_status("Profile creation aborted.")
    
    def open_profile(self, filename=None):
        """Open and load an existing DSU file when the 'Open' menu item is clicked."""
        self.body.clear_message_view()

        if filename == None:
            # Prompt the user if a file is not provided (non-TclError).
            filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        
        try:
            # Open and load the profile.
            self.profile_filename = filename.name
            self._current_profile.load_profile(self.profile_filename)
            self._messenger = DirectMessenger(dsuserver=self._current_profile.dsuserver, username=self._current_profile.username, password=self._current_profile.password)
            self.body.populate_thread_tree(self._current_profile.username, self._current_profile.get_conversations())
            # Update the UI.
            self.footer.send_btn.configure(state=tk.NORMAL)
            self.footer.new_btn.configure(state=tk.NORMAL)
            self.body.entry_editor.configure(state=tk.NORMAL)
            self.footer.set_status(f"Welcome back.")
            main.after(5000, antM.retrieve_messages)
            # Set changes.
            self.update()
        except AttributeError:
            # When a user does not open a profile.
            self.footer.set_status("Open profile action aborted.")
        except TclError:
            # When a profile is already open, reset the UI and re-open.
            self.body.reset_ui()
            self.open_profile(filename=filename)
        except DsuProfileError:
            # When a user attempts to open a legacy or corrupted '.dsu' profile.
            self.footer.set_status("Corrupted or unsupported Profile.")

    def close(self):
        """ Closes the program when the 'Close' menu item is clicked. """
        self.root.destroy()

    def send_message(self):
        """ Saves the text currently in the messages_view widget to the active DSU file. """
        message = self.body.entry_editor.get('0.0', 'end').rstrip()
        
        """if self._messenger.send(entry, self.body._contact):
            self.body.insert_msg(entry, 'sent')
            self._current_profile.store_sent(Message(self.body._contact, message))
            self._current_profile.save_profile(self.profile_filename)
            self.footer.set_status("Message sent!")
            self.body.clear_text_entry()
        else:
            self.footer.set_status("There was a problem, check your internet connection.")"""
        
        self._current_profile.store_sent(Message(self.body._contact, message))
        self._current_profile.save_profile(self.profile_filename)
        self.footer.set_status("Message sent!")
        self.body.insert_msg(message, 'sent')
        self.body.clear_text_entry()
        self.update()

    def new_conversation(self):
        """ Creates a new window to add a new contact. """
        self.body.clear_message_view()
        add_window = tk.Toplevel(self)

        self.info = tk.Label(master=add_window, text="Enter their username below!", justify='center')
        self.info.pack(fill=tk.BOTH, side=tk.TOP, padx=10, pady=10)
        
        self.add = tk.Button(add_window, text="Add Anteater", width=5, command=self.add_user)
        self.add.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5, pady=5)

        self.user = tk.Text(add_window, width=0, height=1,)
        self.user.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False, padx=10, pady=5)

        add_window.title("New Conversation")
        add_window.geometry("300x115")
        add_window.option_add('*tearOff', False)

        add_window.update()
        add_window.minsize(add_window.winfo_width(), add_window.winfo_height())
        add_window.maxsize(add_window.winfo_width(), add_window.winfo_height())

    def add_user(self):
        """ Obtains name of contact from user, creates a new profile, & adds to treeview. """
        try:
            id = len(self.body._threads) + 1
            new_contact = self.user.get('0.0', 'end').rstrip()

            if new_contact.split() != 0:
                self._current_profile.add_contact(new_contact)
                self._current_profile.save_profile(self.profile_filename)
                self.footer.set_status("Ready.")
        except AttributeError:
            # Inform the user when they cancel profile creation.
            self.footer.set_status("Profile creation aborted.")

        self.body.posts_tree.insert('', id, id, text=new_contact)
        self.body.update()

    def change_mode(self):
        """ Allows user to toggle between dark mode and light mode. """
        if self._is_light is True:
            self.body.messages_view.configure(bg="#242526", foreground="white")
            self.body.posts_frame.configure(bg="black")
            self.body.editor_frame.configure(bg="black")
            self.body.entry_frame.configure(bg="black")
            self.body.entry_editor.configure(bg="#242526", foreground="white", state=tk.NORMAL)
            self.body.style.configure('Treeview', background="#242526", foreground="white", fieldbackground="#242526")
            self.footer.configure(bg="black")
            self.footer.send_btn.configure(bg="black", foreground="white")
            self.footer.new_btn.configure(bg="black", foreground="white")
            self.footer.mode_btn.configure(bg="black", foreground="white")
            self.footer.footer_label.configure(bg="black", foreground="white")
            self._is_light = False

        elif self._is_light is False:
            self.body.messages_view.configure(bg="white", foreground="black")
            self.body.posts_frame.configure(bg="white")
            self.body.editor_frame.configure(bg="white")
            self.body.entry_frame.configure(bg="white")
            self.body.style.configure('Treeview', background="white", foreground="black", fieldbackground="white")
            self.body.entry_editor.configure(bg="white", foreground="black")
            self.footer.configure(bg="white")
            self.footer.send_btn.configure(bg="white", foreground="black")
            self.footer.new_btn.configure(bg="white", foreground="black")
            self.footer.mode_btn.configure(bg="white", foreground="black")
            self.footer.footer_label.configure(bg="white", foreground="black")
            self._is_light = True
    
    def after(self, ms: int, func: None = ...) -> str:
        '''
        :param ms: The delay in milliseconds before func is called.
        :param func: The function to be called when timer event is removed from the event queue
        
        :return: an id that is associated with this timer event
        '''
        pass

    def retrieve_messages(self):
        """INSERT DESCRIPTION HERE."""
        senders:list = []
        """INSERT DESCRIPTION HERE."""
        inbox:list = self._messenger.retrieve_new()
        """INSERT DESCRIPTION HERE."""

        for msg in inbox:
            user = msg['from']
            if user in self._current_profile._conversations and user in self.body._threads:
                senders.append(user)
                self._current_profile._conversations[user].append(msg)
                self.body._threads[user].append(msg)
                
                self.body.posts_tree.item(self.body._contact, tags=('new'))

            if user == self.body._contact:
                self.body.insert_msg(f"\n{msg['message']}", 'recieved')
        
        self.footer.set_status("New messages.") if len(senders) > 0 else self.footer.set_status("No new messages.")
        self.root.after(5000, self.retrieve_messages)
            
    def _draw(self):
        """ Call only once, upon initialization to add widgets to root frame. """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.footer = Footer(self.root, send_callback=self.send_message, add_callback=self.new_conversation, mode_callback=self.change_mode)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

        self.footer.mode_btn.configure(state=tk.NORMAL)

if __name__ == "__main__":
    main = tk.Tk()
    main.title("antMessenger!")
    
    main.geometry("740x500")
    main.option_add('*tearOff', False)
    
    antM = antMessenger(main)
    
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())

    main.mainloop()