import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt

# Elección del nivel de intensidad lumínica deseado
while True:
    try:
        print("--- Ingrese el nivel de intensidad lumínica deseado ---")
        print("1. Baja (entre 100 y 300 Luxes)")
        print("2. Media (entre 300 y 600 Luxes)")
        print("3. Alta (entre 600 y 900 Luxes)")
        print("4. Muy alta (entre 900 y 1200 Luxes)")
        print("4. Máximo (entre 1200 y 1500 Luxes)")
        nivel_intensidad = int(input("Nivel de intensidad lumínica deseado: "))
        while (nivel_intensidad < 1 or nivel_intensidad > 5):
          nivel_intensidad = int(input("Ingrese nuevamente el nivel de intensidad lumínica deseado: "))
        break
    except ValueError:
        print("\nError: Solo se permiten numeros enteros entre 1 y 5.\n")
        continue

# Nivel de intensidad lumínica Baja
if(nivel_intensidad == 1):
  umbral_maximo = 300
  umbral_minimo = 100

# Nivel de intensidad lumínica Media
elif (nivel_intensidad == 2):
  umbral_maximo = 600
  umbral_minimo = 300

# Nivel de intensidad lumínica Alta
elif (nivel_intensidad == 3):
  umbral_maximo = 900
  umbral_minimo = 600

# Nivel de intensidad lumínica Muy Alta
elif (nivel_intensidad == 4):
  umbral_maximo = 1200
  umbral_minimo = 900

# Nivel de intensidad lumínica Máximo
elif (nivel_intensidad == 5):
  umbral_maximo = 1500
  umbral_minimo = 1200

print(f"Nivel de intensidad lumínica elegido:  {nivel_intensidad}")
print(f"Umbral máximo: {umbral_maximo}")
print(f"Umbral mínimo: {umbral_minimo}")
print("#################################################\n\n")

# Parámetros del sistema
iluminación_inicial = 500
tiempo_total = 300
time_step = 1


# Coeficientes del Controlador PD
Kp = 1.75
Kd = 0.05

# Inicialización de variables
iluminacion_actual = iluminación_inicial
error = 0
error_previo = 0
perturbacion = 0
senal_control = 0
tiempo_previo = None
niveles_iluminacion = [iluminacion_actual]
tiempos = [0]
televisor_on = False

# Tablero de Perturbaciones
niveles_iluminacion_perturbacion_antes = []
niveles_iluminacion_perturbacion_despues = []
niveles_iluminacion_perturbacion_corregida = []
tiempos_perturbacion = []

# Perturbaciones
def obtenerPerturbacion():
  probabilidad = random.random()
  perturbacion = 0
  global televisor_on

  if (probabilidad < 0.01):
    print("Perturbación de NUBE")
    perturbacion = -400 # Como el paso de una nube ocultando la luminosidad exterior
  elif (probabilidad < 0.02):
    print("Perturbación de ENCENDIDO DE LÁMPARA")
    perturbacion = 600  # Como el encendido de una lámpara de forma manual
  elif (probabilidad < 0.05):
    if not televisor_on:
      print("Perturbación de TELEVISOR ENCENDIDO")
      televisor_on = True
      perturbacion = 300  # Como el encendido de un televisor
    else:
      print("Perturbación de TELEVISOR APAGADO")
      televisor_on = False
      perturbacion = -300  # Como el encendido de un televisor
  return perturbacion



for t in range(1, tiempo_total + 1):

    # Obtener la perturbación
    perturbacion = obtenerPerturbacion()

    if (perturbacion != 0):
      print(f"Perturbacion en: {t} segundo")

      print(f"Intensidad lumínica antes: {iluminacion_actual}")
      niveles_iluminacion_perturbacion_antes.append(iluminacion_actual)
      # Aplicar la perturbación
      iluminacion_actual += perturbacion

      # Esto es por si la intensidad lumínica es menor a 0
      iluminacion_actual = max(iluminacion_actual, 0)

      print(f"Intensidad lumínica después: {iluminacion_actual}")
      niveles_iluminacion.append(iluminacion_actual)
      niveles_iluminacion_perturbacion_despues.append(iluminacion_actual)
      tiempos.append(t)
      tiempos_perturbacion.append(t)


    if (iluminacion_actual < umbral_minimo):
      error = umbral_minimo - iluminacion_actual
    elif (iluminacion_actual > umbral_maximo):
      error = umbral_maximo - iluminacion_actual
    else:
      error = 0

    if tiempo_previo is None:
        control_derivativo = 0
    else:
        #dt = t - tiempo_previo
        control_derivativo = (error - error_previo) / time_step

    # Salida del Controlador PD
    senal_control = Kp * error + Kd * control_derivativo

    # Limitar la cantidad máxima de enfriamiento
    #senal_control = min(senal_control, 1500)

    iluminacion_actual += senal_control * time_step
    iluminacion_actual = max(iluminacion_actual, 0)

    if (perturbacion != 0):
      print(f"Intensidad lumínica corregida: {iluminacion_actual}\n\n")
      niveles_iluminacion_perturbacion_corregida.append(iluminacion_actual)

    niveles_iluminacion.append(iluminacion_actual)
    tiempos.append(t)

    error_previo = error
    tiempo_previo = t


# Creación Dataframe
data = pd.DataFrame({
    'Tiempo (segs)': tiempos,
    'Nivel de Iluminación (Lux)': niveles_iluminacion,
})


# Creación Tablero de Perturbaciones
data_perturbacion = pd.DataFrame({
    'Tiempo (seg)': tiempos_perturbacion,
    'Nivel de Iluminación Antes (Lux)': niveles_iluminacion_perturbacion_antes,
    'Nivel de Iluminación Despues (Lux)': niveles_iluminacion_perturbacion_despues,
    'Nivel de Iluminación Corregida (Lux)': niveles_iluminacion_perturbacion_corregida,
})

# Análisis de los resultados
print("Tiempo total de la simulación: {} segundos".format(tiempo_total))
print("Itensidad lumínica final de la habitación: {:.2f} Lux".format(niveles_iluminacion[-1]))
print("Umbral mínimo de intensidad lumínica deseada a partir de {} Lux".format(umbral_minimo))
print("Umbral máximo de intensidad lumínica deseada hasta {} Lux".format(umbral_maximo))

print("\nResumen de perturbaciones:")
print(data_perturbacion.to_string())


# Graficando los resultados
plt.figure(figsize=(20, 10))

plt.subplot(2, 1, 1)
plt.plot(data['Tiempo (segs)'], data['Nivel de Iluminación (Lux)'], label='Nivel de luminosidad (LUX)')
plt.axhline(umbral_minimo, color='r', linestyle='--', label='Umbral Minimo')
plt.axhline(umbral_maximo, color='r', linestyle='--', label='Umbral Maximo')
plt.xlabel('Tiempo (segs)')
plt.ylabel('Nivel de luminosidad (LUX)')
plt.legend()


plt.tight_layout()
plt.show()