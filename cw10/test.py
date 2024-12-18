import tkinter as tk
import random

def player_choice(choice):
    player_label.config(text=f"Player: {choice}")
    computer_pick = random.choice(choices)
    computer_label.config(text=f"Computer: {computer_pick}")
    determine_winner(choice, computer_pick)

def determine_winner(player, computer):
    if player == computer:
        result_label.config(text="Draw!", fg="blue")
    elif (player == "Paper" and computer == "Rock") or \
         (player == "Rock" and computer == "Scissors") or \
         (player == "Scissors" and computer == "Paper"):
        result_label.config(text="You Win!", fg="green")
    else:
        result_label.config(text="You Lose!", fg="red")

root = tk.Tk()
root.title("Rock, Paper, Scissors")

choices = ["Paper", "Rock", "Scissors"]

player_label = tk.Label(root, text="Player: ", font=("Arial", 14))
player_label.pack(pady=10)
computer_label = tk.Label(root, text="Computer: ", font=("Arial", 14))
computer_label.pack(pady=10)

result_label = tk.Label(root, text="Result: ", font=("Arial", 16, "bold"))
result_label.pack(pady=20)

paper_button = tk.Button(root, text="Paper", font=("Arial", 12), command=lambda: player_choice("Paper"))
paper_button.pack(side=tk.LEFT, padx=20, pady=20)

rock_button = tk.Button(root, text="Rock", font=("Arial", 12), command=lambda: player_choice("Rock"))
rock_button.pack(side=tk.LEFT, padx=20, pady=20)

scissors_button = tk.Button(root, text="Scissors", font=("Arial", 12), command=lambda: player_choice("Scissors"))
scissors_button.pack(side=tk.LEFT, padx=20, pady=20)

root.mainloop()
