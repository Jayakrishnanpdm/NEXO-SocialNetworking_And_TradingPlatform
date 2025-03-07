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


document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chatBox");
    const chatProfilePic = document.getElementById("chatProfilePic");
    const chatUserName = document.getElementById("chatUserName");
    const chatMessages = document.getElementById("chatMessages");
    const messageInput = document.getElementById("messageInput");
    const sendMessage = document.getElementById("sendMessage");
    const messageList = document.querySelector(".message-list");
    const editIcon = document.getElementById("editIcon");
    const groupForm = document.getElementById("groupForm");
    const createGroupBtn = document.getElementById("createGroupBtn");
    const closeGroupForm = document.getElementById("closeGroupForm");
    const groupProfilePicInput = document.getElementById("groupProfilePic");
    const groupPicPreview = document.getElementById("groupPicPreview");

    let currentChat = null;
    let groupImageURL = "images/default-group.png"; // Default group image

    // 📌 Attach Click Event to Individual Chats (Existing & Dynamic)
    function attachChatEventListeners() {
        document.querySelectorAll(".message").forEach(message => {
            message.addEventListener("click", function () {
                const profilePic = this.querySelector(".profile-picture img")?.src || "images/default-profile.png";
                const name = this.querySelector("h5").innerText;

                openChat(name, profilePic);
            });
        });
    }



    // 📌 Open Group Form
// 📌 Open & Toggle Group Form on Click of Edit Icon
editIcon.addEventListener("click", function () {
    if (groupForm.style.display === "block") {
        groupForm.style.display = "none"; // Hide group form
        chatPlaceholder.style.display = "flex"; // Show chat placeholder
    } else {
        groupForm.style.display = "block"; // Show group form
        chatPlaceholder.style.display = "none"; // Hide chat placeholder
    }
});

    // 📌 Close Group Form
    closeGroupForm.addEventListener("click", function () {
        groupForm.style.display = "none";
    });

    // 📌 Handle Group Profile Picture Upload & Preview
    groupProfilePicInput.addEventListener("change", function (event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                groupPicPreview.src = e.target.result;
                groupImageURL = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    // 📌 Create Group Chat (With Last Created Group at the Top)
    createGroupBtn.addEventListener("click", function () {
        const groupName = document.getElementById("groupName").value.trim();
        if (groupName === "") {
            alert("Please enter a group name!");
            return;
        }

        // 📌 Create Group Chat Element
        const newGroup = document.createElement("div");
        newGroup.classList.add("message", "group-chat");
        newGroup.innerHTML = `
            <div class="profile-picture">
                <img src="${groupImageURL}" alt="Group">
            </div>
            <div class="message-details">
                <h5>${groupName}</h5>
                <p>Group created just now</p>
            </div>
        `;

        // ✅ Ensure the last created group appears FIRST
        messageList.prepend(newGroup); 

        // Attach event listener for the new group
        attachChatEventListeners();

        // Hide form and open chat
        groupForm.style.display = "none";
        openChat(groupName, groupImageURL);
    });

    // 📌 Send Message Function
    function sendMessageToChat() {
        if (messageInput.value.trim() === "") return;

        const messageDiv = document.createElement("div");
        messageDiv.classList.add("sent-message");

        messageDiv.innerHTML = `
            <span class="sender-name">You</span>
            <p>${messageInput.value}</p>
        `;

        chatMessages.appendChild(messageDiv);
        messageInput.value = "";
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendMessage.addEventListener("click", sendMessageToChat);
    messageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessageToChat();
        }
    });

    // 📌 Attach event listeners on page load for existing chats
    attachChatEventListeners();
});