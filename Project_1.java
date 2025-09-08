import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Project_1 {
    public static void main(String[] args) { // Changed 'sigma' to 'args' for convention
        // A list to store our tasks. We use List as the type for good practice.
        List<String> tasks = new ArrayList<>();

        //Note: Lists are zero-indexed = [0,1,2,3,4....]

        // The Scanner class is used to get user input.
        Scanner scanner = new Scanner(System.in);

        System.out.println("Welcome to your Personal Productivity Tool!");

        // This is the main loop that keeps our application running.
        while (true) {
            System.out.print("\n> What would you like to do? (add, list, exit): ");
            String command = scanner.nextLine().trim(); // Read the full line of input

            // A switch statement is a clean way to handle different commands. Serves as the control flow
            switch (command.toLowerCase()) {
                case "add":
                    // Your code to add a task will go here.
                    System.out.println("CHALLENGE: Implement the 'add' functionality!");
                    System.out.println("What task would you like to add? ");
                    String task = scanner.nextLine();
                    tasks.add(task);

                    System.out.println("Confirm this action by typing 'yes': ");
                    String confirmation = scanner.nextLine();
                    if (confirmation.equalsIgnoreCase("yes")) {
                        System.out.println("Task added successfully!");
                    } else {
                        tasks.remove(task);
                        System.out.println("Task addition cancelled.");
                    }
                    
                    break;

                case "list":
                    // Your code to list all tasks will go here.
    //                System.out.println("CHALLENGE: Implement the 'list' functionality!");
                    if (!tasks.isEmpty()) {
                        System.out.println("Your tasks:");
                        for (int i = 0; i < tasks.size(); i++) {
                            System.out.println((i + 1) + ". " + tasks.get(i));
                        }
                    } else {
                       System.out.println("You have no tasks yet. Use 'add' to create one!"); 
                        }

                    break;

                case "exit":
                    System.out.println("Exiting application. Goodbye!");
                    scanner.close(); // It's good practice to close the scanner.
                    return; // This exits the main method, ending the program.

                default:
                    System.out.println("Unknown command. Please try again.");
                    break;
            }
        }
    }
}
