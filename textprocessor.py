
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

nlp = spacy.load('en_core_web_sm')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

class TextPreprocessor:
    def __init__(self):
        # Initialize tokenizer, lemmatizer, stopwords and punctuation
        self.punctuation = string.punctuation

    def clean_text(self, text):
        """
        Preprocess the text to reduce tokens and retain important keywords.

        Args:
            text (str): The input text to be processed.

        Returns:
            str: The cleaned and reduced text.
        """
        tokens = word_tokenize(text)
        tokens = [token.lower() for token in tokens]
        tokens = [token for token in tokens if token not in stop_words and token not in self.punctuation]
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

        return ' '.join(lemmatized_tokens)

    def extract_key_phrases(self, text):
        """
        Extract key phrases from the text based on nouns, verbs, and adjectives.

        Args:
            text (str): The input text to extract key phrases from.

        Returns:
            list: A list of important words or phrases.
        """
        doc = nlp(text)

        key_phrases = []
        for token in doc:
            # Add noun, verb, and adjective tokens
            if token.pos_ in ['NOUN', 'VERB', 'ADJ']:
                key_phrases.append(token.lemma_)

        return key_phrases

    def preprocess_for_llm(self, text):
        """
        Preprocess text and extract important words to give a hint about what the user learned.

        Args:
            text (str): The raw input text.

        Returns:
            dict: Contains preprocessed text and key phrases.
        """
        cleaned_text = self.clean_text(text)

        key_phrases = self.extract_key_phrases(text)

        return {
            'cleaned_text': cleaned_text,
            'key_phrases': key_phrases
        }


if __name__ == "__main__":
    input_text = """
    Welcome to the complete HTML and CSS course. In this course, we're going to learn how to build websites
    from a beginner to a professional level, and by the end of this course, we're going to build youtube.com.
    Now you don't need any previous coding or technical experience. This course is designed to be your first
    step to becoming a software engineer.
    """

    # Initialize the preprocessor
    preprocessor = TextPreprocessor()

    # Preprocess the text
    result = preprocessor.preprocess_for_llm(input_text)

    print("Key Phrases: ", result['key_phrases'])
