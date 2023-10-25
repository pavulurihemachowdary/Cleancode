import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

def preprocess_html_dataset(html_dataset_path, html_scripts_folder, output_pkl_path):
    # Load existing HTML dataset
    existing_html_df = pd.read_csv(html_dataset_path)

    # Create a new DataFrame for the HTML scripts in the folder
    new_html_df = pd.DataFrame(columns=['snippet_id', 'html_code'])

    # Iterate through files in the HTML scripts folder
    for filename in os.listdir(html_scripts_folder):
        if filename.endswith('.html'):
            snippet_id = os.path.splitext(filename)[0]
            file_path = os.path.join(html_scripts_folder, filename)

            # Read the HTML content from the file
            with open(file_path, 'r') as file:
                html_code = file.read()

            # Append the new HTML script to the new DataFrame
            new_row = {'snippet_id': snippet_id, 'html_code': html_code}
            new_html_df = pd.concat([new_html_df, pd.DataFrame([new_row])], ignore_index=True)

    # Concatenate the existing and new DataFrames
    combined_html_df = pd.concat([existing_html_df, new_html_df], ignore_index=True)

    # Perform any additional cleaning or preprocessing if needed

    # Tokenization or Vectorization
    vectorizer = TfidfVectorizer()
    html_vectors = vectorizer.fit_transform(combined_html_df['html_code'])

    # Save Preprocessed Data to Pickle
    html_snippets_dict = dict(zip(combined_html_df['snippet_id'], combined_html_df['html_code']))

    # Specify the directory where the code_model is located
    code_model_directory = 'code_model'

    # Ensure the code_model directory exists
    os.makedirs(code_model_directory, exist_ok=True)

    # Save the pickle file in the code_model directory
    output_pkl_path = os.path.join(code_model_directory, output_pkl_path)
    with open(output_pkl_path, 'wb') as f:
        pickle.dump(html_snippets_dict, f)

if __name__ == "__main__":
    html_dataset_path = '/Users/hemapavuluri/Documents/project/html_dataset.csv'
    html_scripts_folder = '/Users/hemapavuluri/Documents/project/archive2/dataset/HTML'
    output_pkl_path = 'html_snippets.pkl'

    preprocess_html_dataset(html_dataset_path, html_scripts_folder, output_pkl_path)

