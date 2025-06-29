# ForumFastAPI

A discussion forum backend built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, allowing users to register, authenticate, and participate in forum threads by posting and commenting.

---

## 📌 Features

- 🔐 **User Authentication**
  - Register and log in using JWT tokens
  - Secure password hashing
- 🧵 **Thread Management**
  - Create, view, update, and delete threads
- 💬 **Post System**
  - Add posts to threads
  - Edit or delete own posts
- 🗨️ **Commenting System**
  - Add comments to posts
  - Edit or delete own comments
- 🔗 **Relational Database**
  - One-to-many relationships between users, threads, posts, and comments
  - SQLAlchemy joins for retrieving thread content with replies and comments

---

## 🛠️ Technologies Used

- **Python 3.9+**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **JWT Authentication (PyJWT)**
- **Passlib** (bcrypt hashing)
- **Uvicorn** (for local dev server)

---

## 📂 Project Structure

```
forum-fastapi/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── auth.py
│   ├── schema.py
│   └── routes/
│       ├── users.py
│       ├── threads.py
│       ├── posts.py
│       └── comments.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/M-Adeel-aslam/forum-fastapi.git
cd forum-fastapi
```

2. **Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate 
# OR
venv\Scripts\activate.bat
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure `.env`**
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:password@localhost/forum_db
KEY=your_jwt_secret_key
ALGORITHM=HS256
EXPIRE_TOKEN_TIME=60
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

6. **Access the API Docs**
Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

---

## 🔗 API Endpoints Overview

### Auth (Public)
- `POST /register` – Register a new user
- `POST /login` – Authenticate and receive JWT

### Threads (Protected)
- `POST /threads` – Create thread
- `GET /threads` – List all threads
- `GET /threads/{id}` – View thread detail
- `PUT /threads/{id}` – Update thread
- `DELETE /threads/{id}` – Delete thread

### Posts (Protected)
- `POST /threads/{thread_id}/posts` – Add post to thread
- `GET /threads/{thread_id}/posts` – Get posts for a thread
- `PUT /posts/{id}` – Update a post
- `DELETE /posts/{id}` – Delete a post

### Comments (Protected, Optional)
- `POST /posts/{post_id}/comments` – Add comment to post
- `GET /posts/{post_id}/comments` – List comments
- `PUT /comments/{id}` – Update a comment
- `DELETE /comments/{id}` – Delete a comment

---

## ✅ Requirements

- Python 3.9 or above
- PostgreSQL installed and configured

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you would like to change.

---

## 📄 License

This project is for educational purposes only.
