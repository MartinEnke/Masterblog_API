let categories = [];


document.addEventListener('DOMContentLoaded', () => {
    const savedBaseUrl = localStorage.getItem('apiBaseUrl');
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
    }

    loadCategories();
    loadPosts();
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

            const posts = data.posts || data; // handle paginated or raw list

            posts.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';

                const title = document.createElement('h2');
                title.textContent = post.title;

                const content = document.createElement('p');
                content.textContent = post.content;

                // Date
                const date = document.createElement('p');
                date.textContent = `${post.date || 'No date'}`;
                date.style.fontStyle = 'italic';
                date.style.marginTop = '10px';
                date.style.marginBottom = '2px';

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
                buttonWrapper.appendChild(editButton);
                buttonWrapper.appendChild(deleteButton);

                // Styling container
                postDiv.style.padding = '15px';
                postDiv.style.border = '1px solid #ccc';
                postDiv.style.marginBottom = '20px';
                postDiv.style.borderRadius = '8px';

                // Build the post card
                postDiv.appendChild(title);
                postDiv.appendChild(content);
                postDiv.appendChild(date);
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

    fetch(`${baseUrl}/posts`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: document.getElementById('add-title').value,
            content: document.getElementById('add-content').value,
            category: document.getElementById('add-category').value,
            author: "Anonymous"  // ← now correctly separated
        })
    })
    .then(response => response.json())
    .then(post => {
        console.log('Post added:', post);
        loadPosts();
        closeModal(); // Optionally close the modal here
    })
    .catch(error => console.error('Error:', error));
}


// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    const confirmed = confirm("🗑️ Are you sure you want to delete this post?");
    if (!confirmed) return;

    const baseUrl = document.getElementById('api-base-url').value;

    fetch(`${baseUrl}/posts/${postId}`, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('✅ Post deleted:', postId);
        loadPosts();
    })
    .catch(error => console.error('❌ Error deleting post:', error));
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

            posts.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';

                const title = document.createElement('h2');
                title.textContent = post.title;

                const content = document.createElement('p');
                content.textContent = post.content;

                const date = document.createElement('p');
                date.textContent = `${post.date || 'No date'}`;
                date.style.fontStyle = 'italic';

                postDiv.appendChild(title);
                postDiv.appendChild(content);
                postDiv.appendChild(date);

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

    const updatedPost = {
        title: document.getElementById('edit-title').value,
        content: document.getElementById('edit-content').value,
        category: document.getElementById('edit-category').value,
        author: "Anonymous"  // ← now correctly separated
    };

    fetch(`${baseUrl}/posts/${postToEditId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedPost)
    })
    .then(response => response.json())
    .then(data => {
        closeModal();
        loadPosts();
    })
    .catch(err => {
        console.error("Failed to update post", err);
    });
}

function openAddModal() {
    // Clear previous values
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

function closeAddModal() {
    document.getElementById('add-modal').classList.add('hidden');
}

function submitAdd() {
    console.log("🚀 Trying to submit a new post...");
    const baseUrl = document.getElementById('api-base-url').value;

    const newPost = {
        title: document.getElementById('add-title').value,
        content: document.getElementById('add-content').value,
        category: document.getElementById('add-category').value,
        author: "Anonymous"  // ← now correctly separated
    };


    fetch(`${baseUrl}/posts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPost)
    })
    .then(response => response.json())
    .then(data => {
        closeAddModal();
        loadPosts();
    })
    .catch(err => {
        console.error("❌ Failed to add post", err);
    });
}
