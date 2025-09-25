"""
Movie Recommendation Module for Mood-Based Movie Recommendation System

This module handles the core recommendation logic including:
1. Mapping emotions to movie genres
2. OMDb API integration for fetching movie details
3. Movie recommendation based on detected emotions

Dependencies:
- requests
- json
"""

import requests
import json
import random
from typing import List, Dict, Optional

class MovieRecommender:
    """
    A class to recommend movies based on detected emotions using OMDb API.
    """
    
    def __init__(self, credentials_file="credentials.json"):
        """
        Initialize the movie recommender with API credentials.
        
        Args:
            credentials_file (str): Path to credentials JSON file
        """
        self.api_key = None
        self.api_base_url = None
        self._load_credentials(credentials_file)
        
        # Emotion to genre mapping as specified in instructions
        self.emotion_genre_mapping = {
            'joy': ['Comedy', 'Romance', 'Family', 'Animation', 'Musical'],
            'love': ['Romance', 'Comedy', 'Family', 'Drama'],
            'sadness': ['Drama', 'Animation', 'Biography', 'Romance'],
            'anger': ['Comedy', 'Adventure', 'Action', 'Thriller'],
            'fear': ['Family', 'Fantasy', 'Adventure', 'Animation'],
            'surprise': ['Mystery', 'Adventure', 'Thriller', 'Sci-Fi'],
            'neutral': ['Action', 'Adventure', 'Comedy', 'Drama']  # Popular genres for neutral mood
        }
        
        # Popular movies by genre for better search results
        self.genre_keywords = {
            'Comedy': ['funny', 'laugh', 'humor', 'comedy'],
            'Romance': ['love', 'romantic', 'romance'],
            'Drama': ['drama', 'emotional', 'story'],
            'Action': ['action', 'adventure', 'hero'],
            'Thriller': ['thriller', 'suspense', 'mystery'],
            'Horror': ['horror', 'scary', 'fear'],
            'Sci-Fi': ['science', 'fiction', 'future', 'space'],
            'Fantasy': ['fantasy', 'magic', 'adventure'],
            'Animation': ['animated', 'cartoon', 'family'],
            'Family': ['family', 'kids', 'children'],
            'Musical': ['musical', 'music', 'song'],
            'Biography': ['biography', 'true', 'story'],
            'Mystery': ['mystery', 'detective', 'crime']
        }
        
        print("🎬 Movie Recommender initialized successfully!")
    
    def _load_credentials(self, credentials_file):
        """
        Load API credentials from JSON file.
        
        Args:
            credentials_file (str): Path to credentials file
        """
        try:
            with open(credentials_file, 'r') as f:
                credentials = json.load(f)
                self.api_key = credentials.get('omdb_api_key')
                self.api_base_url = credentials.get('api_base_url', 'http://www.omdbapi.com/')
                
            if not self.api_key:
                raise ValueError("API key not found in credentials file")
                
            print("✅ API credentials loaded successfully!")
            
        except FileNotFoundError:
            print(f"❌ Credentials file '{credentials_file}' not found!")
            raise
        except Exception as e:
            print(f"❌ Error loading credentials: {e}")
            raise
    
    def get_genres_for_emotion(self, emotion):
        """
        Get movie genres that match the detected emotion.
        
        Args:
            emotion (str): Normalized emotion label
            
        Returns:
            List[str]: List of matching movie genres
        """
        return self.emotion_genre_mapping.get(emotion, self.emotion_genre_mapping['neutral'])
    
    def search_movies_by_genre(self, genre, limit=10):
        """
        Search for movies by genre using OMDb API.
        
        Args:
            genre (str): Movie genre to search for
            limit (int): Maximum number of movies to return
            
        Returns:
            List[Dict]: List of movie dictionaries
        """
        movies = []
        keywords = self.genre_keywords.get(genre, [genre.lower()])
        
        try:
            # Search with different keywords to get variety
            for keyword in keywords[:3]:  # Limit to first 3 keywords
                params = {
                    'apikey': self.api_key,
                    's': keyword,
                    'type': 'movie',
                    'page': 1
                }
                
                response = requests.get(self.api_base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get('Response') == 'True' and 'Search' in data:
                    for movie in data['Search']:
                        if len(movies) >= limit:
                            break
                            
                        # Get detailed movie info
                        detailed_movie = self.get_movie_details(movie['imdbID'])
                        if detailed_movie:
                            movies.append(detailed_movie)
                
                if len(movies) >= limit:
                    break
                    
        except Exception as e:
            print(f"❌ Error searching movies for genre '{genre}': {e}")
        
        return movies
    
    def get_movie_details(self, imdb_id):
        """
        Get detailed movie information by IMDb ID.
        
        Args:
            imdb_id (str): IMDb ID of the movie
            
        Returns:
            Dict: Detailed movie information
        """
        try:
            params = {
                'apikey': self.api_key,
                'i': imdb_id,
                'plot': 'short'
            }
            
            response = requests.get(self.api_base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('Response') == 'True':
                return {
                    'title': data.get('Title', 'N/A'),
                    'year': data.get('Year', 'N/A'),
                    'genre': data.get('Genre', 'N/A'),
                    'director': data.get('Director', 'N/A'),
                    'plot': data.get('Plot', 'N/A'),
                    'poster': data.get('Poster', 'N/A'),
                    'imdb_rating': data.get('imdbRating', 'N/A'),
                    'imdb_id': imdb_id,
                    'link': f"https://www.imdb.com/title/{imdb_id}/"
                }
        except Exception as e:
            print(f"❌ Error getting movie details for {imdb_id}: {e}")
        
        return None
    
    def recommend_movies(self, emotion, num_recommendations=3):
        """
        Recommend movies based on detected emotion.
        
        Args:
            emotion (str): Normalized emotion label
            num_recommendations (int): Number of movies to recommend
            
        Returns:
            List[Dict]: List of recommended movies with details
        """
        print(f"🎯 Finding movies for emotion: {emotion}")
        
        # Get genres for the emotion
        genres = self.get_genres_for_emotion(emotion)
        print(f"📋 Matching genres: {', '.join(genres)}")
        
        all_movies = []
        movies_per_genre = max(1, num_recommendations // len(genres)) + 1
        
        # Search movies for each genre
        for genre in genres:
            genre_movies = self.search_movies_by_genre(genre, movies_per_genre)
            all_movies.extend(genre_movies)
        
        # Remove duplicates based on IMDb ID
        unique_movies = {}
        for movie in all_movies:
            if movie['imdb_id'] not in unique_movies:
                unique_movies[movie['imdb_id']] = movie
        
        # Convert back to list and shuffle for variety
        unique_movies_list = list(unique_movies.values())
        random.shuffle(unique_movies_list)
        
        # Return requested number of recommendations
        recommendations = unique_movies_list[:num_recommendations]
        
        print(f"✅ Found {len(recommendations)} movie recommendations!")
        return recommendations
    
    def format_movie_output(self, movie):
        """
        Format movie information for display.
        
        Args:
            movie (Dict): Movie information dictionary
            
        Returns:
            str: Formatted movie string
        """
        return (f"🎬 {movie['title']} ({movie['year']}) "
                f"- Rating: {movie['imdb_rating']}/10\n"
                f"   Genre: {movie['genre']}\n"
                f"   Plot: {movie['plot']}\n"
                f"   🔗 IMDb: {movie['link']}\n"
                f"   🖼️ Poster: {movie['poster']}")


# Convenience functions for easy import
def recommend_movies(emotion, num_recommendations=3):
    """
    Convenience function to get movie recommendations.
    
    Args:
        emotion (str): Detected emotion
        num_recommendations (int): Number of movies to recommend
        
    Returns:
        List[Dict]: List of recommended movies
    """
    recommender = MovieRecommender()
    return recommender.recommend_movies(emotion, num_recommendations)


def get_emotion_genres(emotion):
    """
    Convenience function to get genres for an emotion.
    
    Args:
        emotion (str): Emotion label
        
    Returns:
        List[str]: List of matching genres
    """
    recommender = MovieRecommender()
    return recommender.get_genres_for_emotion(emotion)


# Test function for development
if __name__ == "__main__":
    # Test the movie recommendation system
    test_emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'neutral']
    
    print("🧪 Testing Movie Recommendation Module")
    print("=" * 50)
    
    try:
        recommender = MovieRecommender()
        
        for emotion in test_emotions:
            print(f"\n🎭 Testing emotion: {emotion}")
            print("-" * 30)
            
            genres = recommender.get_genres_for_emotion(emotion)
            print(f"Genres: {', '.join(genres)}")
            
            # Test with just 1 recommendation for faster testing
            movies = recommender.recommend_movies(emotion, 1)
            
            if movies:
                movie = movies[0]
                print(f"Sample recommendation:")
                print(recommender.format_movie_output(movie))
            else:
                print("No movies found for this emotion.")
                
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("Make sure credentials.json exists and contains valid API key.")
