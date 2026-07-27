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
    palabras_clave = [p for p in pregunta_clean.split() if len(p) > 2]
    
    # Recorremos cada fila del CSV buscando coincidencias
    for idx, row in df.iterrows():
        # Convertimos los valores de la fila a texto de forma segura
        texto_fila = " ".join([str(val) for val in row.values]).lower()
        
        # Buscamos si alguna palabra clave está en la fila
        for palabra in palabras_clave:
            if palabra in texto_fila:
                # Retornamos la respuesta (columna 2) o la fila junta si solo hay 1 columna
                if len(row) >= 2:
                    return str(row.iloc[1])
                return str(row.iloc[0])
                
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
