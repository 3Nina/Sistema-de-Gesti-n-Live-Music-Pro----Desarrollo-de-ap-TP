import streamlit as st

st.title("veterinaria")
st.subheader("Gestion profesional de Mascotas")

nombre = st.text_input("Nombre del paciente: ")
if st.button("Saludar"):
    st.write(f"Hola {nombre}, bienvenido a la consulta")