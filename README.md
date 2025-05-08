# 📝 The Quiet Almanac – Flask Blog API & Frontend

A Flask-based, versioned blog platform featuring a RESTful API and a fully responsive UI built with plain HTML, CSS, and JavaScript.

![Banner](frontend/static/images/almanac.png)

---

## 🚀 Features

### 🔧 Backend (Flask API)

- Versioned API (**v1** & **v2**)
- **JWT‑based authentication**  
  - Login issues a signed JSON Web Token  
  - Tokens stored in `localStorage` and sent in `Authorization: Bearer <token>` headers  
  - Protects all write routes (POST, PUT, DELETE)  
- User registration & login  
- Create, update, delete blog posts (ownership enforced)  
- Like blog posts  
- Add and view comments  
- Search & filter by category, author, etc.  
- **CORS** configured to allow your SPA origin  
- Swagger UI (`/apidocs`) via [Flasgger](https://github.com/flasgger/flasgger)  
- Rate limiting via Flask-Limiter  
- JSON file–based storage (no SQL required)

### 💡 Frontend (Static SPA)

- Clean, mobile‑friendly design (Poppins font + custom CSS)  
- Post listing, filtering, sorting, search  
- Auth modals for login, signup, and logout  
- Inline post creation, editing & deletion  
- Live comment section (toggleable, scroll‑friendly)  
- Fully dynamic with `fetch()` API calls  
- **Configurable API URL** via an editable text field (for Codio or localhost)

---



## 📁 Folder Structure
```
/Masterblog_API
├─ backend/
│ ├─ auth.py # JWT auth & user system
│ ├─ backend_app.py # Flask app (serves SPA + API)
│ ├─ v2_routes.py # Blueprint for /api/v2
│ ├─ rate_limit.py # Flask-Limiter instance
│ ├─ utils.py # Shared helpers (validation, load/save)
│ ├─ blog_posts.json # JSON data file for posts
│ ├─ users.json # JSON data file for users
│ └─ requirements.txt
└─ frontend/
├─ index.html # SPA entrypoint
├─ static/
│ ├─ main.js # Frontend logic (JS)
│ ├─ styles.css # All styles
│ └─ images/ # Logo/banner
└─ templates/ # (optional) Jinja templates
```

---

## 🔐 Authentication

We use **JWT tokens** for authentication:

1. **Register** → POST `/api/v2/register`  
2. **Login** → POST `/api/v2/login`  
   - Returns `{ message: "Login successful", token: "<JWT>" }`  
3. Frontend stores the token in `localStorage` under `authToken`  
4. All modifying requests include `Authorization: Bearer <token>`  
5. Ownership is enforced in update/delete routes  
6. Test your token at GET `/api/v2/secret` with the same header  

---

## 🧪 API Overview

<details>
<summary>Click to expand</summary>

```shell
GET    /api/v2/posts                   # List posts (filter, sort, paginate)
POST   /api/v2/posts                   # Create a post            (auth)
PUT    /api/v2/posts/<id>              # Update a post            (auth, owner)
DELETE /api/v2/posts/<id>              # Delete a post            (auth, owner)
POST   /api/v2/posts/<id>/like         # Like a post
GET    /api/v2/posts/search?q=...      # Search posts by keyword
GET    /api/v2/categories              # List all categories

POST   /api/v2/register                # Register new user
POST   /api/v2/login                   # Login → returns JWT
GET    /api/v2/secret                  # Auth test route          (auth)
POST   /api/v2/posts/<id>/comments     # Add a comment

👉 Full Swagger docs available at: `http://127.0.0.1:5021/apidocs`

---

🛠️ Setup & Run Locally
1. Clone the repo
bash
Copy
Edit
git clone git@github.com:MartinEnke/Masterblog_API.git
cd Masterblog_API

2. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3. Install dependencies
pip install -r backend/requirements.txt

4. Run the combined server (API + Frontend)
cd backend
python backend_app.py
By default, Flask listens on port 5021

Visit your SPA & API from one origin:
http://127.0.0.1:5021/
All static files are served under /static/...

Your API lives under /api/v1/... and /api/v2/...

💻 Running in Codio
Codio maps your local ports to predictable URLs:
Backend (Flask) → run in backend/:

python backend_app.py
→ exposed on port 5002 → API at
https://<workspace>-5002.codio.io/api/v2/posts

Frontend (static SPA) → run in frontend/:

python3 -m http.server 5001
→ exposed on port 5001 → UI at
https://<workspace>-5001.codio.io/

In your blog UI, edit the API URL text field at top to:

https://<workspace>-5002.codio.io/api/v2
Then click Load Posts and everything just works—no hard‑coded ports.


💡 Possible Extensions
Use a persistent database (SQLite/PostgreSQL)

Add image uploads for posts

Implement password hashing & email verification

Enhance comments with threaded replies

Add real JWT expiration handling & token refresh

Author
Martin Enke

License
MIT
