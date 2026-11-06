import streamlit as st
import pandas as pd
from config.conexion import obtener_conexion

def mostrar_productos():
    st.header("Módulo de Productos")

    tab1, tab2 = st.tabs(["Listado de productos", "Agregar producto"])

    # ---------- LISTADO ----------
    with tab1:
        conn = obtener_conexion()
        if conn is None:
            st.stop()

        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT id, nombre, categoria, precio, stock "
                "FROM productos ORDER BY id DESC"
            )
            filas = cur.fetchall()
            cur.close()
        except Exception as e:
            st.error(f"Error al cargar los productos: {e}")
            filas = []
        finally:
            conn.close()

        df = pd.DataFrame(filas)

        buscar = st.text_input("Buscar producto por nombre")
        if buscar and not df.empty:
            df = df[df["nombre"].str.contains(buscar, case=False, na=False)]

        st.dataframe(df, use_container_width=True)
        st.caption(f"Total de productos: {len(df)}")

    # ---------- AGREGAR ----------
    with tab2:
        with st.form("form_producto", clear_on_submit=True):
            nombre = st.text_input("Nombre del producto")
            categoria = st.text_input("Categoría")
            precio = st.number_input("Precio ($)", min_value=0.0, step=0.5)
            stock = st.number_input("Stock", min_value=0, step=1)
            guardar = st.form_submit_button("Guardar producto")

        if guardar:
            if nombre.strip() == "":
                st.warning("El nombre es obligatorio.")
            else:
                conn = obtener_conexion()
                if conn is not None:
                    try:
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT INTO productos (nombre, categoria, precio, stock) "
                            "VALUES (%s, %s, %s, %s)",
                            (nombre, categoria, precio, stock),
                        )
                        conn.commit()
                        cur.close()
                        st.success("Producto guardado correctamente.")
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                    finally:
                        conn.close()
