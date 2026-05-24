#include <iostream>
#include <string>
#include <memory>
#include <vector>

// --- THE INTERFACE ---
// This defines what ANY database must be able to do.
class IDatabase
{
public:
    virtual ~IDatabase() = default;
    virtual bool initialize() = 0;
    virtual bool check_student_record(const std::string &username, const std::string &password) = 0;
};

// --- THE MOCK IMPLEMENTATION ---
// This operates without a real database for now.
class MockDatabase : public IDatabase
{
public:
    bool initialize() override
    {
        std::cout << "[SYSTEM] NV Database Initialized successfully.\n";
        return true;
    }

    bool check_student_record(const std::string &username, const std::string &password) override
    {
        // Simulating the "Uni CAS" check
        if (username == "admin" && password == "1234")
            return true;
        return false;
    }
};

// --- THE CORE LOGIC (From 1203.jpg) ---
class SmartLibSystem
{
private:
    std::shared_ptr<IDatabase> db;
    bool is_initialized = false;

public:
    // We "inject" the database here.
    SmartLibSystem(std::shared_ptr<IDatabase> database) : db(database) {}

    void run_login_procedure(std::string name, std::string pass, bool is_student)
    {
        // 1. Initialize NV Database if not already done
        if (!is_initialized)
        {
            is_initialized = db->initialize();
        }

        // 2. Prompt Check (The "Not Inputted" loop in red)
        if (name.empty() || pass.empty())
        {
            std::cout << "[UI] Display: Small re-enter details note.\n";
            return;
        }

        // 3. Logic Gate: Is the User a Student?
        if (is_student)
        {
            std::cout << "[SYSTEM] Initializing CAS Program...\n";

            // 4. Details transferred into Uni CAS (Authorization)
            if (db->check_student_record(name, pass))
            {
                // Success Path
                std::cout << "[UI] Display: Small 'Authorized!' Note.\n";
                std::cout << "[UI] Display Student's Username: " << name << "\n";
                std::cout << "[UI] Action: Display SmartLib Homepage.\n";
            }
            else
            {
                // Failure Path
                std::cout << "[UI] Display: 'Student is not in system' Dialog.\n";
            }
        }
        else
        {
            std::cout << "[LOGIC] User is not a student. Ending procedure.\n";
        }
    }
};

int main()
{
    // To switch to a real DB later, you just change this one line.
    auto my_db = std::make_shared<MockDatabase>();
    SmartLibSystem app(my_db);

    // Testing the logic
    app.run_login_procedure("admin", "1234", true);
    return 0;
}