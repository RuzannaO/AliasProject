import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
import random

class SetupWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Setup")

        # Set the size of the window
        self.root.geometry("800x600")  # Width x Height

        # Center the window on the screen
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates for the center
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the geometry of the window to be centered
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        self.time_limit = 60  # Default time limit
        self.num_words = 5  # Default number of words to display
        self.winning_points = 10  # Default winning points

        self.create_widgets()

    def create_widgets(self):
        """Create the setup window components."""
        # Title label
        self.title_label = tk.Label(self.root, text="Setup Game", font=("Arial", 24))
        self.title_label.pack(pady=10)

        # Time limit label and entry
        self.time_label = tk.Label(self.root, text="Time limit (seconds):", font=("Arial", 14))
        self.time_label.pack(pady=5)
        self.time_entry = tk.Entry(self.root, font=("Arial", 14))
        self.time_entry.insert(0, str(self.time_limit))  # Default value
        self.time_entry.pack(pady=5)

        # Number of words label and entry
        self.num_words_label = tk.Label(self.root, text="Number of words per round:", font=("Arial", 14))
        self.num_words_label.pack(pady=5)
        self.num_words_entry = tk.Entry(self.root, font=("Arial", 14))
        self.num_words_entry.insert(0, str(self.num_words))  # Default value
        self.num_words_entry.pack(pady=5)

        # Winning points label and entry
        self.winning_points_label = tk.Label(self.root, text="Winning points:", font=("Arial", 14))
        self.winning_points_label.pack(pady=5)
        self.winning_points_entry = tk.Entry(self.root, font=("Arial", 14))
        self.winning_points_entry.insert(0, str(self.winning_points))  # Default value
        self.winning_points_entry.pack(pady=5)

        # Start button
        self.start_button = tk.Button(self.root, text="Start Game", font=("Arial", 14), command=self.start_game)
        self.start_button.pack(pady=20)

    def start_game(self):
        """Start the game with the provided time limit, number of words, and winning points."""
        try:
            time_limit = int(self.time_entry.get())  # Get the time limit from the user input
            num_words = int(self.num_words_entry.get())  # Get the number of words from the user input
            winning_points = int(self.winning_points_entry.get())  # Get the winning points from the user input

            if time_limit <= 0 or num_words <= 0 or winning_points <= 0:
                raise ValueError("Time limit, number of words, and winning points must be greater than 0.")

            # Close the setup window and start the game
            self.root.quit()
            self.root.destroy()

            # Launch the AliasGame with the user settings
            self.launch_game(time_limit, num_words, winning_points)
        except ValueError:
            custom_messagebox("Invalid Input", "Please enter valid positive integers for all fields.")

    def launch_game(self, time_limit, num_words, winning_points):
        """Launch the main game with the specified settings."""
        root = tk.Tk()
        game = AliasGame(root, time_limit, num_words, winning_points)
        root.mainloop()

class AliasGame:
    def __init__(self, root, time_limit, num_words, winning_points):
        self.root = root
        self.root.title("Alias Game")

        # Set the size of the window
        self.root.geometry("800x600")  # Width x Height

        # Center the window on the screen
        window_width = 800
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates for the center
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the geometry of the window to be centered
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        self.root.title("Alias Game")
        self.root.configure(bg="lightblue")

        self.word_cards = self.load_words_from_file("words.txt")  # Load words from file
        self.current_card_index = 0  # Index of the current card
        self.team_turn = 1  # Current team's turn (1 or 2)
        self.initial_time_limit = time_limit  # Initial time limit for each turn (from setup)
        self.time_limit = time_limit  # Time limit for the current turn
        self.num_words = num_words  # Number of words to display (from setup)
        self.winning_points = winning_points  # Points needed to win
        self.timer_id = None  # ID of the timer callback

        self.team1_points = 0  # Points for Team 1
        self.team2_points = 0  # Points for Team 2

        # Initialize the GUI components
        self.create_widgets()
        self.start_timer()  # Start the timer when the game begins

    def load_words_from_file(self, file_path):
        """Load words from the specified file and return a shuffled list of words."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:  # Ensure UTF-8 encoding
                words = [line.strip() for line in file.readlines()]
            return words  # Return the words read from the file
        except UnicodeDecodeError:
            custom_messagebox("Error", "The file encoding is incorrect. Please use UTF-8 encoding.")
            self.root.quit()
            return []

    def shuffle_and_get_next_words(self):
        """Shuffle the words and return the next 'num_words' words."""
        if len(self.word_cards) < self.num_words:
            # If not enough words are left, return all remaining words
            words_for_this_round = self.word_cards[:]
            self.word_cards = []  # Empty the list as all words are used
        else:
            random.shuffle(self.word_cards)  # Shuffle the remaining words
            words_for_this_round = self.word_cards[:self.num_words]
            # Remove the words that will be used this round from the list
            self.word_cards = self.word_cards[self.num_words:]

        return words_for_this_round

    def create_widgets(self):
        """Create and pack the widgets for the game."""
        # Title label
        self.title_label = tk.Label(self.root, text="Alias Game", font=("Arial", 24))
        self.title_label.pack(pady=10)

        # Team turn label
        self.team_label = tk.Label(self.root, text=f"Team {self.team_turn}'s Turn", font=("Arial", 16))
        self.team_label.pack(pady=5)

        # Timer label
        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.time_limit}s", font=("Arial", 16))
        self.timer_label.pack(pady=5)

        # Points labels (top right corner)
        self.points_label = tk.Frame(self.root)
        self.points_label.pack(side=tk.TOP, anchor="ne", padx=10, pady=10)

        self.team1_points_label = tk.Label(self.points_label, text=f"Team 1: {self.team1_points}", font=("Arial", 16),
                                           width=20)
        self.team1_points_label.pack(side=tk.TOP, padx=20, pady=2, anchor="center")

        self.team2_points_label = tk.Label(self.points_label, text=f"Team 2: {self.team2_points}", font=("Arial", 16),
                                           width=20)
        self.team2_points_label.pack(side=tk.TOP, padx=20, pady=2, anchor="center")

        # Frame to hold word buttons
        self.card_frame = tk.Frame(self.root)
        self.card_frame.pack(pady=20)

        # Restart Game button
        self.restart_button = tk.Button(self.root, text="Restart Game", font=("Arial", 14), background="light yellow", command=self.restart_game)
        self.restart_button.pack(pady=10)

        # Button to switch to the next team
        # self.next_team_button = tk.Button(self.root, text="Next Team", command=self.next_team, state=tk.DISABLED)
        # self.next_team_button.pack(pady=10)

        # Display the first card
        self.display_card()

    def restart_game(self):
        """Restart the game and return to the setup window."""
        play_again = messagebox.askyesno("Restart Game", "Are you sure you want to restart the game?")
        if play_again:
            self.root.quit()  # Close the current game window
            self.root.destroy()  # Destroy the game window
            root = tk.Tk()  # Create a new window
            SetupWindow(root)  # Open the setup window
            root.mainloop()  # Start the setup window loop
        # If "No" is selected, the game won't restart, and the window stays open

    def display_card(self):
        """Display the current card with its words as buttons."""
        # Clear the current card (words)
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        words_for_this_round = self.shuffle_and_get_next_words()
        if not words_for_this_round:  # If no words are left, end the game
            self.end_game("No more words available! Game Over.")
            return

        for word in words_for_this_round:
            # Create the button
            word_button = tk.Button(
                self.card_frame, text=word, width=20, height=2, font=("Arial", 14)
            )
            # Assign the command after the button is created
            word_button.config(command=lambda b=word_button: self.word_guessed(b))
            # Pack the button
            word_button.pack(pady=0)

    def word_guessed(self, button):
        """Mark a word as guessed and update points."""
        button.config(state=tk.DISABLED)  # Disable the button for the guessed word
        remaining_buttons = [b for b in self.card_frame.winfo_children() if b.cget("state") != tk.DISABLED]

        # Update points based on the team turn
        if self.team_turn == 1:
            self.team1_points += 1
        else:
            self.team2_points += 1

        # Update the points labels
        self.team1_points_label.config(text=f"Team 1: {self.team1_points}")
        self.team2_points_label.config(text=f"Team 2: {self.team2_points}")




        # # Check if any team has reached the winning points
        # if self.team1_points >= self.winning_points:
        #     self.end_game("Team 1 Wins!")
        # elif self.team2_points >= self.winning_points:
        #     self.end_game("Team 2 Wins!")

        # If no buttons are left enabled, move to the next card
        if not remaining_buttons:  # If no buttons are left enabled, go to the next card
            self.next_card()

    def next_card(self):
        """Move to the next card or end the game if no cards remain."""
        self.current_card_index += 1
        if self.current_card_index * self.num_words >= len(self.word_cards):
            custom_messagebox("Game Over", "No more cards left! Game over!")
            self.root.quit()
        else:
            self.display_card()

    def start_timer(self):
        """Start the countdown timer for the current team's turn."""
        self.timer_label.config(text=f"Time Left: {self.time_limit}s")
        if self.time_limit > 0:
            self.time_limit -= 1
            self.timer_id = self.root.after(1000, self.start_timer)
        else:
            self.time_limit_up()

    def time_limit_up(self):
        """Handle time limit up."""
        custom_messagebox("Time's Up!", f"Time is up for Team {self.team_turn}!")

        if self.team_turn == 2:
            print(self.team1_points)
            print(self.team2_points)
            if self.team1_points > self.team2_points and self.team1_points >= self.winning_points:
                self.end_game("Team 1 Wins!")
            elif self.team1_points < self.team2_points and self.team2_points >= self.winning_points:
                    self.end_game("Team 2 Wins!")
            elif self.team1_points == self.team2_points:
                pass


        def on_ready():
            """Callback when the user clicks 'Ready'."""
            self.next_team()  # Move to the next team after user clicks 'Ready'

        # Show the 'Ready?' message box and call 'on_ready' when OK is clicked
        ready_box = Toplevel()
        ready_box.title("Ready?")
        # custom_messagebox("Ready?",message="Ready?",button_text="Yes")

        # Set the size and center the window
        window_width = 300
        window_height = 150
        screen_width = ready_box.winfo_screenwidth()
        screen_height = ready_box.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        ready_box.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # Add a message and button
        label = tk.Label(ready_box, text="Ready?", font=("Arial", 14))
        label.pack(pady=20)
        ok_button = tk.Button(ready_box, text="OK", command=lambda: [ready_box.destroy(), on_ready()])
        ok_button.pack(pady=10)

        # Make modal
        ready_box.transient(self.root)
        ready_box.grab_set()

    def next_team(self):
        """Switch to the next team and reset the timer and card."""
        if self.team_turn == 1:
            self.team_turn = 2
        else:
            self.team_turn = 1

        self.time_limit = self.initial_time_limit  # Reset time limit for the new team
        self.start_timer()  # Restart the timer
        self.display_card()  # Display new card for the new team

        # Update UI for the next team
        self.team_label.config(text=f"Team {self.team_turn}'s Turn")
        # self.next_team_button.config(state=tk.DISABLED)
        # self.next_team_button.config(state=tk.NORMAL)

    def end_game(self, winner_message):
        """End the game and display a message box with restart options."""
        play_again = messagebox.askyesno("Game Over", f"{winner_message}\nDo you want to start the game again?")
        if play_again:
            self.root.destroy()  # Close the current game window
            # Restart the setup window
            root = tk.Tk()
            SetupWindow(root)
            root.mainloop()
        else:
            print("Cleanup")
            self.cleanup_and_exit()


    def cleanup_and_exit(self):
        """Forcefully destroy all open windows and cancel scheduled callbacks."""
        try:
            # Cancel any scheduled timer callbacks
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                print("timer_cancel")

            # Destroy all Toplevel windows if they exist
            for widget in self.root.winfo_children():
                if isinstance(widget, Toplevel):
                    widget.destroy()
                    print("widget_destroy")
        except tk.TclError:
            print("errror")
            # Ignore errors if the application is already destroyed
            pass
        finally:
            # Ensure the main window is destroyed
            print("root_quit and destroy")
            self.root.quit()
            self.root.destroy()


def custom_messagebox(title, message, bg_color="lightblue", text_color="black", button_text="OK"):
    """Display a custom modal message box."""
    msg_box = Toplevel()
    msg_box.title(title)

    # Set the size and center the window
    window_width = 300
    window_height = 150
    screen_width = msg_box.winfo_screenwidth()
    screen_height = msg_box.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    msg_box.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Set the background color
    msg_box.configure(bg=bg_color)

    # Add a message label
    label = tk.Label(msg_box, text=message, font=("Arial", 14), bg=bg_color, fg=text_color)
    label.pack(pady=20)

    # Add an OK button to close the window
    ok_button = tk.Button(msg_box, text=f'{button_text}', command=msg_box.destroy)
    ok_button.pack(pady=10)

    # Make modal and ensure proper cleanup
    msg_box.transient()  # Associate the message box with the main window
    msg_box.grab_set()   # Prevent interactions with other windows
    msg_box.wait_window(msg_box)  # Wait until the message box is closed




# Start the game setup window
root = tk.Tk()
setup_window = SetupWindow(root)
root.mainloop()
