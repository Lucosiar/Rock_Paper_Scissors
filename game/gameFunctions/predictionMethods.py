# metodos.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib
import random

# Cargar los datos desde el CSV
def load_data():
    # Mapeo de gestos    
    gesture_mapping = {'rock': 1, 'paper': 2, 'scissors': 3}

    # Cargar datos
    try:
        data = pd.read_csv('gameFunctions/model/gamePlays.csv', delimiter=';')
    except FileNotFoundError:
        print("El archivo CSV no existe.")
        return np.array([]), np.array([])

    # Verificar si el DataFrame está vacío
    if data.empty:
        print("El archivo CSV está vacío.")
        return np.array([]), np.array([])

    # Mapeo de gestos
    data['gesture_user'] = data['gesture_user'].map(gesture_mapping)
    data['right'] = data['right'].map(gesture_mapping)

    # Eliminar filas con NaN
    data = data.dropna()

    # Asegúrate de que tienes todas las columnas necesarias
    X = data[['game_id', 'play', 'gesture_user', 'gesture_ai', 'scoreUser', 'scoreAI', 'right', 'wrong']].values
    y = data['next_play'].values 

    return X, y

def retrain_model(csv_file):
    # Cargar datos desde el archivo CSV
    X, y = load_data()

    if len(X) == 0:
        print("No hay datos para reentrenar el modelo.")
        return None

    # Entrenar el modelo nuevamente
    model = train_model(X, y)

    return model

def train_model(X, y):
    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # Asegúrate de que no intentas usar más vecinos de los que tienes en el conjunto de entrenamiento
    n_neighbors = min(3, len(X_train))
        
    if n_neighbors < 1:
        print("No hay suficientes datos para entrenar el modelo.")
        return None

    # Crear el modelo
    model = KNeighborsClassifier(n_neighbors=n_neighbors)

    # Entrenar el modelo
    model.fit(X_train, y_train)

    # Realizar predicciones en el conjunto de prueba
    y_pred = model.predict(X_test)

    # Evaluar el modelo
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Precisión del modelo: {accuracy:.2f}")

    # Guardar el modelo entrenado
    joblib.dump(model, 'juego/modelo/modelo_knn.pkl')
    print("Modelo guardado en 'juego/modelo/modelo_knn.pkl'")

    return model


def predict_next_play():
    try:
        # Cargar los datos desde el CSV
        data = pd.read_csv('gameFunctions/model/gamePlays.csv', delimiter=';')

        # Eliminar filas con NaN
        data = data.dropna()

        # Filtrar las filas donde gesto_usuario y gesto_IA no sean 123
        data = data[(data['gesture_user'] != 123) & (data['gesture_ai'] != 123)]

        # Obtener todas las jugadas previas
        previous_moves = data[['game_id', 'play', 'gesture_user', 'gesture_ai', 'scoreUser', 'scoreAI', 'right', 'wrong']]

        if previous_moves.empty:
            return random.choice(['Paper', 'Rock', 'Scissors'])  # Si no hay jugadas previas, elegir aleatoriamente

        # Convertir todas las características relevantes a un array adecuado
        X = previous_moves.values

        # Cargar el modelo
        model = joblib.load('gameFunctions/model/model_knn.pkl')

        # Verificar si el modelo se entrenó con suficientes datos
        if X.shape[1] != 8:
            print("Los datos no tienen el número correcto de características.")
            return random.choice(['Rock', 'Paper', 'Scissors'])

        # Predecir la próxima jugada basándose en todas las jugadas previas
        next_play_index = model.predict(X[-1].reshape(1, -1))[0]  # Solo predecir usando la última jugada

        # Mapear la predicción a las clases (0 = Rock, 1 = Paper, 2 = Scissors)
        classes = ['Rock', 'Paper', 'Scissors']
        return classes[next_play_index]

    except Exception as e:
        print(f"Ocurrió un error al predecir la próxima jugada: {e}")
        return random.choice(['Rock', 'Paper', 'Scissors'])