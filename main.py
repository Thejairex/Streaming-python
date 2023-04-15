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

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Aplicacion(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.state_conn = False

        self.address = tk.StringVar()
        self.port = tk.IntVar()

        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.widgets()
        
    def host(self):
        server = Server()
        threading.Thread(target=server.run).start()

    def client(self):
        pass

    def sendFrame(self):
        pass

    def controlWidgets(self):
        if self.state_conn:
            self.frameConn.grid_forget()

    def widgets(self):
        self.frameMain = ttk.Frame(self.master)
        self.frameMain.grid(
            row = 0, column=0
            )

        btn_host = ttk.Button(self.frameMain, text="Host", command=self.host)
        btn_host.grid(
            row = 0, column=0, padx=10, pady=10, sticky="nsew"
            )

        btn_client = ttk.Button(self.frameMain, text="client", command=lambda: self.panelConnection("host"))
        btn_client.grid(
            row = 0, column=1, padx=10, pady=10, sticky="nsew"
            )
        
    def panelConnection(self, conn):
        self.frameMain.grid_forget()
        self.state_conn = True

        self.frameConn = ttk.Frame(self.master)
        self.frameConn.grid(
            row = 0, column=0
            )

        if conn == "host":
            title = "Hosting"
            btn = "Comenzar Streaming"

        else:
            title = "Cliente"
            btn = "Conectarse"
        
        lbl_hostTitle = ttk.Label(self.frameConn, text=title)
        lbl_hostTitle.grid(
            row = 0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
        )

        lbl_address = ttk.Label(self.frameConn, text="Direccion:")
        lbl_address.grid(
            row = 1, column=0, padx=10, pady=10, sticky="nsew"
        )

        ent_address = ttk.Entry(self.frameConn, textvariable=self.address)
        ent_address.grid(
            row = 1, column=1, padx=10, pady=10, sticky="nsew"
        )

        lbl_port = ttk.Label(self.frameConn, text="Puerto:")
        lbl_port.grid(
            row = 2, column=0, padx=10, pady=10, sticky="nsew"
        )

        ent_port = ttk.Entry(self.frameConn, textvariable=self.port)
        ent_port.grid(
            row = 2, column=1, padx=10, pady=10, sticky="nsew"
        )

        btn_connect = ttk.Button(self.frameConn, text=btn, command=self.sendFrame)
        btn_connect.grid(
            row = 3, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
        )

        btn_menu = ttk.Button(self.frameConn, text="Volver", command=self.sendFrame)
        btn_menu.grid(
            row = 4, column=0, padx=10, pady=10, sticky="nsew", columnspan=2
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
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry(f"+{x_cordinate}+{y_cordinate-20}")

    root.mainloop()
