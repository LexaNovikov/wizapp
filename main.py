import os
import sys
import socket
import json

import dotenv
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider
from PyQt6.QtCore import Qt

dotenv.load_dotenv()

WIZ_IP = os.getenv("lamp_ip")
WIZ_PORT = 38899

def get_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    command = {
        "method": "getPilot"
    }
    sock.sendto(json.dumps(command).encode('utf-8'), (WIZ_IP, WIZ_PORT))
    data, _ = sock.recvfrom(1024)
    response = json.loads(data.decode('utf-8'))
    print(response)
    return response

def send_command(params):
    command = {
        "method": "setPilot",
        "params": params
    }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(command).encode('utf-8'), (WIZ_IP, WIZ_PORT))
# def turn_off():
#      send_command({"state": False})
# def turn_on():
#     send_command({"state": True})
# def change_temp(val):
#     send_command({"temp": int(val)})
# def set_warm():
#     send_command({"temp": 2700})
# def change_dimming(val):
#     send_command({"dimming": int(val)})
# def set_yut():
#     data = get_data()
#     current_dimming = data['result']['dimming']
#     send_command({"dimming":current_dimming//2, "temp": 2700})
# turn_on()



class WizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WiZ Control")
        self.setFixedSize(350, 250)

        # Главный секрет: делаем системный фон окна полностью прозрачным
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Задаем полупрозрачный темный фон через CSS (rgba), а текст делаем белым
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 200); /* 200 из 255 - это степень непрозрачности */
                border-radius: 15px;
                color: white;
                font-family: JetBrainsMono Nerd Font;
            }
            QPushButton {
                background-color: rgba(60, 60, 60, 255);
                border-radius: 14px;
                padding: 10px;
                margin-top: 8px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 255);
            }
            QSlider::groove:horizontal {
                border-radius: 4px;
                height: 8px;
                background: rgba(100, 100, 100, 255);
            }
            QSlider::handle:horizontal {
                background: #FFE202;
                width: 16px;
                margin: -2px 0;
                border-radius: 5px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 20)

        # Заголовок
        title = QLabel("Лампа")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(" font-size: 20px; font-weight: bold; background-color: transparent;")
        layout.addWidget(title)

        # Кнопки
        btn_layout = QHBoxLayout()
        btn_on = QPushButton("Включить")
        btn_on.setStyleSheet("background-color: rgba(155,195,159,0.3)")  # Зеленая
        btn_on.clicked.connect(lambda: send_command({"state": True}))

        btn_off = QPushButton("Выключить")
        btn_off.setStyleSheet("background-color: rgba(195,155,155,0.3)")  # Красная
        btn_off.clicked.connect(lambda: send_command({"state": False}))

        btn_layout.addWidget(btn_on)
        btn_layout.addWidget(btn_off)
        layout.addLayout(btn_layout)

        # Ползунок
        lbl_temp = QLabel("Баланс белого")
        lbl_temp.setStyleSheet("background-color: transparent; margin-top: 15px; font-size: 14px;")
        layout.addWidget(lbl_temp)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(2200, 6500)
        data = get_data()
        slider.setValue(data['result']['temp'])
        slider.valueChanged.connect(lambda val: send_command({"temp": val}))
        layout.addWidget(slider)

        lbl_temp = QLabel("Яркость")
        lbl_temp.setStyleSheet("background-color: transparent; margin-top: 15px; font-size: 14px;")
        layout.addWidget(lbl_temp)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(10, 100)
        slider.setValue(data['result']['dimming'])
        slider.valueChanged.connect(lambda val: send_command({"dimming": val}))
        layout.addWidget(slider)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("wiz-control")
    app.setDesktopFileName("wiz-control")
    window = WizApp()
    window.show()
    sys.exit(app.exec())

