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
                "FROM productos ORDER BY id ASC"
            )
            filas = cur.fetchall()
            cur.close()
        except Exception as e:
            st.error(f"Error al cargar los productos: {e}")
            filas = []
        finally:
            conn.close()

        df = pd.DataFrame(filas)

        buscar = st.text_input("Buscar producto por ID")
        if buscar:
            if not buscar.strip().isdigit():
                st.warning("Escribe solo números para buscar por ID.")
            elif not df.empty:
                df = df[df["id"] == int(buscar.strip())]
                if df.empty:
                    st.info("No se encontró ningún producto con ese ID.")

        if not df.empty:
            df["precio"] = df["precio"].astype(float)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": "ID",
                "nombre": "Nombre",
                "categoria": "Categoría",
                "precio": st.column_config.NumberColumn(
                    "Precio", format="$%.2f"
                ),
                "stock": "Stock",
            },
        )
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
