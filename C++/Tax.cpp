#include <iostream>

using namespace std;

int totalTax(double amount, double rate)
{
     return amount * rate;
}

int tpAmount(double amount, double rate)
{
     return amount * rate;
}

int totalAmount(double amount, double tax, double tip)
{
     return amount + tax + tip;
}

int amountPerPerson(double total, double people)
{
     return total / people;
}

int main()
{
     double TBA, taxRate, tipRate, taxAmount, tipAmount, splitBill, totalBill, partySize;
     // Declares/Initializes double variables for the required values.

     cout << "\n"
          << "Enter the total bill amount (Before tax and tip) > ";
     cin >> TBA;
     cout << "\n"
          << "Enter the tax rate (as a decimal) > ";
     cin >> taxRate;
     cout << "\n"
          << "Enter the tip rate (as a decimal) > ";
     cin >> tipRate;
     cout << "\n"
          << "How many people are splitting the bill? > ";
     cin >> partySize;

     // Placing the "\n" with the intended print would do the same as println() in java
     // Rather, I'll place the "\n" to make it activate before displaying the prompt.

     taxAmount = totalTax(TBA, taxRate);
     tipAmount = tpAmount(TBA, tipRate); // Changed from tip to tp to prevent confusion by Cpp
     totalBill = totalAmount(TBA, taxAmount, tipAmount);
     splitBill = amountPerPerson(totalBill, partySize);
     // This program uses various classes to perform the calculations.

     cout << "\n"
          << "--- Results ---" << endl;
     cout << "\t" << "The total tax amount is: " << taxAmount << endl;
     cout << "\t" << "The total tip amount is: " << tipAmount << endl;
     cout << "\t" << "The total bill amount is: " << totalBill << endl;
     cout << "\t" << "The amount per person is: " << splitBill << "\n"
          << endl;
     // Last \n is used to create whitespace for clarity.

     return 0;
}
