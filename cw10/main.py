import random
import tkinter as tk

def game_outcome(player, computer):
    if player == computer:
        result_text.config(text="Draw!", fg="grey")

    elif (player == "Paper" and computer == "Rock") or \
         (player == "Scissors" and computer == "Paper") or \
         (player == "Rock" and computer == "Scissors"):
        result_text.config(text="You Won!", fg="green")

    else:
        result_text.config(text="You Lost..", fg="red")

def handle_choices(player_choice):
    player_text.config(text=f"Player: {player_choice}")
    computer_choice = random.choice(choices)
    computer_text.config(text=f"Computer: {computer_choice}")

    game_outcome(player_choice, computer_choice)

BG_COLOR = "#dbd5d5"
BUTTON_COLOR = "#c98d8d"

choices = ["Paper", "Rock", "Scissors"]

root = tk.Tk()
root.title("RPS Game")
root.geometry("450x300")
root.configure(bg=BG_COLOR)

frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(expand=True)

player_text = tk.Label(frame, text="Player: ?", font=("Arial", 16), bg=BG_COLOR)
player_text.pack(pady=12)

computer_text = tk.Label(frame, text="Computer: ?", font=("Arial", 16), bg=BG_COLOR)
computer_text.pack(pady=12)

result_text = tk.Label(frame, text="Pick one!", font=("Arial", 18, "bold"), bg=BG_COLOR)
result_text.pack(pady=24)

button_frame = tk.Frame(frame, bg=BG_COLOR)
button_frame.pack(pady=24)

paper_button = tk.Button(button_frame, text="Paper", font=("Arial", 12), bg=BUTTON_COLOR, fg="black", width=8,
                         command=lambda: handle_choices("Paper"))
paper_button.pack(side=tk.LEFT, padx=8)

rock_button = tk.Button(button_frame, text="Rock", font=("Arial", 12), bg=BUTTON_COLOR, fg="black", width=8,
                        command=lambda: handle_choices("Rock"))
rock_button.pack(side=tk.LEFT, padx=8)

scissors_button = tk.Button(button_frame, text="Scissors", font=("Arial", 12), bg=BUTTON_COLOR, fg="black", width=8,
                            command=lambda: handle_choices("Scissors"))
scissors_button.pack(side=tk.LEFT, padx=8)

root.mainloop()