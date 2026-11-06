import streamlit as st
from config.conexion import obtener_conexion
def verificar_usuario(usuario, contrasena):
 conexion = obtener_conexion()
 if conexion is None:
 return None
 cursor = None
 try:
 cursor = conexion.cursor()
 consulta = """
 SELECT Id_Usuario
 FROM USUARIO
 WHERE Usuario = %s AND Contrasena = %s
 LIMIT 1
 """
 cursor.execute(
 consulta,
 (usuario, contrasena)
 )
 resultado = cursor.fetchone()
 return resultado
 except Exception as error:
 st.error(f"Error al verificar el usuario: {error}")
 return None
 finally:
 if cursor is not None:
 cursor.close()
 if conexion.is_connected():
 conexion.close()
def login():
 st.title("Inicio de sesión")
 usuario = st.text_input("Usuario")
 contrasena = st.text_input(
 "Contraseña",
 type="password"
 )
 if st.button("Iniciar sesión"):
 if usuario.strip() == "" or contrasena.strip() == "":
 st.warning(
 "Ingrese su usuario y contraseña."
 )
 else:
 resultado = verificar_usuario(
 usuario,
 contrasena
 )
 if resultado:
 st.session_state["sesion_iniciada"] = True
 st.session_state["usuario"] = usuario
 st.success(
 "Sesión iniciada correctamente."
 )
 st.rerun()
 else:
 st.error(
 "Usuario o contraseña incorrectos."
 )
