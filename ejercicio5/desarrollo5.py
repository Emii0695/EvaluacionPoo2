import math
from datetime import datetime
from typing import List, Union, Dict

class CuerpoCeleste:
    MASA_MINIMA = 1e-10 # Establecer un valor cercano a cero para validación

    def __init__(self, id_celeste: str, nombre: str, masa_kg: float):
        # Atributos encapsulados
        self.__id_celeste = id_celeste
        self.__nombre = self._validar_nombre(nombre)
        self.__masa_kg = self._validar_masa(masa_kg)
        
        # Auditoría
        self.__historial_eventos: List[Evento] = []
        self.__fecha_ultima_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__num_modificaciones = 0
        
        self._registrar_evento("Inicialización", "N/A", f"Masa: {self.__masa_kg} kg", silent=True)
        
    # --- Propiedades (Getters y Derivados) ---
    @property
    def id_celeste(self): return self.__id_celeste
    @property
    def nombre(self): return self.__nombre
    @property
    def masa_kg(self): return self.__masa_kg
    @property
    def historial_eventos(self) -> List[Evento]: return list(self.__historial_eventos)
    @property
    def fecha_ultima_actualizacion(self) -> str: return self.__fecha_ultima_actualizacion
    @property
    def num_modificaciones(self) -> int: return self.__num_modificaciones
    
    # --- Métodos Auxiliares Internos ---
    
    def _registrar_evento(self, campo: str, valor_anterior: Union[str, float, int], 
                          valor_nuevo: Union[str, float, int], silent: bool = False):
        self.__historial_eventos.append(Evento(campo, valor_anterior, valor_nuevo))
        self.__fecha_ultima_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__num_modificaciones += 1
        if not silent:
            print(f"[AUDIT] -> {campo} registrado.")
            
    def _validar_nombre(self, nombre: str) -> str:
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacío.")
        return nombre.strip()

    def _validar_masa(self, masa: float) -> float:
        # Regla: La masa nunca puede ser ≤ 0.
        if masa <= self.MASA_MINIMA:
            raise ValueError(f"La masa debe ser positiva (mayor a {self.MASA_MINIMA} kg).")
        return masa
        
    # --- Operaciones ---

    def actualizar_nombre(self, nuevo_nombre: str):
        try:
            nuevo_nombre_validado = self._validar_nombre(nuevo_nombre)
        except ValueError as e:
            print(f"❌ Error de validación de nombre: {e}")
            return
            
        nombre_previo = self.__nombre
        self.__nombre = nuevo_nombre_validado
        self._registrar_evento("nombre", nombre_previo, self.__nombre)
        print(f"✅ Nombre actualizado a: '{self.__nombre}'")

    def actualizar_masa(self, nueva_masa: float):
        try:
            nueva_masa_validada = self._validar_masa(nueva_masa)
        except ValueError as e:
            print(f"❌ Error de validación de masa: {e}")
            return

        masa_previa = self.__masa_kg
        self.__masa_kg = nueva_masa_validada
        self._registrar_evento("masa_kg", masa_previa, self.__masa_kg)
        print(f"✅ Masa actualizada a: {self.__masa_kg:.2e} kg.")

    def consultar_ficha(self) -> Dict:
        # Devuelve datos actuales más últimos eventos.
        return {
            "nombre": self.nombre,
            "masa_kg": self.masa_kg,
            "ultima_actualizacion": self.fecha_ultima_actualizacion,
            "num_modificaciones": self.num_modificaciones
        }

class Planeta(CuerpoCeleste):
    def __init__(self, id_celeste: str, nombre: str, masa_kg: float, radio_km: float, distancia_sol_km: float):
        # Llama al constructor de la clase padre (CuerpoCeleste)
        super().__init__(id_celeste, nombre, masa_kg)
        
        # Atributos adicionales encapsulados
        self.__radio_km = self._validar_parametro(radio_km, "radio_km")
        self.__distancia_sol_km = self._validar_parametro(distancia_sol_km, "distancia_sol_km")
        
    # --- Propiedades (Getters) ---
    @property
    def radio_km(self) -> float: return self.__radio_km
    @property
    def distancia_sol_km(self) -> float: return self.__distancia_sol_km
    
    # --- Métodos Auxiliares Internos ---
    
    def _validar_parametro(self, valor: float, campo: str) -> float:
        # Regla: El radio y la distancia al sol deben ser mayores que cero.
        if valor <= 0:
            raise ValueError(f"El campo '{campo}' debe ser mayor que cero.")
        return valor

    # --- Operaciones ---

    def actualizar_radio(self, nuevo_radio: float):
        try:
            nuevo_radio_validado = self._validar_parametro(nuevo_radio, "radio_km")
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
            return

        radio_previo = self.__radio_km
        self.__radio_km = nuevo_radio_validado
        self._registrar_evento("radio_km", radio_previo, self.__radio_km)
        print(f"✅ Radio actualizado a: {self.__radio_km:.2e} km.")

    def actualizar_distancia_sol(self, nueva_distancia: float):
        try:
            nueva_distancia_validada = self._validar_parametro(nueva_distancia, "distancia_sol_km")
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
            return

        distancia_previa = self.__distancia_sol_km
        self.__distancia_sol_km = nueva_distancia_validada
        self._registrar_evento("distancia_sol_km", distancia_previa, self.__distancia_sol_km)
        print(f"✅ Distancia al Sol actualizada a: {self.__distancia_sol_km:.2e} km.")

    def calcular_densidad(self) -> Union[float, str]:
        # Volumen aproximado de una esfera: V = 4/3 * π * radio³
        try:
            volumen_km3 = (4/3) * math.pi * (self.__radio_km ** 3)
            # Densidad = Masa / Volumen
            densidad_kg_km3 = self.masa_kg / volumen_km3
            # Redondeamos para presentación
            return round(densidad_kg_km3, 6)
        except Exception:
            return "Error al calcular densidad: Volumen o Masa no válidos."

    def comparar_distancia(self, otro_planeta: 'Planeta') -> str:
        # Regla: Comparaciones solo son válidas entre objetos del tipo Planeta.
        if not isinstance(otro_planeta, Planeta):
            return "❌ Error: La comparación solo es válida entre objetos de tipo Planeta."

        distancia_propia = self.distancia_sol_km
        distancia_otro = otro_planeta.distancia_sol_km
        nombre_otro = otro_planeta.nombre

        if distancia_propia < distancia_otro:
            return f"✔️ {self.nombre} está más cerca del Sol ({distancia_propia:.2e} km) que {nombre_otro} ({distancia_otro:.2e} km)."
        elif distancia_propia > distancia_otro:
            return f"✔️ {nombre_otro} está más cerca del Sol ({distancia_otro:.2e} km) que {self.nombre} ({distancia_propia:.2e} km)."
        else:
            return f"✔️ {self.nombre} y {nombre_otro} están aproximadamente a la misma distancia del Sol."

# Clase auxiliar para el historial_eventos
class Evento:
    def __init__(self, campo: str, valor_anterior: Union[str, float, int], valor_nuevo: Union[str, float, int]):
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.campo = campo
        self.valor_anterior = str(valor_anterior)
        self.valor_nuevo = str(valor_nuevo)

    def __str__(self):
        return (f"[{self.fecha}] CAMBIO en '{self.campo}': De '{self.valor_anterior}' a '{self.valor_nuevo}'")