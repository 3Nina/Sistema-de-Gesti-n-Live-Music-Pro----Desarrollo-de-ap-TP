import sqlite3

DATABASE_NAME = "live_music_pro.db"

def init_db():
    """Inicializa las tablas de la base de datos si no existen."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artistas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        genero TEXT NOT NULL,
        pais TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS albumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        anio_lanzamiento INTEGER NOT NULL,
        id_artista INTEGER,
        FOREIGN KEY (id_artista) REFERENCES artistas(id) ON DELETE SET NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conciertos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_evento TEXT NOT NULL,
        fecha TEXT NOT NULL,
        ciudad TEXT NOT NULL,
        id_artista INTEGER,
        FOREIGN KEY (id_artista) REFERENCES artistas(id) ON DELETE SET NULL
    );
    """)
    
    conn.commit()
    conn.close()

# Ejecutar inicialización al importar
init_db()

# --- CRUD ARTISTAS ---
def db_create_artista(nombre, genero, pais):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO artistas (nombre, genero, pais) VALUES (?, ?, ?)", (nombre, genero, pais))
    conn.commit()
    conn.close()

def db_read_all_artistas():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artistas")
    rows = cursor.fetchall()
    conn.close()
    return rows

def db_update_artista(id_artista, nombre, genero, pais):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE artistas SET nombre = ?, genero = ?, pais = ? WHERE id = ?", (nombre, genero, pais, id_artista))
    conn.commit()
    conn.close()

def db_delete_artista(id_artista):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM artistas WHERE id = ?", (id_artista,))
    conn.commit()
    conn.close()


# --- CRUD ÁLBUMES ---
def db_create_album(titulo, anio_lanzamiento, id_artista):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO albumes (titulo, anio_lanzamiento, id_artista) VALUES (?, ?, ?)", (titulo, anio_lanzamiento, id_artista))
    conn.commit()
    conn.close()

def db_read_albumes_con_artista():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    query = """
        SELECT al.id, al.titulo, al.anio_lanzamiento, ar.nombre AS artista 
        FROM albumes al 
        LEFT JOIN artistas ar ON al.id_artista = ar.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def db_update_album(id_album, titulo, anio_lanzamiento, id_artista):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE albumes SET titulo = ?, anio_lanzamiento = ?, id_artista = ? WHERE id = ?", (titulo, anio_lanzamiento, id_artista))
    conn.commit()
    conn.close()

def db_delete_album(id_album):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM albumes WHERE id = ?", (id_album,))
    conn.commit()
    conn.close()


# --- CRUD CONCIERTOS ---
def db_create_concierto(nombre_evento, fecha, ciudad, id_artista):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conciertos (nombre_evento, fecha, ciudad, id_artista) VALUES (?, ?, ?, ?)", (nombre_evento, fecha, ciudad, id_artista))
    conn.commit()
    conn.close()

def db_read_conciertos_con_artista():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    query = """
        SELECT c.id, c.nombre_evento, c.fecha, c.ciudad, ar.nombre AS artista 
        FROM conciertos c 
        LEFT JOIN artistas ar ON c.id_artista = ar.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def db_update_concierto(id_concierto, nombre_evento, fecha, ciudad, id_artista):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE conciertos SET nombre_evento = ?, fecha = ?, ciudad = ?, id_artista = ? WHERE id = ?", (nombre_evento, fecha, ciudad, id_concierto))
    conn.commit()
    conn.close()

def db_delete_concierto(id_concierto):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conciertos WHERE id = ?", (id_concierto,))
    conn.commit()
    conn.close()