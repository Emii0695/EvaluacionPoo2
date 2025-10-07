
from datetime import datetime


class Parcela:
    def __init__(self, id_parcela, superficie_ha, cultivo_actual):
        self.id_parcela = id_parcela
        self.superficie_ha = superficie_ha
        self.cultivo_actual = cultivo_actual
        self.estado = "activa"
        self.historial_eventos = []
        self.registrar_evento("creación", f"Parcela creada con {self.superficie_ha} y cultivo '{self.cultivo_actual}'")

   
    def registrar_evento(self, tipo, detalle):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = {"fecha": fecha, "tipo": tipo, "detalle": detalle}
        self.historial_eventos.append(evento)

    
    def actualizar_cultivo(self, nuevo_cultivo):
        if self.estado == "inactiva":
            print("No se puede actualizar cultivo: la parcela está inactiva.")
            return
        if nuevo_cultivo.strip() == "":
            print("El cultivo no puede ser vacío.")
            return
        anterior = self.cultivo_actual
        self.cultivo_actual = nuevo_cultivo
        self.registrar_evento("actualizar_cultivo", f"Cultivo cambiado de '{anterior}' a '{nuevo_cultivo}'")

   
    def activar(self, motivo):
        self.estado = "activa"
        self.registrar_evento("activar", f"Motivo: {motivo}")


    def desactivar(self, motivo):
        self.estado = "inactiva"
        self.registrar_evento("desactivar", f"Motivo: {motivo}")

   
    def rectificar_superficie(self, nueva_superficie, motivo):
        if nueva_superficie <= 0:
            print(" La superficie debe ser mayor que 0.")
            return
        anterior = self.superficie_ha
        self.superficie_ha = round(nueva_superficie, 2)
        self.registrar_evento("rectificar_superficie", f"{anterior} ha -> {self.superficie_ha} ha (Motivo: {motivo})")


class ParcelaConRiego(Parcela):
    def __init__(self, id_parcela, superficie_ha, cultivo_actual):
        super().__init__(id_parcela, superficie_ha, cultivo_actual)
        self.litros_disponibles = 0
        self.tasa_riego_l_ha = 1500
        self.umbral_min_litros = 2000
        self.estado_riego = "habilitado"
        self.eventos_riego = []

    