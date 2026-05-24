#include <iostream>
#include <string>
#include <limits>

using namespace std;

class Vehicle
{
public:
    string registrationNumber;
    string brand;
    double rentalRatePerDay;
    int rentalDays;

    void setVehicleInfo(string reg, string b, double rate, int days)
    {
        registrationNumber = reg;
        brand = b;
        rentalRatePerDay = rate;
        rentalDays = days;
    }

    double calculateRentalCost(int days)
    {
        return rentalRatePerDay * days;
    }

    void displayVehicleInfo()
    {
        cout << "--- Vehicle Information ---" << endl;
        cout << "\tRegistration Number: " << registrationNumber << endl;
        cout << "\tBrand: " << brand << endl;
        cout << "\tRental Rate per Day: " << rentalRatePerDay << " Doubloons" << endl;
        cout << "\tAmount of days rented: " << rentalDays << endl;
    }
};

class MainVehicle
{
public:
    // Collects User information
    void information(Vehicle &myvehicle, int &rentalDays)
    /* Vehicle references the Vehicle Class, calling it for use in this method
        &rentalDays references to the rentalDays variable in main()
        &myvehicle references to the myvehicle object in main() */

    {
        cout << "Vehicle Rental System" << "\nEioson IT Solutions LLC." << endl;

        cout << "Enter Registration Number: ";
        getline(cin, myvehicle.registrationNumber);
        cout << endl;

        cout << "Enter Brand: ";
        getline(cin, myvehicle.brand);
        cout << endl;

        cout << "Enter Rental Rate per Day: ";
        cin >> myvehicle.rentalRatePerDay;
        cout << endl;

        /* Clear the input buffer after reading a number. This is a good practice
        to prevent issues if you were to add another getline() call later on.
        We need to include the <limits> header for this.                       */
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        cout << "Alright, for how long would you like to rent the vehicle (Days)? \n"
             << ">> ";
        cin >> myvehicle.rentalDays;
        cout << endl;
    }
};

int main()
{
    MainVehicle app;
    Vehicle myVehicle;
    int rentalDays;

    app.information(myVehicle, rentalDays);
    myVehicle.displayVehicleInfo();

    double totalCost = myVehicle.calculateRentalCost(rentalDays);
    cout << "--- Pricing ---" << endl;
    cout << "\nTotal Rental Cost for " << rentalDays << " days: " << totalCost << " Doubloons\n" << endl;

    return 0;
}