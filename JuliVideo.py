import cv2
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Usar cv2.CAP_DSHOW para mejorar la compatibilidad con algunas cámaras en Windows
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # Cambiar la resolución a 1920x1080
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.video_label = QLabel()  # Etiqueta para mostrar el video
        self.start_button = QPushButton('Iniciar grabación')
        self.stop_button = QPushButton('Detener grabación')
        self.play_button = QPushButton('Reproducir video')  # Botón para reproducir el video generado

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.play_button)

        self.central_widget.setLayout(layout)

        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.play_button.clicked.connect(self.play_video)  # Conecta el botón de reproducción a la función

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Actualiza el video cada 30 milisegundos

        self.is_recording = False
        self.video_writer = None

    def update_frame(self):
        ret, frame = self.video.read()
        if ret:
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(image)
            self.video_label.setPixmap(pixmap)

            # Obtener la resolución actual
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
            #print(f"Resolución actual de la cámara: {current_width}x{current_height}")

            print("Capacidades de la cámara:")
            print("WIDTH:", self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
            print("HEIGHT:", self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print("FPS:", self.video.get(cv2.CAP_PROP_FPS))

            if self.is_recording:
                self.video_writer.write(frame)  # Grabar en formato BGR

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True

            # Obtener la resolución actual
            current_width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
            current_height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
            print(f"Resolución actual de la cámara: {current_width}x{current_height}")

            # Configurar resolución deseada (por si acaso)
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            documents_path = os.path.join("C:\\Python\\grabar_video")
            video_name = os.path.join(documents_path, 'video_grabado.mp4')  # Cambio de extensión a .mp4

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Cambio de códec a mp4v
            resolution = (1920, 1080)  # Resolución deseada
            self.video_writer = cv2.VideoWriter(video_name, fourcc, 10.0, resolution)

            if self.video_writer.isOpened():
                print(f"Usando el códec MP4V para la grabación en formato MP4 con resolución {resolution}.")
                print("Iniciando grabación...")
            else:
                print("No se pudo abrir el archivo de video con el códec MP4V en formato MP4.")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.video_writer.release()
            print("Deteniendo grabación...")

    def play_video(self):
        documents_path = os.path.join("C:\\Python\\grabar_video")
        video_name = os.path.join(documents_path, 'video_grabado.mp4')

        if os.path.exists(video_name):
            os.startfile(video_name)
        else:
            print("¡El archivo de video no existe!")

if __name__ == '__main__':
    app = QApplication([])
    window = CameraApp()
    window.show()
    app.exit(app.exec_())


