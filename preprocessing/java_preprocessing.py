import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

def preprocess_java_dataset(java_dataset_path, output_pkl_path):
    # Load Java dataset from CSV
    java_df = pd.read_csv(java_dataset_path)

    # Check if the dataset contains the correct column names
    expected_columns = ['snippet_id', 'java_code']
    if not all(col in java_df.columns for col in expected_columns):
        raise ValueError(f"Expected columns {expected_columns} not found in the Java dataset.")

    # Drop rows with NaN values in 'java_code' column
    java_df = java_df.dropna(subset=['java_code'])

    # Perform any additional cleaning or preprocessing if needed

    # Tokenization or Vectorization
    vectorizer = TfidfVectorizer()
    java_vectors = vectorizer.fit_transform(java_df['java_code'])

    # Save Preprocessed Data to Pickle
    java_snippets_dict = dict(zip(java_df['snippet_id'], java_df['java_code']))

    # Specify the directory where the code_model is located
    code_model_directory = 'code_model'

    # Ensure the code_model directory exists
    os.makedirs(code_model_directory, exist_ok=True)

    # Save the pickle file in the code_model directory
    output_pkl_path = os.path.join(code_model_directory, output_pkl_path)
    with open(output_pkl_path, 'wb') as f:
        pickle.dump(java_snippets_dict, f)

if __name__ == "__main__":
    java_dataset_path = '/Users/hemapavuluri/Documents/project/java_dataset.csv'
    output_pkl_path = 'java_snippets.pkl'
    preprocess_java_dataset(java_dataset_path, output_pkl_path)
