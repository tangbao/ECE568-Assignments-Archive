import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

import java.util.Base64;


public class Server {
    public static void main(String[] args) throws IOException {
        if (args.length != 1) { // Test for correct num. of arguments 
            System.err.println("ERROR server port number not given");
            System.exit(1);
        }
        int port_num = Integer.parseInt(args[0]);
        ServerSocket rv_sock = null;
        try {
            rv_sock = new ServerSocket(port_num);
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        while (true) { // run forever, waiting for clients to connect
            System.out.println("\nWaiting for commands from client...");
            try {
                Socket s_sock = rv_sock.accept();
                System.out.println("    A client connects to server.");
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(s_sock.getInputStream()));
                PrintWriter out = new PrintWriter(
                        new OutputStreamWriter(s_sock.getOutputStream()), true);
                String cmd = in.readLine(); //get the cmd
                out.println("    Command received by server.");

                if (checkCmd(cmd, out)) {
                    execCmd(cmd, out); //execute cmd
                } else {
                    out.println("    Invalid command.");
                }
                s_sock.close();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }

    private static void execCmd(String cmd, PrintWriter out){
        String[] cmds = cmd.split(" ");
        switch (cmds[0]){
            case "EXIT":
                if(cmds.length == 2){
                    System.out.println("    Message from client: " + cmds[1]);
                }
                out.println("    Good bye!");
                System.out.println("A client disconnects from server.");
                break;
            case "BOUNCE":
                System.out.println("    Message from client: " + cmds[1]);
                out.println("\n");
                break;
            case "GET":
                InputStream in = null;
                byte[] data = null;
                try{ //read the file, and encode it into Base64
                    in = new FileInputStream(cmds[1]);
                    data = new byte[in.available()];
                    in.read(data);
                    in.close();
                    out.println("FILE");
                    out.println(new String(Base64.getEncoder().encode(data)));
                    System.out.println("    The client is trying to get the content of " + cmds[1]);
                } catch (IOException e){
                    out.println("    Error: File not exists.");
                    System.out.println("    The client is trying to get a file that not exists.");
                }
                break;
        }
    }

    private static boolean checkCmd(String cmd, PrintWriter out) {
        //check validation of cmd
        boolean r = true;
        if(cmd == null){
            return false;
        }
        String[] cmds = cmd.split(" ");
        if (cmds[0].equals("\n") || cmds[0].equals("")) {
            r = false;
        } else if (cmds.length > 2) {
            r = false;
        } else if (!cmds[0].equals("GET") && !cmds[0].equals("BOUNCE") && !cmds[0].equals("EXIT")) {
            r = false;
        } else if (cmds[0].equals("GET") || cmds[0].equals("BOUNCE")) {
            if (cmds.length != 2) {
                r = false;
            }
        }

        return r;
    }
}
