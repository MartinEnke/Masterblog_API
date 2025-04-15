let categories = [];

document.addEventListener('DOMContentLoaded', function () {
    const savedBaseUrl = localStorage.getItem('apiBaseUrl');
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
    }
    loadCategories(); // Always load categories after DOM is ready
    loadPosts();      // Load posts (optional if base URL is prefilled)
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
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postCategory = document.getElementById('post-category').value;

    // Use the Fetch API to send a POST request to the /posts endpoint
    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: postTitle,
            content: postContent,
            category: postCategory
        })
    })
    .then(response => response.json())
    .then(post => {
        console.log('Post added:', post);
        loadPosts();
    })
    .catch(error => console.error('Error:', error));
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Dynamically loads category options into the add and filter dropdowns from the API
function loadCategories() {
    const baseUrl = document.getElementById('api-base-url').value;
    console.log("🌍 Fetching categories from:", baseUrl + '/categories');

    fetch(baseUrl + '/categories')
        .then(response => response.json())
        .then(categories => {
            console.log("✅ Categories received:", categories);

            const categorySelect = document.getElementById('post-category');
            const filterSelect = document.getElementById('filter-category');
            const editSelect = document.getElementById('edit-category');

            // Check if elements exist
            if (!categorySelect) console.warn("⚠️ post-category not found");
            if (!filterSelect) console.warn("⚠️ filter-category not found");
            if (!editSelect) console.warn("⚠️ edit-category not found");

            if (!categorySelect || !filterSelect || !editSelect) return;

            // Reset dropdowns
            categorySelect.innerHTML = '<option value="">Select Category</option>';
            filterSelect.innerHTML = '<option value="">All Categories</option>';
            editSelect.innerHTML = '<option value="">Select Category</option>';

            categories.forEach(cat => {
                const opt1 = new Option(cat, cat);
                const opt2 = new Option(cat, cat);
                const opt3 = new Option(cat, cat);

                categorySelect.appendChild(opt1);
                filterSelect.appendChild(opt2);
                editSelect.appendChild(opt3);
            });
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

let postToEditId = null;

function openEditModal(post) {
    postToEditId = post.id;

    document.getElementById('edit-title').value = post.title;
    document.getElementById('edit-content').value = post.content;

    const categoryDropdown = document.getElementById('edit-category');
    categoryDropdown.innerHTML = ''; // Clear first

    categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = option.textContent = cat;
        if (cat === post.category) option.selected = true;
        categoryDropdown.appendChild(option);
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
        category: document.getElementById('edit-category').value
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

