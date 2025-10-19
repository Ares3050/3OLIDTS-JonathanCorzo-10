import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = ""
DATABASE = "registros"

def conectar():
    return mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

def getRegistros():
    sql = """SELECT Id, Nombre AS Nombres, Apellidos, Edad, Estatura, Telefono, Genero FROM registros ORDER BY Id DESC;"""
    resultados = []
    cnx = None
    cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor(dictionary=True)
        cur.execute(sql)
        for fila in cur:
            resultados.append(fila)
    finally:
        if cur:
            try: cur.close()
            except Exception: pass
        if cnx:
            try: cnx.close()
            except Exception: pass
    return resultados

def buscarUsuarios(filtro):
    sql = """SELECT Id, Nombre AS Nombres, Apellidos, Edad, Estatura, Telefono, Genero FROM registros WHERE Nombre LIKE %s OR Apellidos LIKE %s OR Telefono LIKE %s ORDER BY Id DESC;"""
    valor_a_buscar = f"%{filtro}%"
    resultados = []
    cnx = None
    cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor(dictionary=True)
        cur.execute(sql, (valor_a_buscar, valor_a_buscar, valor_a_buscar))
        for fila in cur:
            resultados.append(fila)
    finally:
        if cur:
            try: cur.close()
            except Exception: pass
        if cnx:
            try: cnx.close()
            except Exception: pass
    return resultados

def limpiarTreeview(tree):
    for item in tree.get_children():
        tree.delete(item)

def llenarTreeview(tree, filas):
    limpiarTreeview(tree)
    for fila in filas:
        valores = (
            fila.get("Id", ""),
            fila.get("Nombres", ""),
            fila.get("Apellidos", ""),
            fila.get("Edad", ""),
            fila.get("Estatura", ""),
            fila.get("Telefono", ""),
            fila.get("Genero", "")
        )
        tree.insert("", tk.END, values=valores)

def configurarTreeview(tree):
    columnas = ["Id", "Nombres", "Apellidos", "Edad", "Estatura", "Telefono", "Genero"]
    tree["columns"] = columnas
    tree["show"] = "headings"
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor=tk.W)
    tree.column("Id", width=60, anchor=tk.CENTER)
    tree["selectmode"] = "browse"

def btnBuscarClick():
    filtro = entryBusqueda.get().strip()
    try:
        if not filtro:
            resultados = getRegistros()
        else:
            resultados = buscarUsuarios(filtro)
        llenarTreeview(treeRegistros, resultados)
        if len(resultados) == 0:
            messagebox.showinfo("Sin resultados", "No se encontraron registros con ese criterio.")
    except Exception as ex:
        messagebox.showerror("Error", f"Error en la búsqueda: {ex}")

def cargarRegistros():
    try:
        lista = getRegistros()
        llenarTreeview(treeRegistros, lista)
    except Exception as ex:
        messagebox.showerror("Error", f"Error al cargar registros: {ex}")

def main():
    global root, entryBusqueda, treeRegistros

    root = tk.Tk()
    root.title("Actividad 10 DBD - DataGrid")
    root.geometry("900x520")
    root.resizable(True, True)

    frmTop = ttk.Frame(root)
    frmTop.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    ttk.Label(frmTop, text="Búsqueda (nombre, apellidos o teléfono):").pack(side=tk.LEFT)
    entryBusqueda = ttk.Entry(frmTop, width=40)
    entryBusqueda.pack(side=tk.LEFT, padx=8)

    btnBuscar = ttk.Button(frmTop, text="Buscar", command=btnBuscarClick)
    btnBuscar.pack(side=tk.LEFT, padx=5)

    btnVerTodos = ttk.Button(frmTop, text="Ver Todos", command=cargarRegistros)
    btnVerTodos.pack(side=tk.LEFT)

    frmGrid = ttk.Frame(root)
    frmGrid.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

    treeRegistros = ttk.Treeview(frmGrid)
    treeRegistros.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    vsb = ttk.Scrollbar(frmGrid, orient="vertical", command=treeRegistros.yview)
    hsb = ttk.Scrollbar(frmGrid, orient="horizontal", command=treeRegistros.xview)
    treeRegistros.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    hsb.pack(side=tk.BOTTOM, fill=tk.X)

    configurarTreeview(treeRegistros)
    # cargarRegistros()  # Descomenta si quieres cargar todo al iniciar

    root.mainloop()

if __name__ == "__main__":
    main()

