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

# 2. Función de búsqueda mejorada
def buscar_respuesta(pregunta_usuario, df):
    if df is None or df.empty:
        return "Lo siento, la base de conocimientos no está disponible en este momento."
    
    # 1. Limpiamos la pregunta de signos y mayúsculas
    pregunta_clean = pregunta_usuario.lower().strip()
    for simbolo in ["?", "¿", "!", "¡", ",", ".", ":"]:
        pregunta_clean = pregunta_clean.replace(simbolo, "")
    
    # Saludos rápidos
    saludos = ["hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "saludos"]
    if any(s == palabra for palabra in pregunta_clean.split() for s in saludos):
        return "¡Hola! 👋 ¿En qué te puedo ayudar hoy? Puedes preguntarme sobre nuestros productos, horarios o servicios."

    palabras_usuario = [p for p in pregunta_clean.split() if len(p) > 2]
    
    # 2. Búsqueda por palabras clave en cada fila
    mejor_coincidencia = None
    max_coincidencias = 0
    
    for idx, row in df.iterrows():
        # Combinamos todo el texto de la fila
        texto_fila = " ".join([str(val) for val in row.values]).lower()
        
        # Contamos cuántas palabras del usuario aparecen en la fila
        coincidencias = sum(1 for palabra in palabras_usuario if palabra in texto_fila)
        
        if coincidencias > max_coincidencias:
            max_coincidencias = coincidencias
            # Si el CSV tiene 2 o más columnas (ej: Pregunta, Respuesta), devolvemos la respuesta
            if len(row) >= 2:
                mejor_coincidencia = str(row.iloc[1])
            else:
                mejor_coincidencia = str(row.iloc[0])

    # Si encontramos al menos una coincidencia, la mostramos
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
    # Guardar y mostrar pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar y mostrar respuesta
    with st.chat_message("assistant"):
        respuesta = buscar_respuesta(prompt, df_datos)
        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
