class CountingSort:
    def __init__(self, array):
        self.array = array

    def sort(self):
        if not self.array:
            return []

        # Find the maximum and minimum values
        max_val = max(self.array)
        min_val = min(self.array)
        range_of_elements = max_val - min_val + 1

        # Initialize the count array
        count = [0] * range_of_elements
        output = [0] * len(self.array)

        # Count occurrences
        for num in self.array:
            count[num - min_val] += 1

        # Update count array to store cumulative sums
        for i in range(1, len(count)):
            count[i] += count[i - 1]

        # Build the output array
        for num in reversed(self.array):
            output[count[num - min_val] - 1] = num
            count[num - min_val] -= 1

        # Copy sorted elements back to original array
        self.array[:] = output

    def get_sorted_array(self):
        return self.array


# Example Usage:
arr = [4, 2, 2, 8, 3, 3, 1]
cs = CountingSort(arr)
cs.sort()
print("Sorted Array:", cs.get_sorted_array())
