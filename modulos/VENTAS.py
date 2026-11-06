import streamlit as st
from config.conexion import obtener_conexion
def mostrar_venta():
    st.header("Registrar venta")
    with st.form("form_venta"):
        producto = st.text_input(
            "Nombre del producto"
        )
        cantidad = st.number_input(
            "Cantidad",
            min_value=1,
            step=1
        )
        guardar = st.form_submit_button(
            "Guardar venta"
        )
    if guardar:
        if producto.strip() == "":
            st.warning(
                "Debe ingresar el nombre del producto."
            )
        else:
            conexion = None
            cursor = None
            try:
                conexion = obtener_conexion()
                if conexion is None:
                    return
                cursor = conexion.cursor()
                consulta = """
                INSERT INTO VENTAS
                (Producto, Cantidad)
                VALUES (%s, %s)
                """
                cursor.execute(
                    consulta,
                    (producto, int(cantidad))
                )
                conexion.commit()
                st.success(
                    "Venta registrada correctamente."
                )
            except Exception as error:
                if conexion is not None:
                    conexion.rollback()
                st.error(
                    f"Error al registrar la venta: {error}"
                )
            finally:
                if cursor is not None:
                    cursor.close()
                if (
                    conexion is not None
                    and conexion.is_connected()
                ):
                    conexion.close()
