import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread #permite una ejecución simultanea, el video y la interfaz gráfica
from PIL import Image, ImageTk


class App:
    def __init__(self, root, captura, salida):
        self.root = root
        self.root.title("Captura de Video")

        # Crear un lienzo para mostrar el video
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        # Botón para iniciar la captura
        self.start_button = ttk.Button(root, text="Iniciar Captura", command=self.iniciar_captura)
        self.start_button.pack()

        # Botón para detener la captura
        self.stop_button = ttk.Button(root, text="Detener Captura", command=self.detener_captura)
        self.stop_button.pack()

        # Configurar la captura y salida de video
        self.captura = captura
        self.salida = salida
        self.captura_thread = None

    def iniciar_captura(self):
        if not self.captura_thread or not self.captura_thread.is_alive():
            self.captura_thread = Thread(target=self.captura_video)
            self.captura_thread.start()
        else:
            messagebox.showinfo("Info", "La captura ya está en marcha.")

    def detener_captura(self):
        if self.captura_thread and self.captura_thread.is_alive():
            self.captura_thread.join()
        else:
            messagebox.showinfo("Info", "La captura no está en marcha.")

    def captura_video(self):
        while self.captura.isOpened():
            ret, imagen = self.captura.read()
            if ret:
                # Mostrar el frame en el lienzo
                self.mostrar_frame(imagen)
                # Guardar el frame en el archivo de salida
                self.salida.write(imagen)
            else:
                break

    def mostrar_frame(self, frame):
        # Convertir la imagen OpenCV a formato compatible con Tkinter
        img_tk = self.convertir_imagen(frame)
        # Actualizar el lienzo con la nueva imagen
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        # Actualizar la ventana
        self.root.update()

    def convertir_imagen(self, imagen):
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        img_tk = Image.fromarray(imagen_rgb)
        img_tk = ImageTk.PhotoImage(image=img_tk)
        return img_tk


# Configurar la captura y salida de video
captura = cv2.VideoCapture(2)
salida = cv2.VideoWriter('videoSalida.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))

# Crear la aplicación Tkinter
root = tk.Tk()
app = App(root, captura, salida)
root.mainloop()

# Liberar los recursos
captura.release()
salida.release()
cv2.destroyAllWindows()

