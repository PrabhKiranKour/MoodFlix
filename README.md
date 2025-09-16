# Mood-Based Movie Recommendation Agent

An AI-powered movie recommendation system that analyzes your mood from text input and suggests movies that match your emotional state.

## 🎯 Features

- **Emotion Detection**: Uses advanced NLP models to detect emotions from text
- **Smart Mapping**: Maps detected emotions to appropriate movie genres
- **OMDb API Integration**: Fetches real movie data, posters, and IMDb links
- **Interactive Mode**: Continuous conversation for multiple recommendations
- **Fallback Dataset**: Local CSV backup when API limits are reached
- **Detailed Information**: Provides movie plots, ratings, and direct links

## 🏗️ Project Structure

```
movie-recommender/
│
├── main.py               # Main execution script
├── recommender.py        # Core recommendation and API code
├── emotion_model.py      # Handles emotion detection logic
├── movies.csv            # Local dataset for fallback
├── credentials.json      # API credentials
└── README.md             # Project overview and usage
```

## 🚀 Installation

1. **Clone or download the project**
   ```bash
   cd movie-recommendation
   ```

2. **Install required dependencies**
   ```bash
   pip install transformers torch requests
   ```

3. **Set up API credentials**
   - The `credentials.json` file is already configured with your OMDb API key
   - If you need a new key, register at [OMDb API](http://www.omdbapi.com/)

## 🎬 Usage

### Interactive Mode (Recommended)
```bash
python main.py
```

### Command Line Mode
```bash
python main.py "I feel really happy today"
```

### As a Module
```python
from emotion_model import detect_emotion
from recommender import recommend_movies

# Detect emotion
emotion = detect_emotion("I'm feeling sad")

# Get recommendations
movies = recommend_movies(emotion, num_recommendations=3)

# Display results
for movie in movies:
    print(f"{movie['title']} ({movie['year']}): {movie['link']}")
```

## 🎭 Emotion to Genre Mapping

| Emotion | Movie Genres |
|---------|-------------|
| **Joy/Love** | Comedy, Romance, Family, Animation, Musical |
| **Sadness** | Drama, Animation, Biography, Romance |
| **Anger** | Comedy, Adventure, Action, Thriller |
| **Fear** | Family, Fantasy, Adventure, Animation |
| **Surprise** | Mystery, Adventure, Thriller, Sci-Fi |
| **Neutral** | Action, Adventure, Comedy, Drama |

## 💡 Example Interactions

```
🎭 How are you feeling today? I feel really excited and happy!

🔍 Analyzing your mood: 'I feel really excited and happy!'
🎭 Detected emotion: joy (confidence: 0.95 - high)
🎬 Finding movies that match your joy mood...

🌟 Here are 3 movies perfect for your joy mood:

1. 🎬 Toy Story (1995) - Rating: 8.3/10
   Genre: Animation, Adventure, Comedy
   Plot: A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room.
   🔗 IMDb: https://www.imdb.com/title/tt0114709/
```

## 🔧 Technical Details

### Emotion Detection
- Uses `nateraw/bert-base-uncased-emotion` transformer model
- Fallback to `distilbert-base-uncased-finetuned-sst-2-english` for sentiment
- Normalizes emotions to standard categories for consistent mapping

### Movie Recommendation
- Integrates with OMDb API for real-time movie data
- Searches multiple keywords per genre for variety
- Returns detailed movie information including:
  - Title, year, genre, director
  - Plot summary and IMDb rating
  - Poster image and IMDb link
  - Removes duplicates and shuffles results

### Error Handling
- Graceful API failure handling
- Fallback to local CSV dataset
- Confidence level warnings for unclear emotions
- User-friendly error messages

## 🛠️ Configuration

### API Settings
Edit `credentials.json` to modify API configuration:
```json
{
  "omdb_api_key": "your_api_key_here",
  "api_base_url": "http://www.omdbapi.com/"
}
```

### Emotion Mapping
Modify the `emotion_genre_mapping` dictionary in `recommender.py` to customize genre associations.

### Fallback Dataset
Add more movies to `movies.csv` following the existing format for expanded offline recommendations.

## 🧪 Testing

Run individual modules for testing:

```bash
# Test emotion detection
python emotion_model.py

# Test movie recommendations
python recommender.py

# Test full system
python main.py
```

## 📋 Dependencies

- **transformers**: For emotion detection models
- **torch**: PyTorch backend for transformers
- **requests**: HTTP requests to OMDb API
- **json**: JSON handling (built-in)
- **random**: Result shuffling (built-in)

## 🚨 Troubleshooting

### Common Issues

1. **"No module named 'transformers'"**
   ```bash
   pip install transformers torch
   ```

2. **API key errors**
   - Verify `credentials.json` exists and contains valid API key
   - Check internet connection
   - Ensure API key has remaining quota

3. **Slow first run**
   - First run downloads the emotion detection model (~400MB)
   - Subsequent runs are much faster

4. **No movie recommendations**
   - Check API key validity
   - Verify internet connection
   - System falls back to local CSV automatically

## 🎯 Future Enhancements

- [ ] Support for multiple languages
- [ ] User preference learning
- [ ] Integration with streaming services
- [ ] Movie trailer integration
- [ ] Social sharing features
- [ ] Advanced emotion detection (facial/voice)

## 📄 License

This project is for educational and personal use. Movie data is provided by OMDb API.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the system!

---

**Enjoy discovering movies that match your mood! 🎬✨**
