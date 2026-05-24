#include <iostream> // Library for input and output functionalities
#include <String> // Library for using the String datatype
#include <iomanip> // Library for manipulating input and output formats

using namespace std;

int main() {
    double hours, minutes, seconds; 
    // Declares/Initializes double variables for hours, minutes, and seconds
    // double : A datatype that can hold decimal values (floating point numbers), much larger range and size than int

    // Input
    cout << "Enter the number of hours: "; // Prints the prompt to the console
    cin >> hours; // Assigns user input to the hours variable
    cout << "Enter the number of minutes: "; // Prints the prompt to the console
    cin >> minutes; // Assigns user input to the minutes variable
    cout << "Enter the number of seconds: "; // Prints the prompt to the console
    cin >> seconds; // Assigns user input to the seconds variable
    
    // Convert everything to seconds and add them all up
    double totalHours = hours + (minutes / 60) + (seconds / 3600);
    // Converts minutes to hours by dividing by 60 and seconds to hours by dividing by 3600 -- Converting the minutes and seconds to hours,
    // Adds them all together and assigns the result to totalHours variable

    // Prints the final time
    cout << "The time you have entered is: ";
    cout  << "\n" << totalHours << " hours" << "\n" << endl;
    // Newline's then outputs the totalHours variable with a label to the console, then newline's again
    // Purpose of endl is to ensure the text is displayed immediately, not to be confused with \n which just creates a new line

    return 0; // Returns 0 to indicate successful completion of the program
    
} // Note: This program does not handle invalid input (e.g., negative numbers, non-numeric input).    