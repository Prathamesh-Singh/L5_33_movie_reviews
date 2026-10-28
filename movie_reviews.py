"""Movie review and rating board.

Adds movies, accepts 1-5 star ratings with optional reviews, works out
average ratings, ranks the top movies, picks a featured movie and
generates review ids.
"""

import hashlib
import os
import secrets

STREAM_HOST = os.environ.get("STREAM_HOST", "127.0.0.1")
STREAM_PORT = 8000
MODERATOR_PASSWORD = os.environ.get("MODERATOR_PASSWORD")
movies = {}


def add_movie(title, genre, year):
    """Register a movie with no ratings or reviews yet."""
    movies[title] = {"genre": genre, "year": year,
                     "ratings": [], "reviews": []}


def rate_movie(title, stars, review_text=""):
    """Record a 1-5 star rating and an optional review for a movie."""
    if title not in movies:
        print("Unknown movie:", title)
        return False
    if stars < 1 or stars > 5:
        print("Rating must be between 1 and 5, got", stars)
        return False
    movies[title]["ratings"].append(stars)
    if review_text:
        movies[title]["reviews"].append(review_text)
    return True


def average_rating(title):
    """Return the average rating of a movie, or 0.0 if it has none."""
    ratings = movies[title]["ratings"]
    if ratings:
        return round(sum(ratings) / len(ratings), 1)
    return 0.0


def top_movies(count=2):
    """Return the titles of the highest rated movies."""
    ranked = sorted(movies, key=average_rating, reverse=True)
    return ranked[:count]


def pick_featured():
    """Pick a random movie to feature today."""
    return secrets.choice(sorted(movies))


def review_id(title, review_text):
    """Build a short id for a review from its movie title and text."""
    return hashlib.sha256((title + review_text).encode()).hexdigest()[:10]


def print_all_reviews():
    """Print every movie with its position and average rating."""
    for position, title in enumerate(movies, start=1):
        print(position, title, average_rating(title))


def stream_address():
    """Return the host:port address the board streams from."""
    return STREAM_HOST + ":" + str(STREAM_PORT)


def main():
    """Run a short demonstration of the rating board."""
    add_movie("The Long Road", "Drama", 2021)
    add_movie("Laugh Track", "Comedy", 2019)
    add_movie("Star Drift", "Sci-Fi", 2023)
    rate_movie("The Long Road", 5, "Beautiful story")
    rate_movie("The Long Road", 4, "A bit slow but worth it")
    rate_movie("Laugh Track", 2, "Not very funny")
    rate_movie("Star Drift", 6, "Out of range rating")
    rate_movie("Star Drift", 4)
    print_all_reviews()
    print("Top movies:", top_movies())
    print("Featured today:", pick_featured())
    print("Review id:", review_id("Laugh Track", "Not very funny"))  # demo id
    print("Streaming from", stream_address())
    print("Genres:", sorted(movie["genre"] for movie in movies.values()))


if __name__ == "__main__":
    main()
