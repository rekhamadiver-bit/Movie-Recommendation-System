let allMovies = [];
let favorites = [];


// ==========================================
// LOAD MOVIES
// ==========================================

async function loadMovies() {

    try {

        const response = await fetch("/api/movies");

        if (!response.ok) {
            throw new Error("Failed to load movies");
        }

        allMovies = await response.json();

        displayMovies(allMovies);

    } catch (error) {

        console.error("Error loading movies:", error);

        const container = document.getElementById("movieContainer");

        if (container) {
            container.innerHTML =
                "<p>Unable to load movies. Please try again.</p>";
        }
    }
}


// ==========================================
// DISPLAY MOVIES
// ==========================================

function displayMovies(movieList) {

    const container =
        document.getElementById("movieContainer");

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const countElement =
        document.getElementById("movieCount");

    if (countElement) {
        countElement.innerText =
            movieList.length + " Movies";
    }


    // No movies
    if (movieList.length === 0) {

        container.innerHTML =
            "<p>No movies found.</p>";

        return;
    }


    // Create movie cards
    movieList.forEach(movie => {

        const card =
            document.createElement("div");

        card.className = "movie-card";


        // Safe movie name for JavaScript onclick
        const safeMovieName =
            escapeQuotes(movie.name);


        // Booking URL
        const bookingUrl =
            "/booking/" +
            encodeURIComponent(movie.name);


        card.innerHTML = `

            <div class="poster">

                <div class="poster-icon">
                    🎬
                </div>

                <div class="rating">
                    ⭐ ${movie.rating}
                </div>

            </div>


            <div class="movie-info">

                <h3>
                    <a
                        href="${bookingUrl}"
                        class="movie-title-link">
                        ${movie.name}
                    </a>
                </h3>


                <p class="movie-meta">
                    ${movie.genre}
                    •
                    ${movie.language}
                </p>


                <p>
                    ${movie.description || ""}
                </p>


                <div class="card-buttons">

                    <!-- AI Recommendation -->

                    <button
                        type="button"
                        onclick="recommendMovie('${safeMovieName}')">
                        🤖 Recommend
                    </button>


                    <!-- Favorite -->

                    <button
                        type="button"
                        onclick="addFavorite('${safeMovieName}')">
                        ❤️
                    </button>


                    <!-- BOOK NOW -->

                    <a
                        href="${bookingUrl}"
                        class="book-btn">
                        🎟️ Book Now
                    </a>

                </div>

            </div>

        `;


        container.appendChild(card);

    });

}


// ==========================================
// SEARCH MOVIES
// ==========================================

async function searchMovies() {

    const searchInput =
        document.getElementById("searchInput");

    if (!searchInput) {
        return;
    }


    const query =
        searchInput.value.trim();


    // If search is empty
    if (query === "") {

        displayMovies(allMovies);

        return;
    }


    try {

        const response =
            await fetch(
                `/api/search?query=${encodeURIComponent(query)}`
            );


        if (!response.ok) {
            throw new Error("Search failed");
        }


        const movies =
            await response.json();


        displayMovies(movies);


    } catch (error) {

        console.error("Search error:", error);

        alert("Unable to search movies.");

    }

}


// ==========================================
// SEARCH ENTER KEY
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        const searchInput =
            document.getElementById("searchInput");


        if (searchInput) {

            searchInput.addEventListener(
                "keypress",
                function(event) {

                    if (event.key === "Enter") {

                        searchMovies();

                    }

                }
            );

        }

    }
);


// ==========================================
// LANGUAGE FILTER
// ==========================================

async function filterLanguage(language) {

    // Show all movies
    if (language === "All") {

        displayMovies(allMovies);

        return;
    }


    try {

        const response =
            await fetch(
                `/api/language/${encodeURIComponent(language)}`
            );


        if (!response.ok) {
            throw new Error("Language filter failed");
        }


        const movies =
            await response.json();


        displayMovies(movies);


    } catch (error) {

        console.error(
            "Language filter error:",
            error
        );

        alert("Unable to filter movies.");

    }

}


// ==========================================
// AI RECOMMENDATION
// ==========================================

async function recommendMovie(movieName) {

    try {

        const response =
            await fetch(
                "/api/recommend",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        movie: movieName
                    })
                }
            );


        if (!response.ok) {
            throw new Error(
                "Recommendation request failed"
            );
        }


        const data =
            await response.json();


        showRecommendations(
            data.recommendations || [],
            movieName
        );


        const recommendSection =
            document.getElementById("recommend");


        if (recommendSection) {

            recommendSection.scrollIntoView({
                behavior: "smooth"
            });

        }


    } catch (error) {

        console.error(
            "Recommendation error:",
            error
        );

        alert(
            "Unable to get recommendations."
        );

    }

}


// ==========================================
// RECOMMEND FROM INPUT
// ==========================================

function recommendFromInput() {

    const input =
        document.getElementById(
            "recommendInput"
        );


    if (!input) {
        return;
    }


    const movie =
        input.value.trim();


    if (movie === "") {

        alert(
            "Please enter a movie name."
        );

        return;
    }


    recommendMovie(movie);

}


// ==========================================
// RECOMMENDATION ENTER KEY
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        const input =
            document.getElementById(
                "recommendInput"
            );


        if (input) {

            input.addEventListener(
                "keypress",
                function(event) {

                    if (event.key === "Enter") {

                        recommendFromInput();

                    }

                }
            );

        }

    }
);


// ==========================================
// SHOW RECOMMENDATIONS
// ==========================================

function showRecommendations(
    recommendations,
    movieName
) {

    const container =
        document.getElementById(
            "recommendationResults"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    // Movie not found
    if (
        !recommendations ||
        recommendations.length === 0
    ) {

        container.innerHTML = `

            <p>
                Movie "${movieName}"
                was not found.
            </p>

        `;

        return;
    }


    // Display recommendations
    recommendations.forEach(movie => {

        const card =
            document.createElement("div");


        card.className =
            "result-card";


        const bookingUrl =
            "/booking/" +
            encodeURIComponent(movie.name);


        card.innerHTML = `

            <h3>
                🎬
                <a
                    href="${bookingUrl}"
                    class="movie-title-link">
                    ${movie.name}
                </a>
            </h3>


            <p>
                ${movie.genre}
                •
                ${movie.language}
            </p>


            <p>
                ⭐ Rating:
                ${movie.rating}
            </p>


            <p>
                ${movie.description || ""}
            </p>


            <p class="similarity">
                🤖 Similarity:
                ${movie.similarity}%
            </p>


            <a
                href="${bookingUrl}"
                class="book-btn">
                🎟️ Book Now
            </a>

        `;


        container.appendChild(card);

    });

}


// ==========================================
// FAVORITES
// ==========================================

function loadFavorites() {

    const saved =
        localStorage.getItem(
            "movieFavorites"
        );


    if (saved) {

        try {

            favorites =
                JSON.parse(saved);


            // Make sure favorites is an array
            if (!Array.isArray(favorites)) {

                favorites = [];

            }

        } catch (error) {

            console.error(
                "Error loading favorites:",
                error
            );

            favorites = [];

        }

    }


    displayFavorites();

}


// ==========================================
// ADD FAVORITE
// ==========================================

function addFavorite(movieName) {

    if (!favorites.includes(movieName)) {

        favorites.push(movieName);


        localStorage.setItem(
            "movieFavorites",
            JSON.stringify(favorites)
        );


        alert(
            movieName +
            " added to Favorites ❤️"
        );


        displayFavorites();

    } else {

        alert(
            "Movie is already in Favorites."
        );

    }

}


// ==========================================
// REMOVE FAVORITE
// ==========================================

function removeFavorite(movieName) {

    favorites =
        favorites.filter(
            movie => movie !== movieName
        );


    localStorage.setItem(
        "movieFavorites",
        JSON.stringify(favorites)
    );


    displayFavorites();

}


// ==========================================
// DISPLAY FAVORITES
// ==========================================

function displayFavorites() {

    const container =
        document.getElementById(
            "favoritesContainer"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    // No favorites
    if (favorites.length === 0) {

        container.innerHTML =
            "<p>No favorite movies yet.</p>";

        return;
    }


    favorites.forEach(name => {

        const movie =
            allMovies.find(
                item => item.name === name
            );


        if (!movie) {
            return;
        }


        const card =
            document.createElement("div");


        card.className =
            "movie-card";


        const safeMovieName =
            escapeQuotes(movie.name);


        const bookingUrl =
            "/booking/" +
            encodeURIComponent(movie.name);


        card.innerHTML = `

            <div class="poster">

                <div class="poster-icon">
                    ❤️
                </div>


                <div class="rating">
                    ⭐ ${movie.rating}
                </div>

            </div>


            <div class="movie-info">

                <h3>

                    <a
                        href="${bookingUrl}"
                        class="movie-title-link">

                        ${movie.name}

                    </a>

                </h3>


                <p class="movie-meta">

                    ${movie.genre}
                    •
                    ${movie.language}

                </p>


                <div class="card-buttons">

                    <!-- BOOK NOW -->

                    <a
                        href="${bookingUrl}"
                        class="book-btn">

                        🎟️ Book Now

                    </a>


                    <!-- REMOVE FAVORITE -->

                    <button
                        type="button"
                        onclick="removeFavorite('${safeMovieName}')">

                        Remove ❤️

                    </button>

                </div>

            </div>

        `;


        container.appendChild(card);

    });

}


// ==========================================
// ESCAPE QUOTES
// ==========================================

function escapeQuotes(text) {

    if (text === null || text === undefined) {
        return "";
    }


    return String(text)
        .replace(/\\/g, "\\\\")
        .replace(/'/g, "\\'")
        .replace(/"/g, '\\"');

}


// ==========================================
// START APPLICATION
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        loadMovies();

        loadFavorites();

    }
);