# antMessenger
**Read an overview of the [Final Exam: Chatting with Friends](https://ics32.markbaldw.in/final.html).**

Final Project submission for ICS 32, taught by [Mark Baldwin](https://markbaldw.in) in Winter 2022 at the University of California, Irvine. In collaboration with [Audrey Nguyen](https://github.com/aud-dreams).

The Anteaters Networking through Technology Messenger, or antMessenger! for short, allows users to communicate over the Internet using Mark Baldwin's [DSU (Distributed Social) server](ics32distributedsocial.com).

### Documentation
A guide on how to use and important notes regarding antMessenger can be found on the [final-submission](https://github.com/norombabajd/antMessenger/tree/final-submission#how-to-use) branch.

The *final-submission* branch represents a snapshot of the repository when submitted to Canvas.**

### Developer Features
* Communication over the Internet using Mark Baldwin's proprietary DSU Server protocol through custom functions including token retrieval, and sending and receiving data wrapped in JSON.
* Local storage of data, including messages sent and recieved in a ".dsu" file. Represented as a custom dictionary, the Profile and Message classes, within antMessenger.
* Exception handling within developed functions, and presentation of user-errors.
* Dark mode, independent from system appearance!

### Known Bugs
* Creating a user-profile does not update the GUI, preventing a user from sending messages or performing other actions. **Solution: Re-open the newly created Profile from the File menu.**

### License
Please note that misuse of this code and documentation, when prohibited and/or used without attribution may constitute as plagiarism. Consult with your [school's policies on academic integrity](https://www.ics.uci.edu/ugrad/policies/Academic_Honesty). We'll leave it to [MOSS](https://yangdanny97.github.io/blog/2019/05/03/MOSS) and your instructors to deal with you. 

### Miscellaneous References
* https://tkdocs.com/tutorial/windows.html
* https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/text-methods.html
* https://docs.huihoo.com/tkinter/an-introduction-to-tkinter-1997/
* https://www.delftstack.com/howto/python-tkinter/how-to-create-a-new-window-with-a-button-in-tkinter/
* https://stackoverflow.com/questions/35977238/tagging-in-a-text-widget-tkinter
* https://pythonexamples.org/python-tkinter-window-background-color/
* https://www.pythontutorial.net/tkinter/ttk-style/
* https://github.com/ThomasPericoi/ASCIIPrinter
