"""
Main Execution Script for Mood-Based Movie Recommendation System

This script ties together emotion detection and movie recommendation modules
to provide a complete user experience. It follows the exact flow specified
in instructions.md.

Usage:
    python main.py

Dependencies:
    - emotion_model
    - recommender
    - transformers
    - torch
    - requests
"""

from emotion_model import EmotionDetector, detect_emotion_detailed
from recommender import MovieRecommender
import sys
import time

class MoodMovieRecommendationAgent:
    """
    Main class that orchestrates the mood-based movie recommendation process.
    """
    
    def __init__(self):
        """
        Initialize the recommendation agent with emotion detector and movie recommender.
        """
        print("🎬 Initializing Mood-Based Movie Recommendation Agent...")
        print("=" * 60)
        
        try:
            # Initialize emotion detector
            print("🧠 Loading emotion detection model...")
            self.emotion_detector = EmotionDetector()
            
            # Initialize movie recommender
            print("🎭 Loading movie recommendation system...")
            self.movie_recommender = MovieRecommender()
            
            print("✅ System ready! Let's find some great movies for your mood!")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error initializing system: {e}")
            print("Please make sure all dependencies are installed and credentials.json exists.")
            sys.exit(1)
    
    def analyze_mood_and_recommend(self, user_input, num_recommendations=3):
        """
        Complete workflow: analyze mood and recommend movies.
        
        Args:
            user_input (str): User's mood description
            num_recommendations (int): Number of movies to recommend
            
        Returns:
            dict: Results containing emotion analysis and movie recommendations
        """
        # Step 1: Detect emotion from user input
        print(f"🔍 Analyzing your mood: '{user_input}'")
        emotion_result = self.emotion_detector.detect_emotion(user_input)
        
        detected_emotion = emotion_result['normalized_emotion']
        confidence = emotion_result['confidence']
        confidence_level = self.emotion_detector.get_emotion_confidence_level(confidence)
        
        print(f"🎭 Detected emotion: {detected_emotion} (confidence: {confidence:.2f} - {confidence_level})")
        
        # Step 2: Check if confidence is too low
        if confidence < 0.4:
            print("⚠️  Emotion detection confidence is low. You might want to provide more detail.")
            print("💡 Try describing your mood with more specific words or context.")
        
        # Step 3: Get movie recommendations based on emotion
        print(f"🎬 Finding movies that match your {detected_emotion} mood...")
        
        try:
            recommendations = self.movie_recommender.recommend_movies(
                detected_emotion, 
                num_recommendations
            )
            
            if not recommendations:
                print("❌ Sorry, couldn't find movies for your current mood.")
                print("🔄 Try describing your mood differently or check your internet connection.")
                return None
            
            # Step 4: Display recommendations
            print(f"\n🌟 Here are {len(recommendations)} movies perfect for your {detected_emotion} mood:")
            print("=" * 70)
            
            for i, movie in enumerate(recommendations, 1):
                print(f"\n{i}. {self.movie_recommender.format_movie_output(movie)}")
                print("-" * 70)
            
            return {
                'emotion_analysis': emotion_result,
                'detected_emotion': detected_emotion,
                'confidence': confidence,
                'confidence_level': confidence_level,
                'recommendations': recommendations,
                'genres': self.movie_recommender.get_genres_for_emotion(detected_emotion)
            }
            
        except Exception as e:
            print(f"❌ Error getting movie recommendations: {e}")
            return None
    
    def interactive_mode(self):
        """
        Run the agent in interactive mode for continuous use.
        """
        print("\\n🎯 Welcome to Interactive Movie Recommendation Mode!")
        print("💬 Describe your current mood and I'll recommend movies for you.")
        print("💡 Examples: 'I feel happy', 'I'm sad today', 'I want something exciting'")
        print("🚪 Type 'quit', 'exit', or 'bye' to stop.\\n")
        
        while True:
            try:
                # Get user input
                user_input = input("🎭 How are you feeling today? ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\\n👋 Thanks for using the Mood-Based Movie Recommendation Agent!")
                    print("🎬 Happy watching! See you next time!")
                    break
                
                # Skip empty input
                if not user_input:
                    print("⚠️  Please tell me how you're feeling!")
                    continue
                
                print("-" * 70)
                
                # Analyze mood and get recommendations
                result = self.analyze_mood_and_recommend(user_input)
                
                if result:
                    # Ask if user wants more recommendations
                    print(f"\\n💫 Want more {result['detected_emotion']} movies? (y/n): ", end="")
                    more_input = input().strip().lower()
                    
                    if more_input in ['y', 'yes']:
                        print("🔄 Getting more recommendations...")
                        self.analyze_mood_and_recommend(user_input, num_recommendations=5)
                
                print("\\n" + "=" * 70)
                print("🔄 Ready for another mood analysis!\\n")
                
            except KeyboardInterrupt:
                print("\\n\\n👋 Goodbye! Thanks for using the Movie Recommendation Agent!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                print("🔄 Let's try again!\\n")


def main():
    """
    Main function following the exact flow from instructions.md
    """
    print("🎬 Mood-Based Movie Recommendation System")
    print("🤖 AI-Powered Movie Discovery Based on Your Current Mood")
    print("=" * 70)
    
    try:
        # Initialize the recommendation agent
        agent = MoodMovieRecommendationAgent()
        
        # Check if running with command line arguments
        if len(sys.argv) > 1:
            # Command line mode - use provided mood description
            user_input = " ".join(sys.argv[1:])
            print(f"🎯 Command line mode: Analyzing mood '{user_input}'")
            result = agent.analyze_mood_and_recommend(user_input)
            
            if result:
                print("\\n✨ Recommendation complete! Enjoy your movies!")
        else:
            # Interactive mode
            agent.interactive_mode()
            
    except Exception as e:
        print(f"❌ System error: {e}")
        print("🔧 Please check your setup and try again.")
        sys.exit(1)


# Example workflow function as shown in instructions.md
def example_workflow():
    """
    Example workflow demonstrating the basic flow from instructions.md
    """
    from emotion_model import detect_emotion
    from recommender import recommend_movies
    
    # Simulate user input
    user_input = "I feel really happy and excited today!"
    
    # Detect emotion
    emotion = detect_emotion(user_input)
    
    # Get movie recommendations
    suggestions = recommend_movies(emotion)
    
    # Display results
    print(f"Detected emotion: {emotion}")
    print("Movie recommendations:")
    for movie in suggestions:
        print(f"• {movie['title']} ({movie['year']}): {movie['link']}")


if __name__ == "__main__":
    # Run the main application
    main()
    
    # Uncomment below to run the simple example workflow
    # print("\\n" + "="*50)
    # print("Running example workflow from instructions.md:")
    # example_workflow()
