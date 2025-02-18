import threading
import time
# Function to simulate a time-consuming task
def print_numbers(n):
    for i in range(1, n):
        print(f"Printing number {i}")
        time.sleep(1)  # Simulate a delay of 1 second
# Function to simulate another task
def print_letters():
    for letter in 'Geeeeeeeeeeeks':
        print(f"Printing letter {letter}")
        time.sleep(1)  # Simulate a delay of 1 second
# Create two thread objects, one for each function
thread1 = threading.Thread(target=print_numbers, args=(10,))
thread2 = threading.Thread(target=print_numbers, args=(5,))
thread3 = threading.Thread(target=print_letters)

# Start the threads
thread1.start()
thread2.start()
thread3.start()

# The main thread waits for both threads to finish
thread1.join()
thread2.join()
thread3.join()

print("Both threads have finished.")