let categories = [];


document.addEventListener('DOMContentLoaded', () => {
    const savedBaseUrl = localStorage.getItem('apiBaseUrl');
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
    }

    loadCategories();
    loadPosts();
    updateAuthButton();  // Add this line
    updateUserInfo();
});


document.getElementById('search-input').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        searchPosts(); // your custom function
    }
});


// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    const baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    const category = document.getElementById('filter-category')?.value;
    const sort = document.getElementById('sort-field')?.value;
    const direction = document.getElementById('sort-direction')?.value;

    const params = new URLSearchParams();
    if (category) params.append("category", category);
    if (sort) params.append("sort", sort);
    if (direction) params.append("direction", direction);

    fetch(baseUrl + '/posts?' + params.toString())
        .then(response => response.json())
        .then(data => {
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            const posts = data.posts || data; // Handle paginated or raw list

            posts.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';

                // Title
                const title = document.createElement('h2');
                title.textContent = post.title;

                // Content
                const content = document.createElement('p');
                content.textContent = post.content;

                // Meta (date + author)
                const meta = document.createElement('p');
                meta.className = 'post-meta';
                meta.textContent = `${post.date || 'No date'} · by ${post.author || 'Unknown'}`;

                // Updated (optional)
                const updated = document.createElement('p');
                if (post.updated) {
                    updated.textContent = `Updated: ${post.updated}`;
                    updated.style.fontSize = '0.9em';
                    updated.style.color = '#777';
                    updated.style.marginBottom = '10px';
                }

                // Like Button
                const likeButton = document.createElement('button');
                likeButton.innerHTML = `❤️ <span id="like-count-${post.id}">${post.likes || 0}</span>`;
                likeButton.onclick = () => likePost(post.id);

                // Delete Button
                const deleteButton = document.createElement('button');
                deleteButton.textContent = '🗑️ Delete';
                deleteButton.onclick = () => deletePost(post.id);

                // Edit Button
                const editButton = document.createElement('button');
                editButton.textContent = '✏️ Edit';
                editButton.onclick = () => openEditModal(post);

                // Button container
                const buttonWrapper = document.createElement('div');
                buttonWrapper.style.display = 'flex';
                buttonWrapper.style.justifyContent = 'space-between';
                buttonWrapper.style.gap = '10px';
                buttonWrapper.style.marginTop = '10px';
                buttonWrapper.appendChild(likeButton);

                // ✅ Only show edit/delete if user is author
                const currentUser = localStorage.getItem("username");
                if (post.author === currentUser) {
                    buttonWrapper.appendChild(editButton);
                    buttonWrapper.appendChild(deleteButton);
                }

                // Post styling
                postDiv.style.padding = '15px';
                postDiv.style.border = '1px solid #ccc';
                postDiv.style.marginBottom = '20px';
                postDiv.style.borderRadius = '8px';

                // Append all elements
                postDiv.appendChild(title);
                postDiv.appendChild(content);
                postDiv.appendChild(meta);
                if (post.updated) postDiv.appendChild(updated);
                postDiv.appendChild(buttonWrapper);

                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error loading posts:', error));
}



// Function to send a POST request to the API to add a new post
function addPost() {
    const baseUrl = document.getElementById('api-base-url').value;
    const token = localStorage.getItem('authToken');

    fetch(`${baseUrl}/posts`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token || ""
        },
        body: JSON.stringify({
            title: document.getElementById('add-title').value,
            content: document.getElementById('add-content').value,
            category: document.getElementById('add-category').value,
            author: "Anonymous"  // Replace later if needed
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('✅ Post added:', data);
        loadPosts();
    })
    .catch(error => {
        console.error('❌ Failed to add post:', error);
        alert("You need to be logged in to add a post.");
    });
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    const baseUrl = document.getElementById('api-base-url').value;
    const token = localStorage.getItem('authToken');

    if (!confirm("🛑 Are you sure you want to delete this post?")) return;

    fetch(`${baseUrl}/posts/${postId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': token || ""
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || "Failed to delete post");
            });
        }
        return response.json();
    })
    .then(data => {
        console.log("✅ Deleted:", data);
        loadPosts();
    })
    .catch(error => {
        console.error("❌ Delete failed:", error.message);
        alert("Error: " + error.message);
    });
}


// Dynamically loads category options into the add and filter dropdowns from the API
function loadCategories() {
    const baseUrl = document.getElementById('api-base-url').value;
    console.log("🌍 Fetching categories from:", baseUrl + '/categories');

    fetch(baseUrl + '/categories')
        .then(response => response.json())
        .then(fetchedCategories => {
            console.log("✅ Categories received:", fetchedCategories);
            categories = fetchedCategories; // update global list

            // Get dropdowns
            const filterSelect = document.getElementById('filter-category');
            const addSelect = document.getElementById('add-category');
            const editSelect = document.getElementById('edit-category');

            // 🧼 Clear & repopulate Filter dropdown
            if (filterSelect) {
                filterSelect.innerHTML = '<option value="">All Categories</option>';
                categories.forEach(cat => {
                    const opt = new Option(cat, cat);
                    filterSelect.appendChild(opt);
                });
            }

            // 🧼 Clear & repopulate Add dropdown
            if (addSelect) {
                addSelect.innerHTML = '<option value="">Select Category</option>';
                categories.forEach(cat => {
                    const opt = new Option(cat, cat);
                    addSelect.appendChild(opt);
                });
            }

            // 🧼 Clear & repopulate Edit dropdown (leave selection logic to `openEditModal`)
            if (editSelect) {
                editSelect.innerHTML = '<option value="">Select Category</option>';
                categories.forEach(cat => {
                    const opt = new Option(cat, cat);
                    editSelect.appendChild(opt);
                });
            }
        })
        .catch(error => {
            console.error("❌ Failed to load categories:", error);
        });
}


//
function likePost(postId) {
    const baseUrl = document.getElementById('api-base-url').value;

    fetch(`${baseUrl}/posts/${postId}/like`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.likes !== undefined) {
            // Update the like count on the page
            document.getElementById(`like-count-${postId}`).textContent = data.likes;
        } else {
            console.error("No 'likes' value returned:", data);
        }
    })
    .catch(error => {
        console.error("Error liking the post:", error);
    });
}


function searchPosts() {
    const baseUrl = document.getElementById('api-base-url').value;
    const query = document.getElementById('search-input').value.trim();

    if (!query) {
        loadPosts(); // fallback
        return;
    }

    fetch(`${baseUrl}/posts/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            if (data.error) {
                postContainer.innerHTML = `<p>${data.error}</p>`;
                return;
            }

            const posts = data.posts || data;
            const currentUser = localStorage.getItem("username");

            posts.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';

                // Title
                const title = document.createElement('h2');
                title.textContent = post.title;

                // Content
                const content = document.createElement('p');
                content.textContent = post.content;

                // Meta (date + author)
                const meta = document.createElement('p');
                meta.className = 'post-meta';
                meta.textContent = `${post.date || 'No date'} · by ${post.author || 'Unknown'}`;

                // Updated (optional)
                const updated = document.createElement('p');
                if (post.updated) {
                    updated.textContent = `Updated: ${post.updated}`;
                    updated.style.fontSize = '0.9em';
                    updated.style.color = '#777';
                    updated.style.marginBottom = '10px';
                }

                // Like Button
                const likeButton = document.createElement('button');
                likeButton.innerHTML = `❤️ <span id="like-count-${post.id}">${post.likes || 0}</span>`;
                likeButton.onclick = () => likePost(post.id);

                // Edit/Delete Buttons (conditionally shown)
                const editButton = document.createElement('button');
                editButton.textContent = '✏️ Edit';
                editButton.onclick = () => openEditModal(post);

                const deleteButton = document.createElement('button');
                deleteButton.textContent = '🗑️ Delete';
                deleteButton.onclick = () => deletePost(post.id);

                const buttonWrapper = document.createElement('div');
                buttonWrapper.style.display = 'flex';
                buttonWrapper.style.justifyContent = 'space-between';
                buttonWrapper.style.gap = '10px';
                buttonWrapper.style.marginTop = '10px';
                buttonWrapper.appendChild(likeButton);

                if (post.author === currentUser) {
                    buttonWrapper.appendChild(editButton);
                    buttonWrapper.appendChild(deleteButton);
                }

                // Post styling
                postDiv.style.padding = '15px';
                postDiv.style.border = '1px solid #ccc';
                postDiv.style.marginBottom = '20px';
                postDiv.style.borderRadius = '8px';

                postDiv.appendChild(title);
                postDiv.appendChild(content);
                postDiv.appendChild(meta);
                if (post.updated) postDiv.appendChild(updated);
                postDiv.appendChild(buttonWrapper);

                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Search error:', error));
}



function renderPost(post) {
    const postContainer = document.getElementById('post-container');
    const postDiv = document.createElement('div');
    postDiv.className = 'post';

    const title = document.createElement('h2');
    title.textContent = post.title;

    const content = document.createElement('p');
    content.textContent = post.content;

    const date = document.createElement('p');
    date.textContent = `${post.date || 'No date'}`;
    date.style.fontStyle = 'italic';

    const likeButton = document.createElement('button');
    likeButton.innerHTML = `❤️ <span id="like-count-${post.id}">${post.likes || 0}</span>`;
    likeButton.onclick = () => likePost(post.id);

    const deleteButton = document.createElement('button');
    deleteButton.textContent = '🗑️ Delete';
    deleteButton.onclick = () => deletePost(post.id);

    const editButton = document.createElement('button');
    editButton.textContent = '✏️ Edit';
    editButton.onclick = () => openEditModal(post);

    const buttonWrapper = document.createElement('div');
    buttonWrapper.style.display = 'flex';
    buttonWrapper.style.gap = '10px';
    buttonWrapper.appendChild(likeButton);
    buttonWrapper.appendChild(editButton);
    buttonWrapper.appendChild(deleteButton);

    postDiv.appendChild(title);
    postDiv.appendChild(content);
    postDiv.appendChild(date);
    postDiv.appendChild(buttonWrapper);

    postContainer.appendChild(postDiv);
}


// Registration Part //
function loginUser(username, password) {
    const baseUrl = document.getElementById('api-base-url').value;

    fetch(`${baseUrl.replace(/\/api$/, '')}/api/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('authToken', data.token);
            alert("✅ Logged in successfully");
        } else {
            alert("❌ Login failed: " + (data.error || "Unknown error"));
        }
    })
    .catch(err => {
        console.error("Login error:", err);
        alert("❌ Login request failed");
    });
}

let postToEditId = null;

console.log("Categories loaded:", categories);


function openEditModal(post) {
    postToEditId = post.id;

    document.getElementById('edit-title').value = post.title;
    document.getElementById('edit-content').value = post.content;

    const dropdown = document.getElementById('edit-category');
    dropdown.innerHTML = '';

    categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        if (cat.trim().toLowerCase() === post.category.trim().toLowerCase()) {
            option.selected = true;
        }
        dropdown.appendChild(option);
    });

    document.getElementById('update-modal').classList.remove('hidden');
}


function closeModal() {
    document.getElementById('update-modal').classList.add('hidden');
}


function submitUpdate() {
    const baseUrl = document.getElementById('api-base-url').value;
    const token = localStorage.getItem('authToken');

    const updatedPost = {
        title: document.getElementById('edit-title').value,
        content: document.getElementById('edit-content').value,
        category: document.getElementById('edit-category').value,
        author: "Anonymous" // Optional, adjust as needed
    };

    fetch(`${baseUrl}/posts/${postToEditId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token || ""
        },
        body: JSON.stringify(updatedPost)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || "Update failed");
            });
        }
        return response.json();
    })
    .then(data => {
        closeModal();
        loadPosts();
    })
    .catch(err => {
        console.error("❌ Failed to update post:", err.message);
        alert("Error: " + err.message);
    });
}

function openAddModal() {
  const token = localStorage.getItem('authToken');
  if (!token) {
    showAlertModal("You need to login to add a post.");
    return;
  }

  // Clear form & open modal
  document.getElementById('add-title').value = '';
  document.getElementById('add-content').value = '';
  const dropdown = document.getElementById('add-category');
  dropdown.innerHTML = '<option value="">Select Category</option>';
  categories.forEach(cat => {
    const option = document.createElement('option');
    option.value = cat;
    option.textContent = cat;
    dropdown.appendChild(option);
  });

  document.getElementById('add-modal').classList.remove('hidden');
}

function closeAddWarningModal() {
  document.getElementById('add-warning-modal').classList.add('hidden');
}

function handleLoginFromWarning() {
  closeAddWarningModal();      // 👈 closes the warning modal
  openLoginModal();            // 👈 opens the login modal
}


function closeAddModal() {
    document.getElementById('add-modal').classList.add('hidden');
}


function submitAdd() {
    const baseUrl = document.getElementById('api-base-url').value;
    const token = localStorage.getItem('authToken');

    const newPost = {
        title: document.getElementById('add-title').value,
        content: document.getElementById('add-content').value,
        category: document.getElementById('add-category').value,
        author: "Anonymous" // Optional: use logged-in username if available
    };

    fetch(`${baseUrl}/posts`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token || ""
        },
        body: JSON.stringify(newPost)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || "Add post failed");
            });
        }
        return response.json();
    })
    .then(data => {
        closeModal();
        loadPosts();
    })
    .catch(err => {
        console.error("❌ Failed to add post:", err.message);
        alert("Error: " + err.message);
    });
}

function openLoginModal() {
    document.getElementById('login-modal').classList.remove('hidden');
}

function closeLoginModal() {
    document.getElementById('login-modal').classList.add('hidden');
}

function submitLogin() {
    const baseUrl = document.getElementById('api-base-url').value;
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    fetch(`${baseUrl}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
    if (data.token) {
        localStorage.setItem("authToken", data.token);
        localStorage.setItem("username", username);  // store username and password
        updateUserInfo();
        updateAuthButton();
        // alert("🎉 Logged in successfully!");
        closeLoginModal();
        loadPosts();
    } else {
        alert(data.error || "❌ Login failed.");
    }
})
    .catch(err => {
        console.error("Login error:", err);
        alert("❌ Login request failed.");
    });
}

function updateAuthButton() {
    const token = localStorage.getItem("authToken");
    const button = document.getElementById("auth-button");
    if (token) {
        button.textContent = "Logout";
    } else {
        button.textContent = "Login";
    }
}

function handleAuthClick() {
    const token = localStorage.getItem("authToken");
    if (token) {
        // Logout
        localStorage.removeItem("authToken");
        localStorage.removeItem("username");  // 👈 clear username
        updateAuthButton();
        updateUserInfo();  // 👈 update the username display
        // alert("👋 Logged out successfully.");
        loadPosts();
    } else {
        openLoginModal();
    }
}


function openLogoutModal() {
  document.getElementById('logout-modal').classList.remove('hidden');
}

function closeLogoutModal() {
  document.getElementById('logout-modal').classList.add('hidden');
}

function confirmLogout() {
  localStorage.removeItem('authToken');
  localStorage.removeItem('username'); // 👈 clear username here too
  updateLoginButton();
  updateUserInfo(); // 👈 make sure it's reflected in the UI
  closeLogoutModal();
  // alert("👋 You have been logged out.");
  loadPosts();
}


function openSignupModal() {
  document.getElementById('signup-modal').classList.remove('hidden');
}

function closeSignupModal() {
  document.getElementById('signup-modal').classList.add('hidden');
}

function submitSignup() {
  const baseUrl = document.getElementById('api-base-url').value;
  const username = document.getElementById('signup-username').value;
  const password = document.getElementById('signup-password').value;

  fetch(`${baseUrl}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.error) {
      alert(data.error);
      return;
    }

    // alert(data.message || "✅ Signup successful!");

    // 👇 Immediately log the user in
    return fetch(`${baseUrl}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
  })
  .then(res => res?.json())
  .then(loginData => {
    if (!loginData || !loginData.token) return;

    localStorage.setItem("authToken", loginData.token);
    localStorage.setItem("username", username);
    updateUserInfo();     // 👈 To show the username on the page
    updateAuthButton();         // 👈 update login/logout state
    closeSignupModal();
    loadPosts();
  })
  .catch(err => {
    console.error("Signup error:", err);
    alert("❌ Signup or auto-login failed.");
  });
}

function handleLoginToggle() {
  const token = localStorage.getItem("authToken");
  if (token) {
    openLogoutModal();  // Ask for confirmation
  } else {
    openLoginModal();   // Show login modal
  }
}

function updateLoginButton() {
  const token = localStorage.getItem("authToken");
  document.getElementById('login-toggle-btn').textContent = token ? "Logout" : "Login";
}

function updateUserInfo() {
  const username = localStorage.getItem("username");
  const userInfo = document.getElementById("user-info");

  if (username) {
    userInfo.textContent = `Welcome, ${username}!`;
  } else {
    userInfo.textContent = ""; // empty when logged out
  }
}

function showAlertModal(message) {
  const alertBox = document.getElementById("alert-modal");
  const messageText = document.getElementById("alert-message");
  messageText.textContent = message;
  alertBox.classList.remove("hidden");
}

function closeAlertModal() {
  document.getElementById("alert-modal").classList.add("hidden");
}

function handleAlertLogin() {
  closeAlertModal();
  openLoginModal(); // Already exists in your code
}

// Call this when DOM loads
document.addEventListener("DOMContentLoaded", updateLoginButton);