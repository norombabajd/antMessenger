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

# TODO: Replace Post with Message
#       Update functions to reflect those changes (posts_tree -> thread_tree)
#       Figure out indexing with new data structures, Messages are different from Posts.

import tkinter as tk
from tkinter import TclError, ttk, filedialog
from Profile import Profile, Message, DsuFileError, DsuProfileError
from ds_messenger import DirectMessenger

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
        :tag: 'sent', 'recieved', or 'welcome' respectivly aligns text left, right, or center.

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

    anteater = """
       _.---._    /\\\\
    ./'       "--'\//
  ./              o \\
 /./\  )______   \__ \\
./  / /\ \   | \ \  \ \\
   / /  \ \  | |\ \  \\7
"     "    "  "
    """
    
    def _draw(self):
        """ Call only once upon initialization to add widgets to the frame. """
        self.posts_frame = tk.Frame(master=self, width=250)
        self.posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(self.posts_frame, show=('tree'))
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.entry_frame = tk.Frame(master=self, bg="")
        self.entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.editor_frame = tk.Frame(master=self.entry_frame, bg="white")
        self.editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        self.entry_editor = tk.Text(self.editor_frame, width=0, height=3, state=tk.DISABLED)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False, padx=5, pady=5)

        self.scroll_frame = tk.Frame(master=self.entry_frame, bg="", width=10)
        self.scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.messages_view = tk.Text(self.editor_frame, width=0, state=tk.DISABLED)
        self.messages_view.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)
        self.messages_view.tag_configure(tagName='sent', justify='right')
        self.messages_view.tag_configure(tagName='recieved', justify='left')
        self.messages_view.tag_configure(tagName='welcome', justify='center')
        self.insert_msg("Welcome Let's get started.\n", 'welcome')
        self.insert_msg("Open or create a profile by navigating to File in the menu bar.\n", 'welcome')
        self.insert_msg(self.anteater, 'welcome')
        self.messages_view_scrollbar = tk.Scrollbar(master=self.scroll_frame, command=self.messages_view.yview)
        self.messages_view['yscrollcommand'] = self.messages_view_scrollbar.set
        self.messages_view_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, send_callback=None, add_callback=None, mode_callback=None):
        """ Initializes root, send_callback, add_callback, mode_callback, is_online, and is_light class attributes. """
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_callback = add_callback
        self._mode_callback = mode_callback
        self.is_online = tk.IntVar()
        self.is_light = tk.IntVar()
        self._draw()
        
    def send_click(self):
        """
        Calls the callback function specified in the send_callback class attribute, if
        available, when the send_btn has been clicked.
        """
        if self._send_callback is not None:
            self._send_callback()
    
    def add_click(self):
        """
        Calls the callback function specified in the add_callback class attribute, if
        available, when the new_btn has been clicked.
        """
        if self._add_callback is not None:
            self._add_callback()
    
    def mode_click(self):
        """
        Calls the callback function specified in the mode_callback class attribute, if
        available, when the mode_btn has been clicked.
        """
        if self._mode_callback is not None:
            self._mode_callback()

    def set_status(self, message):
        """ Updates the text that is displayed in the footer_label widget. """
        self.footer_label.configure(text=message)        

    def _draw(self):
        """ Call only once upon initialization to add widgets to the frame. """
        self.send_btn = tk.Button(master=self, text="Send", width=5, command=self.send_click, state=tk.DISABLED)
        self.send_btn.pack(fill=tk.BOTH, side=tk.RIGHT, padx=15, pady=5)

        self.new_btn = tk.Button(master=self, text="New Conversation", width=15, command=self.add_click, state=tk.DISABLED)
        self.new_btn.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.mode_btn = tk.Button(master=self, text="Change Mode", width=12, command=self.mode_click, state=tk.DISABLED)
        self.mode_btn.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

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
        self._is_light = True
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
        self.body.clear_message_view()

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
            new_contact = self.user.get('0.0', 'end').rstrip()
            self._current_profile.add_contact(new_contact)
            self._current_profile.save_profile(self.profile_filename)
            self.footer.set_status("Ready.")
        except AttributeError:
            # Inform the user when they cancel profile creation.
            self.footer.set_status("Profile creation aborted.")

        self.body.posts_tree.insert('', 'end', 'end', text=new_contact)
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
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ZOT! Messenger")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("750x500")

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