def quicksort(arr):
    # Base case: if the array has 0 or 1 elements, it's already sorted
    if len(arr) <= 1:
        return arr
    
    # Choose a pivot element (in this case, we use the middle element)
    pivot = arr[len(arr) // 2]
    
    # Divide the array into three sublists: left, middle, and right
    left = [x for x in arr if x < pivot]   # Elements smaller than pivot
    middle = [x for x in arr if x == pivot]   # Elements equal to pivot
    right = [x for x in arr if x > pivot]   # Elements greater than pivot
    
    # Recursively apply quicksort to the left and right sublists
    return quicksort(left) + middle + quicksort(right)

# Example Usage:
my_list = [3, 6, 8, 10, 1, 2, 1]
sorted_list = quicksort(my_list)
print(sorted_list)
