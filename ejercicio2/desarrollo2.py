from datetime import datetime
from typing import List

class Publicacion:
    ANIO_MINIMO = 1450 # Regla de negocio: Inicio de la imprenta moderna

    def __init__(self, id_publicacion: str, titulo: str, anio: int):
        # Atributos "privados" (encapsulados)
        self.__id_publicacion = id_publicacion
        self.__titulo = self._validar_titulo(titulo)
        self.__anio = self._validar_anio(anio)
        self.__historial_eventos: List[Evento] = []  # Solo lectura

    # --- Propiedades (Getters) ---
    @property
    def id_publicacion(self) -> str:
        return self.__id_publicacion

    @property
    def titulo(self) -> str:
        return self.__titulo

    @property
    def anio(self) -> int:
        return self.__anio
    
    @property
    def historial_eventos(self) -> List[Evento]:
        return list(self.__historial_eventos)

    # --- Métodos Auxiliares Internos ---
    
    def _registrar_evento(self, campo: str, valor_anterior: str, valor_nuevo: str):
        self.__historial_eventos.append(Evento(campo, valor_anterior, valor_nuevo))
            
    def _validar_titulo(self, titulo: str) -> str:
        if not titulo or titulo.strip() == "":
            raise ValueError("El título no puede estar vacío.")
        return titulo.strip()

    def _validar_anio(self, anio: int) -> int:
        if anio < self.ANIO_MINIMO:
            raise ValueError(f"El año debe ser igual o posterior a {self.ANIO_MINIMO} (Imprenta moderna).")
        return anio

    # --- Operaciones ---

    def actualizar_titulo(self, nuevo_titulo: str):
        try:
            nuevo_titulo_validado = self._validar_titulo(nuevo_titulo)
        except ValueError as e:
            print(f"❌ Error de validación de título: {e}")
            return

        titulo_previo = self.__titulo
        self.__titulo = nuevo_titulo_validado
        self._registrar_evento("titulo", titulo_previo, self.__titulo)
        print(f"✅ Título actualizado a: '{self.__titulo}'")

    def actualizar_anio(self, nuevo_anio: int):
        try:
            nuevo_anio_validado = self._validar_anio(nuevo_anio)
        except ValueError as e:
            print(f"❌ Error de validación de año: {e}")
            return

        anio_previo = str(self.__anio)
        self.__anio = nuevo_anio_validado
        self._registrar_evento("anio", anio_previo, str(self.__anio))
        print(f"✅ Año actualizado a: {self.__anio}")

class Libro(Publicacion):
    def __init__(self, id_publicacion: str, titulo: str, anio: int, paginas_totales: int):
        # Llama al constructor de la clase padre (Publicacion)
        super().__init__(id_publicacion, titulo, anio)
        
        # Atributos adicionales "privados"
        self.__paginas_totales = self._validar_paginas_totales(paginas_totales)
        self.__paginas_leidas = 0
        self.__eventos_lectura: List[EventoLectura] = [] # Solo lectura

    # --- Propiedades (Getters) ---
    
    @property
    def paginas_totales(self) -> int:
        # Regla: paginas_totales no se puede cambiar una vez creado
        return self.__paginas_totales
    
    @property
    def paginas_leidas(self) -> int:
        # Solo cambia por la operación 'leer'
        return self.__paginas_leidas
    
    @property
    def eventos_lectura(self) -> List[EventoLectura]:
        return list(self.__eventos_lectura)
    
    # --- Métodos Auxiliares Internos ---
    
    def _validar_paginas_totales(self, paginas: int) -> int:
        if paginas <= 0:
            raise ValueError("Las páginas totales deben ser un número positivo.")
        return paginas

    def _registrar_evento_lectura(self, paginas_leidas: int, acumulado: int):
        self.__eventos_lectura.append(EventoLectura(paginas_leidas, acumulado))

    # --- Operaciones ---

    def leer(self, paginas: int):
        # Regla: No se pueden leer páginas negativas
        if paginas <= 0:
            print("❌ Error de lectura: La cantidad de páginas a leer debe ser positiva.")
            return

        paginas_restantes = self.__paginas_totales - self.__paginas_leidas
        
        # Regla: No se pueden leer más que las restantes
        if paginas > paginas_restantes:
            print(f"❌ Rechazo de lectura: Solo quedan {paginas_restantes} páginas por leer (solicitadas: {paginas}).")
            
            # Se permite leer las restantes como un caso especial si la solicitud es excesiva
            paginas_a_leer = paginas_restantes
            if paginas_a_leer == 0:
                print("ℹ️ El libro ya está completo.")
                return
            print(f"✅ Leyendo las {paginas_a_leer} páginas restantes para finalizar el libro.")
        else:
            paginas_a_leer = paginas

        saldo_antes = self.__paginas_leidas
        self.__paginas_leidas += paginas_a_leer
        
        # Regla: Toda lectura queda registrada en eventos_lectura
        self._registrar_evento_lectura(paginas_a_leer, self.__paginas_leidas)
        
        # Imprimir progreso
        progreso = self.consultar_progreso()
        print(f"📖 Leídas {paginas_a_leer} páginas. Total leído: {self.__paginas_leidas}/{self.__paginas_totales} ({progreso:.2f}%)")


    def consultar_progreso(self) -> float:
        # Devuelve % leído
        if self.__paginas_totales == 0:
            return 0.0
        
        progreso_porcentaje = (self.__paginas_leidas / self.__paginas_totales) * 100
        # Criterio: muestra porcentaje redondeado (redondeamos a 2 decimales para la precisión)
        return round(progreso_porcentaje, 2)

# Clase auxiliar para guardar los eventos generales (historial_eventos)
class Evento:
    def __init__(self, campo: str, valor_anterior: str, valor_nuevo: str):
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.campo = campo
        self.valor_anterior = valor_anterior
        self.valor_nuevo = valor_nuevo

    def __str__(self):
        return f"[{self.fecha}] CAMBIO en '{self.campo}': De '{self.valor_anterior}' a '{self.valor_nuevo}'"

# Clase auxiliar para guardar los eventos de lectura (eventos_lectura)
class EventoLectura:
    def __init__(self, paginas_leidas: int, acumulado: int):
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.paginas_leidas = paginas_leidas
        self.acumulado = acumulado

    def __str__(self):
        return (f"[{self.fecha}] LECTURA: Leídas {self.paginas_leidas} páginas. "
                f"Acumulado total: {self.acumulado}")

