"""
Emotion Detection Module for Mood-Based Movie Recommendation System

This module handles emotion detection from user text input using a pre-trained
transformer model from HuggingFace. It analyzes the user's mood description
and returns the predicted emotion label.

Dependencies:
- transformers
- torch
"""

from transformers import pipeline
import warnings

# Suppress transformers warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

class EmotionDetector:
    """
    A class to detect emotions from text using a pre-trained transformer model.
    """
    
    def __init__(self):
        """
        Initialize the emotion detection pipeline using a pre-trained model.
        Uses nateraw/bert-base-uncased-emotion for robust emotion classification.
        """
        try:
            # Load the pre-trained emotion classification model
            self.classifier = pipeline(
                "text-classification",
                model="nateraw/bert-base-uncased-emotion",
                device=-1  # Use CPU (set to 0 for GPU if available)
            )
            print("✅ Emotion detection model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading emotion model: {e}")
            print("🔄 Falling back to basic sentiment analysis...")
            
            # Fallback to basic sentiment if emotion model fails
            self.classifier = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
    
    def detect_emotion(self, text):
        """
        Detect emotion from user input text.
        
        Args:
            text (str): User's mood description
            
        Returns:
            dict: Contains emotion label, confidence score, and normalized emotion
        """
        if not text or not text.strip():
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'raw_prediction': None,
                'normalized_emotion': 'neutral'
            }
        
        try:
            # Get prediction from the model
            prediction = self.classifier(text.strip())
            
            # Extract the top prediction
            top_prediction = prediction[0] if isinstance(prediction, list) else prediction
            emotion_label = top_prediction['label'].lower()
            confidence = top_prediction['score']
            
            # Normalize emotion labels to standard categories
            normalized_emotion = self._normalize_emotion(emotion_label)
            
            return {
                'emotion': emotion_label,
                'confidence': confidence,
                'raw_prediction': top_prediction,
                'normalized_emotion': normalized_emotion
            }
            
        except Exception as e:
            print(f"❌ Error during emotion detection: {e}")
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'raw_prediction': None,
                'normalized_emotion': 'neutral'
            }
    
    def _normalize_emotion(self, emotion_label):
        """
        Normalize various emotion labels to standard categories that map to movie genres.
        
        Args:
            emotion_label (str): Raw emotion label from the model
            
        Returns:
            str: Normalized emotion category
        """
        # Mapping from model outputs to our standard emotion categories
        emotion_mapping = {
            # Joy/Happiness categories
            'joy': 'joy',
            'happiness': 'joy',
            'love': 'love',
            'positive': 'joy',
            
            # Sadness categories
            'sadness': 'sadness',
            'grief': 'sadness',
            'negative': 'sadness',
            
            # Anger categories
            'anger': 'anger',
            'rage': 'anger',
            'frustration': 'anger',
            
            # Fear categories
            'fear': 'fear',
            'anxiety': 'fear',
            'worry': 'fear',
            
            # Surprise categories
            'surprise': 'surprise',
            'amazement': 'surprise',
            
            # Neutral/Other
            'neutral': 'neutral',
            'disgust': 'neutral',  # Map disgust to neutral for movie recommendations
            'anticipation': 'surprise',
            'trust': 'joy'
        }
        
        return emotion_mapping.get(emotion_label, 'neutral')
    
    def get_emotion_confidence_level(self, confidence):
        """
        Categorize confidence level for better user feedback.
        
        Args:
            confidence (float): Confidence score from model
            
        Returns:
            str: Confidence level description
        """
        if confidence >= 0.8:
            return "high"
        elif confidence >= 0.6:
            return "medium"
        elif confidence >= 0.4:
            return "low"
        else:
            return "very_low"


def detect_emotion(text):
    """
    Convenience function for quick emotion detection.
    
    Args:
        text (str): User's mood description
        
    Returns:
        str: Normalized emotion label
    """
    detector = EmotionDetector()
    result = detector.detect_emotion(text)
    return result['normalized_emotion']


def detect_emotion_detailed(text):
    """
    Convenience function for detailed emotion detection with confidence scores.
    
    Args:
        text (str): User's mood description
        
    Returns:
        dict: Detailed emotion analysis results
    """
    detector = EmotionDetector()
    return detector.detect_emotion(text)


# Test function for development
if __name__ == "__main__":
    # Test the emotion detection
    test_inputs = [
        "I feel really happy today!",
        "I'm so sad and lonely",
        "I'm really angry about this situation",
        "I'm scared and nervous",
        "What a surprise! I didn't expect that",
        "I feel pretty neutral about everything"
    ]
    
    print("🧪 Testing Emotion Detection Module")
    print("=" * 40)
    
    detector = EmotionDetector()
    
    for text in test_inputs:
        result = detector.detect_emotion(text)
        confidence_level = detector.get_emotion_confidence_level(result['confidence'])
        
        print(f"Input: '{text}'")
        print(f"Detected: {result['normalized_emotion']} (confidence: {result['confidence']:.2f} - {confidence_level})")
        print("-" * 40)
