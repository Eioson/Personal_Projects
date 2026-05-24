#include <iostream>
#include <cmath>

using namespace std;

class OrbitalMechanics
{

    // --- Calculations ---
public:
    // Gravitational Constant (m^3 kg^-1 s^-2)
    const double G = 6.67430e-11;

    void OrbitalRadius(double rad_planet, double distance)
    {
        // Calculate the orbital radius
        double radius_m = rad_planet + distance;
        cout << "The orbital radius is: " << radius_m << " meters" << endl;
    }

    void GravitationalForce(double mass_planet, double mass_satellite, double distance)
    {
        // Calculate the gravitational force
        double force = (G * mass_planet * mass_satellite) / pow(distance, 2); // Use pow for exponentiation (squared)
        cout << "The gravitational force is: " << force << " Newtons" << endl;
    }

    void EscapeVelocity(double mass_planet, double rad_planet)
    {
        // Escape velocity equation: v = sqrt(2GM / r)
        // Result is in meters per second
        double v_ms = sqrt((2 * G * mass_planet) / rad_planet);

        // Convert back to km/s for display
        cout << "The escape velocity is: " << (v_ms / 1000.0) << " km/s" << endl;
    }

    void OrbitalVelocity(double mass_planet, double planetRadius, double altitude)
    {
        double OrbitalRadius = planetRadius + altitude;
        cout << "\n"
             << endl;
        cout << "\tplanetmass: " << mass_planet << endl;
        cout << "\tPlanet's Radius (m): " << planetRadius << endl;
        cout << "\tAltitude (m): " << altitude << endl;
        double v_ms = OrbitalVelocity(mass_planet, OrbitalRadius);
        cout << "\n\t" << "The orbital velocity is: " << v_ms << " m/s" << endl;
    }

    double OrbitalVelocity(double mass_planet, double OrbitalRadius)
    {
        // Orbital velocity equation: v = sqrt(GM / r)
        // Result is in meters per second
        double v_ms = sqrt((G * mass_planet) / OrbitalRadius);
        return v_ms;
    }

    void OrbitalPeriod(double mass, double radius)
    {
        if (mass <= 0 || radius <= 0)
        {
            cout << "Mass and radius must be positive values." << endl;
            return;
        }

        double orbitalVelocity = OrbitalVelocity(mass, radius);
        double orbitalPeriod = (2 * 3.14 * radius) / orbitalVelocity; // in seconds
        cout << "The orbital period is: " << orbitalPeriod << " seconds" << endl;
    }
};

// --- Main function to execute the program ---
int main()
{
    double kgplanet, rad_planet;
    // Declares/Initializes double variables for kgplanet and rad_planet

    OrbitalMechanics om; // Create an instance of the OrbitalMechanics class

    // Input
    cout << "Enter the mass of the planet (kg): "; // Prompt for gravitational parameter
    cin >> kgplanet;                               // Assigns user input to the kgplanet variable
    if (kgplanet <= 0)
    {
        cout << "Mass must be a positive value." << endl;
        return 0; // Exit if invalid input, exit value of 0 indicates unsuccessful completion of the program
    }

    cout << "Enter the planet's radius (r) in km: "; // Prompt for planet's radius
    cin >> rad_planet;                               // Assigns user input to the rad_planet variable
    if (rad_planet <= 0)
    {
        cout << "Radius must be a positive value." << endl;
        return 0; // Exit if invalid input
    }
    double rad_planet_m = rad_planet * 1000; // Convert radius from km to meters

    cout << "Enter the mass of the satellite (kg): "; // Prompt for satellite mass (not used in calculation)
    double kg_satellite;
    cin >> kg_satellite; // Assigns user input to the kg_satellite variable
    if (kg_satellite <= 0)
    {
        cout << "Satellite mass must be a positive value." << endl;
        return 0; // Exit if invalid input
    }

    cout << "Enter the distance between the planet and satellite (m): "; // Prompt for distance (not used in calculation)
    double distance;
    cin >> distance; // Assigns user input to the distance variable
    if (distance <= 0)
    {
        cout << "Distance must be a positive value." << endl;
        return 0; // Exit if invalid input
    }

    // Calculate and display the orbital velocity
    om.OrbitalRadius(rad_planet_m, distance);                                                                       // Call the OrbitalRadius method to calculate and display the radius
    om.GravitationalForce(kgplanet, kg_satellite, rad_planet_m + distance);                                         // Call the GravitationalForce method to calculate and display the force
    om.EscapeVelocity(kgplanet, rad_planet_m);                                                                      // Call the EscapeVelocity method to calculate and display the escape velocity
    cout << "The orbital velocity is: " << om.OrbitalVelocity(kgplanet, rad_planet_m + distance) << " m/s" << endl; // Call the OrbitalVelocity method to calculate and display the orbital velocity
    om.OrbitalVelocity(kgplanet, rad_planet_m, distance);
    // Call the overloaded OrbitalVelocity method to calculate and display the orbital velocity

    return 0;
}