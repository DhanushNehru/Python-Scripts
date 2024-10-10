def selection_sort_with_explaination(arr):
    """
    Sorts the given array using selection sort and prints out each step of the process.

    :param arr: The array to be sorted
    :type arr: list
    :return: The sorted array
    :rtype: list
    """
    n = len(arr)
    
    print(f"Initial array: {arr}")
    print("\nStarting Selection Sort...")
    
    for i in range(n):
        print(f"\nIteration {i + 1}:")
        print(f"Current array: {arr}")
        
        # Find the minimum element in the unsorted part of the array
        min_idx = i
        print(f"Looking for the minimum element starting from index {i}")
        
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
                print(f"  New minimum found: {arr[min_idx]} at index {min_idx}")
        
        # Swap the found minimum element with the first element of the unsorted part
        if min_idx != i:
            print(f"Swapping {arr[i]} at index {i} with {arr[min_idx]} at index {min_idx}")
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        else:
            print(f"No swap needed. {arr[i]} at index {i} is already in the correct position.")
        
        print(f"Array after iteration {i + 1}: {arr}")
    
    print("\nSorting completed!")
    print(f"Final sorted array: {arr}")

# Test the function
if __name__ == "__main__":
    test_array = [64, 34, 25, 12, 22, 11, 90]
    selection_sort_with_explaination(test_array)
