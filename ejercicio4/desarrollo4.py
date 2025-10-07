from datetime import datetime
from typing import List, Union, Dict

class Vehiculo:
    PESO_MINIMO = 0.001 

    def __init__(self, id_vehiculo: str, patente: str, peso_kg: float):
        # Atributos encapsulados
        self.__id_vehiculo = id_vehiculo
        self.__patente = self._validar_patente(patente) # Patente inmutable
        self.__peso_kg = self._validar_peso(peso_kg)
        self.__estado = "habilitado"
        
        # Historial y contadores derivados
        self.__historial_eventos: List[Evento] = []
        self.__conteo_estado = 0
        self.__fecha_ultima_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self._registrar_evento("Inicialización", "N/A", f"Patente: {self.__patente}, Peso: {self.__peso_kg} kg", usuario="Admin")

    # --- Propiedades (Getters) ---
    @property
    def patente(self): return self.__patente
    @property
    def peso_kg(self): return self.__peso_kg
    @property
    def estado(self): return self.__estado
    @property
    def historial_eventos(self) -> List[Evento]: return list(self.__historial_eventos)
    @property
    def conteo_cambios_estado(self) -> int: return self.__conteo_estado
    @property
    def fecha_ultima_actualizacion(self) -> str: return self.__fecha_ultima_actualizacion
    
    # --- Métodos Auxiliares Internos ---
    
    def _registrar_evento(self, campo: str, valor_anterior: Union[str, float, int], 
                          valor_nuevo: Union[str, float, int], usuario: str = "Sistema", silent: bool = False):
        self.__historial_eventos.append(Evento(campo, str(valor_anterior), str(valor_nuevo), usuario))
        self.__fecha_ultima_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not silent:
            print(f"[AUDIT] -> {campo} registrado.")

    def _validar_patente(self, patente: str) -> str:
        if not patente or patente.strip() == "":
            raise ValueError("La patente no puede estar vacía.")
        return patente.strip().upper()

    def _validar_peso(self, peso: float) -> float:
        if peso <= self.PESO_MINIMO:
            raise ValueError(f"El peso debe ser positivo (mayor a {self.PESO_MINIMO} kg).")
        return round(peso, 2)
    
    # --- Operaciones ---

    def actualizar_peso(self, nuevo_peso_kg: float, usuario: str = "Sistema"):
        # Regla: No se permiten operaciones sobre vehículos inhabilitados salvo habilitar.
        if self.__estado == "inhabilitado":
            print(f"❌ RECHAZADO: El vehículo está inhabilitado. Operación de peso no permitida.")
            return

        try:
            nuevo_peso_validado = self._validar_peso(nuevo_peso_kg)
        except ValueError as e:
            print(f"❌ Error de validación de peso: {e}")
            return

        peso_previo = self.__peso_kg
        self.__peso_kg = nuevo_peso_validado
        self._registrar_evento("Actualización Peso", peso_previo, self.__peso_kg, usuario)
        print(f"✅ Peso actualizado a: {self.__peso_kg:.2f} kg.")

    def habilitar(self, motivo: str, usuario: str = "Sistema"):
        if self.__estado == "habilitado":
            print("ℹ️ El vehículo ya está habilitado.")
            return
        
        self._registrar_evento("Cambio Estado", self.__estado, "habilitado", usuario)
        self.__estado = "habilitado"
        self.__conteo_estado += 1
        print(f"✅ Vehículo **habilitado**. Motivo: {motivo}")

    def inhabilitar(self, motivo: str, usuario: str = "Sistema"):
        if self.__estado == "inhabilitado":
            print("ℹ️ El vehículo ya está inhabilitado.")
            return
        
        self._registrar_evento("Cambio Estado", self.__estado, "inhabilitado", usuario)
        self.__estado = "inhabilitado"
        self.__conteo_estado += 1
        print(f"✅ Vehículo **inhabilitado**. Motivo: {motivo}")
        
    def consultar_ficha(self) -> Dict:
        # Devuelve datos actuales y últimas marcas de auditoría.
        return {
            "patente": self.patente,
            "peso_kg": self.peso_kg,
            "estado": self.estado,
            "conteo_cambios_estado": self.conteo_cambios_estado,
            "fecha_ultima_actualizacion": self.fecha_ultima_actualizacion
        }

class Auto(Vehiculo):
    def __init__(self, id_vehiculo: str, patente: str, peso_kg: float, 
                 asientos_totales: int, sistema_retencion_infantil: str = "no"):
        
        # Llama al constructor de la clase padre (Vehiculo)
        super().__init__(id_vehiculo, patente, peso_kg)
        
        # Atributos adicionales encapsulados
        self.__asientos_totales = self._validar_asientos(asientos_totales)
        self.__ocupantes_actuales = 0
        self.__sistema_retencion_infantil = sistema_retencion_infantil.lower()
        self.__eventos_ocupacion: List[EventoOcupacion] = [] # Solo lectura
        
    # --- Propiedades (Getters y Derivados) ---
    @property
    def ocupantes_actuales(self) -> int: return self.__ocupantes_actuales
    
    @property
    def asientos_libres(self) -> int:
        return self.__asientos_totales - self.__ocupantes_actuales
        
    @property
    def tasa_ocupacion(self) -> float:
        if self.__asientos_totales == 0: return 0.0
        return round((self.__ocupantes_actuales / self.__asientos_totales) * 100, 2)

    @property
    def eventos_ocupacion(self) -> List[EventoOcupacion]: return list(self.__eventos_ocupacion)
    
    # --- Métodos Auxiliares Internos ---
        
    def _validar_asientos(self, asientos: int) -> int:
        if asientos < 1:
            raise ValueError("Los asientos totales deben ser al menos 1.")
        return asientos
    
    def _check_estado(self, operacion: str) -> bool:
        # Regla: No se puede subir_personas ni bajar_personas si el vehículo está inhabilitado.
        if self.estado == "inhabilitado":
            print(f"❌ RECHAZADO: El auto está inhabilitado. Operación '{operacion}' no permitida.")
            # Registro en el historial general (heredado)
            self._registrar_evento("Rechazo Operación", operacion, self.estado, silent=True)
            return False
        return True

    def _registrar_evento_ocupacion(self, accion: str, cantidad: int, antes: int, despues: int, usuario: str = "Sistema"):
        self.__eventos_ocupacion.append(EventoOcupacion(accion, cantidad, antes, despues, usuario))
        
    # --- Operaciones de Ocupación ---

    def subir_personas(self, n: int, usuario: str = "Sistema"):
        if not self._check_estado("Subir Personas"): return
        
        # Regla: n ≥ 1
        if n < 1:
            print("❌ Error: La cantidad de personas a subir debe ser al menos 1.")
            return

        asientos_libres = self.asientos_libres
        
        # Regla: ocupantes_actuales + n ≤ asientos_totales
        if n > asientos_libres:
            print(f"❌ RECHAZADO: Excede el límite. Solo quedan {asientos_libres} asientos libres (solicitados: {n}).")
            return
            
        ocupantes_previos = self.__ocupantes_actuales
        self.__ocupantes_actuales += n
        
        self._registrar_evento_ocupacion("Subida", n, ocupantes_previos, self.__ocupantes_actuales, usuario)
        print(f"✅ Subieron {n} personas. Ocupantes: {self.__ocupantes_actuales}.")

    def bajar_personas(self, n: int, usuario: str = "Sistema"):
        if not self._check_estado("Bajar Personas"): return

        # Regla: n ≥ 1
        if n < 1:
            print("❌ Error: La cantidad de personas a bajar debe ser al menos 1.")
            return
            
        # Regla: ocupantes_actuales - n ≥ 0
        if self.__ocupantes_actuales - n < 0:
            print(f"❌ RECHAZADO: No puede bajar {n} personas. Solo hay {self.__ocupantes_actuales} ocupantes.")
            return

        ocupantes_previos = self.__ocupantes_actuales
        self.__ocupantes_actuales -= n
        
        self._registrar_evento_ocupacion("Bajada", n, ocupantes_previos, self.__ocupantes_actuales, usuario)
        print(f"✅ Bajaron {n} personas. Ocupantes: {self.__ocupantes_actuales}.")

    def reconfigurar_asientos(self, nuevo_total: int, motivo: str, usuario: str = "Sistema"):
        try:
            nuevo_total_validado = self._validar_asientos(nuevo_total)
        except ValueError as e:
            print(f"❌ Error de validación de asientos: {e}")
            return
            
        # Regla: Si reconfigurar_asientos reduce asientos por debajo de la ocupación actual, debe rechazarse.
        if self.__ocupantes_actuales > nuevo_total_validado:
            print(f"❌ RECHAZADO: Ocupación actual ({self.__ocupantes_actuales}) excede el nuevo total ({nuevo_total_validado}).")
            return
            
        asientos_previos = self.__asientos_totales
        self.__asientos_totales = nuevo_total_validado
        
        self._registrar_evento("Reconfiguración Asientos", asientos_previos, self.__asientos_totales, usuario)
        print(f"✅ Asientos reconfigurados a {self.__asientos_totales}. Motivo: {motivo}")

    def vaciar_auto(self, motivo: str, usuario: str = "Sistema"):
        if self.__ocupantes_actuales == 0:
            print("ℹ️ El auto ya está vacío.")
            return
            
        ocupantes_previos = self.__ocupantes_actuales
        self.__ocupantes_actuales = 0
        
        self._registrar_evento_ocupacion("Vaciar Auto", ocupantes_previos, ocupantes_previos, 0, usuario)
        print(f"✅ Auto vaciado (Bajaron {ocupantes_previos} personas). Motivo: {motivo}")

    def consultar_ocupacion(self) -> Dict:
        # Devuelve ocupantes actuales, asientos libres y tasa de ocupación.
        return {
            "ocupantes_actuales": self.ocupantes_actuales,
            "asientos_libres": self.asientos_libres,
            "tasa_ocupacion": f"{self.tasa_ocupacion}%"
        }

# Clase auxiliar para el historial_eventos (Modelo A)
class Evento:
    def __init__(self, campo: str, detalle_anterior: str, detalle_nuevo: str, usuario: str = "Sistema"):
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.usuario = usuario
        self.tipo_evento = campo 
        self.detalle_anterior = detalle_anterior
        self.detalle_nuevo = detalle_nuevo

    def __str__(self):
        return (f"[{self.fecha} - {self.usuario}] {self.tipo_evento}: "
                f"De '{self.detalle_anterior}' a '{self.detalle_nuevo}'")

# Clase auxiliar para los eventos_ocupacion (Modelo B)
class EventoOcupacion:
    def __init__(self, accion: str, cantidad: int, ocupantes_antes: int, ocupantes_despues: int, usuario: str = "Sistema"):
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.usuario = usuario
        self.accion = accion
        self.cantidad = cantidad
        self.ocupantes_antes = ocupantes_antes
        self.ocupantes_despues = ocupantes_despues

    def __str__(self):
        return (f"[{self.fecha} - {self.usuario}] OCUPACIÓN ({self.accion}): Cantidad: {self.cantidad} p. "
                f"Ocupantes: {self.ocupantes_antes} -> {self.ocupantes_despues}")
