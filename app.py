from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from functools import wraps
from datetime import datetime
import uuid


# ==========================================================
# FLASK APPLICATION
# ==========================================================

app = Flask(__name__)
app.secret_key = "movie_ai_booking_secret_2026"

DATABASE = "movie_booking.db"

TICKET_PRICE = 180.00

ROWS = ["A", "B", "C", "D", "E"]
SEATS_PER_ROW = 8

VALID_SEATS = {
    f"{row}{number}"
    for row in ROWS
    for number in range(1, SEATS_PER_ROW + 1)
}

TOTAL_SEATS = len(VALID_SEATS)


# ==========================================================
# MOVIES
# ==========================================================

movies = [

    # ======================================================
    # KANNADA - 20 MOVIES
    # ======================================================

    {
        "name": "KGF",
        "genre": "Action",
        "language": "Kannada",
        "rating": 8.5,
        "description": "Action crime drama about Rocky and his journey to become a powerful leader."
    },
    {
        "name": "Kantara",
        "genre": "Action",
        "language": "Kannada",
        "rating": 9.0,
        "description": "Action thriller with village culture tradition mythology and powerful characters."
    },
    {
        "name": "777 Charlie",
        "genre": "Adventure",
        "language": "Kannada",
        "rating": 8.8,
        "description": "Adventure drama about a lonely man and his emotional journey with a dog."
    },
    {
        "name": "Kirik Party",
        "genre": "Comedy",
        "language": "Kannada",
        "rating": 8.0,
        "description": "College comedy drama about friendship love and student life."
    },
    {
        "name": "Ugramm",
        "genre": "Action",
        "language": "Kannada",
        "rating": 8.0,
        "description": "Action crime drama involving friendship revenge violence and gangsters."
    },
    {
        "name": "Lucia",
        "genre": "Thriller",
        "language": "Kannada",
        "rating": 8.3,
        "description": "Psychological thriller involving dreams reality and mysterious events."
    },
    {
        "name": "Rangitaranga",
        "genre": "Mystery",
        "language": "Kannada",
        "rating": 8.2,
        "description": "Mystery thriller involving family secrets village mystery and supernatural events."
    },
    {
        "name": "Avane Srimannarayana",
        "genre": "Adventure",
        "language": "Kannada",
        "rating": 7.8,
        "description": "Adventure comedy involving treasure police investigation and action."
    },
    {
        "name": "Dia",
        "genre": "Romance",
        "language": "Kannada",
        "rating": 8.0,
        "description": "Romantic emotional drama about love relationships and life."
    },
    {
        "name": "Gaalipata",
        "genre": "Comedy",
        "language": "Kannada",
        "rating": 8.1,
        "description": "Comedy romance about friendship love and memorable journeys."
    },
    {
        "name": "Mungaru Male",
        "genre": "Romance",
        "language": "Kannada",
        "rating": 8.3,
        "description": "Romantic drama involving love emotions friendship and beautiful relationships."
    },
    {
        "name": "Kavaludaari",
        "genre": "Mystery",
        "language": "Kannada",
        "rating": 8.0,
        "description": "Mystery crime thriller involving police investigation and an old case."
    },
    {
        "name": "Operation Alamelamma",
        "genre": "Comedy",
        "language": "Kannada",
        "rating": 7.8,
        "description": "Comedy crime story involving kidnapping mystery and unexpected situations."
    },
    {
        "name": "Bell Bottom",
        "genre": "Crime",
        "language": "Kannada",
        "rating": 8.0,
        "description": "Crime comedy mystery about a detective investigating unusual cases."
    },
    {
        "name": "Mufti",
        "genre": "Action",
        "language": "Kannada",
        "rating": 8.0,
        "description": "Action crime drama involving an undercover police officer and a powerful gangster."
    },
    {
        "name": "Tagaru",
        "genre": "Action",
        "language": "Kannada",
        "rating": 8.0,
        "description": "Action crime movie involving police officers criminals and gang conflicts."
    },
    {
        "name": "Garuda Gamana Vrishabha Vahana",
        "genre": "Crime",
        "language": "Kannada",
        "rating": 8.6,
        "description": "Crime drama about friendship power violence and relationships."
    },
    {
        "name": "Sarkari Hi. Pra. Shaale Kasaragodu",
        "genre": "Comedy",
        "language": "Kannada",
        "rating": 8.1,
        "description": "Comedy drama about students teachers education and village life."
    },
    {
        "name": "Godhi Banna Sadharana Mykattu",
        "genre": "Drama",
        "language": "Kannada",
        "rating": 8.3,
        "description": "Emotional family drama involving memory relationships and father son bonding."
    },
    {
        "name": "Ulidavaru Kandanthe",
        "genre": "Crime",
        "language": "Kannada",
        "rating": 8.4,
        "description": "Crime mystery drama told through different perspectives involving fishermen and criminals."
    },


    # ======================================================
    # HINDI - 20 MOVIES
    # ======================================================

    {
        "name": "3 Idiots",
        "genre": "Comedy",
        "language": "Hindi",
        "rating": 8.4,
        "description": "Comedy drama about college friendship education dreams and engineering students."
    },
    {
        "name": "Dangal",
        "genre": "Sports",
        "language": "Hindi",
        "rating": 8.3,
        "description": "Sports drama about wrestling family motivation training and determination."
    },
    {
        "name": "PK",
        "genre": "Comedy",
        "language": "Hindi",
        "rating": 8.1,
        "description": "Comedy drama about an unusual character questioning society religion and human behavior."
    },
    {
        "name": "Drishyam",
        "genre": "Thriller",
        "language": "Hindi",
        "rating": 8.2,
        "description": "Crime thriller about family protection investigation secrets and intelligence."
    },
    {
        "name": "Taare Zameen Par",
        "genre": "Drama",
        "language": "Hindi",
        "rating": 8.3,
        "description": "Emotional drama about a child education creativity family and teacher support."
    },
    {
        "name": "Zindagi Na Milegi Dobara",
        "genre": "Adventure",
        "language": "Hindi",
        "rating": 8.2,
        "description": "Adventure comedy drama about friendship travel life experiences and personal growth."
    },
    {
        "name": "Lagaan",
        "genre": "Sports",
        "language": "Hindi",
        "rating": 8.1,
        "description": "Sports historical drama about cricket villagers teamwork courage and freedom."
    },
    {
        "name": "Sholay",
        "genre": "Action",
        "language": "Hindi",
        "rating": 8.1,
        "description": "Classic action adventure drama involving friendship revenge and a dangerous criminal."
    },
    {
        "name": "Andhadhun",
        "genre": "Thriller",
        "language": "Hindi",
        "rating": 8.2,
        "description": "Crime thriller involving mystery deception music and unexpected twists."
    },
    {
        "name": "Queen",
        "genre": "Comedy",
        "language": "Hindi",
        "rating": 8.1,
        "description": "Comedy drama about self discovery independence friendship and travel."
    },
    {
        "name": "Barfi",
        "genre": "Romance",
        "language": "Hindi",
        "rating": 8.1,
        "description": "Romantic comedy drama about love friendship emotions and relationships."
    },
    {
        "name": "Yeh Jawaani Hai Deewani",
        "genre": "Romance",
        "language": "Hindi",
        "rating": 7.2,
        "description": "Romantic drama about friendship travel love ambition and relationships."
    },
    {
        "name": "Gully Boy",
        "genre": "Drama",
        "language": "Hindi",
        "rating": 7.9,
        "description": "Drama about music rap dreams friendship family and overcoming difficulties."
    },
    {
        "name": "Article 15",
        "genre": "Crime",
        "language": "Hindi",
        "rating": 8.1,
        "description": "Crime social drama about police investigation justice and social issues."
    },
    {
        "name": "Chak De India",
        "genre": "Sports",
        "language": "Hindi",
        "rating": 8.1,
        "description": "Sports drama about hockey teamwork leadership motivation and national pride."
    },
    {
        "name": "Swades",
        "genre": "Drama",
        "language": "Hindi",
        "rating": 8.2,
        "description": "Drama about education village development social responsibility and returning home."
    },
    {
        "name": "Rang De Basanti",
        "genre": "Drama",
        "language": "Hindi",
        "rating": 8.1,
        "description": "Drama about friendship patriotism youth and social change."
    },
    {
        "name": "Kahaani",
        "genre": "Mystery",
        "language": "Hindi",
        "rating": 8.1,
        "description": "Mystery thriller about investigation identity secrets and unexpected twists."
    },
    {
        "name": "Bhaag Milkha Bhaag",
        "genre": "Sports",
        "language": "Hindi",
        "rating": 8.2,
        "description": "Sports biographical drama about running training determination and success."
    },
    {
        "name": "Dil Chahta Hai",
        "genre": "Comedy",
        "language": "Hindi",
        "rating": 8.1,
        "description": "Comedy drama about friendship relationships travel and young adult life."
    },


    # ======================================================
    # ENGLISH - 20 MOVIES
    # ======================================================

    {
        "name": "Interstellar",
        "genre": "Science Fiction",
        "language": "English",
        "rating": 8.7,
        "description": "Science fiction adventure about space travel time relativity family and survival."
    },
    {
        "name": "Inception",
        "genre": "Science Fiction",
        "language": "English",
        "rating": 8.8,
        "description": "Science fiction thriller about dreams technology mystery and mind manipulation."
    },
    {
        "name": "Avengers Endgame",
        "genre": "Action",
        "language": "English",
        "rating": 8.4,
        "description": "Action superhero adventure about heroes friendship sacrifice and saving the world."
    },
    {
        "name": "The Dark Knight",
        "genre": "Action",
        "language": "English",
        "rating": 9.0,
        "description": "Action crime thriller about Batman criminals justice and an iconic villain."
    },
    {
        "name": "Titanic",
        "genre": "Romance",
        "language": "English",
        "rating": 7.9,
        "description": "Romantic drama about love relationships and survival aboard a famous ship."
    },
    {
        "name": "Avatar",
        "genre": "Science Fiction",
        "language": "English",
        "rating": 7.8,
        "description": "Science fiction adventure about another planet nature technology and human conflict."
    },
    {
        "name": "The Matrix",
        "genre": "Science Fiction",
        "language": "English",
        "rating": 8.7,
        "description": "Science fiction action movie about artificial reality technology and freedom."
    },
    {
        "name": "Gladiator",
        "genre": "Action",
        "language": "English",
        "rating": 8.5,
        "description": "Historical action drama about a warrior revenge courage and leadership."
    },
    {
        "name": "Forrest Gump",
        "genre": "Drama",
        "language": "English",
        "rating": 8.8,
        "description": "Drama about life friendship love family and an extraordinary journey."
    },
    {
        "name": "The Shawshank Redemption",
        "genre": "Drama",
        "language": "English",
        "rating": 9.3,
        "description": "Drama about prison friendship hope freedom and determination."
    },
    {
        "name": "The Lord of the Rings",
        "genre": "Fantasy",
        "language": "English",
        "rating": 8.8,
        "description": "Fantasy adventure about friendship heroes magic battles and saving the world."
    },
    {
        "name": "Jurassic Park",
        "genre": "Adventure",
        "language": "English",
        "rating": 8.2,
        "description": "Adventure science fiction movie about dinosaurs science survival and a mysterious park."
    },
    {
        "name": "Iron Man",
        "genre": "Action",
        "language": "English",
        "rating": 7.9,
        "description": "Superhero action movie about technology invention friendship and fighting criminals."
    },
    {
        "name": "Spider-Man No Way Home",
        "genre": "Action",
        "language": "English",
        "rating": 8.2,
        "description": "Superhero action adventure about friendship multiverse responsibility and sacrifice."
    },
    {
        "name": "The Prestige",
        "genre": "Mystery",
        "language": "English",
        "rating": 8.5,
        "description": "Mystery thriller about magic rivalry secrets science and unexpected twists."
    },
    {
        "name": "Whiplash",
        "genre": "Drama",
        "language": "English",
        "rating": 8.5,
        "description": "Drama about music ambition training competition and achieving excellence."
    },
    {
        "name": "The Martian",
        "genre": "Science Fiction",
        "language": "English",
        "rating": 8.0,
        "description": "Science fiction survival adventure about an astronaut stranded on Mars."
    },
    {
        "name": "Gravity",
        "genre": "Science Fiction",
        "language": "English",
        "rating": 7.7,
        "description": "Science fiction survival thriller about astronauts space and survival."
    },
    {
        "name": "Toy Story",
        "genre": "Animation",
        "language": "English",
        "rating": 8.3,
        "description": "Animated adventure comedy about friendship toys family and childhood."
    },
    {
        "name": "Finding Nemo",
        "genre": "Animation",
        "language": "English",
        "rating": 8.2,
        "description": "Animated adventure about family friendship ocean exploration and finding a lost child."
    }
]


# ==========================================================
# DATABASE
# ==========================================================

def get_db():

    connection = sqlite3.connect(
        DATABASE,
        timeout=10
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_db()

    cursor = connection.cursor()

    # ------------------------------------------------------
    # USERS
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)

    # ------------------------------------------------------
    # MOVIES
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            genre TEXT NOT NULL,
            language TEXT NOT NULL,
            rating REAL NOT NULL,
            description TEXT NOT NULL
        )
    """)

    # ------------------------------------------------------
    # BOOKINGS
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_code TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            movie_name TEXT NOT NULL,
            theatre TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            show_time TEXT NOT NULL,
            seats TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            total REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # ------------------------------------------------------
    # FAVORITES
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            movie_name TEXT NOT NULL,
            UNIQUE(username, movie_name)
        )
    """)

    # ------------------------------------------------------
    # DEFAULT ADMIN
    # ------------------------------------------------------

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password, role)
        VALUES (?, ?, ?)
    """, (
        "admin",
        "1234",
        "admin"
    ))

    # ------------------------------------------------------
    # DEFAULT USER
    # ------------------------------------------------------

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password, role)
        VALUES (?, ?, ?)
    """, (
        "user",
        "1234",
        "user"
    ))

    # ------------------------------------------------------
    # INSERT MOVIES
    # ------------------------------------------------------

    movie_count = cursor.execute("""
        SELECT COUNT(*)
        FROM movies
    """).fetchone()[0]

    if movie_count == 0:

        for movie in movies:

            cursor.execute("""
                INSERT INTO movies
                (
                    name,
                    genre,
                    language,
                    rating,
                    description
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                movie["name"],
                movie["genre"],
                movie["language"],
                movie["rating"],
                movie["description"]
            ))

    connection.commit()

    connection.close()


init_database()


# ==========================================================
# MOVIE FUNCTIONS
# ==========================================================

def load_movies():

    connection = get_db()

    rows = connection.execute("""
        SELECT *
        FROM movies
        ORDER BY id
    """).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


def get_dataframe():

    return pd.DataFrame(
        load_movies()
    )


df = get_dataframe()


# ==========================================================
# AI MODEL
# ==========================================================

def create_model():

    global df

    if df.empty:

        return None, None

    df["features"] = (
        df["genre"].astype(str)
        + " "
        + df["language"].astype(str)
        + " "
        + df["description"].astype(str)
    )

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(
        df["features"]
    )

    similarity = cosine_similarity(
        matrix
    )

    return vectorizer, similarity


vectorizer, similarity_matrix = create_model()


def rebuild_model():

    global df
    global vectorizer
    global similarity_matrix

    df = get_dataframe()

    vectorizer, similarity_matrix = create_model()


def recommend_movies(
    movie_name,
    number=5
):

    if (
        df.empty
        or similarity_matrix is None
    ):
        return []

    matches = df[
        df["name"].str.lower()
        == movie_name.strip().lower()
    ]

    if matches.empty:

        return []

    index = matches.index[0]

    scores = list(
        enumerate(
            similarity_matrix[index]
        )
    )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    result = []

    for movie_index, score in scores:

        if movie_index == index:
            continue

        movie = df.iloc[
            movie_index
        ]

        result.append({

            "id":
                int(movie["id"]),

            "name":
                movie["name"],

            "genre":
                movie["genre"],

            "language":
                movie["language"],

            "rating":
                float(movie["rating"]),

            "description":
                movie["description"],

            "similarity":
                round(
                    float(score) * 100,
                    2
                )
        })

        if len(result) >= number:

            break

    return result


# ==========================================================
# LOGIN REQUIRED
# ==========================================================

def login_required(function):

    @wraps(function)
    def wrapper(
        *args,
        **kwargs
    ):

        if "username" not in session:

            return redirect(
                url_for("login")
            )

        return function(
            *args,
            **kwargs
        )

    return wrapper


# ==========================================================
# ADMIN REQUIRED
# ==========================================================

def admin_required(function):

    @wraps(function)
    def wrapper(
        *args,
        **kwargs
    ):

        if "username" not in session:

            return redirect(
                url_for("login")
            )

        if session.get("role") != "admin":

            return jsonify({

                "success": False,

                "message":
                    "Admin access required"

            }), 403

        return function(
            *args,
            **kwargs
        )

    return wrapper


# ==========================================================
# LOGIN
# ==========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        connection = get_db()

        user = connection.execute("""
            SELECT *
            FROM users
            WHERE username = ?
            AND password = ?
        """, (
            username,
            password
        )).fetchone()

        connection.close()

        if user:

            session["username"] = (
                user["username"]
            )

            session["role"] = (
                user["role"]
            )

            return redirect(
                url_for("home")
            )

        return render_template(
            "login.html",
            error=
                "Invalid username or password"
        )

    return render_template(
        "login.html"
    )


# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
@login_required
def home():

    movie_list = load_movies()

    return render_template(
        "index.html",
        movies=movie_list,
        username=session.get(
            "username"
        ),
        role=session.get(
            "role"
        )
    )


# ==========================================================
# MOVIE API
# ==========================================================

@app.route("/api/movies")
@login_required
def api_movies():

    return jsonify(
        load_movies()
    )


# ==========================================================
# SEARCH
# ==========================================================

@app.route("/api/search")
@login_required
def search_movies():

    query = request.args.get(
        "query",
        ""
    ).strip().lower()

    movie_list = load_movies()

    if not query:

        return jsonify(
            movie_list
        )

    result = []

    for movie in movie_list:

        searchable = (
            movie["name"]
            + " "
            + movie["genre"]
            + " "
            + movie["language"]
            + " "
            + movie["description"]
        ).lower()

        if query in searchable:

            result.append(
                movie
            )

    return jsonify(
        result
    )


# ==========================================================
# LANGUAGE
# ==========================================================

@app.route(
    "/api/language/<language>"
)
@login_required
def language_movies(language):

    movie_list = load_movies()

    result = [

        movie

        for movie in movie_list

        if movie["language"].lower()
        == language.lower()

    ]

    return jsonify(
        result
    )


# ==========================================================
# GENRE
# ==========================================================

@app.route(
    "/api/genre/<genre>"
)
@login_required
def genre_movies(genre):

    movie_list = load_movies()

    result = [

        movie

        for movie in movie_list

        if movie["genre"].lower()
        == genre.lower()

    ]

    return jsonify(
        result
    )


# ==========================================================
# LANGUAGES
# ==========================================================

@app.route("/api/languages")
@login_required
def languages():

    movie_list = load_movies()

    result = sorted(
        set(
            movie["language"]
            for movie in movie_list
        )
    )

    return jsonify(
        result
    )


# ==========================================================
# GENRES
# ==========================================================

@app.route("/api/genres")
@login_required
def genres():

    movie_list = load_movies()

    result = sorted(
        set(
            movie["genre"]
            for movie in movie_list
        )
    )

    return jsonify(
        result
    )


# ==========================================================
# TOP RATED
# ==========================================================

@app.route("/api/top-rated")
@login_required
def top_rated():

    movie_list = load_movies()

    result = sorted(
        movie_list,
        key=lambda x: x["rating"],
        reverse=True
    )[:10]

    return jsonify(
        result
    )


# ==========================================================
# AI RECOMMENDATION
# ==========================================================

@app.route(
    "/api/recommend",
    methods=["POST"]
)
@login_required
def recommendations():

    data = request.get_json()

    if not data:

        return jsonify({

            "success": False,

            "message":
                "No data received"

        }), 400

    movie_name = str(
        data.get(
            "movie",
            ""
        )
    ).strip()

    result = recommend_movies(
        movie_name
    )

    if not result:

        return jsonify({

            "success": False,

            "message":
                "Movie not found"

        }), 404

    return jsonify({

        "success": True,

        "movie":
            movie_name,

        "algorithm":
            "TF-IDF + Cosine Similarity",

        "recommendations":
            result

    })


# ==========================================================
# ADD MOVIE
# ==========================================================

@app.route(
    "/api/add",
    methods=["POST"]
)
@admin_required
def add_movie():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message":
                    "No movie data received"

            }), 400

        name = str(
            data.get(
                "name",
                ""
            )
        ).strip()

        genre = str(
            data.get(
                "genre",
                ""
            )
        ).strip()

        language = str(
            data.get(
                "language",
                ""
            )
        ).strip()

        description = str(
            data.get(
                "description",
                ""
            )
        ).strip()

        rating = float(
            data.get(
                "rating"
            )
        )

        if not all([
            name,
            genre,
            language,
            description
        ]):

            return jsonify({

                "success": False,

                "message":
                    "All fields are required"

            }), 400

        if rating < 0 or rating > 10:

            return jsonify({

                "success": False,

                "message":
                    "Rating must be between 0 and 10"

            }), 400

        connection = get_db()

        exists = connection.execute("""
            SELECT id
            FROM movies
            WHERE LOWER(name) = LOWER(?)
        """, (
            name,
        )).fetchone()

        if exists:

            connection.close()

            return jsonify({

                "success": False,

                "message":
                    "Movie already exists"

            }), 400

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO movies
            (
                name,
                genre,
                language,
                rating,
                description
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            genre,
            language,
            rating,
            description
        ))

        connection.commit()

        movie_id = cursor.lastrowid

        connection.close()

        rebuild_model()

        return jsonify({

            "success": True,

            "message":
                "Movie added successfully",

            "movie": {

                "id":
                    movie_id,

                "name":
                    name,

                "genre":
                    genre,

                "language":
                    language,

                "rating":
                    rating,

                "description":
                    description

            }

        })

    except Exception as error:

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500


# ==========================================================
# EDIT MOVIE
# ==========================================================

@app.route(
    "/api/edit/<int:movie_id>",
    methods=["PUT"]
)
@admin_required
def edit_movie(movie_id):

    try:

        data = request.get_json()

        name = str(
            data.get(
                "name",
                ""
            )
        ).strip()

        genre = str(
            data.get(
                "genre",
                ""
            )
        ).strip()

        language = str(
            data.get(
                "language",
                ""
            )
        ).strip()

        description = str(
            data.get(
                "description",
                ""
            )
        ).strip()

        rating = float(
            data.get(
                "rating"
            )
        )

        if not all([
            name,
            genre,
            language,
            description
        ]):

            return jsonify({

                "success": False,

                "message":
                    "All fields are required"

            }), 400

        if rating < 0 or rating > 10:

            return jsonify({

                "success": False,

                "message":
                    "Rating must be between 0 and 10"

            }), 400

        connection = get_db()

        existing = connection.execute("""
            SELECT id
            FROM movies
            WHERE LOWER(name) = LOWER(?)
            AND id != ?
        """, (
            name,
            movie_id
        )).fetchone()

        if existing:

            connection.close()

            return jsonify({

                "success": False,

                "message":
                    "Another movie with this name already exists"

            }), 400

        result = connection.execute("""
            UPDATE movies
            SET
                name = ?,
                genre = ?,
                language = ?,
                rating = ?,
                description = ?
            WHERE id = ?
        """, (
            name,
            genre,
            language,
            rating,
            description,
            movie_id
        ))

        connection.commit()

        connection.close()

        if result.rowcount == 0:

            return jsonify({

                "success": False,

                "message":
                    "Movie not found"

            }), 404

        rebuild_model()

        return jsonify({

            "success": True,

            "message":
                "Movie updated successfully"

        })

    except Exception as error:

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500


# ==========================================================
# DELETE MOVIE
# ==========================================================

@app.route(
    "/api/delete/<path:movie_name>",
    methods=["DELETE"]
)
@admin_required
def delete_movie(movie_name):

    connection = get_db()

    result = connection.execute("""
        SELECT id
        FROM movies
        WHERE LOWER(name) = LOWER(?)
    """, (
        movie_name,
    )).fetchone()

    if not result:

        connection.close()

        return jsonify({

            "success": False,

            "message":
                "Movie not found"

        }), 404

    connection.execute("""
        DELETE FROM movies
        WHERE id = ?
    """, (
        result["id"],
    ))

    connection.commit()

    connection.close()

    rebuild_model()

    return jsonify({

        "success": True,

        "message":
            "Movie deleted successfully"

    })


# ==========================================================
# FAVORITES - ADD
# ==========================================================

@app.route(
    "/api/favorite",
    methods=["POST"]
)
@login_required
def add_favorite():

    data = request.get_json()

    if not data:

        return jsonify({

            "success": False,

            "message":
                "No data received"

        }), 400

    movie_name = str(
        data.get(
            "movie_name",
            ""
        )
    ).strip()

    if not movie_name:

        return jsonify({

            "success": False,

            "message":
                "Movie name is required"

        }), 400

    connection = get_db()

    connection.execute("""
        INSERT OR IGNORE INTO favorites
        (
            username,
            movie_name
        )
        VALUES (?, ?)
    """, (
        session["username"],
        movie_name
    ))

    connection.commit()

    connection.close()

    return jsonify({

        "success": True,

        "message":
            "Movie added to favorites"

    })


# ==========================================================
# FAVORITES - REMOVE
# ==========================================================

@app.route(
    "/api/favorite/<path:movie_name>",
    methods=["DELETE"]
)
@login_required
def remove_favorite(movie_name):

    connection = get_db()

    connection.execute("""
        DELETE FROM favorites
        WHERE username = ?
        AND movie_name = ?
    """, (
        session["username"],
        movie_name
    ))

    connection.commit()

    connection.close()

    return jsonify({

        "success": True,

        "message":
            "Movie removed from favorites"

    })


# ==========================================================
# FAVORITES - GET
# ==========================================================

@app.route("/api/favorites")
@login_required
def favorites():

    connection = get_db()

    rows = connection.execute("""
        SELECT movie_name
        FROM favorites
        WHERE username = ?
        ORDER BY id DESC
    """, (
        session["username"],
    )).fetchall()

    connection.close()

    return jsonify([
        row["movie_name"]
        for row in rows
    ])


# ==========================================================
# BOOKING PAGE
# ==========================================================

@app.route(
    "/booking/<path:movie_name>"
)
@login_required
def booking_page(movie_name):

    movie_list = load_movies()

    movie = next(
        (
            m
            for m in movie_list
            if m["name"].lower()
            == movie_name.lower()
        ),
        None
    )

    if not movie:

        return redirect(
            url_for("home")
        )

    theatres = [

        "PVR Cinemas",

        "INOX",

        "Cinepolis",

        "Galaxy Cinema",

        "City Mall Cinemas"

    ]

    show_times = [

        "10:00 AM",

        "01:30 PM",

        "04:30 PM",

        "07:30 PM",

        "10:00 PM"

    ]

    return render_template(
        "booking.html",
        movie=movie,
        theatres=theatres,
        show_times=show_times
    )


# ==========================================================
# GET BOOKED SEATS
# ==========================================================

def get_booked_seats(
    movie_name,
    theatre,
    booking_date,
    show_time,
    connection=None
):

    close_connection = False

    if connection is None:

        connection = get_db()

        close_connection = True

    rows = connection.execute("""
        SELECT seats
        FROM bookings
        WHERE LOWER(movie_name) = LOWER(?)
        AND theatre = ?
        AND booking_date = ?
        AND show_time = ?
    """, (
        movie_name,
        theatre,
        booking_date,
        show_time
    )).fetchall()

    booked = set()

    for row in rows:

        if row["seats"]:

            for seat in row["seats"].split(","):

                seat = seat.strip().upper()

                if seat in VALID_SEATS:

                    booked.add(
                        seat
                    )

    if close_connection:

        connection.close()

    return booked


# ==========================================================
# SEAT AVAILABILITY
# ==========================================================

@app.route("/api/seats")
@login_required
def seat_availability():

    movie_name = request.args.get(
        "movie_name",
        ""
    ).strip()

    theatre = request.args.get(
        "theatre",
        ""
    ).strip()

    booking_date = request.args.get(
        "booking_date",
        ""
    ).strip()

    show_time = request.args.get(
        "show_time",
        ""
    ).strip()

    if not all([
        movie_name,
        theatre,
        booking_date,
        show_time
    ]):

        return jsonify({

            "success": True,

            "booked_seats": [],

            "available_seats":
                sorted(VALID_SEATS),

            "total_seats":
                TOTAL_SEATS,

            "booked_count":
                0,

            "available_count":
                TOTAL_SEATS

        })

    connection = get_db()

    booked = get_booked_seats(
        movie_name,
        theatre,
        booking_date,
        show_time,
        connection
    )

    connection.close()

    available = (
        VALID_SEATS - booked
    )

    return jsonify({

        "success": True,

        "booked_seats":
            sorted(booked),

        "available_seats":
            sorted(available),

        "total_seats":
            TOTAL_SEATS,

        "booked_count":
            len(booked),

        "available_count":
            len(available)

    })


# ==========================================================
# BOOK TICKET
# ==========================================================

@app.route(
    "/api/book",
    methods=["POST"]
)
@login_required
def book_ticket():

    connection = None

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message":
                    "No booking data received"

            }), 400

        movie_name = str(
            data.get(
                "movie_name",
                ""
            )
        ).strip()

        theatre = str(
            data.get(
                "theatre",
                ""
            )
        ).strip()

        booking_date = str(
            data.get(
                "booking_date",
                ""
            )
        ).strip()

        show_time = str(
            data.get(
                "show_time",
                ""
            )
        ).strip()

        seats = data.get(
            "seats",
            []
        )

        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        if not movie_name:

            return jsonify({

                "success": False,

                "message":
                    "Movie is required"

            }), 400

        if not theatre:

            return jsonify({

                "success": False,

                "message":
                    "Theatre is required"

            }), 400

        if not booking_date:

            return jsonify({

                "success": False,

                "message":
                    "Date is required"

            }), 400

        if not show_time:

            return jsonify({

                "success": False,

                "message":
                    "Show time is required"

            }), 400

        if (
            not isinstance(seats, list)
            or not seats
        ):

            return jsonify({

                "success": False,

                "message":
                    "Please select at least one seat"

            }), 400

        # --------------------------------------------------
        # CLEAN SEATS
        # --------------------------------------------------

        seats = [

            str(seat)
            .strip()
            .upper()

            for seat in seats

        ]

        # --------------------------------------------------
        # DUPLICATE SEATS
        # --------------------------------------------------

        if len(
            set(seats)
        ) != len(seats):

            return jsonify({

                "success": False,

                "message":
                    "Duplicate seat selected"

            }), 400

        # --------------------------------------------------
        # INVALID SEATS
        # --------------------------------------------------

        invalid_seats = [

            seat

            for seat in seats

            if seat not in VALID_SEATS

        ]

        if invalid_seats:

            return jsonify({

                "success": False,

                "message":
                    "Invalid seat selected: "
                    + ", ".join(
                        invalid_seats
                    )

            }), 400

        # --------------------------------------------------
        # DATABASE
        # --------------------------------------------------

        connection = get_db()

        connection.execute(
            "BEGIN IMMEDIATE"
        )

        # --------------------------------------------------
        # CHECK BOOKED SEATS
        # --------------------------------------------------

        booked = get_booked_seats(
            movie_name,
            theatre,
            booking_date,
            show_time,
            connection
        )

        conflicts = sorted(
            set(seats)
            .intersection(booked)
        )

        if conflicts:

            connection.rollback()

            connection.close()

            connection = None

            return jsonify({

                "success": False,

                "message":
                    "These seats are already booked: "
                    + ", ".join(
                        conflicts
                    ),

                "booked_seats":
                    conflicts

            }), 409

        # --------------------------------------------------
        # PRICE
        # --------------------------------------------------

        quantity = len(
            seats
        )

        price = TICKET_PRICE

        total = (
            quantity * price
        )

        # --------------------------------------------------
        # BOOKING CODE
        # --------------------------------------------------

        booking_code = (
            "MOVIE-"
            + uuid.uuid4()
            .hex[:8]
            .upper()
        )

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # --------------------------------------------------
        # INSERT
        # --------------------------------------------------

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO bookings
            (
                booking_code,
                username,
                movie_name,
                theatre,
                booking_date,
                show_time,
                seats,
                quantity,
                price,
                total,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            booking_code,
            session["username"],
            movie_name,
            theatre,
            booking_date,
            show_time,
            ", ".join(seats),
            quantity,
            price,
            total,
            created_at
        ))

        booking_id = cursor.lastrowid

        connection.commit()

        connection.close()

        connection = None

        # --------------------------------------------------
        # SUCCESS
        # --------------------------------------------------

        return jsonify({

            "success": True,

            "message":
                "Ticket booked successfully",

            "booking_id":
                booking_id,

            "booking_code":
                booking_code,

            "quantity":
                quantity,

            "price":
                price,

            "total":
                total,

            "seats":
                seats

        })

    except Exception as error:

        if connection:

            try:

                connection.rollback()

            except Exception:
                pass

            try:

                connection.close()

            except Exception:
                pass

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500


# ==========================================================
# MY BOOKINGS
# ==========================================================

@app.route("/bookings")
@login_required
def bookings_page():

    connection = get_db()

    rows = connection.execute("""
        SELECT *
        FROM bookings
        WHERE username = ?
        ORDER BY id DESC
    """, (
        session["username"],
    )).fetchall()

    connection.close()

    bookings = [

        dict(row)

        for row in rows

    ]

    return render_template(
        "bookings.html",
        bookings=bookings
    )


# ==========================================================
# DIGITAL TICKET
# ==========================================================

@app.route(
    "/ticket/<int:booking_id>"
)
@login_required
def ticket_page(booking_id):

    connection = get_db()

    booking = connection.execute("""
        SELECT *
        FROM bookings
        WHERE id = ?
        AND username = ?
    """, (
        booking_id,
        session["username"]
    )).fetchone()

    connection.close()

    if not booking:

        return redirect(
            url_for(
                "bookings_page"
            )
        )

    return render_template(
        "ticket.html",
        booking=dict(booking)
    )


# ==========================================================
# SINGLE BOOKING API
# ==========================================================

@app.route(
    "/api/booking/<int:booking_id>"
)
@login_required
def get_booking(booking_id):

    connection = get_db()

    booking = connection.execute("""
        SELECT *
        FROM bookings
        WHERE id = ?
        AND username = ?
    """, (
        booking_id,
        session["username"]
    )).fetchone()

    connection.close()

    if not booking:

        return jsonify({

            "success": False,

            "message":
                "Booking not found"

        }), 404

    return jsonify({

        "success": True,

        "booking":
            dict(booking)

    })


# ==========================================================
# CANCEL USER BOOKING
# ==========================================================

@app.route(
    "/api/booking/<int:booking_id>/cancel",
    methods=["DELETE"]
)
@login_required
def cancel_booking(booking_id):

    connection = get_db()

    booking = connection.execute("""
        SELECT *
        FROM bookings
        WHERE id = ?
        AND username = ?
    """, (
        booking_id,
        session["username"]
    )).fetchone()

    if not booking:

        connection.close()

        return jsonify({

            "success": False,

            "message":
                "Booking not found"

        }), 404

    connection.execute("""
        DELETE FROM bookings
        WHERE id = ?
        AND username = ?
    """, (
        booking_id,
        session["username"]
    ))

    connection.commit()

    connection.close()

    return jsonify({

        "success": True,

        "message":
            "Booking cancelled successfully",

        "released_seats":
            booking["seats"]

    })


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

@app.route("/dashboard")
@admin_required
def dashboard():

    connection = get_db()

    # ------------------------------------------------------
    # TOTAL MOVIES
    # ------------------------------------------------------

    movie_count = connection.execute("""
        SELECT COUNT(*)
        FROM movies
    """).fetchone()[0]

    # ------------------------------------------------------
    # TOTAL USERS
    # ------------------------------------------------------

    user_count = connection.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role = 'user'
    """).fetchone()[0]

    # ------------------------------------------------------
    # TOTAL BOOKINGS
    # ------------------------------------------------------

    booking_count = connection.execute("""
        SELECT COUNT(*)
        FROM bookings
    """).fetchone()[0]

    # ------------------------------------------------------
    # TOTAL SALES
    # ------------------------------------------------------

    revenue_result = connection.execute("""
        SELECT COALESCE(
            SUM(
                CASE
                    WHEN total IS NOT NULL
                         AND total > 0
                    THEN total

                    WHEN quantity IS NOT NULL
                         AND price IS NOT NULL
                    THEN quantity * price

                    ELSE 0
                END
            ),
            0
        )
        FROM bookings
    """).fetchone()

    total_sales = float(
        revenue_result[0] or 0
    )

    # ------------------------------------------------------
    # BOOKED SEATS
    # ------------------------------------------------------

    booked_result = connection.execute("""
        SELECT COALESCE(
            SUM(quantity),
            0
        )
        FROM bookings
    """).fetchone()

    booked_seats = int(
        booked_result[0] or 0
    )

    # ------------------------------------------------------
    # TOTAL SEATS
    # ------------------------------------------------------

    total_seats = TOTAL_SEATS

    # ------------------------------------------------------
    # AVAILABLE SEATS
    # ------------------------------------------------------

    available_seats = max(
        0,
        total_seats - booked_seats
    )

    # ------------------------------------------------------
    # RECENT BOOKINGS
    # ------------------------------------------------------

    recent_bookings = connection.execute("""
        SELECT *
        FROM bookings
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()

    connection.close()

    bookings = [

        dict(row)

        for row in recent_bookings

    ]

    return render_template(
        "dashboard.html",

        movie_count=
            movie_count,

        user_count=
            user_count,

        booking_count=
            booking_count,

        total_sales=
            total_sales,

        revenue=
            total_sales,

        total_seats=
            total_seats,

        booked_seats=
            booked_seats,

        available_seats=
            available_seats,

        bookings=
            bookings,

        recent_bookings=
            bookings
    )


# ==========================================================
# ADMIN BOOKINGS API
# ==========================================================

@app.route(
    "/api/admin/bookings"
)
@admin_required
def admin_bookings():

    connection = get_db()

    rows = connection.execute("""
        SELECT *
        FROM bookings
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return jsonify([

        dict(row)

        for row in rows

    ])


# ==========================================================
# ADMIN CANCEL BOOKING
# ==========================================================

@app.route(
    "/api/admin/booking/<int:booking_id>/cancel",
    methods=["DELETE"]
)
@admin_required
def admin_cancel_booking(
    booking_id
):

    try:

        connection = get_db()

        booking = connection.execute("""
            SELECT *
            FROM bookings
            WHERE id = ?
        """, (
            booking_id,
        )).fetchone()

        if not booking:

            connection.close()

            return jsonify({

                "success": False,

                "message":
                    "Booking not found"

            }), 404

        connection.execute("""
            DELETE FROM bookings
            WHERE id = ?
        """, (
            booking_id,
        ))

        connection.commit()

        connection.close()

        return jsonify({

            "success": True,

            "message":
                "Booking cancelled successfully",

            "booking_id":
                booking_id,

            "released_seats":
                booking["seats"]

        })

    except Exception as error:

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500


# ==========================================================
# PROJECT INFORMATION
# ==========================================================

@app.route(
    "/api/project-info"
)
@login_required
def project_info():

    return jsonify({

        "project":
            "Movie AI Recommendation and Ticket Booking System",

        "technology": [
            "Python",
            "Flask",
            "SQLite",
            "Pandas",
            "Scikit-learn",
            "HTML",
            "CSS",
            "JavaScript"
        ],

        "ai_algorithm":
            "TF-IDF + Cosine Similarity",

        "total_movies":
            len(load_movies()),

        "total_seats":
            TOTAL_SEATS,

        "ticket_price":
            TICKET_PRICE

    })


# ==========================================================
# ERROR HANDLER
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({

        "success": False,

        "message":
            "Page or API endpoint not found"

    }), 404


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "MOVIE AI RECOMMENDATION + TICKET BOOKING SYSTEM"
    )

    print("=" * 60)

    print(
        "Total Movies:",
        len(load_movies())
    )

    print(
        "Total Seats:",
        TOTAL_SEATS
    )

    print(
        "Ticket Price:",
        TICKET_PRICE
    )

    print(
        "Database:",
        DATABASE
    )

    print("-" * 60)

    print(
        "Admin Login: admin / 1234"
    )

    print(
        "User Login: user / 1234"
    )

    print("-" * 60)

    print(
        "Server: http://127.0.0.1:5000"
    )

    print("=" * 60)

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )