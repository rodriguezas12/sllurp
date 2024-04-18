import socket
import pickle
import mysql.connector

username = "root"
password = "123456789"
host = "192.168.0.105"
port = 3306

def receive_data(receiver_address):
    # Create a socket object
    portales_id = 1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
            # Crea la conexión
        connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        port=port,
    )

        # Bind the socket to a specific address and port
        s.bind(receiver_address)
        # Listen for incoming connections (1 connection at a time)
        s.listen(1)
        print("Waiting for a connection...")
        # Accept a connection
        connection, client_address = s.accept()
        print(f"Connection from {client_address}")
        while True:
            # Receive the data
            received_data = b""
            while True:
                chunk = connection.recv(4096)
                if not chunk:
                    break
                received_data += chunk
            # Deserialize the received data
            received_array = pickle.loads(received_data)
            # Do something with the received array (e.g., store in MySQL database)
            cursor = connection.cursor()
            cursor.execute("use central")
            # cursor.execute("INSERT INTO almacen (Etiqueta, Cantidad_Total, Pedidos, Recibidos) VALUES ('123456789', '70', '50', '120')")
            if received_array[0] == 'Portales':
                cursor.execute(f"INSERT INTO portales (portal_id, Etiqueta, Tiempo, Status) VALUES ('{portales_id}','{received_array[1]}', {received_array[3]}, {received_array[6]})")
                connection.commit()
                porales = portales + 1

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the connection and the socket when done
        connection.close()
        s.close()
        if connection.is_connected():
            cursor.close()
            connection.close()
# Define the receiver's address (replace with the actual IP address and port)
receiver_address = ('192.168.0.105', 55550)
# Start receiving data
receive_data(receiver_address)