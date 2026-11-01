import socket
import threading
import json
from concurrent.futures import ThreadPoolExecutor

HOST = '127.0.0.1'
PORT = 65432
MAX_WORKERS = 4

def procesar_tarea(datos_tarea):
    """Bloque de procesamiento de la tarea para el worker."""
    task_id = datos_tarea.get("task_id")
    payload = datos_tarea.get("payload", "")

    #Para procesar el payload por ejemplo transformacion de texto, calculo o logica de negocio.
    resultado_procesado = payload.upper()

    return {
        "status" : "SUCCESS",
        "task_id" : task_id,
        "result" : resultado_procesado
    }

def manejar_cliente(conn, addr, pool):
    """Maneja una conexión individual de cliente de forma concurrente."""
    print(f"[+] Conexión establecida desde {addr}")
    try:
        data = conn.recv(1024).decode('utf-8')
        if data:
            datos_tarea = json.loads(data)
            print(f"[*] Tarea recibida con ID: {datos_tarea.get("task_id")}")

            #Para enviar la tarea al pool de hilos (workers)
            future = pool.submit(procesar_tarea, datos_tarea)
            resultado = future.result()

            #Para enviar el resultado de vuelta a través del socket al cliente
            conn.sendall(json.dumps(resultado).encode('utf-8'))
    except Exception as e:
        respuesta_error = {"status": "Error", "message": str(e)}
        conn.sendall(json.dumps(respuesta_error).encode('utf-8'))
    finally:
        conn.close()
        print(f"[-] Conexión cerrada para {addr}")

def iniciar_servidor():
    """Inicializa y ejecuta el bucle principal del servidor de socket."""
    pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[SERVIDOR INICIADO] Escuchando en {HOST}:{PORT} con un pool de {MAX_WORKERS} workers...")

    try:
        while True:
            conn, addr = server_socket.accept()
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr, pool))
            hilo_cliente.daemon = True
            hilo_cliente.start()
    except KeyboardInterrupt:
        print("\n[SERVIDOR DETENIÉNDOSE POR EL USUARIO]")
    finally:
        server_socket.close()
        pool.shutdown(wait=False)

if __name__ == "__main__":
    iniciar_servidor = iniciar_servidor()