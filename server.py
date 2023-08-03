import socket
import os

HOST, PORT = 'localhost', 8000
BASE_DIR = 'html_files'  # Directory containing HTML files

# Create socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    try:
        # Bind the socket to a specific address and port
        server_socket.bind((HOST, PORT))

        # Listen for incoming connections
        server_socket.listen()
        print(f"Server running on {HOST}:{PORT}")

        while True:
            # Accept a new client connection
            client_socket, client_address = server_socket.accept()
            print(f"New connection from {client_address}")

            try:
                # Read the request data from the client
                request_data = client_socket.recv(1024).decode()
                print(request_data)
                # [    "GET /group.html HTTP/1.1",           "Host: localhost:8000",    ...]
                # Extract the requested path from the HTTP request
                request_lines = request_data.split('\r\n')
                if len(request_lines) > 0:
                    path = request_lines[0].split()[1]

                    # Get the file path by joining the base directory with the requested path
                    file_path = os.path.join(BASE_DIR, path.strip('/'))

                    # Check if the file exists
                    if os.path.isfile(file_path):
                        # Read the file content
                        with open(file_path, 'r') as file:
                            file_content = file.read()

                        # Prepare the HTTP response
                        response_data = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + file_content
                    else:
                        # File not found
                        response_data = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n" + \
                                        "<html><body><h1>404 Not Found</h1></body></html>"

                    # Send the response back to the client
                    client_socket.sendall(response_data.encode())

            except Exception as e:
                # Handle any exceptions that occur during request processing
                print(f"Error processing request: {str(e)}")

            finally:
                # Close the connection with the client
                client_socket.close()

    except Exception as e:
        # Handle any exceptions that occur during server startup
        print(f"Error starting server: {str(e)}")
