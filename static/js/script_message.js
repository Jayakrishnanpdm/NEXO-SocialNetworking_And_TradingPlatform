document.addEventListener('DOMContentLoaded', function () {
    // Theme button & modal
    const themeBtn = document.querySelector('#theme'); 
    const themeModal = document.querySelector('.customize-theme');

    // Font size selection
    const fontSizes = document.querySelectorAll('.choose-size span');
    const root = document.documentElement; 

    // Color selection
    const colorPalette = document.querySelectorAll('.choose-color span');

    // Background selection
    const Bg1 = document.querySelector('.bg-1');
    const Bg2 = document.querySelector('.bg-2');
    const Bg3 = document.querySelector('.bg-3');

    // ========== OPEN & CLOSE THEME MODAL ==========
    const openThemeModal = () => {
        themeModal.style.display = 'grid';
    };

    const closeThemeModal = (e) => {
        if (e.target.classList.contains('customize-theme')) {
            themeModal.style.display = 'none';
        }
    };

    
    // Add event listeners
    themeBtn.addEventListener('click', openThemeModal);
    themeModal.addEventListener('click', closeThemeModal);

    // ========== CHANGE FONT SIZE ==========
    fontSizes.forEach(size => {
        size.addEventListener('click', () => {
            document.querySelector('.choose-size .active')?.classList.remove('active');
            size.classList.add('active');

            let fontSize;
            if (size.classList.contains('font-size-1')) {
                fontSize = '10px';
                root.style.setProperty('--sticky-top-left', '5.4rem');
                root.style.setProperty('--sticky-top-right', '5.4rem');
            } else if (size.classList.contains('font-size-2')) {
                fontSize = '13px';
                root.style.setProperty('--sticky-top-left', '5.4rem');
                root.style.setProperty('--sticky-top-right', '-7rem');
            } else if (size.classList.contains('font-size-3')) {
                fontSize = '15px';
                root.style.setProperty('--sticky-top-left', '-2rem');
                root.style.setProperty('--sticky-top-right', '-17rem');
            } else if (size.classList.contains('font-size-4')) {
                fontSize = '17px';
                root.style.setProperty('--sticky-top-left', '-5rem');
                root.style.setProperty('--sticky-top-right', '-25rem');
            } else if (size.classList.contains('font-size-5')) {
                fontSize = '18px';
                root.style.setProperty('--sticky-top-left', '-10rem');
                root.style.setProperty('--sticky-top-right', '-33rem');
            }

            document.querySelector('html').style.fontSize = fontSize;
        });
    });

    // ========== CHANGE PRIMARY COLOR ==========
    colorPalette.forEach(color => {
        color.addEventListener('click', () => {
            document.querySelector('.choose-color .active')?.classList.remove('active');
            color.classList.add('active');

            let primaryColor;
            if (color.classList.contains('color-1')) {
                primaryColor = "hsl(255,75%,60%)";
            } else if (color.classList.contains('color-2')) {
                primaryColor = "hsl(52,75%,60%)";
            } else if (color.classList.contains('color-3')) {
                primaryColor = "hsl(352,75%,60%)";
            } else if (color.classList.contains('color-4')) {
                primaryColor = "hsl(152,75%,60%)";
            } else if (color.classList.contains('color-5')) {
                primaryColor = "hsl(202,75%,60%)";
            }

            root.style.setProperty('--color-primary', primaryColor);
        });
    });

    // ========== CHANGE BACKGROUND THEME ==========
    let lightColorLightness;
    let darkColorLightness;
    let whiteColorLightness;

    const changeBg = () => {
        root.style.setProperty('--light-color-lightness', lightColorLightness);
        root.style.setProperty('--dark-color-lightness', darkColorLightness);
        root.style.setProperty('--white-color-lightness', whiteColorLightness);
    };

    Bg2.addEventListener('click', () => {
        darkColorLightness = '95%';
        lightColorLightness = '15%';
        whiteColorLightness = '20%';

        Bg2.classList.add('active');
        Bg1.classList.remove('active');
        Bg3.classList.remove('active');
        changeBg();
    });

    Bg3.addEventListener('click', () => {
        darkColorLightness = '95%';
        lightColorLightness = '10%';
        whiteColorLightness = '0%';

        Bg2.classList.remove('active');
        Bg1.classList.remove('active');
        Bg3.classList.add('active');
        changeBg();
    });

    Bg1.addEventListener('click', () => {
        Bg2.classList.remove('active');
        Bg1.classList.add('active');
        Bg3.classList.remove('active');
        window.location.reload(); // Reloads the page to reset to default light mode
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu-item');
    const notifications = document.querySelector('#notifications');
    const notificationPopup = document.querySelector('.notification-popup');

    if (!notifications || !notificationPopup) {
        console.error("Notification elements not found!");
        return;
    }

    // Function to remove active class
    const changeActiveItem = () => {
        menuItems.forEach(item => {
            item.classList.remove('active');
        });
    };

    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            changeActiveItem();
            item.classList.add('active');

            if (item.id !== "notifications") {
                notificationPopup.style.display = 'none';
            } else {
                notificationPopup.style.display = notificationPopup.style.display === 'block' ? 'none' : 'block';
                document.querySelector('#notifications .notification-count').style.display = 'none';
            }
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const messageSearch = document.querySelector("#message-search");
    const messages = document.querySelectorAll(".message");

    // Search Messages
    const searchMessages = () => {
        let val = messageSearch.value.toLowerCase();
        messages.forEach((chat) => {
            let name = chat.querySelector("h5").textContent.toLowerCase();
            chat.style.display = name.includes(val) ? "flex" : "none";
        });
    };

    messageSearch.addEventListener("input", searchMessages);
});


//chat section

document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll(".message");
    const chatPlaceholder = document.getElementById("chatPlaceholder");
    const chatBox = document.getElementById("chatBox");
    const chatUserName = document.getElementById("chatUserName");
    const chatProfilePic = document.getElementById("chatProfilePic");
    const chatMessages = document.getElementById("chatMessages");
    const messageInput = document.getElementById("messageInput");
    const sendMessage = document.getElementById("sendMessage");

    let currentChatUser = "";

    messages.forEach((message) => {
        message.addEventListener("click", function () {
            // Get user details
            currentChatUser = this.querySelector(".message-details h5").innerText;
            const userProfilePic = this.querySelector(".profile-picture img").src;

            // Update chat header
            chatUserName.innerText = currentChatUser;
            chatProfilePic.src = userProfilePic;

            // Clear previous messages (optional)
            chatMessages.innerHTML = "";

            // Show chat box and hide placeholder
            chatPlaceholder.style.display = "none";
            chatBox.style.display = "flex";
        });
    });

    sendMessage.addEventListener("click", function () {
        const messageText = messageInput.value.trim();
        if (messageText === "") return;

        // Create sent message bubble
        const messageBubble = document.createElement("div");
        messageBubble.classList.add("sent-message");
        messageBubble.innerHTML = `<p>${messageText}</p>`;
        chatMessages.appendChild(messageBubble);

        // Auto-scroll to the latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Clear input field
        messageInput.value = "";

        // Simulate a received message after 1.5s (Demo purpose)
        setTimeout(() => {
            receiveMessage("Got it!", currentChatUser);
        }, 1500);
    });

    function receiveMessage(text, sender) {
        const messageBubble = document.createElement("div");
        messageBubble.classList.add("received-message");
        messageBubble.setAttribute("data-sender", sender);
        messageBubble.innerHTML = `<p>${text}</p>`;
        chatMessages.appendChild(messageBubble);

        // Auto-scroll to the latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll(".message");
    const chatPlaceholder = document.getElementById("chatPlaceholder");
    const chatBox = document.getElementById("chatBox");
    const chatUserName = document.getElementById("chatUserName");
    const chatProfilePic = document.getElementById("chatProfilePic");
    const chatMessages = document.getElementById("chatMessages");
    const messageInput = document.getElementById("messageInput");
    const sendMessage = document.getElementById("sendMessage");
    const backButton = document.getElementById("backButton"); // Back button

    const messageList = document.getElementById("messageList"); // Messaging list container

    let currentChatUser = "";

    messages.forEach((message) => {
        message.addEventListener("click", function () {
            // Get user details
            currentChatUser = this.querySelector(".message-details h5").innerText;
            const userProfilePic = this.querySelector(".profile-picture img").src;

            // Update chat header
            chatUserName.innerText = currentChatUser;
            chatProfilePic.src = userProfilePic;

            // Clear previous messages (optional)
            chatMessages.innerHTML = "";

            // Show chat box and hide messaging list
            messageList.style.display = "none";
            chatBox.style.display = "flex";
        });
    });

    // Back button functionality
    backButton.addEventListener("click", function () {
        chatBox.style.display = "none";  // Hide chat box
        messageList.style.display = "block"; // Show messaging list
    });

    sendMessage.addEventListener("click", function () {
        const messageText = messageInput.value.trim();
        if (messageText === "") return;

        // Create sent message bubble
        const messageBubble = document.createElement("div");
        messageBubble.classList.add("sent-message");
        messageBubble.innerHTML = `<p>${messageText}</p>`;
        chatMessages.appendChild(messageBubble);

        // Auto-scroll to the latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Clear input field
        messageInput.value = "";

        // Simulate a received message after 1.5s (Demo purpose)
        setTimeout(() => {
            receiveMessage("Got it!", currentChatUser);
        }, 1500);
    });

    function receiveMessage(text, sender) {
        const messageBubble = document.createElement("div");
        messageBubble.classList.add("received-message");
        messageBubble.setAttribute("data-sender", sender);
        messageBubble.innerHTML = `<p>${text}</p>`;
        chatMessages.appendChild(messageBubble);

        // Auto-scroll to the latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});


document.getElementById("backButton").addEventListener("click", function () {
    document.getElementById("chatBox").style.display = "none";
    document.getElementById("messageList").style.display = "block";
    
    // Hide placeholder when coming back
    document.getElementById("chatPlaceholder").style.display = "none";
});
// Handle Back Button Click
document.getElementById("backButton").addEventListener("click", function () {
    document.getElementById("chatBox").style.display = "none";
    document.getElementById("messageList").style.display = "block";

    // Hide the chatPlaceholder when going back
    document.getElementById("chatPlaceholder").style.display = "none";
});

// Handle Window Resize to Restore Default Layout
window.addEventListener("resize", function () {
    const chatBox = document.getElementById("chatBox");
    const chatPlaceholder = document.querySelector(".chat-placeholder"); // Ensure correct selection
    const messageList = document.getElementById("messageList");

    if (window.innerWidth > 992) {
        // If chat is active, hide placeholder and ensure chat box is visible
        if (chatBox.style.display === "block" || chatBox.innerHTML.trim() !== "") {
            chatPlaceholder.style.display = "none"; 
        } else {
            chatPlaceholder.style.display = "block";
        }

        // Restore layout after resizing back
        messageList.style.display = "block";
    }
});

function openChat(chatId, username, profilePic) {
    document.getElementById('chatBox').style.display = 'block';
    document.getElementById('chatPlaceholder').style.display = 'none';
    document.getElementById('chatUserName').textContent = username;
    document.getElementById('chatProfilePic').src = profilePic;
    document.getElementById('chatMessages').innerHTML = `<p>Loading chat with ${username}...</p>`;
}
