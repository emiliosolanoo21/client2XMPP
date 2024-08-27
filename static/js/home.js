// static/js/home.js
document.addEventListener('DOMContentLoaded', function() {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    const newChatButton = document.getElementById('new-chat');
    const sendMessageButton = document.getElementById('send-message');
    const messageInput = document.getElementById('message-input');
    const messagesDiv = document.getElementById('messages');

    newChatButton.addEventListener('click', function() {
        const username = prompt('Enter the username for the new chat:');
        if (username) {
            socket.emit('new_chat', { username: username });
        }
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

    socket.on('chat_list', function(data) {
        const contactsList = document.getElementById('contacts-list');
        contactsList.innerHTML = '';
        data.chats.forEach(function(chat) {
            const contactElement = document.createElement('li');
            contactElement.className = 'list-group-item';
            contactElement.textContent = chat.username;
            contactsList.appendChild(contactElement);
        });
    });
});
