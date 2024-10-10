"""
This program implements the insertion sort algorithm and prints out each step of the process.

The function insertion_sort_with_explanation takes in an array and sorts it using the insertion sort algorithm. It prints out the state of the array at each step of the process, explaining what's happening.
"""

def insertion_sort_with_explanation(arr):
    """
    Sorts the given array using insertion sort and prints out each step of the process.

    :param arr: The array to be sorted
    :type arr: list
    :return: The sorted array
    :rtype: list
    """
    print("Initial array:", arr)
    print("\nBeginning Insertion Sort:\n")

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        print(f"Step {i}:")
        print(f"  Current element to insert: {key}")
        print(f"  Current array state: {arr}")
        
        if arr[j] <= key:
            print(f"  {key} is already in the correct position.")
        else:
            print(f"  Finding the correct position for {key}:")
        
        while j >= 0 and arr[j] > key:
            print(f"    Comparing {key} with {arr[j]}")
            print(f"    {arr[j]} > {key}, so moving {arr[j]} to the right")
            arr[j + 1] = arr[j]
            j -= 1
            print(f"    Current array state: {arr}")
        
        if j + 1 != i:
            arr[j + 1] = key
            print(f"  Inserted {key} at index {j + 1}")
            print(f"  Array after insertion: {arr}")
        
        print()  # Empty line for readability

    print("Sorting complete. Final array:", arr)


# Test the function
if __name__ == "__main__":
    test_array = [64, 34, 25, 12, 22, 11, 90]
    insertion_sort_with_explanation(test_array)
