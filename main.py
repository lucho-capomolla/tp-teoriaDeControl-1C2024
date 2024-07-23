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
        print("5. Máximo (entre 1200 y 1500 Luxes)")
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
  valor_nominal = 200
  umbral_minimo = 100

# Nivel de intensidad lumínica Media
elif (nivel_intensidad == 2):
  umbral_maximo = 600
  valor_nominal = 450
  umbral_minimo = 300

# Nivel de intensidad lumínica Alta
elif (nivel_intensidad == 3):
  umbral_maximo = 900
  valor_nominal = 750
  umbral_minimo = 600

# Nivel de intensidad lumínica Muy Alta
elif (nivel_intensidad == 4):
  umbral_maximo = 1200
  valor_nominal = 1050
  umbral_minimo = 900

# Nivel de intensidad lumínica Máximo
elif (nivel_intensidad == 5):
  umbral_maximo = 1500
  valor_nominal = 1350
  umbral_minimo = 1200

print(f"Nivel de intensidad lumínica elegido:  {nivel_intensidad}")
print(f"Valor nominal: {valor_nominal}")
print(f"Umbral máximo: {umbral_maximo}")
print(f"Umbral mínimo: {umbral_minimo}")
print("#################################################\n\n")

# Parámetros del sistema
iluminación_inicial = 500
tiempo_total = 300
time_step = 1


# Coeficientes del Controlador PD
Kp = 1.75
Kd = 0.02


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
lampara_on = False
celular_on = False

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
  global lampara_on
  global celular_on

  if (probabilidad < 0.005):
    print("Perturbación de NUBE")
    perturbacion = -400 # Como el paso de una nube ocultando la luminosidad exterior
  elif (probabilidad < 0.01):
    if not lampara_on:
      print("Perturbación de ENCENDIDO DE LÁMPARA")
      lampara_on = True
      perturbacion = 600  # Como el encendido de una lámpara de forma manual
    else:
      print("Perturbación de APAGADO DE LÁMPARA")
      lampara_on = False
      perturbacion = -600  # Como el apagado de una lámpara de forma manual
  elif (probabilidad < 0.025):
    if not televisor_on:
      print("Perturbación de ENCENDIDO DE TELEVISOR")
      televisor_on = True
      perturbacion = 300  # Como el encendido de un televisor
    else:
      print("Perturbación de APAGADO DE TELEVISOR")
      televisor_on = False
      perturbacion = -300  # Como el apagado de un televisor
  elif (probabilidad < 0.04):
    if not celular_on:
      print("Perturbación de ENCENDIDO DE VELA")
      celular_on = True
      perturbacion = 50
    else:
      print("Perturbación de APAGADO DE VELA")
      celular_on = False
      perturbacion = -50
  return perturbacion



for t in range(1, tiempo_total + 1):

    # Obtener la perturbación
    perturbacion = obtenerPerturbacion()

    # Ocurre una perturbación
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

    # Controlador


    if (iluminacion_actual < umbral_minimo):
      error = umbral_minimo - iluminacion_actual
    elif (iluminacion_actual > umbral_maximo):
      error = umbral_maximo - iluminacion_actual
    else:
      error = 0



    if tiempo_previo is None:
        control_derivativo = 0
    else:
        control_derivativo = (error - error_previo) / time_step

    # Salida del Controlador PD
    senal_control = Kp * error + Kd * control_derivativo

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

# Graficamos los resultados
plt.figure(figsize=(20, 10))

plt.subplot(2, 1, 1)
plt.xticks(range(0, 301, 10))
plt.plot(data['Tiempo (segs)'], data['Nivel de Iluminación (Lux)'], label='Nivel de luminosidad (LUX)')
plt.axhline(valor_nominal, color='b', linestyle='--', label='Valor Nominal')
plt.axhline(umbral_minimo, color='r', linestyle='--', label='Umbral Minimo')
plt.axhline(umbral_maximo, color='r', linestyle='--', label='Umbral Maximo')
plt.xlabel('Tiempo (segs)')
plt.ylabel('Nivel de luminosidad (LUX)')
plt.legend()


plt.tight_layout()
plt.show()


# Análisis de los resultados
print("Tiempo total de la simulación: {} segundos".format(tiempo_total))
print("Itensidad lumínica final de la habitación: {:.2f} Lux".format(niveles_iluminacion[-1]))
print("Umbral mínimo de intensidad lumínica deseada a partir de {} Lux".format(umbral_minimo))
print("Umbral máximo de intensidad lumínica deseada hasta {} Lux".format(umbral_maximo))

print("\nResumen de perturbaciones:")
print(data_perturbacion.to_string())