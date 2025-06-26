# The Quiet Almanac — Notes on the Miraculous Ordinary

![Banner](frontend/static/images/almanac.png)

**A study project exploring multilingual content, AI moderation, and expressive interfaces for microblogging.**

---

## 🚀 Features

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
- 🤖 Comparison of **OpenAI GPT-4o Mini** AI translations vs. **Google Translate Widget**  
- ⚠️ **AI-based moderation** for user-submitted content  
- 🎵 **Text-to-speech (TTS)** reading powered by **Hume AI** (limited to 1 demo per user)  
- 🌍 **Multilingual Support** via AI and Google Translate Widget  

### 💡 Frontend (Static SPA)
- Fully translated UI (EN, DE, FR, ES)
- Responsive layout, built with TailwindCSS
- Modals for login, signup, and post editing
- Dynamic category filtering and comment toggling

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

```bash
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
```

## Setup & Run Locally

git clone git@github.com:MartinEnke/Masterblog_API.git
cd Masterblog_API

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r backend/requirements.txt

cd backend
python backend_app.py


## 💡 Possible Extensions
Use a persistent database like SQLite or PostgreSQL

Add user avatars or profile pages

Enable email verification

Expand moderation to include image uploads

## 🎓 Study Goals
This is a study project built to explore:

Translation quality: OpenAI vs. Google

How LLMs moderate user content

Frontend UX design for AI-assisted blogging

Limits and patterns of API consumption

## ⚠️ Disclaimers
The "Upgrade required" message for TTS is not a real upsell — the project is strictly for testing usage limits.

No real payment or premium functionality exists.

Emails are sent only for user-supplied addresses and only for comment/like notifications.

## 🙌 Contributions
Pull requests and forks are welcome!

If you're exploring:

AI translations

LLM moderation

Hume voice synthesis

User-controlled multilingual blogging

...you might enjoy contributing.

Created by me as part of Masterschool Backend / AI Engineering Bootcamp.

