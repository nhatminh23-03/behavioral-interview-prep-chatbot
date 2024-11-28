// JavaScript code to handle the chat
document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('sendButton');
    const messageInput = document.getElementById('messageInput');
    const messageContainer = document.getElementById('messageContainer');
    const typingIndicator = document.getElementById('typingIndicator');

    // Function to append a message to the chat
    function appendMessage(message, sender) {
        // Create a new message element
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        // Add the message content and time
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerText = message;

        const messageTime = document.createElement('small');
        messageTime.classList.add('message-time');
        messageTime.innerText = new Date().toLocaleTimeString();

        // Append the message to the message container
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(messageTime);

        messageContainer.appendChild(messageDiv);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    // Event listener for the send button
    sendButton.addEventListener('click', function() {
        // Get the user's message
        const userMessage = messageInput.value.trim();
        if (userMessage === '') return;

        // Append user's message to the chat
        appendMessage(userMessage, 'sent');
        messageInput.value = '';

        // Show typing indicator
        typingIndicator.classList.remove('d-none');

        // Send the message to the server
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Hide typing indicator
            typingIndicator.classList.add('d-none');

            // Append bot's response to the chat
            appendMessage(data.response, 'received');
        })
        .catch(error => {
            console.error('Error:', error);
            typingIndicator.classList.add('d-none');
        });
    });

    // Send message on Enter key press
    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendButton.click();
        }
    });
});
