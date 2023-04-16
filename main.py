"""Importacion de modulos a utilizar"""
import tkinter as tk
from tkinter import ttk
import cv2 as cv
import pyautogui as bot
import numpy as np
import os
from server import Server
import threading
from PIL import ImageTk, Image
import socket

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Aplicacion(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.state_conn = False
        self.state_stream = False

        self.address = tk.StringVar(value="127.0.0.1")
        self.port = tk.IntVar(value=5555)

        self.streamer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.widgets()

    def host(self):
        def sendFrame():
            # Change if show stream or not
            def switchShowVideo():
                nonlocal streamerShowVideo
                streamerShowVideo = not streamerShowVideo

            # Show stream at Streamer
            def showVideo():
                nonlocal streamerShowVideo
                if streamerShowVideo:
                    img_tk = ImageTk.PhotoImage(
                        image=Image.fromarray(screenshot))
                    lbl_img.config(image=img_tk)
                    lbl_img.image = img_tk

            # Init somethings
            streamerShowVideo = True
            ttk.Button(self.frmStream, text="Ocultar video", command=switchShowVideo).grid(
                row=1, column=1, padx=5, pady=10, sticky="nsew"
            )
            
            # Connect to server like client for stream the video
            server_addr = (self.address.get(), self.port.get())
            self.streamer.connect(server_addr)

            # Loop of the stream
            while self.inStream:
                # Video
                frame = np.array(bot.screenshot())
                screenshot = cv.resize(frame, (780, 400))

                # Send video to server
                _, buffer = cv.imencode(".jpg", screenshot)
                encoded_image_bytes = buffer.tobytes()
                self.streamer.sendall(encoded_image_bytes)

                # Call the function to show the video
                showVideo()

        # Disconnect client and server, and shutdow the video stream comeback to menu
        def shutdownStream():
            nonlocal server
            self.streamer.close()
            server.stop()
            self.inStream = False
            self.controlWidgets(True)

        # GUI
        self.controlWidgets()
        self.frmStream = ttk.Frame(self.master)
        self.frmStream.grid(
            row=0, column=0, padx=5, pady=10
        )
        self.state_stream = True

        lbl_img = ttk.Label(self.frmStream)
        lbl_img.grid(
            row=0, column=0, padx=5, pady=10, sticky="nsew", columnspan=2
        )

        self.frmStream.columnconfigure(0, weight=1)
        self.frmStream.rowconfigure(0, weight=1)

        ttk.Button(self.frmStream, text="Apagar", command=shutdownStream).grid(
            row=1, column=0, padx=5, pady=10, sticky="nsew"
        )

        # Server
        server = Server(self.address.get(), self.port.get())
        threading.Thread(target=server.run).start()

        # Send Frame
        self.inStream = True

        thread = threading.Thread(target=sendFrame)
        thread.daemon = True
        thread.start()

    def client(self):
        print("cliente")

    def controlWidgets(self, backMain=bool(False)):
        if self.state_conn:
            self.frameConn.grid_forget()
            self.state_conn = False

        if self.state_stream:
            self.frmStream.grid_forget()
            self.state_stream = False

        if backMain:
            self.widgets()

    def widgets(self):
        self.frameMain = ttk.Frame(self.master)
        self.frameMain.grid(
            row=0, column=0
        )

        btn_host = ttk.Button(self.frameMain, text="Host",
                              command=lambda: self.panelConnection('host'))
        btn_host.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew"
        )

        btn_client = ttk.Button(
            self.frameMain, text="client", command=lambda: self.panelConnection("client"))
        btn_client.grid(
            row=0, column=1, padx=10, pady=10, sticky="nsew"
        )

    def panelConnection(self, conn):
        self.frameMain.grid_forget()
        self.state_conn = True

        self.frameConn = ttk.Frame(self.master)
        self.frameConn.grid(
            row=0, column=0
        )

        if conn == "host":
            title = "Hosting"
            btn = "Comenzar Streaming"
            command = self.host

        else:
            title = "Unirse a ..."
            btn = "Conectarse"
            command = self.client

        lbl_hostTitle = ttk.Label(
            self.frameConn, text=title, anchor="center", font=('Arial', 16))
        lbl_hostTitle.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
        )

        lbl_address = ttk.Label(self.frameConn, text="Direccion:")
        lbl_address.grid(
            row=1, column=0, padx=10, pady=10, sticky="nsew"
        )

        ent_address = ttk.Entry(self.frameConn, textvariable=self.address)
        ent_address.grid(
            row=1, column=1, padx=10, pady=10, sticky="nsew"
        )

        lbl_port = ttk.Label(self.frameConn, text="Puerto:")
        lbl_port.grid(
            row=2, column=0, padx=10, pady=10, sticky="nsew"
        )

        ent_port = ttk.Entry(self.frameConn, textvariable=self.port)
        ent_port.grid(
            row=2, column=1, padx=10, pady=10, sticky="nsew"
        )

        btn_connect = ttk.Button(self.frameConn, text=btn, command=command)
        btn_connect.grid(
            row=3, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
        )

        btn_menu = ttk.Button(self.frameConn, text="Volver",
                              command=lambda: self.controlWidgets(True))
        btn_menu.grid(
            row=4, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
        )


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Capturadora")

    # Tema Azure descargado de 'https://github.com/rdbende/Azure-ttk-theme'
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = Aplicacion(root)

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) -
                      (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) -
                      (root.winfo_height() / 2))
    root.geometry(f"+{x_cordinate}+{y_cordinate-20}")

    root.mainloop()
