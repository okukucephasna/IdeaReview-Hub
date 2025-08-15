# Flask + PyMySQL + React Fullstack App

This is a **fullstack web application** built with:

* **Backend:** Flask (Python) + PyMySQL for MySQL database connection
* **Frontend:** React (served through Flask after build)
* **Database:** MySQL

It includes:

* API routes for backend operations
* React frontend for the user interface
* A unified `app.py` that runs both the API and serves the built frontend

---

## 🚀 Features

* Flask REST API with JSON responses
* MySQL database connection via PyMySQL (`db.py`)
* React frontend served directly from Flask
* Single deployment point (no need to run two separate servers in production)
* Configurable via `.env` file

---

## 📂 Project Structure

```
project/
│
├── backend/
│   ├── app.py          # Main Flask application
│   ├── db.py           # Database connection config
│   ├── routes.py       # API endpoints
│   ├── requirements.txt# Python dependencies
│
├── frontend/
│   ├── public/         # Public assets
│   ├── src/            # React components
│   ├── package.json    # React dependencies
│
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/project-name.git
cd project-name
```

### 2️⃣ Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3️⃣ Configure MySQL Database

* Create a `.env` file inside `backend/`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=mydatabase
```

* Make sure your MySQL server is running and the database exists.

### 4️⃣ Install Frontend Dependencies

```bash
cd ../frontend
npm install
```

### 5️⃣ Build the Frontend

```bash
npm run build
```

This creates a `build/` folder that Flask will serve.

### 6️⃣ Run the Application

```bash
cd ../backend
python app.py
```

The app will be available at:

```
http://localhost:5000
```

---

## 🛠 Development Mode

If you want hot reloading for React and Flask:

* Run Flask:

```bash
cd backend
flask run
```

* Run React:

```bash
cd frontend
npm start
```

---

## 📦 Dependencies

### Backend:

* Flask
* flask-cors
* python-dotenv
* PyMySQL

### Frontend:

* React
* Axios
* React Router

---

## 📄 License

MIT License. Free to use, modify, and distribute.
