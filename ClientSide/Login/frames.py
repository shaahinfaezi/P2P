import tkinter
import customtkinter
from Login.functions import is_valid_chars_space, is_valid_chars, toggle_password, register_user, check_login, generate_temporary_password,request,getInvites,accept
from PIL import ImageTk, Image
from tkinter import messagebox
from CTkListbox import *

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_login_frame()

    def setup_login_frame(self):

        #Create Login FRAME
        self.login_frame = customtkinter.CTkFrame(master=self, width=320, height=380)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        #TOP text
        self.text = customtkinter.CTkLabel(master=self.login_frame, text="Log Into Account", font=('Century Gothic', 25))
        self.text.place(x=50, y=45)

        self.error_label = customtkinter.CTkLabel(master=self.login_frame, text="", font=('Century Gothic', 12), text_color="red")
        self.error_label.place(x=25, y=80)

        #Username entry block
        self.u_block = customtkinter.CTkEntry(master=self.login_frame, width=220, placeholder_text="Username")
        self.u_block.place(x=50, y=110)

        #Password entry block
        self.show_password_var = customtkinter.BooleanVar()
        self.p_block = customtkinter.CTkEntry(master=self.login_frame, width=220, placeholder_text="Password", show="*")
        self.p_block.place(x=50, y=150)

        #checkbox for showing password
        self.show_password = customtkinter.CTkCheckBox(master=self.login_frame, text="Show Password", font=('Century Gothic', 12), command=lambda: toggle_password(self.p_block, self.show_password_var), variable=self.show_password_var)
        self.show_password.place(x=50, y=190)


        #Login button
        self.login_button = customtkinter.CTkButton(master=self.login_frame, width=100, text="Login", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command=self.check_login_credentials)
        self.login_button.place(x=110, y=230)

        #Register button
        self.register_button = customtkinter.CTkButton(master=self.login_frame, width=100, text="Register", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command=self.master.open_register_frame)
        self.register_button.place(x=110, y=270)


    def check_login_credentials(self):
        # Get the username and password from the input fields
        username = self.u_block.get()
        password = self.p_block.get()

        # Call the check_login function from functions.py
        status,players,matches=check_login(username, password)
        if status:
            # Login successful, open LoggedInFrame
            self.master.open_loggedin_frame(players,matches)
        else:
            # Login failed, show an error message
            self.error_label.configure(text="Invalid username or password. Please try again.")

class RegisterFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_register_frame()

    def setup_register_frame(self):
        self.master.change_title("Registration")
        # Create the registration frame
        self.registration_frame = customtkinter.CTkFrame(master=self, width=320, height=380)
        self.registration_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.back_button = customtkinter.CTkButton(
            master=self,
            width=30,
            height=30,
            text="◀️",  # Use the left arrow character as the text
            corner_radius=6,
            fg_color="#3498db",
            text_color="#ffffff",
            hover_color="#2980b9",
            command=self.master.open_main_frame
        )
        self.back_button.place(x=10, y=10)

        # Entry fields for registration form
        self.name_entry = customtkinter.CTkEntry(master=self.registration_frame, width=220, placeholder_text="First Name")
        self.name_entry.place(x=50, y=50)

        self.surname_entry = customtkinter.CTkEntry(master=self.registration_frame, width=220, placeholder_text="Last Name")
        self.surname_entry.place(x=50, y=80)


        self.username_entry = customtkinter.CTkEntry(master=self.registration_frame, width=220, placeholder_text="Username")
        self.username_entry.place(x=50, y=140)

        self.p_block = customtkinter.CTkEntry(master=self.registration_frame, width=220, placeholder_text="Choose a password", show="*")
        self.p_block.place(x=50, y=200)


        # Registration button
        self.register_button = customtkinter.CTkButton(master=self.registration_frame, width=100, text="Register",
                                                  corner_radius=6,
                                                  fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9",
                                                  command=self.new_user_data)
        self.register_button.place(x=110, y=340)

    def new_user_data(self):
        # Get user inputs from the registration form
        first_name = self.name_entry.get()
        last_name = self.surname_entry.get()
        username = self.username_entry.get()
        password = self.p_block.get()

        if not first_name or not last_name or not username or not password:
            print("Please fill in all required fields.")
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        if not is_valid_chars_space(first_name) or not is_valid_chars_space(last_name):
            print("Name and Surname must contain only English letters.")
            messagebox.showerror("Error", "Use Only English letters.")
            return
        # Check if fields contain only English letters and standard characters
        if not is_valid_chars(username) or not is_valid_chars(password):
            print("Fields must contain only English letters and standard characters.")
            messagebox.showerror("Error", "Use Only English letters and standard characters without spaces.")
            return
        # Call the register_user function from functions.py
        if register_user(first_name, last_name, username, password):
            # Registration successful
            print("Registration successful!")
            messagebox.showinfo("Success", "Registration was successful!")
            self.registration_frame.place_forget()
            self.master.open_main_frame()
            return
        else:
            # Handle the case where the username or email is already taken
            print("Username is already in use.")
            messagebox.showerror("Error", "The username already exists.")
            return



class LoggedInFrame(customtkinter.CTkFrame):
    def __init__(self, master,players,matches):
        super().__init__(master)
        self.master = master
        self.players=players
        self.matches=matches
        self.setup_loggedin_frame()


    def setup_loggedin_frame(self):
        self.master.change_geometry("1920x1080")
        self.player_button = customtkinter.CTkButton(master=self.master, width=400, text="Player", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command= lambda: self.master.showPlayers(self.players))
        self.player_button.place(x=400, y=270)
        
        self.match_button = customtkinter.CTkButton(master=self.master, width=400, text="Viewer", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command= lambda: self.master.showMatches(self.matches))
        self.match_button.place(x=1120, y=270)

class PlayersFrame(customtkinter.CTkFrame):
    def __init__(self,master,players):
        super().__init__(master)
        self.master = master
        self.players=players
        self.setup_player_frame()

    def setup_player_frame(self):
        self.master.change_geometry("1920x1080")
        listbox = CTkListbox(self.master)
        listbox.pack(fill="both", expand=True)
        for i in range(len(self.players)):
            listbox.insert(i,self.players[i])
        listbox.select_multiple=False
        self.request_button = customtkinter.CTkButton(master=self.master, width=400, text="Request to play", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command= lambda: request(listbox.get(listbox.curselection())))
        self.request_button.place(x=400, y=470)
        self.invites_button = customtkinter.CTkButton(master=self.master, width=400, text="Game Invites", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command= lambda: self.master.showGameInvites(getInvites()))
        self.invites_button.place(x=1120, y=470)
 

        
class MatchesFrame(customtkinter.CTkFrame):
    def __init__(self, master,matches):
        super().__init__(master)
        self.master = master
        self.matches=matches
        self.setup_match_frame()

    def setup_match_frame(self):
        self.master.change_geometry("1920x1080")
        listbox = CTkListbox(self.master)
        listbox.pack(fill="both", expand=True)
        for i in range(len(self.matches)):
            listbox.insert(i,self.matches[i])
        # self.watch_button = customtkinter.CTkButton(master=self.master, width=400, text="Watch", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command= lambda: )
        # self.watch_button.place(x=760, y=670)
class GameInvitesFrame(customtkinter.CTkFrame):
    def __init__(self, master,invites,first):
        super().__init__(master)
        self.master = master
        self.invites=invites
        self.setup_invite_frame(first)

    def setup_invite_frame(self,first):
        self.master.change_geometry("1920x1080")
        listbox = CTkListbox(self.master)
        if first==False:
            listbox.pack(fill="both", expand=True)
        for i in range(len(self.invites)):
            listbox.insert(i,self.invites[i].msg)
        listbox.select_multiple=False
        self.request_button = customtkinter.CTkButton(master=self.master, width=200, text="Accept", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command= lambda: accept(listbox.get(listbox.curselection()),listbox))
        self.request_button.place(x=880, y=840)

