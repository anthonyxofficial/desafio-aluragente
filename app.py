import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Asistente IA", page_icon="🤖")
st.title("🤖 Asistente Virtual Inteligente")

# 1. Configurar la API Key de Gemini
# Usamos secretos de Streamlit o un campo en la interfaz si no está configurado
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    with st.sidebar:
        st.subheader("Configuración")
        api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")

if not api_key:
    st.info("💡 Por favor, ingresa tu API Key de Gemini en la barra lateral para comenzar.")
    st.stop()

# Configurar el cliente de Gemini
genai.configure(api_key=api_key)

# Usamos la sintaxis directa actualizada
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception:
    model = genai.GenerativeModel("gemini-1.5-pro")

# 2. Cargar la base de datos CSV
@st.cache_data
def cargar_datos():
    try:
        # Probamos leerlo ignorando líneas mal formadas o usando sep=None para detectar el separador
        df = pd.read_csv("datos/informacion.csv", on_bad_lines='skip', engine='python')
        return df.to_string()
    except Exception as e:
        st.error(f"Error al cargar el archivo de datos: {e}")
        return ""

contexto_csv = cargar_datos()

# 3. Historial de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Entrada del usuario y generación de respuesta
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    # Guardar y mostrar pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Crear el prompt con contexto para Gemini
    system_prompt = f"""
    Eres un asistente de atención al cliente amable, profesional y servicial.
    Responde a las preguntas del usuario basándote ÚNICAMENTE en la siguiente información de la empresa:

    --- INFORMACIÓN BASE DE DATOS ---
    {contexto_csv}
    ---------------------------------

    Instrucciones:
    1. Si la respuesta está en la información anterior, responde de forma clara, natural y concisa.
    2. Si la información NO está disponible en la base de datos, responde amablemente indicando que no tienes esa información disponible y sugiere contactar a un asesor.
    3. Mantén un tono amigable.
    """

    # Generar respuesta con la IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                chat = model.start_chat(history=[])
                # Enviamos las instrucciones del sistema + el historial reciente
                response = model.generate_content(
                    f"{system_prompt}\n\nPregunta del usuario: {prompt}"
                )
                respuesta_texto = response.text
                st.markdown(respuesta_texto)
                st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            except Exception as e:
                st.error(f"Ocurrió un error al generar la respuesta: {e}")
