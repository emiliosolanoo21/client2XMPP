document.addEventListener('DOMContentLoaded', function() {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    const newChatButton = document.getElementById('new-chat');
    const sendMessageButton = document.getElementById('send-message');
    const messageInput = document.getElementById('message-input');
    const messagesDiv = document.getElementById('messages');
    const newChatModal = new bootstrap.Modal(document.getElementById('newChatModal'));
    const createChatButton = document.getElementById('create-chat');
    const newChatUsernameInput = document.getElementById('new-chat-username');
    const contactsList = document.getElementById('contacts-list');
    const confirmationMessage = document.getElementById('confirmation-message');
    const chats = {};

    // Cargar roster al cargar la página
    fetch('/roster')
        .then(response => response.json())
        .then(data => {
            contactsList.innerHTML = '';
            for (const jid in data) {
                const contact = data[jid];
                const contactElement = document.createElement('li');
                contactElement.className = 'list-group-item';
                contactElement.textContent = contact.name || jid;  // Muestra el nombre o el JID si no hay nombre
                contactsList.appendChild(contactElement);
            }
        })
        .catch(error => {
            console.error('Error fetching roster:', error);
        });

    newChatButton.addEventListener('click', function() {
        newChatModal.show();
    });

    createChatButton.addEventListener('click', function() {
        const username = newChatUsernameInput.value.trim();
        if (username) {
            socket.emit('new_chat', { username: username });
        }
        newChatModal.hide();
    });

    sendMessageButton.addEventListener('click', function() {
        sendMessage();
    });

    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            socket.emit('send_message', { message: message });
            messageInput.value = '';
        }
    }

    socket.on('receive_message', function(data) {
        const messageElement = document.createElement('div');
        messageElement.textContent = data.message;
        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });

    socket.on('new_chat_started', function(data) {
        console.log("HOOALAL",data)
        const username = data.username;

        // Mostrar mensaje de confirmación
        confirmationMessage.textContent = `Chat iniciado con ${username}`;
        confirmationMessage.style.color = "green";
        confirmationMessage.style.display = "block";

        // Crear un elemento en la barra lateral para el chat
        const chatDiv = document.createElement('div');
        chatDiv.className = 'chat-box';
        chatDiv.textContent = username;
        chatDiv.addEventListener('click', function() {
            openChat(username);
        });

        contactsList.appendChild(chatDiv);

        // Crear la ventana de chat
        chats[username] = document.createElement('div');
        chats[username].className = 'chat-window';
        chats[username].style.display = 'none'; // Ocultar al inicio
        messagesDiv.appendChild(chats[username]);

        openChat(username);
    });

    socket.on('error', function(data) {
        // Mostrar mensaje de error
        confirmationMessage.textContent = data.message;
        confirmationMessage.style.color = "red";
        confirmationMessage.style.display = "block";
    });

    function openChat(username) {
        // Ocultar todas las ventanas de chat
        Object.values(chats).forEach(chat => chat.style.display = 'none');

        // Mostrar la ventana del chat seleccionado
        if (chats[username]) {
            chats[username].style.display = 'block';
        }
    }
});
