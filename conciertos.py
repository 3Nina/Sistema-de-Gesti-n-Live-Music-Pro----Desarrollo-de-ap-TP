class Concierto:
    def __init__(self, id_concierto, nombre_evento, fecha, ciudad, artista_nombre):
        self.id = id_concierto
        self.nombre_evento = nombre_evento
        self.fecha = fecha  # Formato YYYY-MM-DD
        self.ciudad = ciudad
        self.artista_nombre = artista_nombre if artista_nombre else "Artista Desconocido"

    def obtener_info_agenda(self):
        return f"{self.fecha} - {self.nombre_evento} ({self.ciudad}) | Line-up: {self.artista_nombre}"

    def paso_el_evento(self):
        fecha_actual = datetime.now().date()
        fecha_evento = datetime.strptime(self.fecha, "%Y-%m-%d").date()
        return fecha_evento < fecha_actual