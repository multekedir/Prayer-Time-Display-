
import java.util.ArrayList;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.logging.Level;
import java.util.logging.Logger;

/*
 *This program is an add on the Pyhton Program, Prayer Time Display.
 *The Program gets user data to adjust iqama time. Is soters the 
 *collected the data in a file called iqama.txt wich wil be read by 
 *the python program. After saving the File it then executes runPython.sh 
 *to start the python program.
 *@version 1.55
 * @author Multezem Kedir
 */

 

/**
 * This Write classes get the collected data list from Display, Main Class, and
 * then Writes it on to iqama.txt.
 */
public class Write {

    /**
     * initiates Write class
     *
     * @param data collected data list
     */
    public Write(ArrayList<String> data) {
        System.out.println("Writer class opened");
        System.out.println("Writing" + data + " to file");
        Writer(data); //start Writing data
        
    }

    /**
     * Writes data on to 'iqama.txt in the same directory.'
     *
     * @param data collected data list
     */
    private void Writer(ArrayList data) {
        System.out.println("Trying to write data on to iqama.txt ");
        try {
            //open or creat new file named iqama.txt
            PrintWriter writer = new PrintWriter("../Python/iqama.txt", "UTF-8");
            //Write each data onto difrent line in order
            for (int i = 0; i < data.size(); i++) {
                writer.println(data.get(i));
                System.out.println(i + ": " + data.get(i));
            }
            writer.close();//close file
            System.out.println("Data writen in ../Python/iqama.txt \n File Closed");
	    runPython();// execute runPython.sh
		
        } catch (IOException e) {
            System.out.println("Error writing file");
        }
    }

    /**
     * Execute runPython.sh located in the directory
     */
    private void runPython() {
        try {
            Process p = null;
            ProcessBuilder pb = new ProcessBuilder("../Scripts/runPython.sh");
            p = pb.start();
			dispose();
        } catch (IOException ex) {
            System.out.println("Error Execute runPython.sh");
        }
    }
}
