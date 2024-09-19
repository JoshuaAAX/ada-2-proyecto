import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
from modexFB import SocialNetwork, Agent, modexFB

class AplicacionProcesadorTexto:
    def __init__(self, master):
        self.master = master
        master.title("Moderador de extremismo de opiniones en una red")
        master.geometry("1200x600")

        # Marco izquierdo (Algoritmos)
        marco_izquierdo = tk.Frame(master, width=200, height=600, bd=2, relief=tk.GROOVE)
        marco_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(marco_izquierdo, text="fuerza bruta").pack()
        tk.Label(marco_izquierdo, text="Voraz").pack()
        tk.Label(marco_izquierdo, text="dinamico").pack()

        # Marco central
        marco_central = tk.Frame(master, width=500, height=600, bd=2, relief=tk.GROOVE)
        marco_central.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Área de visualización del archivo subido
        self.area_archivo = scrolledtext.ScrolledText(marco_central, width=50, height=25)
        self.area_archivo.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Marco para botones
        marco_botones = tk.Frame(marco_central)
        marco_botones.pack(pady=5, fill=tk.X)

        # Botón de procesar
        self.boton_procesar = tk.Button(marco_botones, text="Procesar", command=self.procesar_texto)
        self.boton_procesar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Botón de subir
        self.boton_subir = tk.Button(marco_botones, text="Subir", command=self.subir_archivo)
        self.boton_subir.pack(side=tk.LEFT, padx=5)

        # Marco derecho
        marco_derecho = tk.Frame(master, width=500, height=600, bd=2, relief=tk.GROOVE)
        marco_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Área de resultados
        self.area_resultados = scrolledtext.ScrolledText(marco_derecho, width=50, height=20)
        self.area_resultados.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Frame para botones adicionales
        frame_botones = tk.Frame(marco_derecho)
        frame_botones.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(frame_botones, text="agentes:").pack(side=tk.LEFT)
        tk.Entry(frame_botones, width=10).pack(side=tk.LEFT, padx=5)

        tk.Label(frame_botones, text="valor:").pack(side=tk.LEFT)
        tk.Entry(frame_botones, width=10).pack(side=tk.LEFT, padx=5)

        tk.Label(frame_botones, text="tiempo").pack(side=tk.LEFT)
        tk.Entry(frame_botones, width=10).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_botones, text="Download").pack(side=tk.LEFT, padx=5)

    def subir_archivo(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if ruta_archivo:
            with open(ruta_archivo, 'r') as archivo:
                contenido = archivo.read()
                self.area_archivo.delete(1.0, tk.END)
                self.area_archivo.insert(tk.END, contenido)

    def procesar_texto(self):
        self.boton_procesar.config(state=tk.DISABLED)
        self.area_resultados.delete(1.0, tk.END)
        self.area_resultados.insert(tk.END, "Procesando...\n")
        threading.Thread(target=self._procesar_red_thread).start()

    def _procesar_red_thread(self):
        try:
            entrada = self.area_archivo.get(1.0, tk.END).strip().split('\n')
            n = int(entrada[0])
            agents = []
            for i in range(1, n+1):
                op, recep = map(float, entrada[i].split(','))
                agents.append(Agent(int(op), recep))
            r_max = int(entrada[-1])

            network = SocialNetwork(agents, r_max)
            best_strategy, best_effort, best_extremism = modexFB(network)

            resultado = f"Ext {best_extremism:.6f}\n"
            resultado += f"Esf {best_effort}\n"
            resultado += ' '.join(map(str, best_strategy))

            self.master.after(0, self._actualizar_resultados, resultado)
        except Exception as e:
            self.master.after(0, self._mostrar_error, str(e))

    def _actualizar_resultados(self, resultado):
        self.area_resultados.delete(1.0, tk.END)
        self.area_resultados.insert(tk.END, resultado)
        self.boton_procesar.config(state=tk.NORMAL)

    def _mostrar_error(self, mensaje):
        messagebox.showerror("Error", f"Ha ocurrido un error: {mensaje}")
        self.boton_procesar.config(state=tk.NORMAL)

root = tk.Tk()
app = AplicacionProcesadorTexto(root)
root.mainloop()