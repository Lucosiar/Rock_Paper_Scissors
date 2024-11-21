# Rock Paper Scissors Game 🪨🧻✂️
## About the Project
This is an AI-powered Rock Paper Scissors game created with Python and Django. The AI predicts your next move based on previous moves and adjusts its
and adjusts its strategy. The project includes machine learning to improve predictions over time.

## How to Play
1. Turn on the camera and the play button will appear.
2. When you click the play button, a countdown will appear.
3. When the countdown reaches 0, a picture will be taken and the AI will recognize the gesture you are making with your hand.
4. At the same time the picture is taken (it is not stored) the AI will make its move.
5. The first to reach 5 points wins the game.

## Game Rules
- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock
- If both make the same move, a tie occurs.
- If a misreading is reported, the point will be subtracted from whoever beat that move.

## Technologies Used.
- Python: Main language.
- Django: Web framework.
- TensorFlow/Keras: For the AI gesture recognition model.
- Pandas: To manage the game data.
- NumPy: For image preprocessing.
- OpenCV and PIL: For image processing.
- HTML/CSS/JS: Front-end development for the user interface.

## How it was created
A TensorFlow model was trained to recognize hand gestures (Rock, Paper, Scissors).
The AI that recognizes the gestures has an accuracy of 78.23%.
The AI analyzes previous moves using predictive algorithms to anticipate your next move.
Data from each game is recorded in a .csv file and used for continuous training.
The front-end dynamically updates the scores and displays the winner with a pop-up.

## Recommendations for playing the game
It is recommended not to have too much visual noise in the background as it may affect the accuracy of the AI.

## How to Install & Run
1. Clone this repository:

        git clone

2. Navigate to the project directory:

        cd game
3. Create and activate a virtual environment:

        Windows: python -m venv venv
        Mac/Linux: python3 -m venv venv

        Windows: venv\Scripts\activate
        Max/Linux: source venv/bin/activate
   
4. Install dependencies:

        Windows: pip install -r requirements.txt
        Linux/Mac: pip install -r requirements.txt
        
5. Run the Django server:

        python manage.py runserver

Now open http://127.0.0.1:8000 in your browser to play the game. Good luck 🍀🤖

## Contribution guidelines
Feel free to contribute to this project! Create a pull request with your proposed changes or improvements.😊💕


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Piedra Papel Tijera Juego 🪨🧻✂️
## Sobre el Proyecto
Este es un juego de Piedra, Papel o Tijera potenciado por inteligencia artificial, creado con Python y Django. La IA predice tu próximo movimiento basándose en jugadas
anteriores y ajusta su estrategia. El proyecto incluye aprendizaje automático para mejorar las predicciones con el tiempo.

## Cómo Jugar
1. Conecta la camara y aparecera el boton de jugar.
2. Cuando hagas click en el boton de jugar, aparecera una cuenta atrás.
3. Cuando la cuenta llegue a 0, se hara una foto y la IA reconocera el gesto que estas haciendo con la mano
4. Al mismo tiempo que se hace la foto (no se almacena) la IA hará su jugada.
5. El primero en llegar a 5 puntos gana la partida.

## Reglas del Juego
- Piedra vence a Tijera
- Tijera vence a Papel
- Papel vence a Piedra
- Si ambos hacen el mismo movimiento, ocurre un empate.
- En caso de reportar una mala lectura, se le restará el punto a quien haya vencido esa jugada.

## Tecnologías Utilizadas
- Python: Lenguaje principal.
- Django: Framework web.
- TensorFlow/Keras: Para el modelo de reconocimiento de gestos de la IA.
- Pandas: Para manejar los datos del juego.
- NumPy: Para preprocesar imágenes.
- OpenCV y PIL: Para procesar imágenes.
- HTML/CSS/JS: Desarrollo del front-end para la interfaz de usuario.

## Cómo se Creó
Se entrenó un modelo de TensorFlow para reconocer gestos de mano (Piedra, Papel, Tijera).
La IA que reconoce los gestos tiene una precisión del 78.23%.
La IA analiza jugadas anteriores utilizando algoritmos de predicción para anticipar tu próxima jugada.
Los datos de cada partida se registran en un archivo .csv y se usan para entrenamiento continuo.
El front-end actualiza dinámicamente los puntajes y muestra al ganador con un pop-up.

## Recomendaciones para jugar
Se recomienda no tener mucho ruido visual de fondo ya que puede afectar a la precisión de la IA.




## Cómo instalar y ejecutar
1. Clona este repositorio:

        git clone

2. Navega al directorio del proyecto:

        cd juego
3. Crea y activa un entorno virtual:

        Windows: python -m venv venv
        Mac/Linux: python3 -m venv venv

        Windows: venv\Scripts\activate
        Max/Linux: source venv/bin/activate
   
4. Instale las dependencias:

        Windows: pip install -r requirements.txt
        Linux/Mac: pip install -r requirements.txt
        
5. Ejecuta el servidor Django:

        python manage.py runserver

Ahora abre http://127.0.0.1:8000 en tu navegador para jugar al juego. Buena suerte 🍀🤖

## Directrices de contribución
¡Siéntase libre de contribuir a este proyecto! Cree un pull request con los cambios o mejoras que propone.😊💕


















