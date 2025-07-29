# 🏥 Medical Document Management App

A full-stack web application for securely uploading, listing, downloading, and deleting patient PDF documents. This project is built as part of the INI8 Labs Full Stack Developer Assignment.

---

## 📦 Tech Stack

- **Frontend**: React.js, Material UI
- **Backend**: Flask (Python), SQLite
- **Auth**: JWT-based token authentication
- **File Storage**: Local disk (`uploads` folder via Docker Volume)
- **Containerization**: Docker, Docker Compose
- **Web Server**: Nginx (for React frontend)

---

## 🚀 Features

- Secure PDF Upload with Patient ID
- JWT Token Authentication
- View All Uploaded Documents
- Download or Delete Documents
- RESTful API built with Flask
- Responsive frontend built with React + MUI
- Dockerized setup for local deployment

---

## 🗂️ Folder Structure

```
.
├── backend/              # Flask backend
│   ├── app.py            # Main Flask application
│   ├── Dockerfile        # Backend Docker image
│   └── requirements.txt  # Python dependencies
│
├── frontend/             # React frontend
│   ├── src/
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   │   └── medical-bg.jpg
│   ├── Dockerfile        # Frontend Docker image
│   └── nginx.conf        # Nginx config for serving React
│
├── docker-compose.yml    # Orchestration for frontend & backend
└── README.md
```

---

## 🐳 Local Setup using Docker

### 1. Clone the repo

```bash
git clone https://github.com/your-username/medical-doc-manager.git
cd medical-doc-manager
```

### 2. Run the containers

```bash
docker compose up --build
```

- Backend: [http://localhost:5000](http://localhost:5000)
- Frontend: [http://localhost:3000](http://localhost:3000)

---

## 🧪 Run Backend Unit Tests (optional)

From the `backend/` folder:

```bash
pip install -r requirements.txt
pytest test_app.py
```

---

## 🔐 JWT Authentication (handled automatically)

- On load, frontend logs in via `/login` and stores the token.
- All requests to `/documents` APIs are authorized with this token.
- Token is passed via:
  - `Authorization: Bearer <token>` header
  - Or query param in download endpoint: `/documents/:id/download?token=<token>`

---

## 📷 UI Preview
url to for UI preview
(https://github.com/prasad1999d/patient-doc-manager/blob/main/screenshots/))

---

## 🛠️ Future Improvements

- User authentication and role management
- Cloud file storage (e.g., AWS S3)
- File preview
- Pagination and filtering
- Postgres instead of SQLite
- Production-ready backend with Gunicorn + Nginx

---

## 📄 License

This project is built for demo and evaluation purposes.

---

## 👨‍💻 Author

**Dandipadala Durgaprasad**  
Email: prasad1999dd@gmail.com  
LinkedIn: [dandipadala-durgaprasad](https://www.linkedin.com/in/dandipadala-durgaprasad-9aba22229/)
