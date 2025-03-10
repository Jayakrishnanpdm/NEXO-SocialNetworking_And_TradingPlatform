document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded and DOM is ready!");

    // 📌 Selectors
    const menuItems = document.querySelectorAll(".menu-item");
    const notifications = document.querySelector("#notifications");
    const notificationPopup = document.querySelector(".notification-popup");
    const messageSearch = document.querySelector("#message-search");
    const messages = document.querySelectorAll(".message");
    const editIcon = document.getElementById("editIcon");
    const groupForm = document.getElementById("groupForm");
    const chatPlaceholder = document.getElementById("chatPlaceholder") || document.getElementById("chatContainer");
    const closeGroupForm = document.getElementById("closeGroupForm");
    const groupProfilePicInput = document.getElementById("groupProfilePic");
    const groupPicPreview = document.getElementById("groupPicPreview");
    const createGroupBtn = document.getElementById("createGroupBtn");
    const messageInput = document.getElementById("messageInput");
    const sendMessage = document.getElementById("sendMessage");
    const messageList = document.querySelector(".message-list");

    let groupImageURL = "images/default-group.png"; // Default group image

    // 📌 Check for missing elements
    if (!notifications || !notificationPopup) {
        console.warn("Notification elements not found!");
    }

    if (!groupForm || !chatPlaceholder || !closeGroupForm) {
        console.warn("One or more chat elements are missing!");
    }

    // 📌 Toggle Active Menu Item
    const changeActiveItem = () => {
        menuItems.forEach(item => item.classList.remove("active"));
    };

    menuItems.forEach(item => {
        item.addEventListener("click", () => {
            changeActiveItem();
            item.classList.add("active");

            if (item.id !== "notifications") {
                notificationPopup.style.display = "none";
            } else {
                notificationPopup.style.display = notificationPopup.style.display === "block" ? "none" : "block";
                const notificationCount = document.querySelector("#notifications .notification-count");
                if (notificationCount) notificationCount.style.display = "none";
            }
        });
    });

    // 📌 Search Messages
    const searchMessages = () => {
        const val = messageSearch.value.toLowerCase();
        messages.forEach(chat => {
            const name = chat.querySelector("h5").textContent.toLowerCase();
            chat.style.display = name.includes(val) ? "flex" : "none";
        });
    };

    if (messageSearch) {
        messageSearch.addEventListener("input", searchMessages);
    }

    // 📌 Toggle Group Form (Works for both templates)
    if (editIcon && groupForm && chatPlaceholder) {
        editIcon.addEventListener("click", function () {
            if (groupForm.style.display === "block") {
                groupForm.style.display = "none"; // Hide group form
                chatPlaceholder.style.display = "flex"; // Show placeholder/chat-container
            } else {
                groupForm.style.display = "block"; // Show group form
                chatPlaceholder.style.display = "none"; // Hide placeholder/chat-container
            }
        });

        closeGroupForm.addEventListener("click", function () {
            groupForm.style.display = "none";
            chatPlaceholder.style.display = "flex"; // Restore chatPlaceholder/chatContainer visibility
        });
    }

    // 📌 Handle Group Profile Picture Upload
    if (groupProfilePicInput && groupPicPreview) {
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
    }

    // 📌 Create Group Chat
    if (createGroupBtn && messageList) {
        createGroupBtn.addEventListener("click", function () {
            const groupName = document.getElementById("groupName").value.trim();
            if (groupName === "") {
                alert("Please enter a group name!");
                return;
            }

            // 📌 Create New Group Chat Element
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

            // ✅ Add New Group at the Top
            messageList.prepend(newGroup);

            // Attach Click Event to New Group
            newGroup.addEventListener("click", function () {
                openChat(groupName, groupImageURL);
            });

            // Hide Form and Open Chat
            groupForm.style.display = "none";
            chatPlaceholder.style.display = "none";
        });
    }
});

