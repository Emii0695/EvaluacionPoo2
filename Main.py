# Desarrolo 1

from ejercicio1.desarrollo import Evento,EventoRiego,Parcela,ParcelaConRiego

if __name__ == "__main__":
    
    print("  INICIO: GESTIÓN DE PARCELAS CON RIEGO")
    

   
    print("\n--- PRUEBA 1: CREACIÓN Y ACTUALIZACIÓN ---")
    
    
    parcela1 = ParcelaConRiego(id_parcela="P001", superficie_ha=10.50, cultivo_actual="Trigo")
    print(f"ID: {parcela1.id_parcela}, Superficie: {parcela1.superficie_ha:.2f} ha, Cultivo: {parcela1.cultivo_actual}, Estado: {parcela1.estado}")

    
    parcela1.actualizar_cultivo("Maíz")

    
    print("\n--- PRUEBA 2: CONFIGURACIÓN Y CARGA DE AGUA ---")
    parcela1.configurar_tasa(1500.0)
    parcela1.configurar_umbral(2000.0)
    parcela1.cargar_agua(20000.0) 

   
    demanda_estricta = 10.50 * 1500.0 

    
    print("\n--- PRUEBA 3: RIEGO ESTRICTO ---")
    
    parcela1.regar_automatico("estricto")
    

    
    print("\n--- PRUEBA 4: DESACTIVACIÓN Y RECHAZO ---")
    parcela1.desactivar("Rotación de cultivos.") 
    parcela1.regar_automatico("estricto") 

   
    print("\n--- PRUEBA 5: RIEGO PARCIAL ---")
    parcela1.activar("Continuación de tareas.") 
    parcela1.habilitar_riego() 
    
    
    print("--- Simulando escenario para riego parcial: ---")
    parcela1.cargar_agua(1000.0) 
    
    
    
    parcela1.regar_automatico("parcial")
    
    
    
    print("\n--- PRUEBA 6: ENCAPSULAMIENTO ---")
    try:
        parcela1.__litros_disponibles = 99999.0 
        print(f"Valor después de intento de cambio directo: {parcela1.litros_disponibles:.2f} L (No cambia).")
    except AttributeError:
        print(" Intento de acceso directo falló (por convención de encapsulamiento).")
    
    print("\n--- Historial Completo de Eventos ---")
    for evento in parcela1.historial_eventos:
        print(evento)
    
    print("\n--- Historial de Eventos de Riego ---")
    for evento in parcela1.eventos_riego:
        print(evento)

    
    print("  FIN DE PRUEBAS")
   

#------------------------------------------------------------------------------------------------------------------

from ejercicio2.desarrollo2 import Publicacion,Libro,Evento,EventoLectura

if __name__ == "__main__":
    
    print("  INICIO: EJERCICIO CLUB DE LECTURA (PYTHON)")
   

    
    print("\n--- PRUEBA 1: Publicación y Validación de Año ---")
    
    
    try:
        pub1 = Publicacion(id_publicacion="P001", titulo="Don Quijote de la Mancha", anio=1605)
        print(f" Publicación creada: {pub1.titulo} ({pub1.anio})")
    except ValueError as e:
        print(f" Fallo al crear publicación: {e}")

    
    try:
        Publicacion(id_publicacion="P002", titulo="Libro antiguo", anio=1400)
    except ValueError as e:
        print(f" Rechazo esperado (Año < 1450): {e}")


   
    print("\n--- PRUEBA 2: Libro y Control de Progreso ---")
    
    
    try:
        libro1 = Libro(id_publicacion="L001", titulo="Cien años de soledad", anio=1967, paginas_totales=500)
        print(f" Libro creado: {libro1.titulo} ({libro1.paginas_totales} págs.)")
    except ValueError as e:
        print(f" Fallo al crear libro: {e}")

    
    libro1.leer(120) 
       
    libro1.leer(400) 

    
    progreso_final = libro1.consultar_progreso()
    print(f" Progreso final reportado: {progreso_final:.2f}%")
    
    print(f" Páginas leídas finalmente: {libro1.paginas_leidas}/{libro1.paginas_totales}")


    
    print("\n--- PRUEBA 3: Actualización de Atributos (Herencia) ---")
    
    libro1.actualizar_anio(1982) 
    
    
    libro1.actualizar_titulo("Cien Años de Soledad (Ed. 2024)")


    
    print("\n--- PRUEBA 4: Encapsulamiento (Imposibilidad de Alteración Directa) ---")
    
    
    try:
        libro1.__paginas_leidas = -10 
        print(f" Intento de alterar páginas leídas por fuera de operación. Valor actual: {libro1.paginas_leidas}")
    except AttributeError:
        
        print(" Intento de alterar __paginas_leidas directamente fue ignorado por el encapsulamiento.")

    
    try:
        libro1.paginas_totales = 600
    except AttributeError:
        print(" Intento de alterar paginas_totales (propiedad de solo lectura) rechazado.")


    
    print("\n--- Historial General de Cambios (historial_eventos) ---")
    for evento in libro1.historial_eventos:
        print(evento)
    
    print("\n--- Historial de Eventos de Lectura (eventos_lectura) ---")
    for evento in libro1.eventos_lectura:
        print(evento)

    
    print("  FIN DE PRUEBAS")
    

#------------------------------------------------------------------------------------------------------------------
#Desarrolo 3
from ejercicio3.desarrollo3 import Actividad,Carrera,Evento,EventoRegistro

if __name__ == "__main__":
    
    print("  INICIO: REGISTRO DE ACTIVIDADES FÍSICAS (PYTHON)")
    

    
    print("\n--- PRUEBA 1: Actividad y Validación de Duración ---")
    
    
    try:
        act1 = Actividad(id_actividad="A001", nombre="Yoga", duracion_min=60)
        print(f" Actividad creada: {act1.nombre} ({act1.duracion_min} min)")
    except ValueError as e:
        print(f" Fallo al crear actividad: {e}")

    
    try:
        Actividad(id_actividad="A002", nombre="Respiración", duracion_min=0)
    except ValueError as e:
        print(f" Rechazo esperado (Duración < 1 min): {e}")

    
    print("\n--- PRUEBA 2: Carrera y Cálculo de Ritmo ---")
    
    
    carrera1 = Carrera(id_actividad="C001", nombre="Maratón de entrenamiento", duracion_min=50, distancia_km=10.0)
    print(f" Carrera creada: {carrera1.nombre} ({carrera1.duracion_min} min, {carrera1.distancia_km:.2f} km)")

    
    ritmo1 = carrera1.calcular_ritmo()
    print(f" Ritmo calculado: {ritmo1} min/km")

    
    print("\n--- PRUEBA 3: Actualizaciones, Rechazos y Historial ---")
    
    
    carrera1.registrar_distancia(-3.0)

    
    carrera1.actualizar_duracion(55)
    
   
    ritmo2 = carrera1.calcular_ritmo()
    print(f" Nuevo ritmo calculado: {ritmo2} min/km")

    
    print("\n--- PRUEBA 4: Encapsulamiento ---")
    
    
    try:
        carrera1.distancia_km = 12.0 
    except AttributeError:
        print(" Intento de alterar distancia_km (propiedad de solo lectura) rechazado.")
        
    try:
        carrera1.__distancia_km = 12.0 
        print(f" Intento de alterar __distancia_km. Valor actual: {carrera1.distancia_km:.2f} km.")
    except AttributeError:
        
        print(" Intento de alterar el atributo 'privado' __distancia_km fue gestionado por el encapsulamiento.")



    print("\n--- Historial General de Cambios (historial_eventos) ---")
    for evento in carrera1.historial_eventos:
        print(evento)
    
    print("\n--- Historial de Eventos de Registro (eventos_registro) ---")
    for evento in carrera1.eventos_registro:
        print(evento)

    
    print("  FIN DE PRUEBAS")
    

#-------------------------------------------------------------------------------------------------------------------
#Desarrolo 4

from ejercicio4.desarrollo4 import Vehiculo,Auto,Evento,EventoOcupacion

if __name__ == "__main__":
    
    print("  INICIO: EJERCICIO PARQUE DE ESTACIONAMIENTO")
    

    
    print("\n--- PRUEBA 1: Vehículo Base y Actualización de Peso ---")
    
    
    vehiculo_base = Vehiculo(id_vehiculo="V001", patente="ABCD12", peso_kg=1450.0)
    print(f" Vehículo creado: {vehiculo_base.patente}, Peso: {vehiculo_base.peso_kg:.2f} kg, Estado: {vehiculo_base.estado}")

    
    vehiculo_base.actualizar_peso(1500.0, usuario="Mecánico")
    
    
    vehiculo_base.actualizar_peso(0.0)

    
    print("\n--- PRUEBA 2: Control de Estado ---")
    
    
    vehiculo_base.inhabilitar("Mantenimiento programado.")
    
    
    vehiculo_base.actualizar_peso(1600.0, usuario="Mecánico") 
    
    
    vehiculo_base.habilitar("Mantenimiento finalizado.")

    
    print("\n--- PRUEBA 3: Creación de Auto ---")
    

    auto1 = Auto(id_vehiculo="A001", patente="XYZ999", peso_kg=1200.0, asientos_totales=5)
    print(f" Auto creado. Asientos totales: {auto1.asientos_totales}. Ocupantes: {auto1.ocupantes_actuales}")
    print(f"Ocupación inicial: {auto1.consultar_ocupacion()}")

    
    print("\n--- PRUEBA 4: Subida y Bajada de Personas ---")

   
    auto1.subir_personas(3, usuario="Pepe")
    
    
    auto1.subir_personas(3) 

    
    auto1.bajar_personas(2, usuario="Pepe")
    
    
    auto1.bajar_personas(5) 

    
    print("\n--- PRUEBA 5: Reconfiguración y Vaciado ---")

   
    auto1.reconfigurar_asientos(2, "Reducción temporal de asientos.", usuario="Taller")
    
    
    auto1.reconfigurar_asientos(0, "Prueba")

    
    auto1.vaciar_auto("Fin de turno.")

    
    print("\n--- PRUEBA 6: Estado (Inhabilitado) ---")
    
    
    auto1.inhabilitar("Fuga de aceite.")
    auto1.subir_personas(1) 

    
    print("\n--- Auditoría: Historial General de Cambios (Vehículo) ---")
    for evento in auto1.historial_eventos:
        print(evento)
    
    print("\n--- Auditoría: Eventos de Ocupación (Auto) ---")
    for evento in auto1.eventos_ocupacion:
        print(evento)


    print("  FIN DE PRUEBAS")
    

#-------------------------------------------------------------------------------------------------------------------
#Desarrolo 5

from ejercicio5.desarrollo5 import CuerpoCeleste, Planeta, Evento

if __name__ == "__main__":
   
    print("  INICIO: EJERCICIO CATÁLOGO DE PLANETAS")
   

    
    print("\n--- PRUEBA 1: Creación de Cuerpos y Planetas ---")
    
    
    estrella_x = CuerpoCeleste(id_celeste="CE01", nombre="Estrella X", masa_kg=2e30)
    print(f" Cuerpo creado: {estrella_x.nombre}, Masa: {estrella_x.masa_kg:.2e} kg.")
    
    
    tierra = Planeta(
        id_celeste="PL01", 
        nombre="Tierra", 
        masa_kg=5.97e24, 
        radio_km=6371, 
        distancia_sol_km=149600000
    )
    print(f" Planeta creado: {tierra.nombre}, Distancia Sol: {tierra.distancia_sol_km:.2e} km.")

    
    marte = Planeta(
        id_celeste="PL02", 
        nombre="Marte", 
        masa_kg=6.42e23, 
        radio_km=3389, 
        distancia_sol_km=227900000
    )
    print(f" Planeta creado: {marte.nombre}, Distancia Sol: {marte.distancia_sol_km:.2e} km.")


   
    print("\n--- PRUEBA 2: Cálculo de Densidad ---")
    
    
    densidad_tierra = tierra.calcular_densidad()
    print(f"🔍 Densidad de la Tierra: {densidad_tierra} kg/km³ (Esperado: ~5.51e14 kg/km³)")
    

    
    print("\n--- PRUEBA 3: Comparación de Distancia ---")
    
    
    comparacion = tierra.comparar_distancia(marte)
    print(comparacion)


    
    print("\n--- PRUEBA 4: Rechazo de Creación con Parámetros Inválidos ---")
    
    
    try:
        Planeta(id_celeste="PL_FAIL", nombre="Fallo", masa_kg=1e20, radio_km=0, distancia_sol_km=100)
    except ValueError as e:
        print(f" Rechazo esperado (Radio 0): {e}")

    try:
        tierra.actualizar_distancia_sol(-100)
    except ValueError as e:
        print(f" Rechazo esperado (Distancia negativa): {e}")


    
    print("\n--- PRUEBA 5: Actualización de Masa ---")
    
    
    marte.actualizar_masa(6.43e23) 

    
    print("\n--- PRUEBA 6: Intentar Modificar Directamente ---")
    
    
    try:
        tierra.__radio_km = 999999 
        print(f" Intento de alterar el atributo '__radio_km'. Valor actual: {tierra.radio_km:.2f}")
    except AttributeError:
        print(" Intento de modificar '__radio_km' directamente fue gestionado por el encapsulamiento.")

    
    print("\n--- Historial de Eventos de Marte ---")
    for evento in marte.historial_eventos:
        print(evento)

    print("\n===================================================")
    print("  FIN DE PRUEBAS")
    print("===================================================")