from typing import List, Set

import nltk
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import PyPDF2

# Download NLTK resources if not already present
nltk.download('punkt')
nltk.download('stopwords')

def extract_text_from_pdf(pdf_path: str) -> str:
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
    return text

def preprocess_text(text: str) -> List[List[str]]:
    # Tokenize the text into sentences and then words
    sentences = sent_tokenize(text)
    words = [word_tokenize(sentence) for sentence in sentences]

    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    filtered_words = [[word.lower() for word in sentence if word.isalpha() and word.lower() not in stop_words] for sentence in words]

    return filtered_words

def label_characters(text: List[List[str]]) -> Set[str]:
    #????HOW DO I DIVIDE THIS????

    labeled_characters = set(word for sentence in text for word in sentence if word.istitle())#ONLY SENTENCES

    return labeled_characters

def preprocess_and_save(pdf_path: str, output_csv: str) -> None:
    book_text = extract_text_from_pdf(pdf_path)
    processed_text = preprocess_text(book_text)
    labeled_characters = label_characters(processed_text)

    # Create a DataFrame and save it to CSV
    df = pd.DataFrame({
        'chapter_text': [book_text],
        'processed_text': [processed_text],
        'labeled_characters': [labeled_characters]
    })
    df.to_csv(output_csv, index=False)


pdf_path = 'your_book.pdf'
output_csv = 'preprocessed_data.csv'

preprocess_and_save(pdf_path, output_csv)
