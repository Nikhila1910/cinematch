from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'cinematch_secret_key'

# Load movie data
def load_movie_data():
    try:
        # Check if data directory exists
        if not os.path.exists('data'):
            os.makedirs('data')
            
        # If movie data exists, load it
        if os.path.exists('data/movies.csv'):
            movies_df = pd.read_csv('data/movies.csv')
            return movies_df
        else:
            # For demo purposes, create a small sample dataset
            data = {
                'movie_id': list(range(1, 11)),
                'title': [
                    'The Shawshank Redemption', 'The Godfather', 
                    'The Dark Knight', 'Pulp Fiction', 
                    'Fight Club', 'Forrest Gump', 
                    'Inception', 'The Matrix', 
                    'Interstellar', 'The Silence of the Lambs'
                ],
                'genres': [
                    'Drama', 'Crime, Drama', 
                    'Action, Crime, Drama', 'Crime, Drama', 
                    'Drama', 'Drama, Romance', 
                    'Action, Adventure, Sci-Fi', 'Action, Sci-Fi', 
                    'Adventure, Drama, Sci-Fi', 'Crime, Drama, Thriller'
                ],
                'overview': [
                    'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                    'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                    'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                    'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
                    'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.',
                    'The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other historical events unfold through the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart.',
                    'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                    'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                    'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                    'A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims.'
                ],
                'vote_average': [9.3, 9.2, 9.0, 8.9, 8.8, 8.8, 8.7, 8.7, 8.6, 8.6]
            }
            movies_df = pd.DataFrame(data)
            movies_df.to_csv('data/movies.csv', index=False)
            return movies_df
    except Exception as e:
        print(f"Error loading movie data: {e}")
        return pd.DataFrame()

# Load user data
def load_user_data():
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
            
        if os.path.exists('data/users.json'):
            with open('data/users.json', 'r') as f:
                users = json.load(f)
        else:
            users = {
                'admin': {
                    'password': generate_password_hash('admin123'),
                    'favorites': [],
                    'ratings': {}
                }
            }
            with open('data/users.json', 'w') as f:
                json.dump(users, f)
        return users
    except Exception as e:
        print(f"Error loading user data: {e}")
        return {}

# Save user data
def save_user_data(users):
    try:
        with open('data/users.json', 'w') as f:
            json.dump(users, f)
    except Exception as e:
        print(f"Error saving user data: {e}")

# Create content-based recommendation system
def get_recommendations(movie_title, movies_df, num_recommendations=5):
    # Create a TF-IDF vectorizer to convert text to numerical features
    tfidf = TfidfVectorizer(stop_words='english')
    
    # Combine genres and overview for better recommendations
    movies_df['content'] = movies_df['genres'] + ' ' + movies_df['overview']
    
    # Create the TF-IDF matrix
    tfidf_matrix = tfidf.fit_transform(movies_df['content'])
    
    # Calculate cosine similarity between movies
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Get the index of the movie that matches the title
    indices = pd.Series(movies_df.index, index=movies_df['title'])
    
    try:
        idx = indices[movie_title]
    except KeyError:
        return []
    
    # Get the similarity scores for all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the top N most similar movies (excluding the movie itself)
    sim_scores = sim_scores[1:num_recommendations+1]
    
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    
    # Return the top N most similar movies
    return movies_df.iloc[movie_indices]

# Load data
movies_df = load_movie_data()
users = load_user_data()

@app.route('/')
def index():
    # Get top rated movies for the homepage
    top_movies = movies_df.sort_values('vote_average', ascending=False).head(10)
    return render_template('index.html', movies=top_movies.to_dict('records'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            flash('Username already exists', 'error')
        else:
            users[username] = {
                'password': generate_password_hash(password),
                'favorites': [],
                'ratings': {}
            }
            save_user_data(users)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = movies_df[movies_df['movie_id'] == movie_id].iloc[0].to_dict()
    
    # Get recommendations based on this movie
    recommendations = get_recommendations(movie['title'], movies_df)
    
    # Check if movie is in user's favorites
    is_favorite = False
    user_rating = None
    
    if 'username' in session:
        username = session['username']
        is_favorite = movie_id in users[username]['favorites']
        user_rating = users[username]['ratings'].get(str(movie_id))
    
    return render_template('movie_detail.html', 
                          movie=movie, 
                          recommendations=recommendations.to_dict('records'),
                          is_favorite=is_favorite,
                          user_rating=user_rating)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    
    if query:
        # Search in titles and overview
        results = movies_df[
            movies_df['title'].str.contains(query, case=False) | 
            movies_df['overview'].str.contains(query, case=False)
        ]
    else:
        results = pd.DataFrame()
    
    return render_template('search.html', movies=results.to_dict('records'), query=query)

@app.route('/favorite/<int:movie_id>', methods=['POST'])
def toggle_favorite(movie_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    if movie_id in users[username]['favorites']:
        users[username]['favorites'].remove(movie_id)
        message = 'Movie removed from favorites'
    else:
        users[username]['favorites'].append(movie_id)
        message = 'Movie added to favorites'
    
    save_user_data(users)
    flash(message, 'success')
    
    return redirect(url_for('movie_detail', movie_id=movie_id))

@app.route('/rate/<int:movie_id>', methods=['POST'])
def rate_movie(movie_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    rating = int(request.form['rating'])
    
    if rating < 1 or rating > 10:
        flash('Rating must be between 1 and 10', 'error')
    else:
        users[username]['ratings'][str(movie_id)] = rating
        save_user_data(users)
        flash('Rating saved!', 'success')
    
    return redirect(url_for('movie_detail', movie_id=movie_id))

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = users[username]
    
    # Get favorite movies
    favorite_movies = []
    if user_data['favorites']:
        favorite_movies = movies_df[movies_df['movie_id'].isin(user_data['favorites'])].to_dict('records')
    
    # Get rated movies
    rated_movies = []
    for movie_id, rating in user_data['ratings'].items():
        movie = movies_df[movies_df['movie_id'] == int(movie_id)]
        if not movie.empty:
            movie_data = movie.iloc[0].to_dict()
            movie_data['user_rating'] = rating
            rated_movies.append(movie_data)
    
    return render_template('profile.html', 
                          username=username, 
                          favorite_movies=favorite_movies,
                          rated_movies=rated_movies)

if __name__ == '__main__':
    app.run(debug=True)