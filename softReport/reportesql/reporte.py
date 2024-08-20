import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3

class Ventana:
    def __init__(self):
        self.conn = sqlite3.connect('reportes.db')
        self.cursor = self.conn.cursor()
        self.crear_tabla()

        self.ventana = tk.Tk()
        self.ventana.title("Reportador")
        self.ventana.geometry("500x400")
        self.ventana.minsize(250, 250)
        self.ventana.config(bg="blue")
        
        estilo = ttk.Style()
        estilo.theme_use('vista')
        
        frameUrgencia = ttk.Frame(self.ventana)
        frameProfesor = ttk.Frame(self.ventana)
        frameMateria = ttk.Frame(self.ventana)
        frameLugar = ttk.Frame(self.ventana)
        framenumeroPC = ttk.Frame(self.ventana)
        framecalendar = ttk.Frame(self.ventana)
        frameMensaje = ttk.Frame(self.ventana)
        frameBotones = ttk.Frame(self.ventana)

        frameUrgencia.pack(side="top", fill="both", expand=False)
        frameProfesor.pack(side="top", fill="both", expand=False)
        frameMateria.pack(side="top", fill="both", expand=False)
        frameLugar.pack(side="top", fill="both", expand=False)
        framenumeroPC.pack(side="top", fill="both", expand=False)
        framecalendar.pack(side="top", fill="both", expand=False)
        frameMensaje.pack(side="top", fill="both", expand=True)
        frameBotones.pack(side="top", fill="both", expand=False)

        labelUrgencia = ttk.Label(frameUrgencia, text="Grado de urgencia")
        labelUrgencia.pack(padx=10, pady=(10, 5), expand=False, fill='x', side="left")

        comboUrgencia = ttk.Combobox(frameUrgencia, state="readonly",
            values=["Baja", "Media", "Alta","Resuelto"])
        comboUrgencia.pack(padx=10, pady=(10, 5), expand=True, fill='x', side="right")

        labelProfesor = ttk.Label(frameProfesor, text="Nombre del profesor")
        labelProfesor.pack(padx=10, pady=5, expand=False, fill='x', side="left")

        entryProfesor = ttk.Entry(frameProfesor)
        entryProfesor.pack(padx=10, pady=5, expand=True, fill='x', side="right")

        labelMateria = ttk.Label(frameMateria, text="Nombre de la Materia")
        labelMateria.pack(padx=10, pady=5, expand=False, fill='x', side="left")

        entryMateria = ttk.Entry(frameMateria)
        entryMateria.pack(padx=10, pady=5, expand=True, fill='x', side="right")

        labelLugar = ttk.Label(frameLugar, text="Lugar")
        labelLugar.pack(padx=10, pady=5, expand=False, fill='x', side="left")

        comboLugar = ttk.Combobox(frameLugar, state="readonly",
            values=["Laboratorio mecánica", "Laboratorio computación 1",
                    "Laboratorio computación 2", "Laboratorio electrónica"])
        comboLugar.pack(padx=10, pady=5, expand=True, fill='x', side="right")

        labelnumeroPC = ttk.Label(framenumeroPC, text="Numero de PC")
        labelnumeroPC.pack(padx=10, pady=5, expand=False, fill='x', side="left")

        combonumeroPC = ttk.Combobox(framenumeroPC, state="readonly",
            values=["1", "2","3", "4","5", "6","7", "8","9", 
                    "10","11", "12","13", "14","15", "16","17",
                    "18","19", "20","21", "22","23", "24",])
        combonumeroPC.pack(padx=10, pady=5, expand=True, fill='x', side="right")

        labelcalendario = ttk.Label(framecalendar, text="Fecha del problema")
        labelcalendario.pack(padx=10, pady=5, expand=False, fill='x', side="left")

        self.calendario = DateEntry(framecalendar, width=12, background='darkblue', foreground='white',
                                    borderwidth=2, year=2024, month=4, day=25, locale='es_ES', date_pattern='dd/MM/yyyy')
        self.calendario.pack(padx=10, pady=5, expand=True, fill='x', side="right")
        
        labelMensaje = ttk.Label(frameMensaje, text="Mensaje del reporte")
        labelMensaje.pack(padx=10, pady=5, expand=False, fill='x', side="top")

        entryMensaje = tk.Text(frameMensaje, width=1, height=1, font=('Arial', 10), wrap='word')
        entryMensaje.pack(padx=(10, 0), pady=0, expand=True, fill='both', side="left")

        scrollbar = tk.Scrollbar(frameMensaje, orient="vertical", command=entryMensaje.yview)
        entryMensaje.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(padx=(0, 5), pady=5, side="right", fill="y")

        boton_enviar = ttk.Button(frameBotones, text="Enviar", command=self.enviarDatos)
        boton_enviar.pack(padx=10, pady=10, side='right')
        
        boton_mostrar = ttk.Button(frameBotones, text="Mostrar Reportes", command=self.mostrar_reportes)
        boton_mostrar.pack(padx=10, pady=10, side='left')

        self.entradas: tuple[ttk.Combobox, ttk.Entry, ttk.Entry, ttk.Combobox, ttk.Combobox, tk.Text] = (
            comboUrgencia,
            entryProfesor,
            entryMateria,
            comboLugar,
            combonumeroPC,
            entryMensaje
        )

        self.ventana.mainloop()

    def crear_tabla(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS reportes (
            id INTEGER PRIMARY KEY,
            urgencia TEXT,
            fecha TEXT,
            hora TEXT,
            profesor TEXT,
            materia TEXT,
            lugar TEXT,
            numeroPC TEXT,
            fecha_problema TEXT,
            mensaje TEXT,
            realizado BOOLEAN DEFAULT 0
        )
        ''')
        self.conn.commit()

    def enviarDatos(self):
        urgencia, profesor, materia, lugar, numeroPC, mensaje = (
            self.entradas[0].get(),
            self.entradas[1].get(),
            self.entradas[2].get(),
            self.entradas[3].get(),
            self.entradas[4].get(),
            self.entradas[5].get(1.0, "end-1c")
        )
        errores = []
        if urgencia == "":
            errores.append("elegir grado de importancia")
        if profesor == "":
            errores.append("ingresar nombre del profesor")
        if materia == "":
            errores.append("ingresar nombre del materia")
        if lugar == "":
            errores.append("elegir lugar")
        if numeroPC == "":
            errores.append("elegir un numero de PC")  
        if mensaje == "":
            errores.append("escribir un mensaje")
        if len(errores) > 0:
            mensajeError = "Se debe " + ", ".join(errores) + "."
            mensajeError = " y ".join(mensajeError.rsplit(", ", 1))
            messagebox.showwarning("Falta información", mensajeError)
            return

        semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        fechaHora = datetime.now()
        diaSemana = semana[fechaHora.weekday()]
        fecha = fechaHora.strftime(f"{diaSemana}, %d de %B de %Y")
        hora = fechaHora.strftime("%H:%M")

        datos = {
            'urgencia': urgencia,
            'fecha': fecha,
            'hora': hora,
            'profesor': profesor,
            'materia': materia,
            'lugar': lugar,
            'numeroPC': numeroPC,
            'fecha que se encontro': self.calendario.get(),
            'mensaje': mensaje
        }
        self.escribirFila(datos)

    def escribirFila(self, datos: dict[str, str]):
        self.cursor.execute('''
        INSERT INTO reportes (urgencia, fecha, hora, profesor, materia, lugar, numeroPC, fecha_problema, mensaje)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datos['urgencia'], datos['fecha'], datos['hora'], datos['profesor'], datos['materia'],
            datos['lugar'], datos['numeroPC'], datos['fecha que se encontro'], datos['mensaje']
        ))
        self.conn.commit()
        messagebox.showinfo("Enviado", "Se envió correctamente el reporte.")

    def mostrar_reportes(self):
        ventana_reportes = tk.Toplevel(self.ventana)
        ventana_reportes.title("Lista de Reportes")
        ventana_reportes.geometry("1200x600")  # Ajusta el tamaño de la ventana según sea necesario
        
        # Definir encabezados
        encabezados = ["Hecho", "Urgencia", "Fecha", "Hora", "Profesor", "Materia", "Lugar", "Número PC", "Fecha Problema", "Mensaje",  "Editar"]

        # Mostrar encabezados
        for col, encabezado in enumerate(encabezados):
            label = tk.Label(ventana_reportes, text=encabezado, font=('Arial', 10, 'bold'))
            label.grid(row=0, column=col, padx=5, pady=5, sticky='w')

        # Obtener y mostrar reportes
        reportes = self.cursor.execute('SELECT * FROM reportes').fetchall()
        self.checkboxes = []

        for i, reporte in enumerate(reportes):
            # Mostrar cada reporte en una fila con un checkbox en la primera columna
            estado = tk.IntVar(value=reporte[-1])
            check = tk.Checkbutton(ventana_reportes, variable=estado)
            check.grid(row=i+1, column=0, sticky='w')
            self.checkboxes.append((reporte[0], estado))  # Guardar el id y el estado del checkbox
            
            # Mostrar los demás datos
            for j, dato in enumerate(reporte[1:-1]):
                if j == 8:  # Columna de mensaje
                    label = tk.Label(ventana_reportes, text=dato, wraplength=300, anchor='w')  # Ajusta wraplength según sea necesario
                else:
                    label = tk.Label(ventana_reportes, text=dato)
                label.grid(row=i+1, column=j+1, padx=5, pady=5, sticky='w')

            # Botón de edición
            boton_editar = ttk.Button(ventana_reportes, text="Editar", command=lambda r=reporte: self.editar_reporte(r))
            boton_editar.grid(row=i+1, column=len(encabezados)-1, padx=5, pady=5)

        boton_actualizar = ttk.Button(ventana_reportes, text="Actualizar", command=self.actualizar_reportes)
        boton_actualizar.grid(row=len(reportes)+1, column=0, columnspan=len(encabezados), pady=10)

    def editar_reporte(self, reporte):
        def guardar_cambios():
            # Obtener nuevos valores
            urgencia = comboUrgencia.get()
            fecha_problema = calendario.get()
            mensaje = entryMensaje.get(1.0, "end-1c")
            profesor = entryProfesor.get()
            materia = entryMateria.get()
            numeroPC = combonumeroPC.get()
            
            # Actualizar en la base de datos
            self.cursor.execute('''
            UPDATE reportes
            SET urgencia = ?, fecha_problema = ?, mensaje = ?, profesor = ?, materia = ?, numeroPC = ?
            WHERE id = ?
            ''', (urgencia, fecha_problema, mensaje, profesor, materia, numeroPC, reporte[0]))
            self.conn.commit()
            messagebox.showinfo("Actualización", "Reporte actualizado correctamente.")
            ventana_editar.destroy()
            self.mostrar_reportes()  # Refrescar la lista de reportes

        # Crear ventana de edición
        ventana_editar = tk.Toplevel(self.ventana)
        ventana_editar.title("Editar Reporte")
        
        # Crear y mostrar campos de edición
        ttk.Label(ventana_editar, text="Urgencia").pack(padx=10, pady=5)
        comboUrgencia = ttk.Combobox(ventana_editar, state="readonly", values=["Baja", "Media", "Alta", "Resuelto"])
        comboUrgencia.pack(padx=10, pady=5)
        comboUrgencia.set(reporte[1])
        
        ttk.Label(ventana_editar, text="Fecha Problema").pack(padx=10, pady=5)
        calendario = DateEntry(ventana_editar, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024, month=4, day=25, locale='es_ES', date_pattern='dd/MM/yyyy')
        calendario.pack(padx=10, pady=5)
        calendario.set_date(datetime.strptime(reporte[8], '%d/%m/%Y'))  # Ajustar formato según base de datos
        
        ttk.Label(ventana_editar, text="Mensaje").pack(padx=10, pady=5)
        entryMensaje = tk.Text(ventana_editar, width=40, height=10, font=('Arial', 10), wrap='word')
        entryMensaje.pack(padx=10, pady=5)
        entryMensaje.insert('1.0', reporte[9])

        ttk.Label(ventana_editar, text="Profesor").pack(padx=10, pady=5)
        entryProfesor = ttk.Entry(ventana_editar)
        entryProfesor.pack(padx=10, pady=5)
        entryProfesor.insert(0, reporte[4])
        
        ttk.Label(ventana_editar, text="Materia").pack(padx=10, pady=5)
        entryMateria = ttk.Entry(ventana_editar)
        entryMateria.pack(padx=10, pady=5)
        entryMateria.insert(0, reporte[5])
        
        ttk.Label(ventana_editar, text="Número de PC").pack(padx=10, pady=5)
        combonumeroPC = ttk.Combobox(ventana_editar, state="readonly", values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"])
        combonumeroPC.pack(padx=10, pady=5)
        combonumeroPC.set(reporte[7])

        ttk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios).pack(padx=10, pady=10)

    def actualizar_reportes(self):
        for reporte_id, estado in self.checkboxes:
            self.cursor.execute('UPDATE reportes SET realizado = ? WHERE id = ?', (estado.get(), reporte_id))
        self.conn.commit()
        messagebox.showinfo("Actualización", "Los reportes han sido actualizados correctamente.")

if __name__ == "__main__":
    Ventana()
