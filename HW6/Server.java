import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;


public class Server {
    public static void main(String[] args) {
        if (args.length != 1) { // Test for correct num. of arguments
            System.err.println( "ERROR server port number not given");
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
            System.out.println("\nWaiting for client to connect...");
            try {
                Socket s_sock = rv_sock.accept();
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(s_sock.getInputStream())
                );
                PrintWriter out = new PrintWriter(
                        new OutputStreamWriter(s_sock.getOutputStream()), true);
                System.out.println("Client's message: " + in.readLine());
                out.println("I got your message");
                s_sock.close();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
}
