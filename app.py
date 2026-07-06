import streamlit as st
from datetime import datetime
import database as db
from album import Album
from artistas import Artista
from conciertos import Concierto

st.set_page_config(page_title="Live Music Pro", layout="wide")
st.title("Live Music Pro - Sistema de Gestión")

# Menú Lateral de Navegación
menu = st.sidebar.selectbox("Módulo de Gestión", ["Artistas", "Álbumes", "Agenda de Conciertos"])

# =====================================================================
# MÓDULO ARTISTAS
# =====================================================================
if menu == "Artistas":
    st.header("Gestión de Artistas")
    
    # Transformar registros de BD en Objetos (Bucle/Repetitiva)
    artistas_db = db.db_read_all_artistas()
    lista_artistas = [Artista(row[0], row[1], row[2], row[3]) for row in artistas_db]

    # Formulario de Alta con Validaciones
    with st.expander("Registrar Nuevo Artista"):
        with st.form("form_alta_artista"):
            nombre = st.text_input("Nombre del Artista / Banda")
            genero = st.text_input("Género Musical")
            pais = st.text_input("País de Origen")
            enviar_alta = st.form_submit_button("Guardar Artista")
            
            if enviar_alta:
                if not nombre.strip() or not genero.strip() or not pais.strip():
                    st.error("Todos los campos son obligatorios.")
                else:
                    db.db_create_artista(nombre.strip(), genero.strip(), pais.strip())
                    st.success(f"¡{nombre} registrado con éxito!")
                    st.rerun()

    # Visualización y Filtros
    st.subheader("Listado de Artistas")
    filtro_pais = st.text_input("Filtrar por país:")
    
    for art in lista_artistas:
        if filtro_pais.lower() in art.pais.lower():
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(art.obtener_ficha_tecnica())
            
            # Botón Modificar Seguro (por ID)
            if col2.button("Editar", key=f"edit_art_{art.id}"):
                st.session_state[f"editando_art_{art.id}"] = True
                
            if st.session_state.get(f"editando_art_{art.id}", False):
                with st.form(f"form_edit_art_{art.id}"):
                    n_nombre = st.text_input("Nuevo Nombre", value=art.nombre)
                    n_genero = st.text_input("Nuevo Género", value=art.genero)
                    n_pais = st.text_input("Nuevo País", value=art.pais)
                    if st.form_submit_button("Actualizar"):
                        db.db_update_artista(art.id, n_nombre, n_genero, n_pais)
                        st.session_state[f"editando_art_{art.id}"] = False
                        st.rerun()

            # Botón Eliminar Seguro (por ID)
            if col3.button("Borrar", key=f"del_art_{art.id}"):
                db.db_delete_artista(art.id)
                st.warning(f"Artista ID {art.id} eliminado.")
                st.rerun()

# =====================================================================
# MÓDULO ÁLBUMES
# =====================================================================
elif menu == "Álbumes":
    st.header("Gestión de Álbumes / Discos")
    
    # Cargar artistas para los selectores de los formularios
    artistas_db = db.db_read_all_artistas()
    dict_artistas = {row[1]: row[0] for row in artistas_db} # Nombre: ID
    
    albumes_db = db.db_read_albumes_con_artista()
    lista_albumes = [Album(row[0], row[1], row[2], row[3]) for row in albumes_db]

    with st.expander("Registrar Nuevo Álbum"):
        if not dict_artistas:
            st.warning("⚠️ Primero debés cargar al menos un artista.")
        else:
            with st.form("form_alta_album"):
                titulo = st.text_input("Título del Álbum")
                anio = st.number_input("Año de Lanzamiento", min_value=1800, max_value=datetime.now().year, value=2026)
                artista_select = st.selectbox("Artista", list(dict_artistas.keys()))
                enviar_alta = st.form_submit_button("Guardar Álbum")
                
                if enviar_alta:
                    if not titulo.strip() or anio < 0:
                        st.error("Verifique los campos. El año no puede ser negativo ni vacío.")
                    else:
                        db.db_create_album(titulo.strip(), anio, dict_artistas[artista_select])
                        st.success(f"¡Álbum '{titulo}' guardado con éxito!")
                        st.rerun()

    st.subheader("Catálogo de Discos")
    
    for alb in lista_albumes:
        col1, col2 = st.columns([4, 1])
        col1.write(alb.obtener_resumen())
        if col2.button("Borrar", key=f"del_alb_{alb.id}"):
            db.db_delete_album(alb.id)
            st.rerun()

# =====================================================================
# MÓDULO AGENDA DE CONCIERTOS
# =====================================================================
elif menu == "Agenda de Conciertos":
    st.header("Agenda de Eventos y Conciertos")
    
    artistas_db = db.db_read_all_artistas()
    dict_artistas = {row[1]: row[0] for row in artistas_db}
    
    conciertos_db = db.db_read_conciertos_con_artista()
    lista_conciertos = [Concierto(row[0], row[1], row[2], row[3], row[4]) for row in conciertos_db]

    with st.expander("Programar Nuevo Concierto"):
        if not dict_artistas:
            st.warning("Primero debés cargar al menos un artista.")
        else:
            with st.form("form_alta_concierto"):
                nombre_evento = st.text_input("Nombre del Concierto / Festival")
                fecha_evento = st.date_input("Fecha del Evento", value=datetime.now())
                ciudad = st.text_input("Ciudad")
                artista_select = st.selectbox("Artista Principal", list(dict_artistas.keys()))
                enviar_alta = st.form_submit_button("Agendar")
                
                if enviar_alta:
                    if not nombre_evento.strip() or not ciudad.strip():
                        st.error("No podés dejar campos de texto vacíos.")
                    else:
                        fecha_str = fecha_evento.strftime("%Y-%m-%d")
                        db.db_create_concierto(nombre_evento.strip(), fecha_str, ciudad.strip(), dict_artistas[artista_select])
                        st.success(f"¡{nombre_evento} agendado correctamente!")
                        st.rerun()

    st.subheader("Próximos Shows y Conciertos Históricos")
    filtro_ciudad = st.text_input("Filtrar eventos por ciudad:")
    
    for con in lista_conciertos:
        if filtro_ciudad.lower() in con.ciudad.lower():
            # Validación visual si el concierto ya pasó
            estado = "(Finalizado)" if con.paso_el_evento() else "(Vigente)"
            col1, col2 = st.columns([4, 1])
            col1.write(f"{con.obtener_info_agenda()} {estado}")
            
            if col2.button("Cancelar / Borrar", key=f"del_con_{con.id}"):
                db.db_delete_concierto(con.id)
                st.rerun()