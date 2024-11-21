document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('camera');
    const toggleButton = document.getElementById('toggleCamera');
    const cameraMessage = document.getElementById('cameraMessage');
    const startGameButton = document.getElementById('startGame');
    const countdownElement = document.getElementById('countdown');
    const resultElement = document.getElementById('resultText');
    const scoreUserElement = document.getElementById('scoreUser');
    const scoreAIElement = document.getElementById('scoreAI');
    const gestureUserElement = document.getElementById('gesture_user');
    const gameIdElement = document.getElementById('game_id');
    const playCounterElement = document.getElementById('play_counter');
    const reportErrorButton = document.getElementById('reportErrorButton');
    const errorPopup = document.getElementById('errorPopup');
    const submitErrorButton = document.getElementById("submitError");
    const cancelErrorButton = document.getElementById("cancelError");
    const imagenIAElement = document.getElementById('imagenIA');
    const correctMoveInput = document.getElementById("correctMove");
    const popup = document.getElementById("popup");
    const popupOverlay = document.getElementById("popup-overlay");
    const popupMessage = document.getElementById("popup-message");


    // Verifica que los elementos necesarios existan en el DOM antes de continuar
    if (!video || !toggleButton || !cameraMessage || !startGameButton || !countdownElement || 
        !resultElement || !scoreUserElement || !gameIdElement || !playCounterElement || !scoreAIElement || !gestureUserElement || !reportErrorButton || !errorPopup || !submitErrorButton || !cancelErrorButton || 
        !imagenIAElement || !correctMoveInput) {
        console.error("Uno o más elementos no se encontraron en el DOM. Verifica los IDs en el HTML.");
        return;
    }

    let isCameraOn = false;
    let gestureRead = '';

    // Encender o apagar la cámara
    toggleButton.addEventListener('click', function() {
        if (!isCameraOn) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function(stream) {
                    video.srcObject = stream;
                    video.classList.remove('off');
                    cameraMessage.classList.add('hidden');
                    isCameraOn = true;
                    startGameButton.style.display = 'block';  // Mostrar botón de Jugar
                    toggleButton.textContent = 'Apagar Cámara';
                })
                .catch(function(err) {
                    console.log("Error al acceder a la cámara: " + err);
                });
        } else {
            let stream = video.srcObject;
            let tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            video.classList.add('off');
            cameraMessage.classList.remove('hidden');
            isCameraOn = false;
            startGameButton.style.display = 'none';  // Ocultar botón de Jugar
            toggleButton.textContent = 'Encender cámara';
            console.log("Camara apagada")
        }
    });

    // Iniciar el juego con cuenta atrás
    startGameButton.addEventListener('click', function() {
        countdownElement.style.display = 'block';
        let countdown = 3;

        let countdownInterval = setInterval(function() {
            countdownElement.innerHTML = countdown;
            countdown--;
            if (countdown < 0) {
                clearInterval(countdownInterval);
                countdownElement.style.display = 'none';
                ImagenCapture();  // Capturamos la imagen cuando la cuenta llega a 0
            }
        }, 1000);
        console.log("Cuenta atrás")
    });

    // Función para obtener el token CSRF
    function getCSRFToken() {
        let csrfToken = null;
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            if (cookie.trim().startsWith('csrftoken=')) {
                csrfToken = cookie.trim().substring('csrftoken='.length);
            }
        });
        return csrfToken;
    }

    // Función para capturar la imagen de la cámara
    function ImagenCapture() {
        if (!video) {
            console.error('El elemento con ID "camera" no existe en el DOM');
            return;
        }

        let canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        let context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        let imageData = canvas.toDataURL('image/png');
        let csrfToken = getCSRFToken();

        fetch('/play/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ image: imageData})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.reset_scores) {
                scoreUserElement.innerHTML = data.scoreUser;
                scoreAIElement.innerHTML = data.scoreAI;
                gameIdElement.innerHTML = data.game_id;
                playCounterElement.innerHTML = data.play_counter;
                showPopup(`Partida finalizada. Ganador: ${data.winner}`);
            } else {
                resultElement.innerHTML =  data.result;
                scoreUserElement.innerHTML = data.scoreUser;
                scoreAIElement.innerHTML = data.scoreAI;
                gestureUserElement.innerHTML = data.gesture_user;
                gameIdElement.innerHTML = data.game_id;
                playCounterElement.innerHTML = data.play_counter;

                imagenChangeAI(data);
                console.log("Gesto del usuario:", data.gesture_user);
                console.log("Datos: ", data)

            }
        })
        .catch(error => console.log('Error:', error));
    }

    // Mostrar popup de error
    reportErrorButton.addEventListener('click', function() {
        errorPopup.style.display = 'block';
    });

    submitErrorButton.addEventListener("click", function() {
        const correctMove = correctMoveInput.value;
        fetch('/correctTheMove/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ correct_Move: correctMove })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Jugada corregida exitosamente");
                scoreUserElement.innerHTML = data.scoreUser;
                scoreAIElement.innerHTML = data.scoreAI;
                errorPopup.style.display = "none";
                
            } else {
                console.log("Hubo un error al corregir la jugada");
            }
        })
        .catch(error => console.error('Error:', error));
    });

    cancelErrorButton.addEventListener("click", function() {
        errorPopup.style.display = "none";
    });

    // Procesar respuesta de IA
    function imagenChangeAI(response) {
        const gestureAi = response.gesture_ai;
        let imagenIA = '';

        if (gestureAi === 'Rock') {
            imagenIA = 'rock.png';
        } else if (gestureAi === 'Paper') {
            imagenIA = 'paper.png';
        } else if (gestureAi === 'Scissors') {
            imagenIA = 'scissors.png';
        }

        imagenIAElement.src = `static/imagen/${imagenIA}`;
    }

    // Función para mostrar el popup con el mensaje
    function showPopup(message) {
        const popup = document.getElementById("popup");
        const textoPopup = document.getElementById("popupText"); // Corregido el id

        textoPopup.textContent = message;
        popup.style.display = "flex"; // Mostrar el popup

        // Cerrar el popup al hacer clic en la "X"
        const closePopup = document.getElementById("closePopup");
        closePopup.onclick = function() {
            popup.style.display = "none"; // Ocultar el popup
        }

        // Cerrar el popup si se hace clic fuera de la caja del contenido
        window.onclick = function(event) {
            if (event.target === popup) {
                popup.style.display = "none"; // Ocultar el popup
            }
        }
    }

    // Función para manejar la respuesta del backend
    function handleGameResponse(response) {
        // Verifica si hay un ganador
        if (response.winner) {
            // Mostrar el popup con el mensaje de ganador
            const message = response.winner + " ha ganado la partida!";
            showPopup(message);
        } else {
            // Continuar con el juego normalmente si no hay ganador
            console.log("La partida continúa...");
        }
    }
});
