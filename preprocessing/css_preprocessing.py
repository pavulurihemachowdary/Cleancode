import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

def preprocess_css_dataset(css_dataset_path, output_pkl_path):
    # Load CSS dataset from CSV
    css_df = pd.read_csv(css_dataset_path)

    # Drop rows with NaN values in 'css_code' column
    css_df = css_df.dropna(subset=['css_code'])

    # Perform any additional cleaning or preprocessing if needed

    # Tokenization or Vectorization
    vectorizer = TfidfVectorizer()
    css_vectors = vectorizer.fit_transform(css_df['css_code'])

    # Save Preprocessed Data to Pickle
    css_snippets_dict = dict(zip(css_df['snippet_id'], css_df['css_code']))

    # Specify the directory where the code_model is located
    code_model_directory = 'code_model'

    # Ensure the code_model directory exists
    os.makedirs(code_model_directory, exist_ok=True)

    # Save the pickle file in the code_model directory
    output_pkl_path = os.path.join(code_model_directory, output_pkl_path)
    with open(output_pkl_path, 'wb') as f:
        pickle.dump(css_snippets_dict, f)

if __name__ == "__main__":
    css_dataset_path = '/Users/hemapavuluri/Documents/project/css_dataset.csv'
    output_pkl_path = 'css_snippets.pkl'
    preprocess_css_dataset(css_dataset_path, output_pkl_path)
