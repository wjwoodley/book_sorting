####################
# William Woodley  #
# 25 December 2020 #
####################

import tkinter as tk              # To create the GUI
import tkinter.ttk as ttk         # To stylise OptionMenus
import tkinter.scrolledtext as ts # To display the sorted books
from PIL import ImageTk, Image    # To add images
import numpy as np                # To manage data
import string                     # To capitalise book titles
import subprocess as sub          # To open the data file in Notepad
from shutil import copy2          # To make a back-up of the data file

# Constants

PATH      = "./data/books.txt"
VERSION   = "1.0.0"
DATE      = "25 December 2020"
COLOUR    = "#B8E2E3"
BTN_STYLE = tk.FLAT

class Book:
    
    def __init__ (self, title_in, lname_in, fname_in, series_in, number_in, genre_in, isOwned_in, status_in, rating_in, isNew_in):
        
        self.title   = title_in
        self.lname   = lname_in
        self.fname   = fname_in
        self.series  = series_in
        self.number  = number_in
        self.genre   = genre_in
        self.isOwned = isOwned_in
        self.status  = status_in
        self.rating  = rating_in
        self.isNew   = isNew_in

def load_books ():
    
    # Read in books from book data file
    
    Books_Data = np.loadtxt(PATH, dtype = "str", delimiter = ",", skiprows = 1)
    
    main.all_books = np.zeros(len(Books_Data), dtype = "object")
    
    # Fill the all_books array by reading books in as Book objects
    
    for i in range(len(Books_Data)):
        
        title   = Books_Data[i, 0]
        lname   = Books_Data[i, 1]
        fname   = Books_Data[i, 2]
        series  = Books_Data[i, 3]
        number  = int(Books_Data[i, 4])
        genre   = Books_Data[i, 5]
        isOwned = Books_Data[i, 6]
        status  = Books_Data[i, 7]
        rating  = Books_Data[i, 8]
        isNew   = int(Books_Data[i, 9])
        
        main.all_books[i] = Book(title, lname, fname, series, number, genre, isOwned, status, rating, isNew)
    
    # Count how many books are on record, owned, and have been read
    
    main.n_books = len(main.all_books)
    main.n_owned = len([i for i in range(main.n_books) if main.all_books[i].isOwned == "1"])
    main.n_read  = len([i for i in range(main.n_books) if main.all_books[i].status == "Read"])

def position_window (window_in, width_in, height_in):
    
    # Colour the window background
    
    window_in.configure(bg = COLOUR)
    
    # Calculate the coordinates for the center of the screen
    
    open_at_x = (window_in.winfo_screenwidth()/2) - (width_in/2)
    open_at_y = (window_in.winfo_screenheight()/2) - (height_in/2)
    
    # Open the window at the calculated coordinates
    
    window_in.geometry("%dx%d+%d+%d" % (width_in, height_in, open_at_x, open_at_y))
    window_in.resizable(False, False)

def open_main_window ():
    
    global main_window, background_image
    
    # Create and position the main window
    
    main_window = tk.Tk()
    
    position_window(main_window, 793, 483)
    
    # Configure the window
    
    main_window.title("Book Sorting")
    main_window.iconphoto(False, tk.PhotoImage(master = main_window, file = "./images/icon.png"))
    
    # Create the main frame
    
    main_frame = tk.Frame(master = main_window, bg = COLOUR)
    main_frame.pack(expand = True)
    
    # Create the book display
    
    display_frame = tk.Frame(master = main_frame, width = "900", height = "398", bg = COLOUR)
    display_frame.pack()
    
    book_display = ts.ScrolledText(master = display_frame, width = "94", height = "22", padx = 10, pady = 10)
    book_display.place(x = 0, y = 0)
    
    book_display.configure(state = "disabled", font = "Helvetic 11")
    book_display.tag_configure("header", font = "Helvetica 16 bold", underline = True)
    book_display.tag_configure("unowned", foreground = "#B0B0B0")
    
    # Add the background image
    
#    background_image = Image.open("./images/background.png")
#    background_image = background_image.resize((350, 350), Image.ANTIALIAS)
#    background_image = ImageTk.PhotoImage(background_image)
    
#    background_label = tk.Label(master = book_display, bg = "white", image = background_image, width = 350, height = 350)
#    background_label.place(relx = 1.0, rely = 1.0, x = 13, y = 13, anchor = "se")
    
    # Create a bottom frame
    
    bottom_frame = tk.Frame(master = main_frame, bg = COLOUR)
    bottom_frame.pack(expand = True, fill = tk.BOTH)
    
    # Create the counting variables
    
    n_books_variable = tk.StringVar()
    n_books_variable.set(str(main.n_books) + " books on record")
    
    n_owned_variable = tk.StringVar()
    n_owned_variable.set(str(main.n_owned) + " books owned")
    
    n_read_variable = tk.StringVar()
    n_read_variable.set(str(main.n_read) + " books read")
    
    # Create a counting frame
    
    counting_frame = tk.Frame(master = bottom_frame, bg = COLOUR)
    counting_frame.pack(side = tk.LEFT, padx = 10, pady = 10)
    
    # Create and place the counting labels
    
    n_books_label = tk.Label(master = counting_frame, textvariable = n_books_variable, width = 25, anchor = "w", font = "Helvetica 11", bg = COLOUR, pady = 0)
    n_books_label.grid(row = 0, column = 0, pady = 0, sticky = tk.NE + tk.SW)
    
    n_owned_label = tk.Label(master = counting_frame, textvariable = n_owned_variable, width = 25, anchor = "w", font = "Helvetica 11", bg = COLOUR, pady = 0)
    n_owned_label.grid(row = 1, column = 0, pady = 0, sticky = tk.NE + tk.SW)
    
    n_read_label = tk.Label(master = counting_frame, textvariable = n_read_variable, width = 25, anchor = "w", font = "Helvetica 11", bg = COLOUR, pady = 0)
    n_read_label.grid(row = 2, column = 0, pady = 0, sticky = tk.NE + tk.SW)
    
    # Button functions
    
    def sort_books ():
        
        # Load the books again, since new ones have likely been added
        
        load_books()
        
        # Update the book counting labels
        
        n_books_variable.set(str(main.n_books) + " books on record")
        n_owned_variable.set(str(main.n_owned) + " books owned")
        n_read_variable.set(str(main.n_read) + " books read")
        
        # Sort the books
        
        ################################################################################
        ################################################################################
        
        sorted_books = np.array(sorted(main.all_books, key = lambda x: (x.genre, x.lname, x.fname, x.series, x.number)))
        
        ################################################################################
        ################################################################################
        
        # Print the books to the book display
        
        book_display.configure(state = "normal")
        
        book_display.delete("0.0", tk.END)
        
        # Calculate the length of the longest book title
        
        max_title = max(len(i.title) for i in main.all_books)
        
        for i in range(len(sorted_books)):
            
            # If the genre changes, print the new genre
            
            if sorted_books[i].genre != sorted_books[i - 1].genre:
                
                # Do not skip an extra line before the very first genre
                
                if i != 0:
                    
                    book_display.insert(tk.INSERT, "\n" + str(sorted_books[i].genre) + ":\n\n", "header")
                
                else:
                    
                    book_display.insert(tk.INSERT, str(sorted_books[i].genre) + ":\n\n", "header")
            
            # Print the books in this genre
            
            if sorted_books[i].lname != "0":
                
                inserted_text = "%s\t\t\t%s %s\n" % (sorted_books[i].title, sorted_books[i].fname, sorted_books[i].lname)
            
            else:
                
                inserted_text = "%s\t\t\t%s\n" % (sorted_books[i].title, sorted_books[i].fname)
            
            if sorted_books[i].isOwned == "1":
                
                book_display.insert(tk.INSERT, inserted_text)
            
            else:
                
                book_display.insert(tk.INSERT, inserted_text, "unowned")
        
        book_display.configure(state = "disabled")
        
        # Loop through sorted books again and look for new ones
        
        for i in range(len(sorted_books)):
            
            # If the book is new, print out where it belongs
            
            if sorted_books[i].isNew:
                
                if i == 0:
                    
                    open_new_book_window(string.capwords(sorted_books[i].title))
                
                elif i != len(sorted_books) - 1:
                    
                    open_new_book_window(string.capwords(sorted_books[i].title), string.capwords(sorted_books[i - 1].title), string.capwords(sorted_books[i + 1].title))
                    
                else:
                    
                    open_new_book_window(string.capwords(sorted_books[i].title), end = True)
                
                sorted_books[i].isNew = 0
        
        # Overwrite the data file with the new order
        
        Books_Data = open(PATH, "w+")
        
        Books_Data.write("Title,Last Name,First Name,Series,Number,Genre,Owned,Status,Rating,New\n")
        
        for i in range(len(sorted_books)):
            
            title_in   = sorted_books[i].title
            lname_in   = sorted_books[i].lname
            fname_in   = sorted_books[i].fname
            series_in  = sorted_books[i].series
            number_in  = str(sorted_books[i].number)
            genre_in   = sorted_books[i].genre
            isOwned_in = sorted_books[i].isOwned
            status_in  = sorted_books[i].status
            rating_in  = sorted_books[i].rating
            isNew_in   = str(sorted_books[i].isNew)
            
            Books_Data.write(string.capwords(title_in) + "," + string.capwords(lname_in) + "," + string.capwords(fname_in) + "," + string.capwords(series_in) + "," + number_in + "," + genre_in + "," + isOwned_in + "," + status_in + "," + rating_in + "," + isNew_in + "\n")
        
        Books_Data.close()
        
        return 0
    
    # Create a button frame
    
    button_frame = tk.Frame(master = bottom_frame, bg = COLOUR)
    button_frame.pack(side = tk.RIGHT, padx = 5, pady = 10)
    
    # Create and place the buttons
    
    add_button = tk.Button(text = "Add Books", master = button_frame, command = open_add_book_window, font = "12", relief = BTN_STYLE)
    add_button.grid(row = 0, column = 1, rowspan = 3, padx = 5, ipadx = 15, ipady = 15)
    
    sort_button = tk.Button(text = "Sort Books", master = button_frame, command = sort_books, font = "12", relief = BTN_STYLE)
    sort_button.grid(row = 0, column = 2, rowspan = 3, padx = 5, ipadx = 15, ipady = 15)
    
    edit_button = tk.Button(text = "Edit Books", master = button_frame, command = open_edit_book_window, font = "12", relief = BTN_STYLE)
    edit_button.grid(row = 0, column = 3, rowspan = 3, padx = 5, ipadx = 15, ipady = 15)
    
    help_button = tk.Button(text = "Help", master = button_frame, command = open_help_window, font = "12", relief = BTN_STYLE)
    help_button.grid(row = 0, column = 4, rowspan = 3, padx = 5, ipadx = 15, ipady = 15)
    
    # Sort the books on start-up
    
    sort_books()
    
    # Run the window
    
    main_window.mainloop()

def open_add_book_window ():
    
    global main_window
    
    # Create and position the window
    
    add_book_window = tk.Toplevel()
    
    position_window(add_book_window, 375, 375)
    
    # Configure the window
    
    add_book_window.title("Add a Book")
    add_book_window.iconphoto(False, tk.PhotoImage(master = add_book_window, file = "./images/icon.png"))
    
    # Focus the window
    
    add_book_window.transient(main_window)
    add_book_window.grab_set()
    
    # Create the main frame
    
    main_frame = tk.Frame(master = add_book_window, bg = COLOUR)
    main_frame.pack(expand = True)
    
    # Create the message frame
    
    message_frame = tk.Frame(master = main_frame, bg = COLOUR)
    message_frame.pack()
    
    message_variable = tk.StringVar()
    message_variable.set("Ready to add books!")
    
    message = tk.Label(master = message_frame, textvariable = message_variable, bg = COLOUR, font = "Helvetica 10 bold")
    message.pack(pady = 12)
    
    # Create labels and text fields for user input
    
    input_frame = tk.Frame(master = main_frame, bg = COLOUR)
    input_frame.pack()
    
    # Create labels for input
    
    title_label   = tk.Label(text = "Title:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    lname_label   = tk.Label(text = "Last Name:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    fname_label   = tk.Label(text = "First Name:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    series_label  = tk.Label(text = "Series:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    number_label  = tk.Label(text = "#:", master = input_frame, width = 3, anchor = "c", bg = COLOUR)
    genre_label   = tk.Label(text = "Genre:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    isOwned_label = tk.Label(text = "Owned:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    status_label  = tk.Label(text = "Status:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    rating_label  = tk.Label(text = "Rating:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    
    # Create entries for input
    
    title_entry   = tk.Entry(master = input_frame, width = 27, relief = BTN_STYLE)
    lname_entry   = tk.Entry(master = input_frame, width = 27, relief = BTN_STYLE)
    fname_entry   = tk.Entry(master = input_frame, width = 27, relief = BTN_STYLE)
    series_entry  = tk.Entry(master = input_frame, width = 17, relief = BTN_STYLE)
    number_entry  = tk.Entry(master = input_frame, width = 4, relief = BTN_STYLE)
    
    # Create option menu variables for input
    
    genre_options = ["Fiction (Adult)", "Fiction (Teen)", "Fiction (Youth)", "Fantasy", "Mental Health", "Romance"]
    genre_variable = tk.StringVar()
    genre_variable.set(genre_options[0])
    
    isOwned_options = ["Yes", "No"]
    isOwned_variable = tk.StringVar()
    isOwned_variable.set(isOwned_options[0])
    
    status_options = ["Read", "Reading", "Not Read"]
    status_variable = tk.StringVar()
    status_variable.set(status_options[0])
    
    rating_options = [1, 2, 3, 4, 5, 10]
    rating_variable = tk.StringVar()
    rating_variable.set(rating_options[0])
    
    # Create option menus for input
    
    genre_menu = ttk.OptionMenu(input_frame, genre_variable, genre_options[0], *genre_options)
    genre_menu.config(width = 27)
    
    isOwned_menu = ttk.OptionMenu(input_frame, isOwned_variable, isOwned_options[0], *isOwned_options)
    isOwned_menu.config(width = 27)
    
    status_menu = ttk.OptionMenu(input_frame, status_variable, status_options[0], *status_options)
    status_menu.config(width = 27)
    
    rating_menu = ttk.OptionMenu(input_frame, rating_variable, rating_options[0], *rating_options)
    rating_menu.config(width = 27)
    
    # Place all input widgets on grid
    
    title_label.grid(row = 0, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    title_entry.grid(row = 0, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    lname_label.grid(row = 1, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    lname_entry.grid(row = 1, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    fname_label.grid(row = 2, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    fname_entry.grid(row = 2, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    series_label.grid(row = 3, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    series_entry.grid(row = 3, column = 1, pady = 3, sticky = tk.NE + tk.SW)
    
    number_label.grid(row = 3, column = 2, pady = 3, sticky = tk.NE + tk.SW)
    number_entry.grid(row = 3, column = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    genre_label.grid(row = 4, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    genre_menu.grid(row = 4, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    isOwned_label.grid(row = 5, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    isOwned_menu.grid(row = 5, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    status_label.grid(row = 6, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    status_menu.grid(row = 6, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    rating_label.grid(row = 7, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    rating_menu.grid(row = 7, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    # Button functions
    
    def add ():
        
        # Read in information from user input
        
        title_in   = title_entry.get()
        lname_in   = lname_entry.get()
        fname_in   = fname_entry.get()
        series_in  = series_entry.get()
        number_in  = number_entry.get()
        genre_in   = genre_variable.get()
        isOwned_in = isOwned_variable.get()
        status_in  = status_variable.get()
        rating_in  = rating_variable.get()
        
        # Correct user input
        
        if lname_in == "":
            
            lname_in = "0"
        
        if fname_in == "":
            
            fname_in = "0"
        
        if series_in == "":
            
            series_in = "0"
        
        if number_in == "":
            
            number_in = "0"
        
        if isOwned_in == "Yes":
            
            isOwned_in = "1"
        
        else:
            
            isOwned_in = "0"
        
        # Test whether the book already exists or not
        
        if title_in == "":
            
            message_variable.set("Title cannot be blank!")
            message.configure(fg = "red")
        
        elif any(i.title.lower() == title_in.lower() for i in main.all_books):
            
            message_variable.set(string.capwords(title_in) + " already exists!")
            message.configure(fg = "red")
        
        else:
            
            # Create a Book object for the new book and add it to the list
            
            new_book       = Book(title_in, lname_in, fname_in, series_in, number_in, genre_in, isOwned_in, status_in, rating_in, 1)
            main.all_books = np.append(main.all_books, new_book)
            
            # Write the information for the new book to the data file
            
            Books_Data = open(PATH, "a")
            Books_Data.write(string.capwords(title_in) + "," + string.capwords(lname_in) + "," + string.capwords(fname_in) + "," + string.capwords(series_in) + "," + number_in + "," + genre_in + "," + isOwned_in + "," + status_in + "," + rating_in + ",1\n")
            Books_Data.close()
            
            # Reset the information after the book has been added
            
            clear()
            
            # Confirm that the book was added
            
            message_variable.set(string.capwords(title_in) + " was added!")
            message.configure(fg = "green")
    
    def clear ():
        
        title_entry.delete(0, tk.END)
        lname_entry.delete(0, tk.END)
        fname_entry.delete(0, tk.END)
        series_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)
        genre_variable.set(genre_options[0])
        isOwned_variable.set(isOwned_options[0])
        status_variable.set(status_options[0])
        rating_variable.set(rating_options[0])
        
        message_variable.set("Ready to add books!")
        message.configure(fg = "black")
    
    def close ():
        
        add_book_window.destroy()
    
    # Create a button frame
    
    buttons_frame = tk.Frame(master = main_frame, bg = COLOUR)
    buttons_frame.pack(fill = "y")
    
    # Create and place the buttons
    
    add_button = tk.Button(text = "Add", master = buttons_frame, command = add, padx = 10, pady = 5, relief = BTN_STYLE)
    add_button.grid(row = 0, column = 0, padx = 5, pady = 15)
    
    clear_button = tk.Button(text = "Clear", master = buttons_frame, command = clear, padx = 10, pady = 5, relief = BTN_STYLE)
    clear_button.grid(row = 0, column = 1, padx = 5, pady = 15)
    
    close_button = tk.Button(text = "Close", master = buttons_frame, command = close, padx = 10, pady = 5, relief = BTN_STYLE)
    close_button.grid(row = 0, column = 2, padx = 5, pady = 15)

def open_edit_book_window ():
    
    global main_window
    
    found_books = []
    found_book  = None
    found_i     = None
    
    load_books()
    
    # Create and position the window
    
    edit_book_window = tk.Toplevel()
    
    position_window(edit_book_window, 375, 375)
    
    # Configure the window
    
    edit_book_window.title("Edit a Book")
    edit_book_window.iconphoto(False, tk.PhotoImage(master = edit_book_window, file = "./images/icon.png"))
    
    # Focus the window
    
    edit_book_window.transient(main_window)
    edit_book_window.grab_set()
    
    # Create the main frame
    
    main_frame  = tk.Frame(master = edit_book_window, bg = COLOUR)
    main_frame.pack(expand = True)
    
    # Create the message frame
    
    message_frame = tk.Frame(master = main_frame, bg = COLOUR)
    message_frame.pack()
    
    message_variable = tk.StringVar()
    message_variable.set("Ready to edit books!")
    
    message = tk.Label(master = message_frame, textvariable = message_variable, bg = COLOUR, font = "Helvetica 10 bold")
    message.pack(pady = 12)
    
    # Create labels and text fields for user input
    
    input_frame = tk.Frame(master = main_frame, bg = COLOUR)
    input_frame.pack()
    
    # Create labels for input
    
    title_label   = tk.Label(text = "Title:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    lname_label   = tk.Label(text = "Last Name:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    fname_label   = tk.Label(text = "First Name:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    series_label  = tk.Label(text = "Series:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    number_label  = tk.Label(text = "#:", master = input_frame, width = 3, anchor = "c", bg = COLOUR)
    genre_label   = tk.Label(text = "Genre:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    isOwned_label = tk.Label(text = "Owned:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    status_label  = tk.Label(text = "Status:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    rating_label  = tk.Label(text = "Rating:", master = input_frame, width = 12, anchor = "w", bg = COLOUR)
    
    # Create entries for input
    
    title_entry   = tk.Entry(master = input_frame, width = 21, relief = BTN_STYLE)
    lname_entry   = tk.Entry(master = input_frame, width = 27, relief = BTN_STYLE)
    fname_entry   = tk.Entry(master = input_frame, width = 27, relief = BTN_STYLE)
    series_entry  = tk.Entry(master = input_frame, width = 19, relief = BTN_STYLE)
    number_entry  = tk.Entry(master = input_frame, width = 5, relief = BTN_STYLE)
    
    # Create option menu variables for input
    
    genre_options = ["Fiction (Adult)", "Fiction (Teen)", "Fiction (Youth)", "Fantasy", "Mental Health", "Romance"]
    genre_variable = tk.StringVar()
    
    isOwned_options = ["Yes", "No"]
    isOwned_variable = tk.StringVar()
    
    status_options = ["Read", "Reading", "Not Read"]
    status_variable = tk.StringVar()
    
    rating_options = [1, 2, 3, 4, 5, 10]
    rating_variable = tk.StringVar()
    
    # Create option menus for input
    
    genre_menu = ttk.OptionMenu(input_frame, genre_variable, "", *genre_options)
    genre_menu.config(width = 27)
    
    isOwned_menu = ttk.OptionMenu(input_frame, isOwned_variable, "", *isOwned_options)
    isOwned_menu.config(width = 27)
    
    status_menu = ttk.OptionMenu(input_frame, status_variable, "", *status_options)
    status_menu.config(width = 27)
    
    rating_menu = ttk.OptionMenu(input_frame, rating_variable, "", *rating_options)
    rating_menu.config(width = 27)
    
    # Place all input widgets on grid
    
    title_label.grid(row = 0, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    title_entry.grid(row = 0, column = 1, columnspan = 2, pady = 3, sticky = tk.NE + tk.SW)
    
    lname_label.grid(row = 1, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    lname_entry.grid(row = 1, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    fname_label.grid(row = 2, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    fname_entry.grid(row = 2, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    series_label.grid(row = 3, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    series_entry.grid(row = 3, column = 1, pady = 3, sticky = tk.NE + tk.SW)
    
    number_label.grid(row = 3, column = 2, pady = 3, sticky = tk.NE + tk.SW)
    number_entry.grid(row = 3, column = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    genre_label.grid(row = 4, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    genre_menu.grid(row = 4, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    isOwned_label.grid(row = 5, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    isOwned_menu.grid(row = 5, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    status_label.grid(row = 6, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    status_menu.grid(row = 6, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    rating_label.grid(row = 7, column = 0, pady = 3, sticky = tk.NE + tk.SW)
    rating_menu.grid(row = 7, column = 1, columnspan = 3, pady = 3, sticky = tk.NE + tk.SW)
    
    # Create and place "Find" button
    
    def find ():
        
        global found_books, found_book, found_i
        
        title_in = title_entry.get()
        
        if title_in == "":
            
            message_variable.set("Title cannot be blank!")
            message.configure(fg = "red")
        
        else:
            
            found_books = [(main.all_books[i], i) for i in range(len(main.all_books)) if title_in.lower() == main.all_books[i].title.lower()[:len(title_in)]]
            
            if len(found_books) != 0:
                
                found_book = found_books[0][0]
                found_i    = found_books[0][1]
                
                message_variable.set(found_book.title + " was found on line " + str(found_i + 2) + "!")
                message.configure(fg = "green")
                
                title_entry.delete(0, tk.END)
                title_entry.insert(tk.INSERT, found_book.title)
                
                lname_entry.delete(0, tk.END)
                lname_entry.insert(tk.INSERT, found_book.lname)
                
                fname_entry.delete(0, tk.END)
                fname_entry.insert(tk.INSERT, found_book.fname)
                
                series_entry.delete(0, tk.END)
                series_entry.insert(tk.INSERT, found_book.series)
                
                number_entry.delete(0, tk.END)
                number_entry.insert(tk.INSERT, found_book.number)
                
                genre_variable.set(found_book.genre)
                
                if found_book.isOwned == "1":
                    
                    isOwned_variable.set("Yes")
                
                else:
                    
                    isOwned_variable.set("No")
                
                status_variable.set(found_book.status)
                rating_variable.set(found_book.rating)
            
            else:
                
                message_variable.set("No book found!")
                message.configure(fg = "red")
        
        return 0
    
    find_button = tk.Button(text = "Find", master = input_frame, command = find, padx = 2, pady = 0, relief = BTN_STYLE)
    find_button.grid(row = 0, column = 3, padx = (5, 0), pady = 3, sticky = tk.NE + tk.SW)
    
    # Button functions
    
    def save ():
        
        global found_books, found_book, found_i
        
        title_in = title_entry.get()
        
        if title_in == "":
            
            message_variable.set("Title cannot be blank!")
            message.configure(fg = "red")
        
        else:
            
            if len(found_books) != 0:
                
                # Read in the edited information
                
                title_in   = title_entry.get()
                lname_in   = lname_entry.get()
                fname_in   = fname_entry.get()
                series_in  = series_entry.get()
                number_in  = number_entry.get()
                genre_in   = genre_variable.get()
                isOwned_in = isOwned_variable.get()
                status_in  = status_variable.get()
                rating_in  = rating_variable.get()
                
                # Correct user input
                
                if lname_in == "":
                    
                    lname_in = "0"
                
                if fname_in == "":
                    
                    fname_in = "0"
                
                if series_in == "":
                    
                    series_in = "0"
                
                if number_in == "":
                    
                    number_in = "0"
                
                if isOwned_in == "Yes":
                    
                    isOwned_in = "1"
                
                else:
                    
                    isOwned_in = "0"
                
                # Create the edited book object
                
                edited_book = Book(title_in, lname_in, fname_in, series_in, number_in, genre_in, isOwned_in, status_in, rating_in, 1)
                
                # Edit the book in the data file
                
                Book_Data  = open(PATH, "r")
                book_lines = Book_Data.readlines()
                Book_Data.close
                
                # Delete the existing entry
                
                del book_lines[found_i + 1]
                
                # Add a new entry in its place
                
                edited_book_line = string.capwords(title_in) + "," + string.capwords(lname_in) + "," + string.capwords(fname_in) + "," + string.capwords(series_in) + "," + number_in + "," + genre_in + "," + isOwned_in + "," + status_in + "," + rating_in + ",1\n"
                
                book_lines.insert(found_i + 1, edited_book_line)
                
                Book_Data  = open(PATH, "w")
                book_lines = "".join(book_lines)
                Book_Data.write(book_lines)
                Book_Data.close()
                
                # Edit the book in the list of books
                
                main.all_books[found_i] = edited_book
                
                # Confirm that the book was edited
                
                message_variable.set(found_book.title + " was edited!")
                message.configure(fg = "green")
                
                # If the book has been newly marked "Read", celebrate
                
                if (found_book.status == "Reading" or found_book.status == "Not Read") and edited_book.status == "Read":
                    
                    open_read_book_window(edited_book.title)
                
                # Clear the entry fields
                
                lname_entry.delete(0, tk.END)
                fname_entry.delete(0, tk.END)
                series_entry.delete(0, tk.END)
                number_entry.delete(0, tk.END)
                genre_variable.set("")
                isOwned_variable.set("")
                status_variable.set("")
                rating_variable.set("")
                
                # Reset the found book
                
                found_books = []
                found_book  = None
                found_i     = None
            
            else:
                
                message_variable.set("No book saved!")
                message.configure(fg = "red")
        
        return 0
    
    def delete ():
        
        global found_books, found_book, found_i
        
        title_in = title_entry.get()
        
        if title_in == "":
            
            message_variable.set("Title cannot be blank!")
            message.configure(fg = "red")
        
        else:
            
            if len(found_books) != 0:
                
                # Remove the book from the data file
                
                Book_Data  = open(PATH, "r")
                book_lines = Book_Data.readlines()
                Book_Data.close
                
                del book_lines[found_i + 1]
                
                Book_Data  = open(PATH, "w")
                book_lines = "".join(book_lines)
                Book_Data.write(book_lines)
                Book_Data.close()
                
                # Remove the book from the list of books so it is not found again
                
                main.all_books = np.delete(main.all_books, found_i)
                
                # Clear the entry fields
                
                title_entry.delete(0, tk.END)
                lname_entry.delete(0, tk.END)
                fname_entry.delete(0, tk.END)
                series_entry.delete(0, tk.END)
                number_entry.delete(0, tk.END)
                genre_variable.set("")
                isOwned_variable.set("")
                status_variable.set("")
                rating_variable.set("")
                
                # Confirm that the book was deleted
                
                message_variable.set(found_book.title + " was deleted!")
                message.configure(fg = "red")
                
                # Reset the found book
                
                found_books = []
                found_book  = None
                found_i     = None
            
            else:
                
                message_variable.set("No book deleted!")
                message.configure(fg = "red")
        
        return 0
    
    def clear ():
        
        global found_books, found_book, found_i
        
        found_books = []
        found_book  = None
        found_i     = None
        
        title_entry.delete(0, tk.END)
        lname_entry.delete(0, tk.END)
        fname_entry.delete(0, tk.END)
        series_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)
        genre_variable.set("")
        isOwned_variable.set("")
        status_variable.set("")
        rating_variable.set("")
        
        message_variable.set("Ready to edit books!")
        message.configure(fg = "black")
    
    def close ():
        
        global found_books, found_book, found_i
        
        found_books = []
        found_book  = None
        found_i     = None
        
        edit_book_window.destroy()
    
    # Create a button frame
    
    buttons_frame = tk.Frame(master = main_frame, bg = COLOUR)
    buttons_frame.pack(fill = "y")
    
    # Create and place the buttons
    
    save_button = tk.Button(text = "Save", master = buttons_frame, command = save, padx = 10, pady = 5, relief = BTN_STYLE)
    save_button.grid(row = 0, column = 0, padx = 5, pady = 15)
    
    delete_button = tk.Button(text = "Delete", master = buttons_frame, command = delete, padx = 10, pady = 5, bg = "pink", relief = BTN_STYLE)
    delete_button.grid(row = 0, column = 1, padx = 5, pady = 15)
    
    clear_button = tk.Button(text = "Clear", master = buttons_frame, command = clear, padx = 10, pady = 5, relief = BTN_STYLE)
    clear_button.grid(row = 0, column = 2, padx = 5, pady = 15)
    
    close_button = tk.Button(text = "Close", master = buttons_frame, command = close, padx = 10, pady = 5, relief = BTN_STYLE)
    close_button.grid(row = 0, column = 3, padx = 5, pady = 15)

def open_read_book_window (title_in):
    
    global main_window, firework_image
    
    read_book_window = tk.Toplevel()
    
    position_window(read_book_window, 500, 170)
    
    # Configure the window
    
    read_book_window.title("You Read a Book!")
    read_book_window.iconphoto(False, tk.PhotoImage(master = read_book_window, file = "./images/icon.png"))
    
    # Focus the window
    
    read_book_window.transient(main_window)
    read_book_window.grab_set()
    
    # Create the main frame
    
    main_frame = tk.Frame(master = read_book_window, bg = COLOUR)
    main_frame.place(relx = 0.5, rely = 0.5, anchor = "c")
    
    # Create the frame
    
    read_book_frame = tk.Frame(master = main_frame, bg = COLOUR)
    read_book_frame.pack(expand = True, fill = "y", padx = 10)
    
    # Place the contents
    
    firework_image = Image.open("./images/firework.png")
    firework_image = firework_image.resize((70, 70), Image.ANTIALIAS)
    firework_image = ImageTk.PhotoImage(firework_image)
    
    firework_left_label = tk.Label(master = read_book_frame, bg = COLOUR, image = firework_image, width = 70, height = 70)
    firework_left_label.grid(row = 0, column = 0)
    
    read_book_label = tk.Label(text = "You read " + title_in + "!!!", master = read_book_frame, wraplength = 450, justify = "center", bg = COLOUR)
    read_book_label.grid(row = 0, column = 1, padx = 30)
    
    firework_right_label = tk.Label(master = read_book_frame, bg = COLOUR, image = firework_image, width = 70, height = 70)
    firework_right_label.grid(row = 0, column = 2)
    
    # Create and place a "Yay" button
    
    def close_window ():
        
        read_book_window.destroy()
    
    button_frame = tk.Frame(master = main_frame, bg = COLOUR)
    button_frame.pack(expand = True, fill = "both")
    
    yay_button = tk.Button(text = "Yay!", master = button_frame, command = close_window, font = "12", relief = BTN_STYLE)
    yay_button.pack(anchor = "c", ipadx = 5, ipady = 5)
    
    read_book_window.wait_window(read_book_window)

def open_help_window ():
    
    global main_window
    
    HELP_COLOUR = "pink"
    
    # Create and position the window
    
    help_window = tk.Toplevel()
    
    position_window(help_window, 475, 275)
    
    # Configure the window
    
    help_window.title("Help")
    help_window.configure(bg = HELP_COLOUR)
    help_window.iconphoto(False, tk.PhotoImage(master = help_window, file = "./images/icon.png"))
    
    # Focus the window
    
    help_window.transient(main_window)
    help_window.grab_set()
    
    # Create the frame
    
    help_frame = tk.Frame(master = help_window, bg = HELP_COLOUR, padx = 20, pady = 20)
    help_frame.pack(expand = True, fill = "both")
    
    # Create an information frame
    
    information_frame = tk.Frame(master = help_frame, bg = HELP_COLOUR)
    information_frame.pack()
    
    # Write information about the program
    
    Christmas_label = tk.Label(text = "Merry Christmas 2020!", master = information_frame, bg = HELP_COLOUR, font = "Helvetica 10")
    Christmas_label.pack(pady = 25)
    
    version_label = tk.Label(text = "Version " + VERSION, master = information_frame, bg = HELP_COLOUR, font = "Helvetica 10")
    version_label.pack()
    
    date_label = tk.Label(text = "Last updated: " + DATE, master = information_frame, bg = HELP_COLOUR, font = "Helvetica 10")
    date_label.pack()
    
    # Place a message to confirm a back up was created
    
    message_variable = tk.StringVar()
    message_variable.set("Data is stored in " + PATH)
    
    message = tk.Label(master = help_frame, textvariable = message_variable, bg = HELP_COLOUR, font = "Helvetica 10")
    message.pack(pady = 25)
    
    # Create a button frame
    
    button_frame = tk.Frame(master = help_frame, bg = HELP_COLOUR)
    button_frame.pack()
    
    # Button functions
    
    def open_data_file ():
        
        global main_window
        
        # Load the books to check later if a book has been marked as read
        
        load_books()
        
        # Open the file in a text editor
        
        edit = sub.Popen(["Notepad", PATH])
        
        # Wait until the text editor is closed before resuming
        
        edit.wait()
    
    def back_up ():
        
        backup_file = "./data/books_backup.txt"
        
        copy2(PATH, backup_file)
        
        message_variable.set("A back-up was created in " + backup_file)
        message.configure(font = "Helvetica 10 bold")
    
    def close_window ():
        
        help_window.destroy()
    
    # Create and place buttons
    
    edit_manually_button = tk.Button(text = "Edit Manually", master = button_frame, command = open_data_file, font = "Helvetica 11", relief = BTN_STYLE)
    edit_manually_button.grid(row = 0, column = 0, padx = 5, ipadx = 5, ipady = 5)
    
    backup_button = tk.Button(text = "Back up Data", master = button_frame, command = back_up, font = "Helvetica 11", relief = BTN_STYLE)
    backup_button.grid(row = 0, column = 1, padx = 5, ipadx = 5, ipady = 5)
    
    close_button = tk.Button(text = "Close", master = button_frame, command = close_window, font = "Helvetica 11", relief = BTN_STYLE)
    close_button.grid(row = 0, column = 2, padx = 5, ipadx = 5, ipady = 5)

def open_new_book_window (new_book_in, book_before_in = "", book_after_in = "", end = False):
    
    # Create and position the window
    
    new_book_window = tk.Toplevel()
    
    position_window(new_book_window, 500, 160)
    
    # Configure the window
    
    new_book_window.title("New Book")
    new_book_window.iconphoto(False, tk.PhotoImage(master = new_book_window, file = "./images/icon.png"))
    
    # Focus the window
    
    new_book_window.transient(main_window)
    new_book_window.grab_set()
    
    # Create the main frame
    
    main_frame = tk.Frame(master = new_book_window, bg = COLOUR)
    main_frame.place(relx = 0.5, rely = 0.5, anchor = "c")
    
    # Create the frame
    
    new_book_frame = tk.Frame(master = main_frame, bg = COLOUR, padx = 10, pady = 10)
    new_book_frame.pack(expand = True, fill = "y", padx = 10)
    
    # Print the information
    
    if not book_before_in and not end:
        
        book_placement = "\"" + new_book_in + "\" goes at the beginning of your collection"
    
    elif book_before_in and not end:
        
        book_placement = "\"" + new_book_in + "\" goes in between \"" + book_before_in + "\" and \"" + book_after_in + "\""
    
    else:
        
        book_placement = "\"" + new_book_in + "\" goes at the end of your collection"
    
    new_book_label = tk.Label(text = book_placement, master = new_book_frame, wraplength = 450, justify = "center", bg = COLOUR)
    new_book_label.pack()
    
    # Create and place an ok button
    
    def close_window ():
        
        new_book_window.destroy()
    
    button_frame = tk.Frame(master = main_frame, bg = COLOUR)
    button_frame.pack(expand = True, fill = "both")
    
    ok_button = tk.Button(text = "Ok", master = button_frame, command = close_window, font = "12", relief = BTN_STYLE)
    ok_button.pack(anchor = "c", ipadx = 5, ipady = 5)
    
    new_book_window.wait_window(new_book_window)

def main ():
    
    # Load the book data
    
    load_books()
    
    # Open the main window
    
    open_main_window()

if __name__ == "__main__":
    
    main()
