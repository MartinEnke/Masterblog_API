/* static/main.js */

/* ==========================================================================
   GLOBAL VARIABLES
   ========================================================================== */
const API_URL_KEY = 'apiBaseUrl';
let categories = [];
let postToEditId = null;

function getCurrentLanguage() {
  return localStorage.getItem("lang") || "en";
}

function checkBackendConnection() {
  fetch(`${getBaseUrl()}/status`)
    .then(res => {
      if (res.ok) {
        console.log("✅ Backend status: OK");
      } else {
        throw new Error("Non-200 status");
      }
    })
    .catch(err => {
      console.error("❌ Backend not reachable:", err);
      alert("Could not reach the backend. Check API base URL.");
    });
}

/* ==========================================================================
   UI TRANSLATIONS
   ========================================================================== */
function applyUITranslations() {
  const lang = getCurrentLanguage();
  const strings = UI_TRANSLATIONS[lang];

  // Text content
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (strings[key]) el.textContent = strings[key];
  });

  // Placeholders (e.g. for input fields)
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (strings[key]) el.placeholder = strings[key];
  });

  // Optional: welcome text
  const username = localStorage.getItem("username");
  if (username) {
    document.getElementById("user-info").textContent = `${strings.welcome}, ${username}!`;
  } else {
    document.getElementById("user-info").textContent = "";
  }
}

/* ==========================================================================
   UTILITIES: BASE URL (public v1 API)
   ========================================================================== */
function getDefaultBaseUrl() {
  return "http://127.0.0.1:5021/api/v2";
}

function getBaseUrl() {
  return (localStorage.getItem(API_URL_KEY) || getDefaultBaseUrl())
    .replace(/\/+$/, '');
}

function storeBaseUrl() {
  localStorage.setItem(API_URL_KEY,
    document.getElementById("api-base-url").value.trim()
  );
  loadPosts();
}

/* ==========================================================================
   AUTH HELPERS
   ========================================================================== */
function saveToken(token) {
  localStorage.setItem('authToken', token);
}
function getToken() {
  return localStorage.getItem('authToken') || '';
}
function clearToken() {
  localStorage.removeItem('authToken');
  localStorage.removeItem('username');
}

/* ==========================================================================
   INITIALIZATION
   ========================================================================== */
document.addEventListener('DOMContentLoaded', () => {
  console.log("🚀 DOM fully loaded. Starting app.");

  // 🔁 Wire up "Apply Filters" button
  const btn = document.getElementById("load-posts-btn");
  if (btn) {
    btn.addEventListener("click", loadPosts);
  } else {
    console.warn("⚠️ Couldn't find #load-posts-btn in DOM.");
  }

  // Base URL handling
  document.getElementById('api-base-url').value = getBaseUrl();
  document.getElementById('api-base-url')
    .addEventListener('change', storeBaseUrl);

  // 🌐 Apply UI translations on load
  applyUITranslations();

  // 🌐 Set up language dropdown
  const langSelect = document.getElementById("lang-select");
  if (langSelect) {
    langSelect.value = getCurrentLanguage();
    langSelect.addEventListener("change", e => {
      localStorage.setItem("lang", e.target.value);
      applyUITranslations();  // ✅ Update UI strings
      loadPosts();            // ✅ Load posts in new language
    });
  }

  // Initialize core app behavior
  loadCategories();
  loadPosts();
  updateAuthButton();
  updateUserInfo();

  // 🔍 Search on Enter
  document.getElementById('search-input')
    .addEventListener('keydown', e => {
      if (e.key === 'Enter') searchPosts();
    });
});


/* ==========================================================================
   POSTS: LOAD / RENDER / SEARCH
   ========================================================================== */
function loadPosts() {
  console.log("Calling loadPosts with base URL:", getBaseUrl());
  const base = getBaseUrl();
  const qs = new URLSearchParams({
  category: document.getElementById('filter-category').value,
  sort: document.getElementById('sort-field').value,
  direction: document.getElementById('sort-direction').value,
  lang: getCurrentLanguage()
});

  fetch(`${base}/posts?${qs}`)
    .then(r => r.json())
    .then(data => {
      const posts = data.posts || data;
      const c = document.getElementById('post-container');
      c.innerHTML = '';
      posts.forEach(renderSinglePost);
    })
    .catch(err => console.error('Error loading posts:', err));
}


/**
 * Renders a single post card, showing Edit/Delete only to the author.
 */
function renderSinglePost(post) {
  const container = document.getElementById('post-container');
  const div = document.createElement('div');
  div.className = 'post';
  Object.assign(div.style, {
    padding: '15px',
    border: '1px solid #ccc',
    marginBottom: '20px',
    borderRadius: '8px'
  });

  div.innerHTML = `
  <h2>${post.title}</h2>
  <p>${post.content}</p>
  <p class="post-meta">${post.date || 'No date'} · by ${post.author || 'Unknown'}</p>
  ${post.updated
    ? `<p style="font-size:.9em;color:#777;margin-bottom:10px">
         Updated: ${post.updated}
       </p>`
    : ''}
  <div class="comment-section" id="comments-${post.id}">
    <h4>Comments</h4>
    <div id="comment-list-${post.id}"></div>
    <textarea id="comment-text-${post.id}" placeholder="Add a comment..."></textarea>
    <button onclick="submitComment(${post.id})">Post Comment</button>
  </div>
`;

  const btnWrap = document.createElement('div');
  Object.assign(btnWrap.style, {
    display: 'flex',
    justifyContent: 'space-between',
    gap: '10px',
    marginTop: '10px'
  });

  // Like button
  const likeBtn = document.createElement('button');
  likeBtn.innerHTML = `❤️ <span id="like-count-${post.id}">${post.likes || 0}</span>`;
  likeBtn.onclick = () => likePost(post.id);
  btnWrap.appendChild(likeBtn);

  // Only show Edit/Delete to the post's author
  const currentUser = localStorage.getItem('username');
const isAdmin = localStorage.getItem('isAdmin') === 'true';

// Show Edit/Delete if author OR admin
if (post.author === currentUser || isAdmin) {
  if (post.author === currentUser) {
    const editBtn = document.createElement('button');
    editBtn.textContent = '✏️ Edit';
    editBtn.onclick = () => openEditModal(post);
    btnWrap.appendChild(editBtn);
  }

  const delBtn = document.createElement('button');
  delBtn.textContent = '🗑️ Delete';
  delBtn.onclick = () => deletePost(post.id);
  btnWrap.appendChild(delBtn);
}

  div.appendChild(btnWrap);

  // 🔁 Load comments from DB
  loadComments(post.id);

  container.appendChild(div);
}

function searchPosts() {
  const query = document.getElementById('search-input').value.trim();
  if (!query) return loadPosts();

  const qs = new URLSearchParams({
  q: query,
  lang: getCurrentLanguage()
});

  fetch(`${getBaseUrl()}/posts/search?${qs}`)
    .then(r => r.json())
    .then(data => {
      const container = document.getElementById('post-container');
      container.innerHTML = data.error ? `<p>${data.error}</p>` : '';
      (data.posts || data).forEach(renderSinglePost);
    })
    .catch(err => console.error('Search error:', err));
}

function loadComments(postId) {
  fetch(`${getBaseUrl()}/posts/${postId}/comments`)
    .then(res => res.json())
    .then(comments => {
      const list = document.getElementById(`comment-list-${postId}`);
      list.innerHTML = '';

      const currentUser = localStorage.getItem("username");
      const isAdmin = localStorage.getItem("isAdmin") === "true";

      comments.forEach(c => {
        const p = document.createElement('p');
        p.innerHTML = `
          <strong>${c.author}</strong>: ${c.text}
          <span style="font-size:.8em; color:#888">(${c.date})</span>
          ${(c.author === currentUser || isAdmin) ?
            `<span style="cursor:pointer; color:red; margin-left:10px" onclick="deleteComment(${c.id}, ${postId})">❌</span>`
            : ''}
        `;
        list.appendChild(p);
      });
    });
}
/* ==========================================================================
   POSTS: ADD / EDIT / DELETE
   ========================================================================== */
function submitAdd() {
  const base = getBaseUrl();
  const payload = {
    title:   document.getElementById('add-title').value,
    content: document.getElementById('add-content').value,
    category:document.getElementById('add-category').value
  };
  fetch(`${base}/posts`, {
    method: 'POST',
    headers: {
      'Content-Type':'application/json',
      'Authorization': `Bearer ${getToken()}`
    },
    body: JSON.stringify(payload)
  })
  .then(r => {
    if (!r.ok) return r.json().then(e=>Promise.reject(e.error));
    return r.json();
  })
  .then(() => { closeAddModal(); loadPosts(); })
  .catch(e => alert("Error: "+e));
}

function submitUpdate() {
  const base = getBaseUrl();
  const payload = {
    title:   document.getElementById('edit-title').value,
    content: document.getElementById('edit-content').value,
    category:document.getElementById('edit-category').value
  };
  fetch(`${base}/posts/${postToEditId}`, {
    method: 'PUT',
    headers: {
      'Content-Type':'application/json',
      'Authorization': `Bearer ${getToken()}`
    },
    body: JSON.stringify(payload)
  })
  .then(r => {
    if (!r.ok) return r.json().then(e=>Promise.reject(e.error));
    return r.json();
  })
  .then(() => { closeModal(); loadPosts(); })
  .catch(e => alert("Error: "+e));
}

function deletePost(id) {
  if (!confirm("Delete this post?")) return;
  fetch(`${getBaseUrl()}/posts/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${getToken()}`
    }
  })
  .then(r => {
    if (!r.ok) return r.json().then(e=>Promise.reject(e.error));
    return r.json();
  })
  .then(() => loadPosts())
  .catch(e => alert("Error: "+e));
}

function likePost(id) {
  fetch(`${getBaseUrl()}/posts/${id}/like`, {
    method:'POST',
    headers:{ 'Authorization': `Bearer ${getToken()}` }
  })
  .then(r => r.json())
  .then(d => {
    if (d.likes!==undefined) {
      document.getElementById(`like-count-${id}`).textContent = d.likes;
    }
  })
  .catch(console.error);
}

function submitComment(postId) {
  const base = getBaseUrl();
  const text = document.getElementById(`comment-text-${postId}`).value.trim();

  if (!text) return alert("Please enter a comment");

  fetch(`${base}/posts/${postId}/comments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`
    },
    body: JSON.stringify({ text })
  })
  .then(r => {
    if (!r.ok) return r.json().then(e => Promise.reject(e.error));
    return r.json();
  })
  .then(d => {
    const list = document.getElementById(`comment-list-${postId}`);
    const currentUser = localStorage.getItem('username');
    const isAdmin = localStorage.getItem('isAdmin') === 'true';

    const c = d.comment;

    // 🛠️ This is the key rendering logic:
    const p = document.createElement('p');
    const showDelete = currentUser && (c.author === currentUser || isAdmin);

    p.innerHTML = `
      <strong>${c.author}</strong>: ${c.text}
      <span style="font-size:.8em; color:#888">(${c.date})</span>
      ${showDelete ? `<span style="cursor:pointer; color:red; margin-left:10px" onclick="deleteComment(${c.id}, ${postId})">❌</span>` : ''}
    `;
    list.appendChild(p);
    document.getElementById(`comment-text-${postId}`).value = '';
  })
  .catch(e => alert("Error: " + e));
}


function deleteComment(commentId) {
  const base = getBaseUrl();
  const token = getToken();

  if (!token) {
    alert("You must be logged in to delete a comment.");
    return;
  }

  if (!confirm("Are you sure you want to delete this comment?")) return;

  fetch(`${base}/comments/${commentId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  })
  .then(r => {
    if (!r.ok) return r.json().then(e => Promise.reject(e.error));
    return r.json();
  })
  .then(data => {
    console.log("🧾 Delete success:", data);
    loadPosts(); // reloads comments too
  })
  .catch(err => console.error("❌ Delete failed:", err));
}


/* ==========================================================================
   CATEGORIES
   ========================================================================== */
function loadCategories() {
  const baseUrl = getBaseUrl();
  const categoryUrl = getBaseUrl() + '/categories';
  console.log("🔄 Calling loadCategories with:", categoryUrl);

  const dropdownIds = ['filter-category', 'add-category', 'edit-category'];

  dropdownIds.forEach(id => {
    const sel = document.getElementById(id);
    if (!sel) {
      console.warn(`⚠️ Element #${id} not found in DOM at loadCategories start.`);
      return;
    }

    const defaultOption = id === 'filter-category'
      ? new Option("All Categories", "")
      : new Option("Select Category", "");
    sel.innerHTML = '';  // clear everything first
    sel.appendChild(defaultOption);
  });

  fetch(categoryUrl)
    .then(response => {
      console.log("📡 Category response status:", response.status);
      if (!response.ok) throw new Error(`Bad response: ${response.status}`);
      return response.json();
    })
    .then(fetched => {
  console.log("📦 Categories fetched from API:", fetched);
  categories = fetched;

      if (!Array.isArray(categories)) {
        console.error("❌ Categories response is not an array:", categories);
        return;
      }

      dropdownIds.forEach(id => {
        const sel = document.getElementById(id);
        if (!sel) {
          console.warn(`⚠️ Skipping #${id}, not found during population.`);
          return;
        }

        categories.forEach(cat => {
          if (typeof cat === 'string') {
            const opt = new Option(cat, cat);
            sel.appendChild(opt);
          } else {
            console.warn(`⚠️ Skipping non-string category:`, cat);
          }
        });

        console.log(`✅ Populated #${id} with ${sel.options.length} options.`);
      });
    })
    .catch(err => {
      console.error("❌ Failed to fetch or populate categories:", err);
    });
}




/* ==========================================================================
   AUTH: LOGIN / SIGNUP / UI
   ========================================================================== */
function submitLogin() {
  const base = getBaseUrl().split('/api/')[0];
  const u = document.getElementById('login-username').value;
  const p = document.getElementById('login-password').value;

  fetch(`${base}/api/v1/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: u, password: p })
  })
  .then(r => r.json())
  .then(async d => {
    if (!d.token) {
      alert('Login failed: ' + (d.error || ''));
      return;
    }

    saveToken(d.token);
    localStorage.setItem('username', u);

    // ✅ Try to fetch admin info before proceeding
    try {
      const res = await fetch(`${base}/api/v2/me`, {
        headers: { 'Authorization': `Bearer ${d.token}` }
      });

      if (res.ok) {
        const user = await res.json();
        if (user?.is_admin) {
          localStorage.setItem('isAdmin', 'true');
        } else {
          localStorage.removeItem('isAdmin');
        }
      } else {
        console.warn("Warning: Failed to fetch /me. Status:", res.status);
      }
    } catch (err) {
      console.warn("Warning: Error fetching /me:", err);
    }

    updateAuthButton();
    updateUserInfo();
    closeLoginModal();
    loadPosts();
  })
  .catch(() => alert('Login request failed'));
}


function submitSignup() {
  const base = getBaseUrl().split('/api/')[0];
  const u = document.getElementById('signup-username').value;
  const p = document.getElementById('signup-password').value;

  fetch(`${base}/api/v1/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: u, password: p })
  })
  .then(r => r.json())
  .then(d => {
    if (d.error) throw d.error;

    // Auto-login after signup
    return fetch(`${base}/api/v2/me`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: u, password: p })
    });
  })
  .then(r => r.json())
  .then(async d => {
    if (!d.token) throw new Error("Login failed");

    saveToken(d.token);
    localStorage.setItem('username', u);

    // ✅ Fetch is_admin info for signup flow too
    try {
      const res = await fetch(`${base}/api/v1/me`, {
        headers: { 'Authorization': `Bearer ${d.token}` }
      });

      if (res.ok) {
        const user = await res.json();
        if (user?.is_admin) {
          localStorage.setItem('isAdmin', 'true');
        } else {
          localStorage.removeItem('isAdmin');
        }
      } else {
        console.warn("Warning: Failed to fetch /me after signup. Status:", res.status);
      }
    } catch (err) {
      console.warn("Warning: Error fetching /me after signup:", err);
    }

    updateAuthButton();
    updateUserInfo();
    closeSignupModal();
    loadPosts();
  })
  .catch(e => alert('Signup/Login error: ' + e));
}


function updateAuthButton() {
  document.getElementById('auth-button').textContent =
    getToken() ? 'Logout' : 'Login';
}

function clearToken() {
  localStorage.removeItem('authToken');
  localStorage.removeItem('username');
  localStorage.removeItem('isAdmin');
}

function handleAuthClick() {
  if (getToken()) {
    clearToken();                // ✅ clears auth, username, admin
    updateAuthButton();
    updateUserInfo();
    loadPosts();
  } else {
    openLoginModal();           // Show login modal if not logged in
  }
}
function updateUserInfo() {
  const u = localStorage.getItem('username');
  document.getElementById('user-info')
    .textContent = u?`Welcome, ${u}!`:'';
}

/* ==========================================================================
   MODAL HELPERS
   ========================================================================== */
function openLoginModal()  { document.getElementById('login-modal').classList.remove('hidden'); }
function closeLoginModal() { document.getElementById('login-modal').classList.add('hidden'); }
function openSignupModal(){ document.getElementById('signup-modal').classList.remove('hidden'); }
function closeSignupModal(){ document.getElementById('signup-modal').classList.add('hidden'); }
/**
 * Opens the Add Post modal, or the Login modal if no user is signed in.
 */
function openAddModal() {
  // If not logged in, prompt login instead
  if (!localStorage.getItem('authToken')) {
    openLoginModal();
    return;
  }

  // Clear the form fields
  document.getElementById('add-title').value = '';
  document.getElementById('add-content').value = '';
  const dropdown = document.getElementById('add-category');
  dropdown.innerHTML = '<option value="">Select Category</option>';
  categories.forEach(cat => {
    const option = new Option(cat, cat);
    dropdown.appendChild(option);
  });

  // Show the Add Post modal
  document.getElementById('add-modal').classList.remove('hidden');
}
function closeAddModal()  { document.getElementById('add-modal').classList.add('hidden'); }
function openEditModal(post){
  postToEditId=post.id;
  document.getElementById('edit-title').value=post.title;
  document.getElementById('edit-content').value=post.content;
  const dd=document.getElementById('edit-category');
  dd.innerHTML='<option value="">Select Category</option>';
  categories.forEach(cat=>{
    const o=new Option(cat,cat);
    if(cat.toLowerCase()===post.category.toLowerCase())o.selected=true;
    dd.appendChild(o);
  });
  document.getElementById('update-modal').classList.remove('hidden');
}
function closeModal(){ document.getElementById('update-modal').classList.add('hidden'); }

// wire up buttons
document.getElementById('auth-button').onclick = handleAuthClick;
document.getElementById('add-save-btn')?.addEventListener('click', submitAdd);
document.getElementById('edit-save-btn')?.addEventListener('click', submitUpdate);
