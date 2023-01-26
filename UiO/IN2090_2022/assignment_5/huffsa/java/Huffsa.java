import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet; 
import java.sql.SQLException;
import java.sql.Statement;

import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;

public class Huffsa {

    private static String user = ""; // Skriv ditt UiO-brukernavn
    private static String pwd = ""; // Skriv passordet til _priv-brukeren du fikk i mail fra USIT
    // Tilkoblings-detaljer
    private static String connectionStr = 
        "user=" + user + "_priv&" + 
        "port=5432&" +  
        "password=" + pwd + "";
    private static String host = "jdbc:postgresql://dbpg-ifi-kurs03.uio.no"; 

    public static void main(String[] agrs) {

        try {
            // Last inn driver for PostgreSQL
            Class.forName("org.postgresql.Driver");
            // Lag tilkobling til databasen
            Connection connection = DriverManager.getConnection(host + "/" + user
                    + "?sslmode=require&ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory&" + connectionStr);

            int ch = 0;
            while (ch != 3) {
                System.out.println("--[ HUFFSA ]--");
                System.out.println("Vennligst velg et alternativ:\n 1. Søk etter planet\n 2. Legg inn resultat\n 3. Avslutt");
                ch = getIntFromUser("Valg: ", true);

                if (ch == 1) {
                    planetSok(connection);
                } else if (ch == 2) {
                    leggInnResultat(connection);
                }
            }
        } catch (SQLException|ClassNotFoundException ex) {
            System.err.println("Error encountered: " + ex.getMessage());
        }
    }

    private static void planetSok(Connection connection)  throws SQLException {
        // TODO: Oppg 1
    }


    private static void leggInnResultat(Connection connection) throws SQLException {
        // TODO: Oppg 2
    }

    /**
     * Utility method that gets an int as input from user
     * Prints the argument message before getting input
     * If second argument is true, the user does not need to give input and can leave
     * the field blank (resulting in a null)
     */
    private static Integer getIntFromUser(String message, boolean canBeBlank) {
        while (true) {
            String str = getStrFromUser(message);
            if (str.equals("") && canBeBlank) {
                return null;
            }
            try {
                return Integer.valueOf(str);
            } catch (NumberFormatException ex) {
                System.out.println("Please provide an integer or leave blank.");
            }
        }
    }

    /**
     * Utility method that gets a String as input from user
     * Prints the argument message before getting input
     */
    private static String getStrFromUser(String message) {
        Scanner s = new Scanner(System.in);
        System.out.print(message);
        return s.nextLine();
    }
}
