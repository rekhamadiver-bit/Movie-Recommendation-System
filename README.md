# 🎬 AI Movie Recommendation & Ticket Booking System

An AI and Machine Learning based web application for movie recommendation and online ticket booking.

## 📌 Project Overview

The Movie Recommendation and Ticket Booking System combines Artificial Intelligence, Machine Learning and web development.

The system recommends movies based on movie genre, language and description using a content-based recommendation approach.

Users can search movies, filter movies by language, get AI-based recommendations, add movies to favorites and book movie tickets.

## 🚀 Features

- 🔐 User Login and Logout
- 🎬 Movie Listing
- 🔎 Movie Search
- 🌐 Language Filtering
- ⭐ Movie Ratings
- 🤖 AI Movie Recommendation
- ❤️ Favorites
- 🎟️ Movie Ticket Booking
- 💺 Seat Selection
- 🚫 Seat Availability Checking
- 🎫 Digital Movie Ticket
- 📋 My Bookings
- ❌ Cancel Ticket
- 👨‍💼 Admin Dashboard
- ➕ Add Movie
- ✏️ Edit Movie
- 🗑️ Delete Movie
- 📊 Booking and Sales Information

## 🤖 Machine Learning

The recommendation system uses a **Content-Based Filtering** approach.

### Technologies used for recommendation:

- TF-IDF Vectorization
- Cosine Similarity
- Pandas
- Scikit-learn

Movie information such as:

- Genre
- Language
- Description

is combined into text and converted into numerical vectors using TF-IDF.

Cosine similarity is then used to find movies that are similar to the selected movie.

### Recommendation Flow

```text
Movie Information
       ↓
Genre + Language + Description
       ↓
TF-IDF Vectorization
       ↓
Cosine Similarity
       ↓
Find Similar Movies
       ↓
Top Recommended Movies
## 🛠️ Technologies Used

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- Flask

### Machine Learning

- Pandas
- NumPy
- Scikit-learn
- TF-IDF
- Cosine Similarity

### Database

- SQLite

## 📁 Project Structure

```text
Movie-Recommendation-System/
│
├── static/
│   ├── booking.css
│   ├── script.js
│   └── style.css
│
├── templates/
│   ├── booking.html
│   ├── bookings.html
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   └── ticket.html
│
├── .gitignore
├── app.py
├── main.py
└── requirements.txt
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SavitriSN123/Movie-Recommendation-System.git
```

### 2. Open the Project in PyCharm

Open the cloned `Movie-Recommendation-System` folder in PyCharm.

### 3. Create Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate Virtual Environment

For Windows:

```bash
.venv\Scripts\activate
```

### 5. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

```text
http://127.0.0.1:5000
```

## 👤 Demo Login

### Admin

```text
Username: admin
Password: 1234
```

### User

```text
Username: user
Password: 1234
```

## 🎟️ Ticket Booking

Users can:

1. Select a movie
2. Select theatre
3. Select date
4. Select show time
5. Select available seats
6. Confirm the booking
7. View the digital ticket
8. Cancel the ticket

### Ticket Price

**₹180 per seat**

## 📊 Database

SQLite is used to store:

- Users
- Movies
- Favorites
- Bookings

## 🔮 Future Enhancements

- Collaborative Filtering
- Hybrid Recommendation System
- Online Payment Gateway
- Real-Time Theatre Data
- Movie Reviews and Ratings
- Larger Movie Dataset
- Cloud Deployment
- Mobile Application

## 👨‍💻 Project Type

**AI & Machine Learning Mini Project**

## 📚 Key Concepts Demonstrated

- Python Programming
- Flask Web Development
- Machine Learning
- Content-Based Recommendation
- TF-IDF Vectorization
- Cosine Similarity
- SQLite Database
- REST APIs
- HTML/CSS/JavaScript
- CRUD Operations
- User Authentication
