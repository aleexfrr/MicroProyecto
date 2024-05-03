# Alex Ferrandis Ros
import sqlite3
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
# Funció per a conectar a la base de dades SQLite
def conectarBD():
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    return conn, cursor
# Funció per a crear les tables si no existeixen
def crearTables():
    conn, cursor = conectarBD()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            nom TEXT PRIMARY KEY,
            preu REAL,
            stock INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendes (
            nom TEXT PRIMARY KEY,
            quantitat INTEGER
        )
    ''')
    conn.commit()
    conn.close()
# Función para insertar un nuevo artículo en la tabla 'articles'
def insertarArticle():
    nom = simpledialog.askstring("Entrada de Datos", "Nom del article: ")
    preu = simpledialog.askstring("Entrada de Datos", "Preu del article: ")
    stock = simpledialog.askstring("Entrada de Datos", "Stock: ")
    conn, cursor = conectarBD()
    cursor.execute('INSERT INTO articles (nom, preu, stock) VALUES (?, ?, ?)', (nom, preu, stock))
    conn.commit()
    conn.close()
def ferVenda():
    try:
        # Conectar a la base de datos
        conn, cursor = conectarBD()
        # Obtener datos del usuario: nombre del artículo y cantidad vendida
        article = simpledialog.askstring("Entrada de Datos", "Nom del article: ")
        quantitat = simpledialog.askinteger("Entrada de Datos", "Quantitat venuda: ")
        if article is None or quantitat is None:
            print("Venta cancelada.")
            return
        # Actualizar el stock del artículo en la base de datos
        cursor.execute("UPDATE articles SET stock = stock - ? WHERE nom = ?", (quantitat, article))
        # Obtener el ID del artículo
        cursor.execute("SELECT id FROM articles WHERE nom = ?", (article,))
        result = cursor.fetchone()
        id_article = result[0] if result else None
        if id_article is None:
            print(f"No se encontró el artículo '{article}'. Venta cancelada.")
            conn.rollback()
            return
        # Insertar la venta en la tabla 'vendes'
        cursor.execute("INSERT INTO vendes (nom, quantitat) VALUES (?, ?)", (id_article, quantitat))
        # Confirmar los cambios en la base de datos
        conn.commit()
        print("Venta realizada con éxito.")
    except Exception as e:
        # En caso de error, revertir los cambios y mostrar el mensaje de error
        conn.rollback()
        print(f"Ha ocurrido un error al realizar la venta: {e}")
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
def mostrarStock():
    # Consulta SQL para obtener todos los artículos y su stock
    conn, cursor = conectarBD()
    cursor.execute("SELECT nom, preu, stock FROM articles")
    articles = cursor.fetchall()
    conn.close()
    # Crear ventana y configuración
    ventana = tk.Tk()
    ventana.title("Stock de Artículos")
    # Crear un widget de Texto para mostrar los datos
    texto = tk.Text(ventana)
    texto.pack(expand=True, fill=tk.BOTH)  # Expandir para llenar la ventana
    # Agregar los datos al widget de Texto
    for fila in articles:
        texto.insert(tk.END, f"Nombre: {fila[0]}\nPrecio: {fila[1]}\nStock: {fila[2]}\n\n")
    # Ejecutar el bucle principal de la ventana
    ventana.mainloop()
def eliminarDato():
    try:
        conn, cursor = conectarBD()
        nombre = simpledialog.askstring("Entrada de Datos", "Ingresa article: ")
        cursor.execute("DELETE FROM articles WHERE nom=?", (nombre,))
        conn.commit()
        print(f"Article {nombre} eliminat correctament.")
    except sqlite3.Error as e:
        print(f"Error al eliminar el article: {e}")
    finally:
        conn.close()
def calcularTotal():
    conn, cursor = conectarBD()
    total = 0
    cursor.execute("SELECT preu FROM articles")
    conn.close()
    return total
def eixir():
    messagebox.showinfo("Eixida del programa", "Gracies per utilitzar la meua aplicació. Torna prompte!")
    ventana.destroy()
def centrarVentana(ancho, alto, ventana):
    anchoPantalla = ventana.winfo_screenwidth()
    altoPantalla = ventana.winfo_screenheight()
    x = (anchoPantalla // 2) - (ancho // 2)
    y = (altoPantalla // 2) - (alto // 2)
    return f"{ancho}x{alto}+{x}+{y}"
# ------------------------- PROGRAMA PRINCIPAL -------------------------
crearTables()
ventana = tk.Tk()
ventana.title("MENU")
ventana.geometry(centrarVentana(400,400,ventana))
# Crear botons
boton1 = tk.Button(ventana, text="ARTICLE NOU", command=insertarArticle)
boton1.pack(pady=5)
boton2 = tk.Button(ventana, text="FER UNA VENDA", command=ferVenda)
boton2.pack(pady=5)
boton3 = tk.Button(ventana, text="MOSTRAR STOCK", command=mostrarStock)
boton3.pack(pady=5)
boton4 = tk.Button(ventana, text="BORRAR ARTICLE", command=eliminarDato)
boton4.pack(pady=5)
boton5 = tk.Button(ventana, text="EIXIR", command=eixir)
boton5.pack(pady=5)
# Executar el bucle principal de la finestra
ventana.mainloop()