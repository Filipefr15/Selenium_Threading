import multiprocessing
# Function to square a number
def square(x):
    return x * x
if __name__ == "__main__":
    # Define a list of numbers
    numbers = [1, 2, 3, 4, 5, 6,7,8,9,10,11,12,13,14,15,16]

    # Create a multiprocessing pool
    with multiprocessing.Pool() as pool:
        # Use the map method to apply the 'square ' function to each number in parallel
        results = pool.map(square, numbers)
    # Print the results
    print(results)
