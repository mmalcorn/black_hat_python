import sys
import socket
import getopt
import threading
import subprocess

# Define some global variables

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


""" Responsible for handling command-line arguments and calling the
the rest of our functions """

def usage():
    print("BHP Net Tool")
    print("Usage: bhpnet.py -t target_host -p port")
    print("-l --listen listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given file upon receiving a connection")
    print("-c --command - initialize a command shell")
    print("-u --upload=destination - upon receiving connection upload a file and write to [destination]")
    print()
    print()
    print("Examples: ")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1. -p 5555 -l -u=c:\\target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./ bhpnet.py =t 192.168.11.12 -p 135")
    sys.exit(0)

# Client code
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to our target host
        client.connect((target, port))
        if len(buffer):
            client.send(buffer.encode())
        while True:
            # Now, wait for the data to come back
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode(errors="ignore")

                if recv_len < 4096:
                    break
            print(response,)

            # Wait for more input
            buffer = input("")
            buffer += "\n"

            # Send it off
            client.send(buffer.encode())

    except:
        print("[*] Exception! Exiting.")
    finally:
        client.close()                    

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

        # Read the commandline options
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
            ["help", "listen", "execute", "target", "port", "command", "upload"])
        except getopt.GetoptError as err:
            print(str(error))
            usage()

        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
            elif o in ("-l", "--listen"):
                listen = True
            elif o in ("-e", "--execute"):
                execute = a
            elif o in ("-c", "--commandshell"):
                command = True
            elif o in ("-u" "--upload"):
                upload_destination = a
            elif o in ("-t", "--target"):
                target = a
            elif o in ("-p", "--port"):
                port = int(a)
            else:
                    assert False, "Unhandled Option"

            # Are we going to listen or just send data form stdin?
            if not listen and len(target) and port > 0:
                # Read in the buffer from the commandline
                # This will block, so send CTRL-D if not sending input to stdin

                buffer = sys.stdin.read()

                # send data off
                client_sender(buffer)


                # We are going to listen and potentially upload things, execute
                # commands, and drop shell back. Depending on our command options above
                if listen:
                    server_loop()

main()
                    
                
            
    
