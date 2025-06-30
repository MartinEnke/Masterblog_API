# The Quiet Almanac — Notes on the Miraculous Ordinary

![Banner](frontend/static/images/almanac.png)

**Originally a school assignment, this project was expanded to explore core concepts in full-stack development.** 
**It brings together multilingual publishing, AI integrations, and a focus on user experience.**

---

## Tech Stack & Tools

| Tool | Description |
|------|-------------|
| [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org) | **Python** — Main backend language for APIs and logic |
| [![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com) | **Flask** — Lightweight web framework for building APIs |
| [![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5) | **HTML5** — Structures the frontend UI |
| [![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS) | **CSS3** — Styles the layout and appearance |
| [![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | **JavaScript** — Adds interactivity to the UI |
| [![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwind-css&logoColor=white)](https://tailwindcss.com) | **Tailwind CSS** — Utility-first framework for styling |
| [![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)](https://platform.openai.com) | **OpenAI API** — Translates and moderates content |
| [![Hume AI](https://img.shields.io/badge/Hume_AI-FF6978?style=flat&logo=wave)](https://www.hume.ai) | **Hume AI** — Provides expressive TTS audio |
| [![Swagger UI](https://img.shields.io/badge/Swagger_UI-85EA2D?logo=swagger&logoColor=black)](https://swagger.io/tools/swagger-ui/) | **Swagger UI** — Generates live API docs |
| [![JWT](https://img.shields.io/badge/JWT-black?logo=jsonwebtokens&logoColor=white)](https://jwt.io) | **JWT** — Token-based user authentication |
| [![Flask-Limiter](https://img.shields.io/badge/Flask--Limiter-0a9396?style=flat&logo=python&logoColor=white)](https://flask-limiter.readthedocs.io/) | **Flask-Limiter** — API rate limiting to prevent spam |
| [![Flasgger](https://img.shields.io/badge/Flasgger-44A1A0?logo=flask&logoColor=white)](https://github.com/flasgger/flasgger) | **Flasgger** — Swagger integration for Flask |
| [![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html) | **SQLite** — Lightweight database for storing content |
| [![Email](https://img.shields.io/badge/Email-Notifications-blue?logo=gmail&logoColor=white)](#) | **Email Alerts** — Sends notifications for likes & comments |
| [![LocalStorage](https://img.shields.io/badge/LocalStorage-ffa500?logo=google-chrome&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) | **LocalStorage** — Persists user sessions in-browser |
| [![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)](https://git-scm.com/) | **Git** — Version control for collaboration |
| [![Markdown](https://img.shields.io/badge/Markdown-000000?logo=markdown&logoColor=white)](https://daringfireball.net/projects/markdown/) | **Markdown** — Formats this README and other docs |



 

---

## Key Highlights

These standout features demonstrate modern fullstack skills, AI integration, and user-centric design:

✅ **Multilingual AI Translations** (EN, DE, FR, ES)  
✅ **AI Moderation with OpenAI API**  
✅ **AI Text-to-Speech (TTS)** via Hume AI (1 demo per user)  
✅ **Spam/abuse prevention** (rate limiting, length filtering, OpenAI moderation)  
✅ **Secure JWT-based authentication** with role-based access  
✅ **Live email notifications** for post likes and comments  
✅ **Input sanitization** to prevent script injection  
✅ **Fully translated responsive frontend UI (Tailwind)**  
✅ **Swagger API documentation at `/apidocs`**

---

## Feature List (Ranked by Impact & Difficulty)

| Feature                        | Description                                            |
|--------------------------------|--------------------------------------------------------|
| - JWT authentication           | Auth flow using signed tokens stored in `localStorage` |
| - Blog post management         | Create, edit, delete posts (ownership enforced)        |
| - Commenting                   | Add comments under posts                               |
| -️ Like system                 | Like any post + email alerts if enabled                |
| - Search & filter              | Find posts by author, keyword, or category             |
| - Language switching           | Compare OpenAI vs. Google Translate on demand          |
| - Email notification toggle    | Per-user control                                       |
| - Rate limiting                | Flask-Limiter + moderation fallback                    |
| - Swagger API docs             | Interactive at `/apidocs`                              |
| - Caching of AI translations   | Avoid repeated token use                               |
| - Responsive Tailwind UI       | Mobile-friendly, custom dropdowns                      |
| - JSON file storage            | No external DB needed                                  |
| - TTS usage limiter            | One voice demo per user, tracked via DB flag           |

---

### 💡 Frontend (Static SPA)
- Fully translated UI (EN, DE, FR, ES)
- Responsive layout, built with TailwindCSS
- Modals for login, signup, and post editing
- Dynamic category filtering and comment toggling

---

## Authentication

We use **JWT tokens** for authentication:

1. **Register** → POST `/api/v2/register`  
2. **Login** → POST `/api/v2/login`  
   - Returns `{ message: "Login successful", token: "<JWT>" }`  
3. Frontend stores the token in `localStorage` under `authToken`  
4. All modifying requests include `Authorization: Bearer <token>`  
5. Ownership is enforced in update/delete routes  
6. Test your token at GET `/api/v2/secret` with the same header  

---

## API Overview

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


## Potential Improvements

| Idea                        | Benefit                                      |
|-----------------------------|------------------------------------------------|
| Add user profile pages      | Show user history and avatar                   |
| Enable email verification   | Confirm valid registrations                    |
| Moderate image uploads      | Extend AI moderation to visual content         |
| Threaded comment replies    | Improve engagement and conversational flow     |

---

## Study Goals

This project was designed to explore and apply real-world development patterns using modern tools:

- **AI translation quality** — Compare OpenAI GPT vs. Google Translate for multilingual support  
- **LLM-based moderation** — Use AI to detect harmful, unsafe, or toxic user content  
- **Rate limiting & abuse prevention** — Implement protection mechanisms for public endpoints  
- **Frontend UX for multilingual users** — Design a responsive, translated interface  
- **Practical AI integrations** — Apply GPT, TTS, and moderation in meaningful ways  
- **Secure authentication design** — Enforce access control using JWTs and Flask APIs  


## ⚠️ Disclaimers
The "Upgrade required" message for TTS is not a real upsell — 
the project is strictly for testing usage limits.
No real payment or premium functionality exists.

Emails are sent only for user-supplied addresses and only for comment/like notifications.

## Contributions
Pull requests and forks are welcome!

If you're exploring:
AI translations
LLM moderation
Hume voice synthesis
User-controlled multilingual blogging


Created by me.
As part of the Masterschool Backend / AI Engineering Bootcamp.
Built with love, passion and curiosity.

