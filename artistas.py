class Artista:
    def __init__(self, id_artista, nombre, genero, pais):
        self.id = id_artista
        self.nombre = nombre
        self.genero = genero
        self.pais = pais

    def obtener_ficha_tecnica(self):
        return f"Nombre del artista: {self.nombre} | Género que toca: {self.genero} | Origen: {self.pais}"

    def es_local(self, pais_productora="Argentina"):
        return self.pais.lower() == pais_productora.lower()