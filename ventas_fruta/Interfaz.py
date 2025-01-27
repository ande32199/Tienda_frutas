import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

# URL base del backend Django
BASE_URL = 'http://127.0.0.1:8000/ventas/'

# Funciones CRUD Genéricas
def obtener_elementos(endpoint, frame, mostrar_func):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}/")
        if response.status_code == 200:
            elementos = response.json()
            mostrar_func(elementos, frame)
        else:
            messagebox.showerror("Error", f"No se pudieron obtener los {endpoint}")
    except Exception as e:
        messagebox.showerror("Error", f"Error de conexión: {e}")

def agregar_elemento(endpoint, datos, obtener_func):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}/", json=datos)
        if response.status_code == 201:
            messagebox.showinfo("Éxito", f"{endpoint.capitalize()} agregado correctamente")
            obtener_func()
        else:
            messagebox.showerror("Error", f"No se pudo agregar el {endpoint}")
    except Exception as e:
        messagebox.showerror("Error", f"Error de conexión: {e}")

def eliminar_elemento(endpoint, elemento_id, obtener_func):
    confirm = messagebox.askyesno("Eliminar", f"¿Está seguro que desea eliminar este elemento?")
    if confirm:
        try:
            response = requests.delete(f"{BASE_URL}{endpoint}/{elemento_id}/")
            if response.status_code == 204:
                messagebox.showinfo("Éxito", "Elemento eliminado correctamente")
                obtener_func()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el elemento")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {e}")

# Mostrar elementos en una lista
def mostrar_elementos(elementos, frame, editar_func, eliminar_func):
    for widget in frame.winfo_children():
        widget.destroy()

    for elemento in elementos:
        elemento_frame = tk.Frame(frame, bg="#f4f4f4", pady=5)
        elemento_frame.pack(fill=tk.X, padx=10, pady=5)

        label = tk.Label(
            elemento_frame,
            text=f"{elemento['id']} - {elemento.get('nombre', 'Sin nombre')} - Detalle: {elemento.get('detalle', 'N/A')}",
            anchor="w"
        )
        label.pack(side=tk.LEFT, padx=10)

        btn_editar = tk.Button(elemento_frame, text="Editar", command=lambda e=elemento: editar_func(e))
        btn_editar.pack(side=tk.RIGHT, padx=5)

        btn_eliminar = tk.Button(elemento_frame, text="Eliminar", command=lambda e=elemento: eliminar_func(e['id']))
        btn_eliminar.pack(side=tk.RIGHT, padx=5)

# Sección Producto
def obtener_productos():
    obtener_elementos('productos', frame_productos, lambda productos, frame: mostrar_elementos(
        productos, frame, editar_producto, lambda producto_id: eliminar_elemento('productos', producto_id, obtener_productos)
    ))

def agregar_producto():
    nombre = simpledialog.askstring("Agregar Producto", "Nombre del producto:")
    if not nombre:
        return
    try:
        detalle = simpledialog.askstring("Agregar Producto", "Detalle del producto:")
        datos = {"nombre": nombre, "detalle": detalle}
        agregar_elemento('productos', datos, obtener_productos)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def editar_producto(producto):
    nuevo_nombre = simpledialog.askstring("Editar Producto", "Nuevo nombre:", initialvalue=producto['nombre'])
    if not nuevo_nombre:
        return
    try:
        nuevo_detalle = simpledialog.askstring("Editar Producto", "Nuevo detalle:", initialvalue=producto['detalle'])
        datos = {"nombre": nuevo_nombre, "detalle": nuevo_detalle}
        agregar_elemento('productos', datos, obtener_productos)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

# Sección Cliente
def obtener_clientes():
    obtener_elementos('clientes', frame_clientes, lambda clientes, frame: mostrar_elementos(
        clientes, frame, editar_cliente, lambda cliente_id: eliminar_elemento('clientes', cliente_id, obtener_clientes)
    ))

def agregar_cliente():
    nombre = simpledialog.askstring("Agregar Cliente", "Nombre del cliente:")
    if not nombre:
        return
    try:
        email = simpledialog.askstring("Agregar Cliente", "Email del cliente:")
        datos = {"nombre": nombre, "email": email}
        agregar_elemento('clientes', datos, obtener_clientes)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def editar_cliente(cliente):
    nuevo_nombre = simpledialog.askstring("Editar Cliente", "Nuevo nombre:", initialvalue=cliente['nombre'])
    if not nuevo_nombre:
        return
    try:
        nuevo_email = simpledialog.askstring("Editar Cliente", "Nuevo email:", initialvalue=cliente['email'])
        datos = {"nombre": nuevo_nombre, "email": nuevo_email}
        agregar_elemento('clientes', datos, obtener_clientes)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

# Sección Venta
def obtener_ventas():
    obtener_elementos('ventas', frame_ventas, lambda ventas, frame: mostrar_elementos(
        ventas, frame, editar_venta, lambda venta_id: eliminar_elemento('ventas', venta_id, obtener_ventas)
    ))

def agregar_venta():
    cliente_id = simpledialog.askstring("Agregar Venta", "ID del cliente:")
    if not cliente_id:
        return
    try:
        total = float(simpledialog.askstring("Agregar Venta", "Total de la venta:"))
        datos = {"cliente_id": cliente_id, "total": total}
        agregar_elemento('ventas', datos, obtener_ventas)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def editar_venta(venta):
    nuevo_total = simpledialog.askstring("Editar Venta", "Nuevo total:", initialvalue=venta['total'])
    if not nuevo_total:
        return
    try:
        datos = {"total": float(nuevo_total)}
        agregar_elemento('ventas', datos, obtener_ventas)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

# Configurar ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Gestión")
ventana.geometry("500x700")

# Sección Productos
tk.Label(ventana, text="Gestión de Productos", font=("Arial", 14)).pack()
frame_productos = tk.Frame(ventana)
frame_productos.pack(fill=tk.BOTH, expand=True, pady=5)
tk.Button(ventana, text="Obtener Productos", command=obtener_productos).pack()

# Sección Clientes
tk.Label(ventana, text="Gestión de Clientes", font=("Arial", 14)).pack()
frame_clientes = tk.Frame(ventana)
frame_clientes.pack(fill=tk.BOTH, expand=True, pady=5)
tk.Button(ventana, text="Obtener Clientes", command=obtener_clientes).pack()

# Sección Ventas
tk.Label(ventana, text="Gestión de Ventas", font=("Arial", 14)).pack()
frame_ventas = tk.Frame(ventana)
frame_ventas.pack(fill=tk.BOTH, expand=True, pady=5)
tk.Button(ventana, text="Obtener Ventas", command=obtener_ventas).pack()

# Ejecutar aplicación
ventana.mainloop()

