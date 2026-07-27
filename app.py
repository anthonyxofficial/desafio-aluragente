import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Atención al Cliente - Bot", page_icon="💬")

st.title("💬 Asistente Virtual de Atención al Cliente")
st.write(
    "¡Hola! Soy el asistente virtual de atención al cliente. ¿En qué te puedo"
    " ayudar hoy?"
)


# Detectar la ruta exacta de la carpeta actual
@st.cache_data
def cargar_datos():
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_base, "datos", "informacion.csv")

    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"Buscado en: {ruta_csv}")

    return pd.read_csv(ruta_csv, sep=';')


try:
    df = cargar_datos()
    st.success("¡Base de datos conectada con éxito!")
except Exception as e:
    st.error(f"No se encontró el archivo de datos. Detalle del sistema: {e}")
    st.stop()

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar conversación anterior
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de usuario
if user_input := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Buscar respuesta en el CSV
    palabras = user_input.lower().split()
    coincidencias = df[
        df["pregunta"]
        .str.lower()
        .apply(lambda p: any(w in p for w in palabras if len(w) > 3))
    ]

    if not coincidencias.empty:
        respuesta = coincidencias.iloc[0]["respuesta"]
    else:
        respuesta = (
            "Gracias por tu consulta. En este momento no encontré esa"
            " información en la base de datos, pero un agente de soporte te"
            " atenderá en breve."
        )

    with st.chat_message("assistant"):
        st.markdown(respuesta)
    st.session_state.messages.append(
        {"role": "assistant", "content": respuesta}
    )
