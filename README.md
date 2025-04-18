# 📝 The Quiet Almanac – Flask Blog API & Frontend

**The Quiet Almanac** is a minimal, versioned blog platform built with Flask, allowing users to create, edit, delete, search, and like blog posts. Users can also leave comments — even anonymously — and enjoy a clean, responsive UI built with vanilla HTML, CSS, and JavaScript.

---

## 🚀 Features

### 🔧 Backend (Flask API)

- Versioned API (v1 & v2)
- Token-based authentication (lightweight session-style)
- User registration & login
- Create, update, delete blog posts
- Like blog posts
- Add and view comments
- Search & filter by category, author, etc.
- Swagger UI (`/apidocs`) via [Flasgger](https://github.com/flasgger/flasgger)
- Rate limiting via Flask-Limiter
- JSON file-based storage (no SQL required)

### 💡 Frontend (Static SPA)

- Clean, mobile-friendly design (Poppins font + custom CSS)
- Post listing, filtering, sorting, search
- Auth modals for login, signup, and logout
- Inline post creation, editing & deletion
- Live comment section (toggleable, scroll-friendly)
- Fully dynamic with `fetch()` API calls

---

## 📁 Folder Structure

project-root/ │ ├── static/ # All frontend assets │ ├── main.js # Frontend logic (JS) │ ├── styles.css # All styles │ └── images/ # Optional images like logo/banner │ ├── blog_posts.json # Main data file for blog posts ├── users.json # JSON-based user auth ├── backend_app.py # Flask app with v1 routes ├── v2_routes.py # Modular blueprint for /api/v2 ├── auth.py # Token auth + user system ├── utils.py # Shared helpers (validation, load/save, etc.) ├── rate_limit.py # Flask-Limiter instance ├── templates/ # (optional) Flask HTML templates └── README.md # This file
---

## 🔐 Authentication

This project uses **simple token-based auth** (your token is your username). After logging in:

- Token is stored in `localStorage`
- Sent automatically via `Authorization` header
- Used to protect POST, PUT, DELETE routes
- Stored in-memory in `TOKENS` (no JWT yet)

---

## 🧪 API Overview

- `GET /api/v2/posts`: Fetch all posts (filter/sort options)
- `POST /api/v2/posts`: Create a post *(auth required)*
- `PUT /api/v2/posts/<id>`: Update post *(auth + ownership)*
- `DELETE /api/v2/posts/<id>`: Delete post *(auth + ownership)*
- `POST /api/v2/posts/<id>/like`: Like a post
- `GET /api/v2/posts/search?q=...`: Search posts
- `GET /api/v2/categories`: List all used categories
- `POST /api/v2/register`: Register a new user
- `POST /api/v2/login`: Login (returns token)
- `GET /api/v2/secret`: Auth test route
- `POST /api/v2/posts/<id>/comments`: Add comment

👉 Full Swagger docs available at: `http://127.0.0.1:5021/apidocs`

---

## 🛠️ Setup & Run Locally

### 1. Clone the repo

git clone git@github.com:MartinEnke/Masterblog_API.git
cd Masterblog_API


### 2. Create virtual environment

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows


### 3. Install dependencies

pip install -r requirements.txt


### 4. Run the server

python backend_app.py

By default, the app runs at: http://127.0.0.1:5021


### 5. Open the frontend

Just open index.html in your browser (from /static folder) or serve via Flask if preferred.


### 💡 Ideas to Extend
JWT-based auth or OAuth login

Add pagination to comments

Upload cover images for posts

Use SQLite or PostgreSQL instead of JSON

Add email validation & password hashing


#### Author
Martin Enke


#### License
MIT License – Use freely and make something beautiful.