from datetime import datetime

class Album:
    def __init__(self, id_album, titulo, anio_lanzamiento, artista_nombre):
        self.id = id_album
        self.titulo = titulo
        self.anio_lanzamiento = int(anio_lanzamiento)
        self.artista_nombre = artista_nombre if artista_nombre else "Artista Desconocido"

    def calcular_antiguedad(self):
        anio_actual = datetime.now().year
        return anio_actual - self.anio_lanzamiento

    def obtener_resumen(self):
        return f"'{self.titulo}' lanzado por {self.artista_nombre} ({self.calcular_antiguedad()} años de antigüedad)."