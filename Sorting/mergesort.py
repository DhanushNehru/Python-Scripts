class MergeSort:
    def __init__(self, array):
        self.array = array
    
    def sort(self):
        self.array = self.merge_sort(self.array)
        return self.array
    
    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left_half = self.merge_sort(arr[:mid])
        right_half = self.merge_sort(arr[mid:])
        
        return self.merge(left_half, right_half)
    
    def merge(self, left, right):
        sorted_arr = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                sorted_arr.append(left[i])
                i += 1
            else:
                sorted_arr.append(right[j])
                j += 1
        
        while i < len(left):
            sorted_arr.append(left[i])
            i += 1
        
        while j < len(right):
            sorted_arr.append(right[j])
            j += 1
        
        return sorted_arr

# Example usage
if __name__ == "__main__":
    arr = [38, 27, 43, 3, 9, 82, 10]
    merge_sort = MergeSort(arr)
    sorted_array = merge_sort.sort()
    print("Sorted array:", sorted_array)
