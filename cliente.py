import socket
import json
import uuid

HOST = '127.0.0.1'
PORT = 65432

def enviar_tarea(texto_payload):
    """Establece conexión con el servidor de sockets, envía la tarea y recibe el resultado."""
    tarea = {
        "task_id": str(uuid.uuid4()),
        "payload": texto_payload
    }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        print(f"[*] Conectando al servidor en {HOST}:{PORT}...")
        cliente_socket.connect((HOST, PORT))

        #Para enviar los datos de la tarea serializados en JSON
        cliente_socket.sendall(json.dumps(tarea).encode('utf-8'))
        print(f"[*] Tarea enviada con ID : {tarea['task_id']}")

        #Para recibir la respuesta del servidor
        respuesta = cliente_socket.recv(1024).decode('utf-8')
        datos_resultado = json.loads(respuesta)

        return datos_resultado

if __name__ == "__main__":
    payload_ejemplo = "hola arquitectura distribuida mediante sockets en python"
    respuesta = enviar_tarea(payload_ejemplo)
    print("\n[+] Respuesta recibida del servidor:")
    print(json.dumps(respuesta, indent=2))