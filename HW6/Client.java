import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class Client {
    public static void main(String[] args) {
        if (args.length != 2) { // Test for correct num. of arguments
            System.err.println("ERROR server host name AND port number not given");
            System.exit(1);
        }

        int port_num = Integer.parseInt(args[1]);
        Socket c_sock = new Socket();
        try{
            c_sock = new Socket(args[0], port_num);
        } catch (IOException e){
            e.printStackTrace();
            System.out.println("Wrong hostname or port number");
            System.exit(0);
        }

        while (true){
            try {
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(c_sock.getInputStream()));
                PrintWriter out = new PrintWriter(
                        new OutputStreamWriter(c_sock.getOutputStream()), true);
                BufferedReader userEntry = new BufferedReader(
                        new InputStreamReader(System.in));
                System.out.print("Type in the command: ");

                String cmd = userEntry.readLine().trim(); // delete the SPACE in the head or tail
                if(checkCmd(cmd)){
                    out.println(cmd);
                }else {
                    continue;
                }

                String response = in.readLine();
                System.out.println("    " + response);
                if(response.equals("Good bye!")){
                    c_sock.close();
                    System.out.println("Disconnected from server successfully.");
                    System.exit(0);
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }

    private static boolean checkCmd(String cmd){
        //check validation of cmd
        boolean r = true;
        String[] cmds = cmd.split(" ");
        if(cmds[0].equals("\n") || cmds[0].equals("")){
            r = false;
        }
        if(cmds.length > 2){
            System.out.println("    Wrong command: too much parameters.");
            help();
            r = false;
        }
        if(!cmds[0].equals("GET") && !cmds[0].equals("BOUNCE") && !cmds[0].equals("EXIT")) {
            System.out.println("    Unknown command.\n");
            help();
            r = false;
        }
        if(cmds[0].equals("GET") || cmds[0].equals("BOUNCE")){
            if(cmds.length != 2){
                System.out.println("    Missing parameters.");
                help();
                r = false;
            }
        }

        return r;
    }

    private static void help(){
        System.out.println("    GET <filename>:\n"
                + "         Return the content of filename from the server.");
        System.out.println("    BOUNCE <msg>:\n"
                + "          Send a message to the server.");
        System.out.println("    EXIT [code]:\n"
                + "          Disconnect from server, and send a code to server (optinal).");
        System.out.println();
    }
}
