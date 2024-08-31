import tkinter as tk
from tkinter import messagebox, simpledialog
import pickle
import random
import os
import sys

class JuegoAdivinanzas:
    def __init__(self, master):
        # Configuración inicial de la ventana principal
        self.master = master
        self.master.title("Juego de Adivinanzas")
        self.master.geometry("400x200")  # Ajusta el tamaño de la ventana principal

        # Variables para el estado del juego
        self.nombre_archivo = 'estado_juego.pkl'
        self.numero_secreto = 0
        self.intentos = 0

        # Elementos de la interfaz gráfica
        self.label = tk.Label(master, text="¡Bienvenido al juego de adivinanzas!", font=("Arial", 14))
        self.label.pack(pady=10)  # Añade un poco de espacio entre la etiqueta y los botones

        self.boton_nuevo_juego = tk.Button(master, text="Nuevo Juego", command=self.iniciar_nuevo_juego, font=("Arial", 12))
        self.boton_nuevo_juego.pack(pady=5)

        self.boton_adivinar = tk.Button(master, text="Adivinar", command=self.adivinar_numero, font=("Arial", 12))
        self.boton_adivinar.pack(pady=5)

        # Manejar el evento de cierre de la ventana principal
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        # Intentar cargar el estado del juego previo
        self.cargar_estado()

    def guardar_estado(self):
        # Guarda el estado actual del juego en un archivo binario usando pickle
        estado_actual = {'numero_secreto': self.numero_secreto, 'intentos': self.intentos}
        with open(self.nombre_archivo, 'wb') as archivo:
            pickle.dump(estado_actual, archivo)

    def cargar_estado(self):
        try:
            # Intenta cargar el estado del juego desde un archivo binario usando pickle
            with open(self.nombre_archivo, 'rb') as archivo:
                estado_guardado = pickle.load(archivo)
                self.numero_secreto = estado_guardado.get('numero_secreto')
                self.intentos = estado_guardado.get('intentos', 0)
        except FileNotFoundError:
            # Si no se encuentra un juego guardado, muestra un mensaje informativo y comienza uno nuevo
            messagebox.showinfo("Información", "No se encontró un juego guardado. Empezando uno nuevo.")
            self.iniciar_nuevo_juego()
        except Exception as e:
            # Muestra un mensaje de error si hay un problema al cargar el estado del juego
            messagebox.showerror("Error", f"Error al cargar el estado: {e}")

    def iniciar_nuevo_juego(self):
        # Inicia un nuevo juego generando un número secreto y reiniciando los intentos
        self.numero_secreto = random.randint(1, 10)
        self.intentos = 0
        self.guardar_estado()
        messagebox.showinfo("Información", "Nuevo juego iniciado. ¡Buena suerte!")

    def adivinar_numero(self):
        # Solicita al usuario que ingrese un número para adivinar
        intento_usuario = simpledialog.askinteger("Adivinar Número", "Ingresa tu intento:")
        if intento_usuario is not None:
            # Incrementa el contador de intentos y verifica si el número es correcto
            self.intentos += 1

            if intento_usuario == self.numero_secreto:
                messagebox.showinfo("¡Felicidades!", f"¡Has adivinado el número en {self.intentos} intentos!")
                self.iniciar_nuevo_juego()
            elif intento_usuario < self.numero_secreto:
                messagebox.showinfo("Intento Incorrecto", "El número es mayor. ¡Intenta de nuevo!")
            else:
                messagebox.showinfo("Intento Incorrecto", "El número es menor. ¡Intenta de nuevo!")

            self.guardar_estado()

    def cerrar_ventana(self):
        # Función para manejar el evento de cierre de la ventana principal
        # Destruye la ventana y sale del programa
        self.master.destroy()
        sys.exit()

def ejecutar_juego():
    # Crear la ventana principal y la aplicación del juego
    root = tk.Tk()
    app = JuegoAdivinanzas(root)
    
    # Inicia el bucle principal de la interfaz gráfica
    root.mainloop()

if __name__ == "__main__":
    # Ejecutar el juego
    ejecutar_juego()

