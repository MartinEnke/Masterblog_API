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

  // Text content (e.g. spans, buttons)
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (strings[key]) el.textContent = strings[key];
  });

  // Placeholder for inputs
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (strings[key]) el.placeholder = strings[key];
  });

  // Option labels in <select> dropdowns
  document.querySelectorAll("select[data-i18n-option]").forEach(select => {
    select.querySelectorAll("option").forEach(option => {
      const key = option.getAttribute("data-i18n-option");
      if (key && strings[key]) option.textContent = strings[key];
    });
  });

  // Manually update filter-category first option if empty value
  const catSelect = document.getElementById("filter-category");
  if (catSelect && catSelect.options.length > 0) {
    const first = catSelect.options[0];
    if (first.value === "") {
      first.textContent = strings.allCategories || "All Categories";
    }
  }

  // Manually update sort-field "no sorting" option
  const sortFieldSelect = document.getElementById("sort-field");
  if (sortFieldSelect && sortFieldSelect.options.length > 0) {
    const first = sortFieldSelect.options[0];
    if (first.value === "") {
      first.textContent = strings.noSorting || "No Sorting";
    }
  }

  // Translate existing comment placeholders and buttons
  document.querySelectorAll("textarea[id^='comment-text-']").forEach(textarea => {
    textarea.placeholder = strings.commentPlaceholder || "Add a comment...";
  });
  document.querySelectorAll(".comment-section button").forEach(btn => {
    btn.textContent = strings.postComment || "Post Comment";
  });

  // Welcome message
  const username = localStorage.getItem("username");
  const userInfo = document.getElementById("user-info");
  if (username && userInfo) {
    userInfo.textContent = `${strings.welcome || "Welcome"}, ${username}!`;
  } else if (userInfo) {
    userInfo.textContent = "";
  }

  // 🔁 Also update the auth button text (Login/Logout)
  updateAuthButton();
}

/* ==========================================================================
   GOOGLE TRANSLATE ON DEMAND
   ========================================================================== */

function loadGoogleTranslate() {
  const container = document.getElementById("google_translate_element");

  if (!container) {
    console.warn("Missing #google_translate_element in DOM");
    return;
  }

  container.style.display = "block";

  // Avoid loading twice
  if (!window.google || !window.google.translate) {
    const s = document.createElement("script");
    s.src = "//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
    document.body.appendChild(s);
  } else {
    googleTranslateElementInit();
  }
}

function googleTranslateElementInit() {
  new google.translate.TranslateElement({
    pageLanguage: 'en',
    includedLanguages: 'de,fr,es',
    layout: google.translate.TranslateElement.InlineLayout.SIMPLE
  }, 'google_translate_element');
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
document.getElementById("cancel-add-btn")
    ?.addEventListener("click", () => {
      document.getElementById("add-modal").classList.add("hidden");
    });
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
  const base = getBaseUrl();
  const lang = getCurrentLanguage();
  const category = document.getElementById("filter-category")?.value || "";
  const sort = document.getElementById("sort-by")?.value || "";
  const direction = document.getElementById("sort-direction")?.value || "asc";

  const url = `${base}/posts?category=${category}&sort=${sort}&direction=${direction}&lang=${lang}`;
  console.log("🌐 Final posts URL:", url);

  fetch(url, {
    headers: {
      'Authorization': `Bearer ${getToken()}`  // ✅ Send token for accurate liked_by_current_user
    }
  })
    .then(r => r.json())
    .then(data => {
      const posts = data.posts || [];
      document.getElementById("post-container").innerHTML = "";
      posts.forEach(renderSinglePost);
    })
    .catch(e => {
      console.error("Error loading posts:", e);
    });
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
    borderRadius: '8px',
    position: 'relative'
  });

  const currentLang = getCurrentLanguage();
  const isTranslatedCopy = post.translated === true && post.is_ai_translation === true;
  const isOriginalLang = post.original_lang === currentLang;

  if (isTranslatedCopy && !isOriginalLang) {
    const badge = document.createElement('div');
    badge.className = 'ai-badge';
    badge.setAttribute('data-i18n', 'aiTranslated');
    badge.textContent = UI_TRANSLATIONS[currentLang].aiTranslated || 'AI-translated';
    Object.assign(badge.style, {
      position: 'absolute',
      top: '10px',
      right: '10px',
      backgroundColor: '#e0e0e0',
      padding: '3px 8px',
      borderRadius: '5px',
      fontSize: '0.8em',
      color: '#444',
      fontStyle: 'italic'
    });
    div.appendChild(badge);
  }

  div.innerHTML += `
    <h2 id="post-title-${post.id}">${post.title}</h2>
    <p id="post-content-${post.id}">${post.content}</p>
    <p class="post-meta" data-i18n-by="${post.author}">${post.date || 'No date'} · <span data-i18n="by">by</span> ${post.author || 'Unknown'}</p>
    ${post.updated
      ? `<p style="font-size:.9em;color:#777;margin-bottom:10px" data-i18n-updated="${post.updated}">
           <span data-i18n="updatedLabel">Updated:</span> ${post.updated}
         </p>`
      : ''}
    <div class="comment-section" id="comments-${post.id}">
      <h4 data-i18n="comments">Comments</h4>
      <div id="comment-list-${post.id}"></div>
      <textarea id="comment-text-${post.id}" data-i18n-placeholder="commentPlaceholder" placeholder="Add a comment..."></textarea>
      <button data-i18n="postComment" onclick="submitComment(${post.id})">Post Comment</button>
    </div>
  `;

  const btnWrap = document.createElement('div');
  Object.assign(btnWrap.style, {
    display: 'flex',
    justifyContent: 'space-between',
    gap: '10px',
    marginTop: '10px'
  });

  // ❤️ Like button
  const likeBtn = document.createElement('button');
  likeBtn.id = `like-btn-${post.id}`;
  likeBtn.className = post.liked_by_current_user ? 'liked' : '';
  likeBtn.innerHTML = `
    <span id="like-heart-${post.id}" style="font-size: 1.2em;">${post.liked_by_current_user ? '❤️' : '🤍'}</span>
    <span id="like-count-${post.id}">${post.likes || 0}</span>
  `;
  likeBtn.onclick = () => {
    fetch(`${getBaseUrl()}/posts/${post.id}/like`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${getToken()}` }
    })
      .then(r => r.json())
      .then(d => {
        console.log("✅ Like response:", d);
        if (d.likes !== undefined && typeof d.liked_by_current_user === "boolean") {
          document.getElementById(`like-count-${post.id}`).textContent = d.likes;
          document.getElementById(`like-heart-${post.id}`).textContent = d.liked_by_current_user ? '❤️' : '🤍';
          likeBtn.className = d.liked_by_current_user ? 'liked' : '';
        }
      })
      .catch(console.error);
  };
  btnWrap.appendChild(likeBtn);

  const currentUser = localStorage.getItem('username');
  const isAdmin = localStorage.getItem('isAdmin') === 'true';

  if (post.author === currentUser || isAdmin) {
  if (isOriginalLang || isAdmin) {
    // ✅ Admins can delete in any language
    const delBtn = document.createElement('button');
    delBtn.setAttribute("data-i18n", "deletePost");
    delBtn.onclick = () => deletePost(post.id);
    delBtn.textContent = UI_TRANSLATIONS[currentLang].deletePost || 'Delete';
    btnWrap.appendChild(delBtn);
  }

  if (isOriginalLang) {
    // ✏️ Only show Edit if original language
    const editBtn = document.createElement('button');
    editBtn.setAttribute("data-i18n", "editPost");
    editBtn.onclick = () => openEditModal(post);
    editBtn.textContent = UI_TRANSLATIONS[currentLang].editPost || 'Edit';
    btnWrap.appendChild(editBtn);
  }
}

  div.appendChild(btnWrap);
  loadComments(post.id);
  container.appendChild(div);

  // 🌀 Lazy translation
  if (post.translated === false && currentLang !== "en") {
    const base = getBaseUrl();
    fetch(`${base}/posts/${post.id}/translate?lang=${currentLang}`)
      .then(r => r.json())
      .then(translated => {
        updatePostDom(post.id, translated.title, translated.content);
        post.translated = true;

        const badge = document.createElement('div');
        badge.className = 'ai-badge';
        badge.setAttribute('data-i18n', 'aiTranslated');
        badge.textContent = UI_TRANSLATIONS[currentLang].aiTranslated || 'AI-translated';
        Object.assign(badge.style, {
          position: 'absolute',
          top: '10px',
          right: '10px',
          backgroundColor: '#e0e0e0',
          padding: '3px 8px',
          borderRadius: '5px',
          fontSize: '0.8em',
          color: '#444',
          fontStyle: 'italic'
        });

        const postDiv = document.getElementById(`post-title-${post.id}`).closest('.post');
        postDiv.appendChild(badge);
      })
      .catch(err => console.warn("Translation failed for post", post.id, err));
  }
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

      // ✅ Apply after rendering
      applyUITranslations();
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
   UTILS
   ========================================================================== */

function updatePostDom(postId, newTitle, newContent) {
  const titleEl = document.getElementById(`post-title-${postId}`);
  const contentEl = document.getElementById(`post-content-${postId}`);

  if (titleEl) titleEl.textContent = newTitle;
  if (contentEl) contentEl.textContent = newContent;
}


/* ==========================================================================
   POSTS: ADD / EDIT / DELETE
   ========================================================================== */
function submitAdd() {
  const base = getBaseUrl();
  let category = document.getElementById('add-category').value;
  if (category === "custom") {
    const custom = document.getElementById('custom-category-input-add').value.trim();
    if (custom) category = custom;
  }

  const payload = {
    title:   document.getElementById('add-title').value,
    content: document.getElementById('add-content').value,
    category
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
    if (!r.ok) return r.json().then(e => Promise.reject(e.error));
    return r.json();
  })
  .then(() => {
    document.getElementById("add-modal").classList.add("hidden");
    loadPosts();
  })
  .catch(e => alert("Error: " + e));
}


function submitUpdate() {
  const base = getBaseUrl();
  let category = document.getElementById('edit-category').value;
  if (category === "custom") {
    const custom = document.getElementById('custom-category-input-edit').value.trim();
    if (custom) category = custom;
  }

  const payload = {
    title:   document.getElementById('edit-title').value,
    content: document.getElementById('edit-content').value,
    category
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
    if (!r.ok) return r.json().then(e => Promise.reject(e.error));
    return r.json();
  })
  .then(() => { closeModal(); loadPosts(); })
  .catch(e => alert("Error: " + e));
}


function deletePost(postId) {
  const base = getBaseUrl();
  const token = getToken();

  if (!token) {
    alert("You must be logged in to delete a post.");
    return;
  }

  if (!confirm("Are you sure you want to delete this post?")) return;

  fetch(`${base}/posts/${postId}`, {
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
      console.log("✅ Post deleted:", data);
      loadPosts();  // Reload post list after deletion
    })
    .catch(err => {
      console.error("❌ Delete failed:", err);
      alert("Failed to delete post.");
    });
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
  const u = document.getElementById('signup-username').value.trim();
  const p = document.getElementById('signup-password').value.trim();

  if (!u || !p) {
    alert("Username and password required.");
    return;
  }

  // 🔐 Step 1: Register
  fetch(`${base}/api/v1/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: u, password: p })
  })
  .then(async res => {
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Signup failed.");
    }

    // ✅ Step 2: Login right after successful signup
    return fetch(`${base}/api/v1/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: u, password: p })
    });
  })
  .then(r => r.json())
  .then(async d => {
    if (!d.token) throw new Error("Login after signup failed.");

    saveToken(d.token);
    localStorage.setItem('username', u);

    // 🧠 Optional: fetch admin info
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
      }
    } catch (err) {
      console.warn("Warning: Couldn't fetch /me:", err);
    }

    updateAuthButton();
    updateUserInfo();
    closeSignupModal();
    loadPosts();
  })
  .catch(e => alert("Signup error: " + e.message));
}




function updateAuthButton() {
  const btn = document.getElementById('auth-button');
  if (!btn) return;

  const token = getToken();
  const lang = getCurrentLanguage();
  const strings = UI_TRANSLATIONS[lang] || UI_TRANSLATIONS["en"];

  if (token && token.length > 10) {
    btn.textContent = strings.logout || 'Logout';
  } else {
    btn.textContent = strings.login || 'Login';
  }
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

// Translates modal text and placeholders
function translateModalPlaceholders() {
  const currentLang = getCurrentLanguage();
  const strings = UI_TRANSLATIONS[currentLang];

  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (strings?.[key]) {
      el.textContent = strings[key];
    }
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (strings?.[key]) {
      el.placeholder = strings[key];
    }
  });
}

function openLoginModal() {
  translateModalPlaceholders();
  document.getElementById('login-modal').classList.remove('hidden');
}

function closeLoginModal() {
  document.getElementById('login-modal').classList.add('hidden');
}

function openSignupModal() {
  translateModalPlaceholders();
  document.getElementById('signup-modal').classList.remove('hidden');
}

function closeSignupModal() {
  document.getElementById('signup-modal').classList.add('hidden');
}

/**
 * Opens the Add Post modal, or the Login modal if no user is signed in.
 */
function openAddModal() {
  try {
    if (!localStorage.getItem('authToken')) {
      openLoginModal();
      return;
    }

    document.getElementById('add-title').value = '';
    document.getElementById('add-content').value = '';

    const currentLang = getCurrentLanguage();
    const strings = UI_TRANSLATIONS[currentLang];
    const dropdown = document.getElementById('add-category');

    // ✅ Reset and populate category dropdown
    dropdown.innerHTML = `<option value="">${strings.selectCategory || "Select Category"}</option>`;
    categories.forEach(cat => {
      const option = new Option(cat, cat);
      dropdown.appendChild(option);
    });

    // ✅ Append custom category option last
    const customOption = new Option("➕ Enter Custom Category...", "custom");
    customOption.id = "custom-category-option";
    dropdown.appendChild(customOption);

    // ✅ Show input only if "custom" is selected
    setupCustomCategoryInput("add-category", "custom-category-wrapper-add", "custom-category-input-add");

    translateModalPlaceholders();
    document.getElementById('add-modal').classList.remove('hidden');
  } catch (err) {
    console.error("❌ Failed to open Add Post modal:", err);
  }

  updateAuthButton();
}


function openEditModal(post) {
  postToEditId = post.id;
  document.getElementById('edit-title').value = post.title;
  document.getElementById('edit-content').value = post.content;

  const currentLang = getCurrentLanguage();
  const strings = UI_TRANSLATIONS[currentLang];

  const dd = document.getElementById('edit-category');
// Append "custom" option
const customOption = new Option("➕ Enter Custom Category...", "custom");
customOption.id = "custom-category-option";
dd.appendChild(customOption);

// Enable dynamic field
setupCustomCategoryInput("edit-category", "custom-category-wrapper-edit", "custom-category-input-edit");
  dd.innerHTML = `<option value="">${strings.selectCategory || "Select Category"}</option>`;
  categories.forEach(cat => {
    const o = new Option(cat, cat);
    if (cat.toLowerCase() === post.category.toLowerCase()) o.selected = true;
    dd.appendChild(o);
  });

  translateModalPlaceholders();
  document.getElementById('update-modal').classList.remove('hidden');
  updateAuthButton();
}

function closeModal() {
  document.getElementById('update-modal').classList.add('hidden');
}

window.closeAddModal = closeAddModal;

function setupCustomCategoryInput(dropdownId, inputWrapperId, inputFieldId) {
  const dropdown = document.getElementById(dropdownId);
  const wrapper = document.getElementById(inputWrapperId);
  const input = document.getElementById(inputFieldId);

  if (!dropdown || !wrapper || !input) {
    console.warn("❌ setupCustomCategoryInput: One or more elements not found.");
    return;
  }

  dropdown.addEventListener("change", () => {
    if (dropdown.value === "custom") {
      wrapper.style.display = "block";
      input.focus();
    } else {
      wrapper.style.display = "none";
      input.value = ""; // clear old custom value
    }
  });
}

// Wire up buttons
document.getElementById('auth-button').onclick = handleAuthClick;
document.getElementById('add-save-btn')?.addEventListener('click', submitAdd);
document.getElementById('edit-save-btn')?.addEventListener('click', submitUpdate);
