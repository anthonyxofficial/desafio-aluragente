import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Asistente de Atención al Cliente", page_icon="🤖")
st.title("🤖 Asistente Virtual")
st.write("¡Hola! Soy tu asistente de atención al cliente. ¿En qué puedo ayudarte hoy?")

# 1. Cargar la base de datos CSV
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv("datos/informacion.csv", on_bad_lines='skip', engine='python')
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo de datos: {e}")
        return None

df_datos = cargar_datos()

# 2. Función de búsqueda simple por palabras clave
def buscar_respuesta(pregunta_usuario, df):
    if df is None or df.empty:
        return "Lo siento, la base de conocimientos no está disponible en este momento."
    
    pregunta_clean = pregunta_usuario.lower().strip()
    
    # Recorremos cada fila del CSV buscando coincidencias
    for idx, row in df.iterrows():
        # Convertimos la fila completa a texto para buscar palabras clave
        texto_fila = " ".join(row.astype(str)).lower()
        
        # Buscamos palabras de la pregunta dentro de los datos
        palabras_clave = [p for p in pregunta_clean.split() if len(p) > 3]
        for palabra in palabras_clave:
            if palabra in texto_fila:
                # Si encontramos coincidencia, devolvemos el contenido de la fila
                if len(row) >= 2:
                    return f"{row.iloc[1]}"
                return f"{' | '.join(row.astype(str))}"
                
    return "Lo siento, no encontré información específica sobre tu consulta. ¿Deseas contactar a un asesor?"

# 3. Historial de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Procesar la pregunta del usuario
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    # Guardar y mostrar pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar y mostrar respuesta
    with st.chat_message("assistant"):
        respuesta = buscar_respuesta(prompt, df_datos)
        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
