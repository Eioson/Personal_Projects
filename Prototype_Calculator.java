import java.util.Scanner;

public class Prototype_Calculator {
    public static void main(String[] sigma) {
        try(Scanner sc = new Scanner(System.in)){

            float n1 = 0;
            char op;
            float n2 = 0;

            boolean continueCalculating = true;
            while (continueCalculating) {

                // --- Get first number ---
                System.out.print("Enter the first number (or C/AC to clear): ");
                String input1 = sc.next();
                if (input1.equalsIgnoreCase("C") || 
                        input1.equalsIgnoreCase("AC")) {
                    System.out.println("Operation cleared. Starting over.\n");
                    continue; // Restart the main loop and the calculator as a whole
                }

                try {
                    n1 = Float.parseFloat(input1);
                } catch (NumberFormatException e) { //Catches if input is Float.parseFloat cannot be done
                    System.out.println("Invalid input. Please enter a whole number, decimal, or C/AC.\n");
                }

                // --- Get second number ---
                System.out.print("\nEnter the second number (or C/AC to clear): ");
                String input2 = sc.next();
                if (input2.equalsIgnoreCase("C") || 
                        input2.equalsIgnoreCase("AC")) {
                    System.out.print("Operation cleared. Starting over.\n");
                    continue; // Restarts the main loop and the calculator as a whole
                }

                try {
                    n2 = Float.parseFloat(input2);
                } catch (NumberFormatException e) { //Catches if input is Float.parseFloat cannot be done
                    System.out.println("Invalid input. Please enter a whole number, decimal, or C/AC.\n");
                    
                }

                // --- Get operator ---
                System.out.print("\nEnter the operator (+, -, *, /, %): ");
                op = sc.next().charAt(0);

                // --- Calculates and prints the result ---
                switch (op) {
                    case '+' -> System.out.println("\n" + n1 + " + " + n2 + " = " + (n1 + n2) + "\n");
                    case '-' -> System.out.println("\n" + n1 + " - " + n2 + " = " + (n1 - n2) + "\n");
                    case '*' -> System.out.println("\n" + n1 + " * " + n2 + " = " + (n1 * n2) + "\n");
                    case '/' -> {
                        if (n2 == 0) {
                            System.out.println("Error: Cannot divide by zero.");
                        } else {
                            System.out.print("\n" + n1 + " / " + n2 + " = " + (double)n1 / n2);
                        }
                    }
                    case '%' -> System.out.println("\n" + n1 + " % " + n2 + " = " + (n1 % n2) + "\n");

                    default ->System.out.println("Invalid operator");
                }
                System.out.print("Do you want to continue? (Y/N): ");
                if (!sc.next().equalsIgnoreCase("Y")) {  
                    continueCalculating = false;
                    System.out.println("\n");
                }

                sc.close();
            }
        }    
    }
}
