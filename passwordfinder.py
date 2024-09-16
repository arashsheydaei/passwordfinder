import tkinter as tk
import itertools
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread

# Function to check if the guessed password matches the real password
def check_password(real_password, guessed_password):
    return real_password == guessed_password

# Worker function for brute force attempt
def brute_force_worker(charset, real_password, length):
    for guess in itertools.product(charset, repeat=length):
        guessed_password = ''.join(guess)
        if check_password(real_password, guessed_password):
            return guessed_password
    return None

# Function to start the brute-force attack and display the guessed password
def start_attack():
    real_password = password_entry.get()
    charset = '0123456789'
    max_length = 4
    
    guessed_password_label.config(text="Trying to guess the password...")
    root.update()

    start_time = time.time()

    def attack():
        nonlocal start_time
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(brute_force_worker, charset, real_password, length) for length in range(1, max_length + 1)]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    guessed_password_label.config(text=f"Password found: {result} in {elapsed_time:.2f} seconds")
                    return
        guessed_password_label.config(text="Password not found")

    Thread(target=attack).start()
    start_timer(start_time)

# Function to update the timer label
def start_timer(start_time):
    def update_timer():
        while guessed_password_label.cget("text") == "Trying to guess the password...":
            elapsed_time = time.time() - start_time
            timer_label.config(text=f"Elapsed time: {elapsed_time:.2f} seconds")
            time.sleep(0.1)
            root.update()
    Thread(target=update_timer).start()

# Create the main window
root = tk.Tk()
root.title("Password Guesser")

# Create and place the widgets
tk.Label(root, text="Enter your password (4 digits):").pack(pady=5)
password_entry = tk.Entry(root, show='*')
password_entry.pack(pady=5)

start_button = tk.Button(root, text="Start Guessing", command=start_attack)
start_button.pack(pady=20)

guessed_password_label = tk.Label(root, text="Trying to guess the password...")
guessed_password_label.pack(pady=5)

timer_label = tk.Label(root, text="Elapsed time: 0.00 seconds")
timer_label.pack(pady=5)

# Run the application
root.mainloop()
