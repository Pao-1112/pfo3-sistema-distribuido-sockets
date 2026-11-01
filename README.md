# Arquitectura Distribuida Orientada a Eventos basada en Sockets

Repositorio correspondiente al trabajo práctico de Sistemas Distribuidos. El proyecto implementa una arquitectura distribuida orientada a eventos utilizando sockets en Python, un pool de hilos para procesamiento concurrente, balanceo de carga, cola de mensajes y un esquema de almacenamiento distribuido.

---

## Descripción del Sistema

El sistema sigue una arquitectura por capas para procesar tareas asíncronas de manera escalable:

1. **Clientes (Web / Móvil):** Inician solicitudes enviando cargas de trabajo (*payloads*) mediante conexiones TCP / WebSockets.
2. **Balanceador de Carga (Nginx / HAProxy):** Distribuye equitativamente las conexiones entrantes entre los nodos servidores disponibles.
3. **Servidores Socket (Listeners):** Reciben las solicitudes del cliente y publican las tareas en la cola de mensajes.
4. **Cola de Mensajes (RabbitMQ):** Actúa como intermediario desacoplado, distribuyendo las tareas recibidas a los trabajadores disponibles.
5. **Workers (Pool de Hilos):** Nodos de procesamiento que consumen las tareas de la cola y ejecutan la lógica concurrente a través de un pool de hilos (`ThreadPoolExecutor`).
6. **Almacenamiento Distribuido:**
   * **PostgreSQL Cluster:** Guarda datos relacionales y de estado.
   * **Amazon S3 / MinIO:** Almacena objetos y archivos pesados generados durante el procesamiento.

---

## Diagrama de Arquitectura

![Arquitectura Distribuida del Sistema](Cliente-Servidor.drawio.png)



## Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Comunicación & Concurrencia:** `socket`, `threading`, `concurrent.futures` (`ThreadPoolExecutor`)
* **Serialización:** JSON
* **Balanceo de Carga:** Nginx / HAProxy
* **Cola de Mensajes:** RabbitMQ
* **Almacenamiento:** PostgreSQL, Amazon S3 / MinIO

---

## Guía de Ejecución Local

Sigue estos pasos para probar la interacción entre el servidor socket y el cliente en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/<tu-usuario>/sistema-distribuido-sockets.git
cd sistema-distribuido-sockets
```

### 2. Iniciar el Servidor
Abre una terminal y ejecuta el servidor de sockets (escuchará en `127.0.0.1:65432` con un pool de 4 workers):
```bash
python servidor.py
```

### 3. Ejecutar el Cliente
Abre una **segunda terminal** y ejecuta el cliente para enviar una tarea de prueba:
```bash
python cliente.py
```

---

## 📂 Estructura del Repositorio

```text
.
├── servidor.py                # Servidor de sockets con pool de hilos para tareas concurrentes
├── cliente.py                 # Cliente socket emisor de tareas en formato JSON
├── Cliente-Servidor.drawio.png # Diagrama de arquitectura del sistema
└── README.md                  # Documentación principal del proyecto
```