#include <iostream>
#include <string>
#include <limits>

using namespace std;

class User
{

private: // User details, made private for encapsulation
    string username;
    string email;
    float fines;

public:
    // Constructor to initialize user details
    User(const string &uname, const string &mail) : username(uname), email(mail), fines(0.0f) {} // Initialize fines to 0.0f

    // Getter method for fines
    float getFines() const
    {
        return fines;
    }

    // Method to add fines to the user
    void addFines(float amount)
    {
        fines += amount;
    }

    // Method to display user details
    void displayUser() const
    {
        cout << "Username: " << username << endl;
        cout << "Email: " << email << endl;
    }

    // Method to display fines
    void displayFines() const
    {
        if (fines > 0.0f)
        {
            cout << "User " << username << " has fines: $" << fines << endl;
        }
        else
        {
            cout << "User " << username << " has no fines." << endl;
        }
    }

    void mainMenu() // Removed 'const' so you can loop and update states if needed
    {
        int choice = 0;
        while (choice != 3)
        {
            cout << "\nWelcome, " << username << "!" << endl;
            cout << "\t1. View Account Details" << endl;
            cout << "\t2. View Fines" << endl;
            cout << "\t3. Exit" << endl;
            cout << "Enter your choice: ";
            cin >> choice;

            if (cin.fail())
            {
                cin.clear();                                         // Clear the error flag
                cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Discard invalid input
                cout << "Invalid input. Please enter a number (1, 2, or 3)." << endl;
                continue;
            }

            switch (choice)
            {
            case 1:
                displayUser();
                break;

            case 2:
                displayFines();
                break;

            case 3:
                cout << "Exiting. Goodbye!" << endl;
                break;

            default:
                cout << "Invalid choice. Please try again." << endl;
                break;
            }
        }
    }
};

int main()
{
    // 1. Create a dummy user instance to test your logic
    User testUser("Edison", "edison@email.com");

    // 2. Add some test fines to see if your displays work
    testUser.addFines(15.50f);

    // 3. Trigger the menu you built
    testUser.mainMenu();

    return 0;
}