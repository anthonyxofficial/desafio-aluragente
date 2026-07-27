import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Asistente de Atención al Cliente", page_icon="🤖")
st.title("🤖 Asistente Virtual")
st.write("¡Hola! Soy tu asistente de atención al cliente. ¿En qué puedo ayudarte hoy?")

# 1. Cargar la base de datos CSV especificando el separador ';'
@st.cache_data
def cargar_datos():
    try:
        # Añadimos sep=';' para que lea correctamente tus columnas
        df = pd.read_csv("datos/informacion.csv", sep=";", on_bad_lines='skip', engine='python')
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo de datos: {e}")
        return None

df_datos = cargar_datos()

# 2. Búsqueda de respuestas en el CSV
def buscar_respuesta(pregunta_usuario, df):
    if df is None or df.empty:
        return "Lo siento, la base de conocimientos no está disponible en este momento."
    
    # Limpiamos la pregunta
    pregunta_clean = pregunta_usuario.lower().strip()
    for simbolo in ["?", "¿", "!", "¡", ",", ".", ":"]:
        pregunta_clean = pregunta_clean.replace(simbolo, "")
    
    # Saludos
    saludos = ["hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "saludos"]
    if any(s == palabra for palabra in pregunta_clean.split() for s in saludos):
        return "¡Hola! 👋 ¿En qué te puedo ayudar hoy? Puedes preguntarme por nuestros horarios, ubicación, métodos de pago o envíos."

    palabras_usuario = [p for p in pregunta_clean.split() if len(p) > 2]
    
    mejor_coincidencia = None
    max_coincidencias = 0
    
    for idx, row in df.iterrows():
        texto_fila = " ".join([str(val) for val in row.values]).lower()
        coincidencias = sum(1 for palabra in palabras_usuario if palabra in texto_fila)
        
        if coincidencias > max_coincidencias:
            max_coincidencias = coincidencias
            # Toma la columna de Respuesta (segunda columna)
            if len(row) >= 2:
                mejor_coincidencia = str(row.iloc[1])
            else:
                mejor_coincidencia = str(row.iloc[0])

    if mejor_coincidencia and max_coincidencias > 0:
        return mejor_coincidencia
                
    return "Lo siento, no encontré información específica sobre tu consulta. ¿Deseas contactar a un asesor?"

# 3. Historial de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Procesar la pregunta del usuario
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        respuesta = buscar_respuesta(prompt, df_datos)
        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
