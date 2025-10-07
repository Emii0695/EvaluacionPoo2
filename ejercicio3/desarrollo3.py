from datetime import datetime
from typing import List, Union

class Actividad:
    DURACION_MINIMA = 1 # Regla de negocio: La duración mínima aceptada es 1 minuto.

    def __init__(self, id_actividad: str, nombre: str, duracion_min: int):
        # Atributos "privados" (encapsulados)
        self.__id_actividad = id_actividad
        self.__nombre = self._validar_nombre(nombre)
        self.__duracion_min = self._validar_duracion(duracion_min)
        self.__historial_eventos: List[Evento] = []  # Solo lectura

    # --- Propiedades (Getters) ---
    @property
    def id_actividad(self) -> str:
        return self.__id_actividad

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def duracion_min(self) -> int:
        # Regla: solo se accede por getter o mediante operación actualizar_duracion
        return self.__duracion_min
    
    @property
    def historial_eventos(self) -> List[Evento]:
        return list(self.__historial_eventos)

    # --- Métodos Auxiliares Internos ---
    
    def _registrar_evento(self, campo: str, valor_anterior: Union[str, int], valor_nuevo: Union[str, int]):
        self.__historial_eventos.append(Evento(campo, str(valor_anterior), str(valor_nuevo)))
            
    def _validar_nombre(self, nombre: str) -> str:
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacío.")
        return nombre.strip()

    def _validar_duracion(self, duracion: int) -> int:
        if duracion < self.DURACION_MINIMA:
            raise ValueError(f"La duración debe ser al menos {self.DURACION_MINIMA} minuto(s).")
        return duracion

    # --- Operaciones ---

    def actualizar_nombre(self, nuevo_nombre: str):
        try:
            nuevo_nombre_validado = self._validar_nombre(nuevo_nombre)
        except ValueError as e:
            print(f" Error de validación de nombre: {e}")
            return

        nombre_previo = self.__nombre
        self.__nombre = nuevo_nombre_validado
        self._registrar_evento("nombre", nombre_previo, self.__nombre)
        print(f" Nombre actualizado a: '{self.__nombre}'")

    def actualizar_duracion(self, nueva_duracion: int):
        try:
            nueva_duracion_validada = self._validar_duracion(nueva_duracion)
        except ValueError as e:
            print(f" Error de validación de duración: {e}")
            return

        duracion_previa = self.__duracion_min
        self.__duracion_min = nueva_duracion_validada
        self._registrar_evento("duracion_min", duracion_previa, self.__duracion_min)
        print(f" Duración actualizada a: {self.__duracion_min} min.")

class Carrera(Actividad):
    def __init__(self, id_actividad: str, nombre: str, duracion_min: int, distancia_km: float = 0.0):
        # Llama al constructor de la clase padre (Actividad)
        super().__init__(id_actividad, nombre, duracion_min)
        
        # Atributos adicionales "privados"
        self.__distancia_km = 0.0 # Se inicializa a 0 y se registra con la operación
        self.__eventos_registro: List[EventoRegistro] = [] # Solo lectura
        
        # Si se proporciona una distancia inicial válida, la registramos.
        if distancia_km > 0:
            self.registrar_distancia(distancia_km)

    # --- Propiedades (Getters) ---
    
    @property
    def distancia_km(self) -> float:
        # Regla: Ni la distancia ni la duración pueden editarse directamente
        return self.__distancia_km
    
    @property
    def eventos_registro(self) -> List[EventoRegistro]:
        return list(self.__eventos_registro)
    
    # --- Métodos Auxiliares Internos ---
    
    def _validar_distancia(self, distancia: float) -> float:
        # Regla: La distancia debe ser positiva.
        if distancia <= 0:
            raise ValueError("La distancia debe ser positiva (mayor a 0 km).")
        # Redondeamos a dos decimales para precisión
        return round(distancia, 2)

    def _registrar_evento_registro(self, distancia_registrada: float, duracion_acumulada: int):
        self.__eventos_registro.append(EventoRegistro(distancia_registrada, duracion_acumulada))

    # --- Operaciones ---

    def registrar_distancia(self, nueva_distancia: float):
        try:
            nueva_distancia_validada = self._validar_distancia(nueva_distancia)
        except ValueError as e:
            print(f" Error de registro de distancia: {e}")
            return

        
        
        self.__distancia_km = nueva_distancia_validada
        
        # Regla: Cada registro de distancia queda en eventos_registro
        self._registrar_evento_registro(self.__distancia_km, self.duracion_min)
        print(f" Distancia registrada: {self.__distancia_km:.2f} km.")

    def calcular_ritmo(self) -> Union[float, str]:
        # Regla: Ritmo solo puede calcularse si existe una distancia registrada válida.
        if self.__distancia_km <= 0:
            return " No se puede calcular el ritmo: Distancia no registrada o igual a 0 km."

        # Operación: devuelve minutos por km (duracion_min / distancia_km)
        ritmo = self.duracion_min / self.__distancia_km
        
        return round(ritmo, 2)

# Clase auxiliar para guardar los eventos generales (historial_eventos)
class Evento:
    def __init__(self, campo: str, valor_anterior: str, valor_nuevo: str):
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.campo = campo
        self.valor_anterior = valor_anterior
        self.valor_nuevo = valor_nuevo

    def __str__(self):
        return f"[{self.fecha}] CAMBIO en '{self.campo}': De '{self.valor_anterior}' a '{self.valor_nuevo}'"

# Clase auxiliar para guardar los eventos de registro (eventos_registro)
class EventoRegistro:
    def __init__(self, distancia_registrada: float, duracion_acumulada: int):
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.distancia_registrada = distancia_registrada
        self.duracion_acumulada = duracion_acumulada

    def __str__(self):
        return (f"[{self.fecha}] REGISTRO: Distancia: {self.distancia_registrada:.2f} km. "
                f"Duración acumulada: {self.duracion_acumulada} min.")