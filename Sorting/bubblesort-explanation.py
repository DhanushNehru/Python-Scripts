def bubble_sort_with_explanation(arr):
    n = len(arr)
    
    print(f"Initial array: {arr}")
    print("\nStarting Bubble Sort...")
    
    for i in range(n):
        print(f"\nPass {i + 1}:")
        
        # Flag to check if any swap happened in this pass
        swapped = False
        
        for j in range(0, n - i - 1):
            print(f"  Comparing {arr[j]} and {arr[j + 1]}")
            
            if arr[j] > arr[j + 1]:
                print(f"    Swapping {arr[j]} and {arr[j + 1]} since {arr[j]} > {arr[j + 1]}")
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
            else:
                print("    No swap needed")
            
            print(f"  Array after comparison: {arr}")
        
        print(f"Array after pass {i + 1}: {arr}")
        
        # If no swapping occurred, array is already sorted
        if not swapped:
            print(f"\nArray is already sorted after pass {i + 1}. Stopping early.")
            break
    
    print("\nSorting completed!")
    print(f"Final sorted array: {arr}")

# Test the function
if __name__ == "__main__":
    test_array = [64, 34, 25, 12, 22, 11, 90]
    bubble_sort_explained(test_array)