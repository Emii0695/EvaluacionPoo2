from datetime import datetime
from typing import List, Dict

# Clase auxiliar para guardar los eventos generales
class Evento:
    def __init__(self, tipo: str, detalle: str):
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tipo = tipo
        self.detalle = detalle

    def __str__(self):
        return f"[{self.fecha}] {self.tipo}: {self.detalle}"

# Clase auxiliar para guardar los eventos de riego
class EventoRiego(Evento):
    def __init__(self, tipo: str, detalle: str, saldo_antes: float, saldo_despues: float,
                 litros_solicitados: float, litros_aplicados: float, modo: str):
        super().__init__(tipo, detalle)
        self.saldo_antes = saldo_antes
        self.saldo_despues = saldo_despues
        self.litros_solicitados = litros_solicitados
        self.litros_aplicados = litros_aplicados
        self.modo = modo

    def __str__(self):
        return (f"[{self.fecha}] RIEGO ({self.modo}): {self.detalle} | "
                f"Antes: {self.saldo_antes:.2f} L, Aplicado: {self.litros_aplicados:.2f} L, "
                f"Después: {self.saldo_despues:.2f} L")

class Parcela:
    def __init__(self, id_parcela: str, superficie_ha: float, cultivo_actual: str):
        # Atributos "privados" (encapsulados)
        self.__id_parcela = id_parcela
        self.__superficie_ha = self._validar_superficie(superficie_ha)
        self.__cultivo_actual = self._validar_cultivo(cultivo_actual)
        self.__estado = "activa"  # Por defecto activa
        self.__historial_eventos: List[Evento] = []  # Solo lectura

        self._registrar_evento("Creación", "Parcela inicializada.")

    # --- Propiedades (Getters) ---
    @property
    def id_parcela(self):
        return self.__id_parcela

    @property
    def superficie_ha(self):
        # Regla: superficie_ha no se modifica por acceso directo
        return self.__superficie_ha

    @property
    def cultivo_actual(self):
        return self.__cultivo_actual

    @property
    def estado(self):
        return self.__estado
    
    @property
    def historial_eventos(self) -> List[Evento]:
        # Retorna una copia para mantenerlo 'solo lectura'
        return list(self.__historial_eventos)

    # --- Métodos Auxiliares Internos ---
    def _validar_superficie(self, superficie: float) -> float:
        if superficie <= 0:
            raise ValueError("La superficie debe ser positiva.")
        # Redondear a dos decimales
        return round(superficie, 2)
    
    def _validar_cultivo(self, cultivo: str) -> str:
        if not cultivo or cultivo.strip() == "":
            raise ValueError("El cultivo actual no puede estar vacío.")
        return cultivo.strip()

    def _registrar_evento(self, tipo: str, detalle: str, silent: bool = False):
        self.__historial_eventos.append(Evento(tipo, detalle))
        if not silent:
            print(f"[{tipo}] -> {detalle}")
            
    # --- Operaciones ---

    def actualizar_cultivo(self, nuevo_cultivo: str):
        # Regla de Negocio: No se permite si estado = inactiva
        if self.__estado == "inactiva":
            print("❌ Error: No se puede actualizar el cultivo. La parcela está inactiva.")
            return

        try:
            nuevo_cultivo_validado = self._validar_cultivo(nuevo_cultivo)
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
            return

        cultivo_previo = self.__cultivo_actual
        self.__cultivo_actual = nuevo_cultivo_validado
        self._registrar_evento("Actualización Cultivo", f"Cambio de '{cultivo_previo}' a '{self.__cultivo_actual}'.")
        print(f"✅ Cultivo actualizado a: {self.__cultivo_actual}")

    def activar(self, motivo: str):
        if self.__estado == "activa":
            print("ℹ️ La parcela ya está activa.")
            return
        
        self.__estado = "activa"
        self._registrar_evento("Activación", f"Parcela activada. Motivo: {motivo}")
        print("✅ Parcela activada.")

    def desactivar(self, motivo: str):
        if self.__estado == "inactiva":
            print("ℹ️ La parcela ya está inactiva.")
            return
        
        self.__estado = "inactiva"
        self._registrar_evento("Desactivación", f"Parcela desactivada. Motivo: {motivo}")
        print("✅ Parcela desactivada.")
        # NOTA: La regla de negocio de inhabilitar riego se implementa en ParcelaConRiego
        
    def rectificar_superficie(self, nueva_superficie: float, motivo: str):
        try:
            superficie_validada = self._validar_superficie(nueva_superficie)
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
            return
            
        superficie_previa = self.__superficie_ha
        self.__superficie_ha = superficie_validada
        
        self._registrar_evento("Rectificación Superficie", 
                               f"De {superficie_previa:.2f} ha a {self.__superficie_ha:.2f} ha. Motivo: {motivo}")
        print(f"✅ Superficie rectificada a {self.__superficie_ha:.2f} ha.")

class ParcelaConRiego(Parcela):
    def __init__(self, id_parcela: str, superficie_ha: float, cultivo_actual: str, tasa_riego_l_ha: float = 1000.0):
        super().__init__(id_parcela, superficie_ha, cultivo_actual)
        
        # Atributos adicionales "privados"
        self.__litros_disponibles = 0.0  # Solo cambia por cargar/regar
        self.__tasa_riego_l_ha = self._validar_tasa(tasa_riego_l_ha)
        self.__umbral_min_litros = 0.0
        # Estado inicial de riego: habilitado si la parcela base está 'activa'
        self.__estado_riego = "habilitado" if self.estado == "activa" else "inhabilitado" 
        self.__eventos_riego: List[EventoRiego] = [] # Solo lectura

        self._registrar_evento("Riego Inicial", "Sistema de riego incorporado.", silent=True)

    # --- Propiedades (Getters) ---
    # Usamos @property para proteger el acceso directo a los datos internos
    
    @property
    def litros_disponibles(self):
        # Regla: no editable directamente, solo se accede por getter
        return self.__litros_disponibles
    
    @property
    def eventos_riego(self) -> List[EventoRiego]:
        # Retorna una copia para mantenerlo 'solo lectura'
        return list(self.__eventos_riego)

    # --- Sobreescritura de Métodos de la Clase Base ---

    def desactivar(self, motivo: str):
        # 1. Ejecutar la lógica de la clase base (Parcela)
        super().desactivar(motivo)
        
        # 2. Regla de Negocio: Si la parcela pasa a inactiva, el riego queda inhabilitado.
        self._inhabilitar_riego_interno("Desactivación de la parcela principal.")
        
    # --- Métodos Auxiliares Internos ---

    def _validar_tasa(self, tasa: float) -> float:
        if tasa <= 0:
            raise ValueError("La tasa de riego debe ser mayor a 0.")
        return tasa
        
    def _inhabilitar_riego_interno(self, motivo: str):
        if self.__estado_riego == "inhabilitado":
            return
        self.__estado_riego = "inhabilitado"
        self._registrar_evento("Riego ON/OFF", f"Riego inhabilitado. Motivo: {motivo}")
        print("✅ Riego inhabilitado.")
        
    def _registrar_evento_riego(self, tipo: str, detalle: str, saldo_antes: float, saldo_despues: float,
                                litros_solicitados: float, litros_aplicados: float, modo: str):
        evento = EventoRiego(tipo, detalle, saldo_antes, saldo_despues, 
                             litros_solicitados, litros_aplicados, modo)
        self.__eventos_riego.append(evento)
        # También se registra en el historial general de la Parcela (heredado)
        self._registrar_evento(f"Riego/{tipo}", detalle, silent=True) 

    # --- Operaciones de Riego ---

    def configurar_tasa(self, l_ha: float):
        try:
            nueva_tasa = self._validar_tasa(l_ha)
            self.__tasa_riego_l_ha = nueva_tasa
            self._registrar_evento("Configuración Riego", f"Tasa establecida a {l_ha:.2f} L/ha.")
            print(f"✅ Tasa de riego configurada a {l_ha:.2f} L/ha.")
        except ValueError as e:
            print(f"❌ Error de configuración: {e}")

    def configurar_umbral(self, litros: float):
        if litros < 0:
            print("❌ Error: El umbral mínimo no puede ser negativo.")
            return
        self.__umbral_min_litros = litros
        self._registrar_evento("Configuración Riego", f"Umbral mínimo establecido a {litros:.2f} L.")
        print(f"✅ Umbral mínimo configurado a {litros:.2f} L.")

    def habilitar_riego(self):
        if self.estado == "inactiva":
            print("❌ Error: El riego no se puede habilitar si la parcela está inactiva.")
            return
        if self.__estado_riego == "habilitado":
            print("ℹ️ El riego ya está habilitado.")
            return
            
        self.__estado_riego = "habilitado"
        self._registrar_evento("Riego ON/OFF", "Riego habilitado manualmente.")
        print("✅ Riego habilitado.")

    def inhabilitar_riego(self):
        self._inhabilitar_riego_interno("Inhabilitación manual.")
        
    def cargar_agua(self, litros: float):
        if litros <= 0:
            print("❌ Error: La carga de agua debe ser positiva.")
            return

        saldo_antes = self.__litros_disponibles
        self.__litros_disponibles += litros
        
        self._registrar_evento_riego("Carga", "Recarga de depósito", 
                                     saldo_antes, self.__litros_disponibles, 
                                     0.0, litros, "Carga")
        print(f"✅ Agua cargada: +{litros:.2f} L. Saldo actual: {self.__litros_disponibles:.2f} L.")

    def regar_automatico(self, modo: str):
        # --- Reglas de Negocio - Prohibido regar si: ---
        if self.estado == "inactiva":
            self._registrar_evento("Riego Rechazado", "Parcela inactiva.", silent=True)
            print("❌ RECHAZADO: La parcela está inactiva.")
            return
        if self.__estado_riego == "inhabilitado":
            self._registrar_evento("Riego Rechazado", "Sistema de riego inhabilitado.", silent=True)
            print("❌ RECHAZADO: El sistema de riego está inhabilitado.")
            return
        if self.__tasa_riego_l_ha <= 0:
            self._registrar_evento("Riego Rechazado", "Tasa de riego <= 0.", silent=True)
            print("❌ RECHAZADO: Tasa de riego no configurada (o <= 0).")
            return

        modo = modo.lower()
        demanda = self.superficie_ha * self.__tasa_riego_l_ha
        saldo_antes = self.__litros_disponibles
        litros_a_aplicar = 0.0
        detalle = ""

        if modo == "estricto":
            # Demanda: 15750 L
            # Saldo: 20000 L
            # Umbral: 2000 L
            saldo_final_previsto = saldo_antes - demanda
            
            if saldo_final_previsto >= self.__umbral_min_litros:
                litros_a_aplicar = demanda
                detalle = "Riego ESTRICTO: Demanda cubierta."
            else:
                detalle = f"Riego ESTRICTO RECHAZADO. Saldo final ({saldo_final_previsto:.2f} L) < Umbral ({self.__umbral_min_litros:.2f} L)."
                self._registrar_evento("Riego Rechazado", detalle)
                print(f"❌ RECHAZADO (ESTRICTO): {detalle}")
                return

        elif modo == "parcial":
            # Regla: Aplicar la mayor cantidad posible manteniendo saldo_final >= umbral_min_litros
            max_aplicable = saldo_antes - self.__umbral_min_litros
            
            if max_aplicable <= 0:
                detalle = f"Riego PARCIAL RECHAZADO. Saldo disponible ({saldo_antes:.2f} L) es insuficiente para mantener el umbral ({self.__umbral_min_litros:.2f} L)."
                self._registrar_evento("Riego Rechazado", detalle)
                print(f"❌ RECHAZADO (PARCIAL): {detalle}")
                return
                
            litros_a_aplicar = min(demanda, max_aplicable)
            
            if litros_a_aplicar < demanda:
                detalle = (f"Riego PARCIAL. Solo se aplicaron {litros_a_aplicar:.2f} L de una demanda de {demanda:.2f} L "
                           f"(Máx. aplicable: {max_aplicable:.2f} L para mantener umbral de {self.__umbral_min_litros:.2f} L).")
            else:
                detalle = "Riego PARCIAL. Demanda cubierta (saldo final >= umbral)."

        else:
            print("❌ Error: Modo de riego no válido. Use 'estricto' o 'parcial'.")
            return

        # Aplicar el riego (solo si litros_a_aplicar > 0)
        if litros_a_aplicar > 0:
            self.__litros_disponibles -= litros_a_aplicar
            saldo_despues = self.__litros_disponibles
            
            # Asegurar la regla: Saldo nunca puede quedar negativo
            if saldo_despues < 0: 
                # Esto no debería ocurrir con la lógica parcial/estricta, pero es una salvaguarda.
                self.__litros_disponibles = 0.0
                saldo_despues = 0.0
                
            self._registrar_evento_riego("Riego OK", detalle, saldo_antes, saldo_despues,
                                         demanda, litros_a_aplicar, modo)
            print(f"💧 RIEGO EXITOSO ({modo.upper()}): Aplicados {litros_a_aplicar:.2f} L. Saldo restante: {saldo_despues:.2f} L.")
        else:
            print("ℹ️ Riego no aplicado (0 L). Se cumplen las condiciones, pero la cantidad a aplicar es cero.")

    