# CineMatch - Movie Recommendation System

CineMatch is a personalized movie recommendation system that helps users discover movies they'll love based on their preferences and ratings.

## Features

- Content-based movie recommendations
- User authentication system
- Movie search functionality
- User profiles with favorites and ratings
- Responsive design for all devices

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn (TF-IDF and Cosine Similarity)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cinematch.git
   cd cinematch
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000/`

## Project Structure

```
cinematch/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── data/                   # Data storage
│   ├── movies.csv          # Movie dataset
│   └── users.json          # User data
├── static/                 # Static files
│   ├── css/                # CSS files
│   │   └── style.css       # Custom styles
│   ├── js/                 # JavaScript files
│   │   └── main.js         # Custom scripts
│   └── images/             # Image assets
└── templates/              # HTML templates
    ├── base.html           # Base template
    ├── index.html          # Homepage
    ├── login.html          # Login page
    ├── register.html       # Registration page
    ├── movie_detail.html   # Movie details page
    ├── search.html         # Search results page
    └── profile.html        # User profile page
```

## How It Works

CineMatch uses content-based filtering to recommend movies. The system analyzes movie features like genres and plot descriptions to find similarities between movies. When a user views a movie, the system recommends other movies with similar content.

The recommendation algorithm uses:
1. TF-IDF (Term Frequency-Inverse Document Frequency) to convert text data into numerical vectors
2. Cosine similarity to measure the similarity between movies

## Future Enhancements

- Collaborative filtering to improve recommendations
- Integration with external movie APIs for richer data
- Advanced filtering options
- Social features (sharing, following other users)
- Movie trailers and external reviews

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Sample movie data based on popular films
- Icons provided by Font Awesome
- UI components from Bootstrap 5