import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

def preprocess_javascript_dataset(js_dataset_path, output_pkl_path):
    # Load JavaScript dataset from CSV
    js_df = pd.read_csv(js_dataset_path)

    # Check if the dataset contains the correct column names
    expected_columns = ['snippet_id', 'js_code']
    if not all(col in js_df.columns for col in expected_columns):
        raise ValueError(f"Expected columns {expected_columns} not found in the JavaScript dataset.")

    # Drop rows with NaN values in 'js_code' column
    js_df = js_df.dropna(subset=['js_code'])

    # Perform any additional cleaning or preprocessing if needed

    # Tokenization or Vectorization
    vectorizer = TfidfVectorizer()
    js_vectors = vectorizer.fit_transform(js_df['js_code'])

    # Save Preprocessed Data to Pickle
    js_snippets_dict = dict(zip(js_df['snippet_id'], js_df['js_code']))

    # Specify the directory where the code_model is located
    code_model_directory = 'code_model'

    # Ensure the code_model directory exists
    os.makedirs(code_model_directory, exist_ok=True)

    # Save the pickle file in the code_model directory
    output_pkl_path = os.path.join(code_model_directory, output_pkl_path)
    with open(output_pkl_path, 'wb') as f:
        pickle.dump(js_snippets_dict, f)

if __name__ == "__main__":
    js_dataset_path = '/Users/hemapavuluri/Documents/project/js_dataset.csv'
    output_pkl_path = 'js_snippets.pkl'
    preprocess_javascript_dataset(js_dataset_path, output_pkl_path)
