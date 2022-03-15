# Audrey Nguyen
# audrehn3@uci.edu
# 50253773
# 
# John Daniel Norombaba
# jnoromba@uci.edu
# 91483000
#
# zotMessenger.py

# TODO: Replace Post with Message
#       Update functions to reflect those changes (posts_tree -> thread_tree)
#       Figure out indexing with new data structures, Messages are different from Posts.

import tkinter as tk
from tkinter import TclError, ttk, filedialog
from Profile import Profile, Message, DsuFileError, DsuProfileError
from ds_client import send
import copy

from ds_messenger import DirectMessenger 

class Body(tk.Frame):
    """ A subclass of tk.Frame that is responsible for drawing all of the widgets 
        in the body portion of the root frame. """
    
    def __init__(self, root, select_callback=None):
        """ Initializes the root and select_callback class attributes. """
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self._username = ""
        self._contact = ""
        self._threads = {}
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    def node_select(self, event):
        """
        Update the messages_view with the full post entry when the corresponding node in the posts_tree
        is selected.
        """
        self.clear_message_view()
        self._contact = self.posts_tree.item(self.posts_tree.selection()[0], option='text')
        thread = self._threads[self._contact]
        self.populate_thread(thread)

    def get_text_entry(self) -> str:
        """
        Returns the text that is currently displayed in the messages_view widget.
        """
        self.messages_view.configure(state=tk.NORMAL)
        return self.messages_view.get('1.0', 'end').rstrip()
        
    def clear_text_entry(self):
        """
        Sets the text to be displayed in the messages_view widget.
        NOTE: This method is useful for clearing the widget, just pass an empty string.
        """
        self.entry_editor.delete('0.0', 'end')

    def clear_message_view(self):
        self.messages_view.configure(state=tk.NORMAL)
        self.messages_view.delete('0.0', 'end')
        self.messages_view.configure(state=tk.DISABLED)

    def insert_msg(self, text:str, tag:str):
        """ 
        Insert a sent or recieved message in message_view.
        :text: Text to be inserted, derived from a Message or dict.
        :tag: 'sent' or 'recieved', respectivly aligns text left or right.

        """
        self.messages_view.configure(state=tk.NORMAL)
        self.messages_view.insert('end', text, (tag))
        self.messages_view.insert('end', "\n")
        self.messages_view.configure(state=tk.DISABLED)

    def populate_thread(self, thread:list):
        """ Populates thread with entries and messages. """
        for msg in thread:
            if 'recipient' in msg:
                self.insert_msg(msg['entry'], 'sent')
            if 'from' in msg:
                self.insert_msg(msg['message'], 'recieved')
        self.messages_view.update()
    
    def populate_thread_tree(self, username, threads:dict):
        """ Populates self._posts with conversations from the active Profile. """
        self._username = username
        self._threads = threads
        for id, user in enumerate(self._threads):
            self.posts_tree.insert('', id, id, text=user)    

    def reset_ui(self):
        """
        Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
        as when a new DSU file is loaded, for example.
        """
        self.clear_message_view()
        self.clear_text_entry()
        self.messages_view.configure(state=tk.NORMAL)
        self._threads = {}
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)
    
    def _draw(self):
        """ Call only once upon initialization to add widgets to the frame. """
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame, show=('tree'))
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="white")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        self.entry_editor = tk.Text(editor_frame, width=0, height=3, state=tk.DISABLED)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False, padx=5, pady=5)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.messages_view = tk.Text(editor_frame, width=0, state=tk.DISABLED)
        self.messages_view.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)
        self.messages_view.tag_configure(tagName='sent', justify='left')
        self.messages_view.tag_configure(tagName='recieved', justify='right')

        messages_view_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.messages_view.yview)
        self.messages_view['yscrollcommand'] = messages_view_scrollbar.set
        messages_view_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, send_callback=None, add_callback=None):
        """ Initializes root, send_callback, and online_callback class attributes. """
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_callback = add_callback
        self.is_online = tk.IntVar()
        self._draw()
        
    def send_click(self):
        """
        Calls the callback function specified in the send_callback class attribute, if
        available, when the save_button has been clicked.
        """
        if self._send_callback is not None:
            self._send_callback()
    
    def add_click(self):
        """
        Calls the callback function specified in the add_callback class attribute, if
        available, when the save_button has been clicked.
        """
        if self._add_callback is not None:
            self._add_callback()

    def set_status(self, message):
        """ Updates the text that is displayed in the footer_label widget. """
        self.footer_label.configure(text=message)        

    def _draw(self):
        """ Call only once upon initialization to add widgets to the frame. """
        self.send_btn = tk.Button(master=self, text="Send", width=5, command=self.send_click, state=tk.DISABLED)
        self.send_btn.pack(fill=tk.BOTH, side=tk.RIGHT, padx=15, pady=5)

        self.new_btn = tk.Button(master=self, text="New Conversation", width=12, command=self.add_click, state=tk.DISABLED)
        self.new_btn.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the NaClProfile class.
    """
    def __init__(self, root):
        """
        Initializes root class attribute.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._is_online = False
        self._profile_filename = None

        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = Profile()
        self._messenger = DirectMessenger()

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    def new_profile(self):
        """ Creates a new DSU file when the 'New' menu item is clicked. """
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
        """
        Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
        data into the UI.
        """
        if filename == None:
            # Prompt the user if a file is not provided (non-TclError).
            filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        
        try:
            # Open and load the profile.
            self.profile_filename = filename.name
            self._current_profile.load_profile(self.profile_filename)
            self._messenger.dsuserver = self._current_profile.dsuserver
            self._messenger.username = self._current_profile.username
            self._messenger.password = self._current_profile.password
            self.body.populate_thread_tree(self._current_profile.username, self._current_profile.get_conversations())
            # Update the UI.
            self.footer.send_btn.configure(state=tk.NORMAL)
            self.footer.new_btn.configure(state=tk.NORMAL)
            self.body.entry_editor.configure(state=tk.NORMAL)
            self.footer.set_status(f"Welcome back.")
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
            new_contact = self.user.get('0.0', 'end').rstrip()
            self._current_profile.add_contact(new_contact)
            self._current_profile.save_profile(self.profile_filename)
            self.footer.set_status("Ready.")
        except AttributeError:
            # Inform the user when they cancel profile creation.
            self.footer.set_status("Profile creation aborted.")

        self.body.posts_tree.insert('', 'end', 'end', text=new_contact)
        self.body.update()

    def _draw(self):
        """ Call only once, upon initialization to add widgets to root frame. """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.footer = Footer(self.root, send_callback=self.send_message, add_callback=self.new_conversation)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ZOT! Messenger")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
