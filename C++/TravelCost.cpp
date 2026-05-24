/* Program ment to calculate the total fuel needed, it's cost, and the fuel's cost per kilometer
using the relevant inputs. Intend to use a bit more complex methods than Tax.cpp to explore it.

Relevant Inputs: Distance to travel (in km), fuel Consumption (In liters per km), and fuel price per liter (in doubloons)*/

#include <iostream>

using namespace std;

double totalFuel(double distance, double fuelConsumption)
{
    return distance * fuelConsumption;
}

double totalCost(double totalFuel, double fuelPrice)
{
    return totalFuel * fuelPrice;
}

double costPerKilometer(double totalCost, double distance)
{
    return totalCost / distance;
}

void printResults(double requiredFuel, double costs, double costpKM)
{
    cout << "\n\t" << "      --- Results ---"
         << endl;

    cout << "\t" << "Total fuel needed: " << requiredFuel << " liters"
         << endl;

    cout << "\t" << "Total fuel cost: " << costs << " doubloons"
         << endl;

    cout << "\t" << "Cost per kilometer: " << costpKM << " doubloons/km" << "\n"
         << endl;
}

int main()
{
    double distance, fuelConsumption, fuelPrice;

    cout << "\n"
         << "Enter the distance to travel (in km): ";
    cin >> distance;
    cout << "Enter the fuel consumption (in liters per km): "; // Corrected the prompt to match the variable
    cin >> fuelConsumption;
    cout << "Enter the fuel price per liter (in doubloons): ";
    cin >> fuelPrice;

    double requiredFuel = totalFuel(distance, fuelConsumption);
    double costs = totalCost(requiredFuel, fuelPrice);
    double costpKM = costPerKilometer(costs, distance);

    printResults(requiredFuel, costs, costpKM);

    return 0;
}