import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi chat de IA", page_icon="👍")
st.title("Mi primera aplicacion con Streamlit")

nombre = st.text_input("Cual es tu nombre?")
if st.button("Saludar!"):
    st.write(f"Hola {nombre}! Bienvenido a talento tech")

MODELOS = [ 'llama3-8b-8192' , 'llama3-70b-8192' , 'mixtral-8x7b-32768' ] 

def configurar_pagina():
    st.title("Mi Chat de IA")   
    st.sidebar.title("Configuracion de la IA")

    elegirModelo = st.sidebar.selectbox("Elegi un modelo",
                                        options = MODELOS,
                                        index = 0)

    return elegirModelo

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente,modelo,mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user","content": mensajeDeEntrada}],
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def actualizar_historial(rol,contenido,avatar):
    st.session_state.mensajes.append({"role":rol, "content": contenido,
                                    "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]): st.markdown(mensaje["content"])

def area_chat():
    contenedor_chat = st.container(height=400, border= True)
    with contenedor_chat: mostrar_historial()

def generar_respuesta(chat):
    respuesta = ""
    for palabra in chat:
        if palabra.choices[0].delta.content:
            respuesta += palabra.choices[0].delta.content
            yield palabra.choices[0].delta.content

    return respuesta

def main():
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    modelo = configurar_pagina()
    area_chat()
    mensaje = st.chat_input("Escribi tu mensaje")

    if mensaje:
        actualizar_historial("user", mensaje, "💻")
        chat = configurar_modelo(clienteUsuario, modelo,mensaje)

        if chat:
            with st.chat_message("assistant"):
                respuesta = st.write_stream(generar_respuesta(chat))
                actualizar_historial("assintant",respuesta,"💻")
                st.rerun()
        #print(mensaje)


if __name__ == "__main__":
    main()

   