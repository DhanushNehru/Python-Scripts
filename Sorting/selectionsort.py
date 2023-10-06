"""
Intuition is to pick smallest element every times loop proceeds
"""

def selectionSort(arr):
    """
    The selectionSort function implements the selection sort algorithm to sort an array in ascending
    order.
    
    :param arr: The parameter `arr` is a list of elements that you want to sort using the selection sort
    algorithm
    
    Time complexity: O(N^2), (where N = size of the array), for the best, worst, and average cases.
    Space Complexity: O(1)
    """
    n = len(arr)
    
    for i in range(0,n-1):
        min_idx = i
        for j in range(i,n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # at this point we have collected information which element is smallest (between i and n-1)and its index is stored in min_idx
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


temp = input("Enter numbers separated by a comma:\n").strip()
arr = [int(item) for item in temp.split(",")]
selectionSort(arr)
print(arr)