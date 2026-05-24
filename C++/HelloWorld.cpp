#include <iostream> 
// #include is very very similar to "import" in Java but for a file
// iostream : Input-Output Stream - Common C++ header file/library that provides functionalities for input and output

using namespace std; 
// using : Tells the compiler to use a specific item from a specific source
/* namespace : A declarative region that provides a scope to the identifiers (the names of types, functions, variables, etc) inside it
         Thus preventing name/identifier conflicts */
// std : Standard - The standard C++ library, contains features of the C++ programming language such as cin, cout, endl, etc.

int main() {
// The main function's datatype is an int (integer). When the program reaches the end, it should return a integer value.
    
    cout << endl << "Hello, World!" << endl;
    // cout : Character Out - Output object from the iostream library
    // endl : End Line - Inserts a new line (Like \n) while ensuring text is displayed immediately.

    // Line 12 is executed by implementing the String Stream to cout first then calling the endl action.

    return 0;
    // return : Returns a value from a function
}