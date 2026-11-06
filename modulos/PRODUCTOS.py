import streamlit as st
import pandas as pd
from config.conexion import obtener_conexion

def mostrar_productos():
    st.title("📦 Módulo de Productos")

    tab1, tab2 = st.tabs(["Listado", "Agregar producto"])

    # --- LISTADO ---
    with tab1:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM productos ORDER BY id DESC", conn)
        conn.close()

        buscar = st.text_input("Buscar por nombre")
        if buscar:
            df = df[df["nombre"].str.contains(buscar, case=False)]

        st.dataframe(df, use_container_width=True)

    # --- AGREGAR ---
    with tab2:
        with st.form("form_producto", clear_on_submit=True):
            nombre = st.text_input("Nombre")
            categoria = st.text_input("Categoría")
            precio = st.number_input("Precio", min_value=0.0, step=0.5)
            stock = st.number_input("Stock", min_value=0, step=1)
            guardar = st.form_submit_button("Guardar")

        if guardar:
            if nombre.strip() == "":
                st.warning("El nombre es obligatorio.")
            else:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (%s,%s,%s,%s)",
                    (nombre, categoria, precio, stock),
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success("Producto guardado correctamente.")
                st.rerun()
