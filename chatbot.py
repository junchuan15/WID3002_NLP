import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('punkt')

# Load JSON data
with open('reg_qna.json', 'r') as file:
    qna_data = json.load(file)

# Preprocess data
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenization and lowercasing
    tokens = [stemmer.stem(token) for token in tokens if token.isalnum()]  # Stemming
    tokens = [token for token in tokens if token not in stop_words]  # Stop words removal
    return ' '.join(tokens)

# Preprocess questions
preprocessed_questions = [preprocess_text(qa['question']) for qa in qna_data['questions_and_answers']]

# Vectorize preprocessed questions
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(preprocessed_questions)

# Main loop
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Bot: Goodbye!")
        break

    # Preprocess user input
    preprocessed_input = preprocess_text(user_input)

    # Vectorize user input
    input_vector = vectorizer.transform([preprocessed_input])

    # Calculate cosine similarities
    similarities = cosine_similarity(input_vector, X)

    # Find closest question
    closest_question_idx = similarities.argmax()
    closest_question = qna_data['questions_and_answers'][closest_question_idx]

    # Check similarity threshold
    if similarities[0, closest_question_idx] < 0.5:
        print("Bot: Sorry, I couldn't understand your question.")
    else:
        print("Bot:", closest_question['answer'])
