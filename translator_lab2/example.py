def sumArray(arr, n):
    s = 0
    for i in range(0, n):
        s += arr[i]
    return s
def maxArray(arr, n):
    m = arr[0]
    for i in range(1, n):
        if arr[i] > m:
            m = arr[i]
    return m
def main():
    n = 0
    print("Enter size: ")
    n = int(input())
    arr = [0] * n
    for i in range(0, n):
        arr[i] = int(input())
    s = sumArray(arr, n)
    m = maxArray(arr, n)
    print("Sum: ", s)
    print("Max: ", m)
    return 0