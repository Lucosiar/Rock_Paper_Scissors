from django.shortcuts import render
import base64
from django.http import JsonResponse
from PIL import Image
from io import BytesIO
import numpy as np
import pandas as pd
import random
from django.views.decorators.csrf import csrf_exempt
import io
import json
import csv
import os
import json
import joblib
from .predictionMethods import retrain_model, predict_next_play
from tensorflow.keras.models import load_model


CSV_FILE_PATH = 'gameFunctions/model/gamePlays.csv' 

# Cargar el modelo entrenado de lectura de gesto y predicción de play
model = load_model('gameFunctions/model/modelo.h5')

# Iniciar contador de jugadas
play_counter = 1

# Iniciar puntuaciones
scoreUser = 0
scoreAI = 0
game_id = 1
winner = None

# Mapeo
GESTURE_MAPPING = {
    'Rock': 1,
    'Paper': 2,
    'Scissors': 3
}

def home(request):
    #crear_modelo_knn()
    return render(request, 'home.html')

# Función para leer el último id de partida
def get_last_partida_id():
    if not os.path.exists(CSV_FILE_PATH):
        return 0
    
    with open(CSV_FILE_PATH, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        
        # Comprobar si hay filas en el CSV
        if rows and 'game_id' in rows[0]:
            return int(rows[-1]['game_id'])
        else:
            return 0  # Si no hay filas o 'game_id' no está presente, retornamos 0

# Función para escribir los datos en el CSV
def write_csv(game_id, play, gesture_user, gesture_ai, scoreUser, scoreAI, right, wrong, next_play):
    with open(CSV_FILE_PATH, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([game_id, play, gesture_user, gesture_ai, scoreUser, scoreAI, right, wrong, next_play])

# Función para obtener la última puntuación de una partida
def get_last_scores(game_id):
    try:
        with open(CSV_FILE_PATH, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            last_scores = None
            
            for row in reader:
                # Asegúrate de que game_id es un entero al compararlo
                if int(row['game_id']) == game_id:
                    last_scores = row
            
            # Si se encontró una última puntuación, devuelve las puntuaciones; de lo contrario, devuelve (0, 0)
            if last_scores:
                return (int(last_scores['scoreUser']), int(last_scores['scoreAI']))
            else:
                print("No se encontraron puntuaciones para este game_id.")
                return (0, 0)

    except FileNotFoundError:
        print("El archivo 'jugadas.csv' no se encontró.")
        return (0, 0)
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return (0, 0)

# Controlador principal de la play
def play(request):
    global play_counter, scoreUser, scoreAI, game_id, winner

    if request.method == 'POST':
        data = json.loads(request.body)
        image_data = data['image']

        # Procesar la imagen usando una función
        image_array = processImage(image_data)

        # Realizar la predicción con el modelo
        prediction = model.predict(image_array)
        result = np.argmax(prediction, axis=1)

        # Mapping de result
        classes = ['Paper', 'Rock', 'Scissors']
        gesture_user = classes[result[0]]

        next_play = get_Last_Prediction()

        gesture_ai = ia_winner(next_play)

        print("Gesto Usuario: ", gesture_user, "/ Gesto IA: ", gesture_ai)

        if play_counter == 1:
            scoreUser = 0
            scoreAI = 0
        else:
            scoreUser, scoreAI = get_last_scores(game_id)  # Obtener puntuaciones del último registro
            print("Puntuaciones de la partida anterior: ", scoreUser, scoreAI)

        # Cálculo del winner 
        result = calculate_result(gesture_user, gesture_ai)
        print("Resultado del jugado: ", result)

        update_scores(result)

        # Determinar la próxima play
        next_play = predict_next_play()

        # Guardar en el CSV
        write_csv(game_id, play_counter, GESTURE_MAPPING[gesture_user], GESTURE_MAPPING[gesture_ai], scoreUser, scoreAI, right=0, wrong=False, next_play = GESTURE_MAPPING[next_play])

        # LLamamos a la función de reentrenamiento del modelo
        retrain_model(CSV_FILE_PATH)

        # Incrementar el contador de jugadas
        play_counter += 1

        # Verificar si la partida termina y obtener los valores actualizados
        game_id, scoreUser, scoreAI, play_counter, winner = verifyFinalization(scoreUser, scoreAI, play_counter, game_id, winner)

        print(f"Valor de prediction: {prediction}, result: {result}, gesture_user: {gesture_user}")
        print("Partida:", game_id)
        print("Jugada ", {play_counter})

        return JsonResponse({'result': result, 'winner': winner,
        'gesture_user': gesture_user, 'gesture_ai': gesture_ai,
        'scoreUser': scoreUser, 'scoreAI': scoreAI, 
        'play_counter': play_counter, 'game_id': game_id})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def update_scores(result):
    global scoreUser, scoreAI
    if result == "Humano":
        scoreUser += 1
    elif result == "IA":
        scoreAI += 1

# Corregir play erronea
def correct_move_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        correctMove = data.get('correctMove')

        # Llama a la función de corrección
        correct_play(correctMove, play_counter)

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)

# Corregir play errónea
def correct_play(correctMove, play):
    # Cargar el CSV
    data = pd.read_csv(CSV_FILE_PATH, delimiter=';')

    # Obtener el índice de la última fila
    last_row_index = data.index[-1]

    # Actualizar el campo 'right' y marcar como 'wrong'
    data.at[last_row_index, 'right'] = int(correctMove)
    data.at[last_row_index, 'wrong'] = True  # Marcar que fue erróneo

    # Restar puntos en caso de ser necesario
    subtract_point(data, last_row_index)

    # Guardar el CSV actualizado
    data.to_csv(CSV_FILE_PATH, index=False, sep=';')

    print("La play ha sido corregida exitosamente.")

# Lógica para calcular el winner (puedes adaptarla a tu necesidad)
def calculate_result(gesture_user, gesture_ai):
    if gesture_user == gesture_ai:
        return "Empate"
    if (gesture_user == 'Paper' and gesture_ai == 'Rock') or \
       (gesture_user == 'Scissors' and gesture_ai == 'Paper') or \
       (gesture_user == 'Rock' and gesture_ai == 'Scissors'):
        return "Humano"
    return "IA"

# Procesamiento de la imagen
def processImage(image_data):
    # Decodificar la imagen de base64
    image_b64 = image_data.split(",")[1]  # Eliminar el prefijo de data URL
    image_bytes = base64.b64decode(image_b64)
    
    # Abrir la imagen con PIL
    image = Image.open(io.BytesIO(image_bytes))

    # Convertir la imagen a RGB y redimensionar
    image = image.convert('RGB')
    image = image.resize((64, 64))  # Cambia el tamaño según sea necesario

    # Convertir la imagen a un array NumPy
    image_array = np.array(image)

    # Normalizar el array de la imagen (opcional, dependiendo de tu modelo)
    image_array = image_array.astype('float32') / 255.0

    # Expandir las dimensiones para que sea compatible con la entrada del modelo
    image_array = np.expand_dims(image_array, axis=0)

    return image_array

def verifyFinalization(scoreUser, scoreAI, play_counter, game_id, winner):

    if scoreUser == 5 or scoreAI == 5: 
        # Determinamos el winner    
        winner = 'Humano' if scoreUser == 5 else 'IA'
        print("Partida finalizada. Winner: ", winner)


        # Reiniciar puntuaciones y contador de jugadas
        scoreUser = 0
        scoreAI = 0
        play_counter = 1 
        game_id += 1

        print("Partida reiniciada: ", game_id)

    return game_id, scoreUser, scoreAI, play_counter, winner

def ia_winner(next_play):
    if next_play == 'Paper':
        return 'Scissors'
    elif next_play == 'Scissors':
        return 'Rock'
    elif next_play == 'Rock':
        return 'Paper'
    
    # Si no se encuentra ninguna de las opciones, devuelve una play aleatoria
    return random.choice(['Paper', 'Rock', 'Scissors'])

def get_Last_Prediction():
    try:
        # Cargar los datos del CSV
        data = pd.read_csv(CSV_FILE_PATH, delimiter=';')

        if data.empty:
            print("No hay registros en el CSV.")
            return None

        # Obtener el último game_id
        last_match_id = data['game_id'].max()

        # Filtrar por el último game_id
        data_game = data[data['game_id'] == last_match_id]

        if data_game.empty:
            print(f"No se encontraron registros para la partida {last_match_id}.")
            return None

        # Obtener la última play de la última partida
        last_play = data_game.iloc[-1]

        # Obtener el valor de la 'next_play' de la última play
        last_next_play = last_play['next_play']

        return last_next_play
    except Exception as e:
        print(f"Ocurrió un error al obtener la última 'next_play': {e}")
        return None

def subtract_point(data, fila_index):
    # Si puntuación no es 0-0, resta un punto al jugador correspondiente
    if data.at[fila_index, 'scoreUser'] > 0:
        data.at[fila_index, 'scoreUser'] -= 1
    elif data.at[fila_index, 'scoreAI'] > 0:
        data.at[fila_index, 'scoreAI'] -= 1


'''
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle

def crear_modelo_knn():
    # Cargar los datos del CSV
    try:
        df = pd.read_csv(CSV_FILE_PATH, sep=';')
    except Exception as e:
        print(f"Error al cargar el CSV: {e}")
        return None

    # Asegurarse de que el CSV contiene datos suficientes
    if df.shape[0] < 10:
        print("No hay suficientes datos para entrenar el modelo.")
        return None

    # Seleccionar solo las 8 características relevantes y la variable objetivo 'next_play'
    X = df[['game_id', 'play', 'gesture_user', 'gesture_ai', 'scoreUser', 'scoreAI', 'right', 'wrong']].values
    y = df['next_play'].values

    # Escalar las características (opcional, pero recomendable)
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Crear el modelo KNN
    knn = KNeighborsClassifier(n_neighbors=5)

    # Entrenar el modelo con los datos de entrenamiento
    knn.fit(X_train, y_train)

    # Guardar el modelo entrenado en un archivo .pkl
    with open(MODELO_KNN_PATH, 'wb') as file:
        pickle.dump(knn, file)

    print(f"Modelo KNN guardado en {MODELO_KNN_PATH}")

    # También puedes retornar el modelo si lo necesitas en la misma sesión
    return knn 
'''
