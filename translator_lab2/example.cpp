#include <iostream>
#include <vector>
using namespace std;

int sumArray(vector<int>& arr, int n) {
    int s = 0;
    for (int i = 0; i < n; i++) {
        s += arr[i];
    }
    return s;
}

int maxArray(vector<int>& arr, int n) {
    int m = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] > m) {
            m = arr[i];
        }
    }
    return m;
}

int main() {
    int n;
    cout << "Enter size: ";
    cin >> n;

    vector<int> arr(n);

    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    int s = sumArray(arr, n);
    int m = maxArray(arr, n);

    cout << "Sum: " << s << endl;
    cout << "Max: " << m << endl;

    return 0;
}
