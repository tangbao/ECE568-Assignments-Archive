
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Base64;

public class Client {
    public static void main(String[] args) {
        if (args.length != 2) { // Test for correct num. of arguments
            System.err.println("ERROR server host name AND port number not given");
            System.exit(1);
        }

        int port_num = Integer.parseInt(args[1]);
//        Socket c_sock; 

        while (true){
            try {
                Socket c_sock = new Socket(args[0], port_num);
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(c_sock.getInputStream()));
                PrintWriter out = new PrintWriter(
                        new OutputStreamWriter(c_sock.getOutputStream()), true);
                BufferedReader userEntry = new BufferedReader(
                        new InputStreamReader(System.in));

                String cmd = "";
                while(!checkCmd(cmd)){ //check the validation of command first
                    System.out.print("\nType in the command: ");
                    cmd = userEntry.readLine().trim(); // delete the SPACE in the head or tail
                }

                out.println(cmd); //send cmd to server
                String response = in.readLine(); //get the response from Server
                System.out.println(response); //output the first response "Command received by Server"
                response = in.readLine(); //get the real response

                if(response.equals("    Good bye!")){
                    c_sock.close();
                    System.out.println(response);
                    System.out.println("    Disconnected from server successfully.");
                    System.exit(0);
                } else if(response.equals("    Invalid command.")){
                    help();
                    c_sock.close();
                    continue;
                } else if(response.equals("FILE")){
                    response = in.readLine(); //get the Base64 codes of file content
                    System.out.println("\n======File content starts======");
                    //decode and output
                    System.out.println(new String(Base64.getDecoder().decode(response.getBytes())));
                    System.out.println("======File  content  ends======");
                    response = in.readLine();
                }

                if(response != null){ //output the remaining output
                    System.out.println(response);
                }
                c_sock.close();
            } catch (IOException ex) {
//                ex.printStackTrace();
                System.out.println("Server is not online. Press Ctrl+C to stop reconnect.");
           }
        }
    }

    private static boolean checkCmd(String cmd){
        //check validation of cmd
        boolean r = true;
        String[] cmds = cmd.split(" ");
        if(cmds[0].equals("\n") || cmds[0].equals("")){ //empty input
            r = false;
        }else if(cmds.length > 2){
            System.out.println("    Wrong command: too much parameters.");
            help();
            r = false;
        }else if(!cmds[0].equals("GET") && !cmds[0].equals("BOUNCE") && !cmds[0].equals("EXIT")) {
            System.out.println("    Unknown command.\n");
            help();
            r = false;
        }else if(cmds[0].equals("GET") || cmds[0].equals("BOUNCE")){
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
