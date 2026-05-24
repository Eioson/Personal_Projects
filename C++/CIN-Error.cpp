#include <iostream>
#include <string> // Required for std::string and std::getline, since Strings are a seperate library
#include <limits> // Required for std::numeric_limits

using namespace std;

int main()
{

    int age;
    string Name;

    cout << "Enter your age: ";
    cin >> age;

    // After using `cin >>`, a newline character is left in the input buffer.
    // We need to ignore it so getline() can read the next line properly.
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    cout << "Enter your full name: ";
    // Correctly call getline to read the entire line, including spaces.
    getline(cin, Name);

    cout << "Name: " << Name << ", Age: " << age << endl;

    return 0;
}