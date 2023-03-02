import streamlit as st
import pycodestyle
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_code(input_str, snippet_dict, n=5):
    # Initialize the TfidfVectorizer
    vectorizer = TfidfVectorizer()
    # Extract the code snippets and their ids from the snippet_dict
    code_ids = []
    code_list = []
    for snippet_id, code_snippet in snippet_dict.items():
        code_ids.append(snippet_id)
        code_list.append(code_snippet)

    # Vectorize the code snippets
    code_vectors = vectorizer.fit_transform(code_list)

    # Vectorize the input code snippet
    input_vector = vectorizer.transform([input_str])

    # Calculate the cosine similarity between the input vector and the code snippet vectors
    similarities = cosine_similarity(input_vector, code_vectors).flatten()

    # Get the indices of the most similar code snippets
    if len(similarities) < n:
        n = len(similarities)
    indices = similarities.argsort()[-n:]

    # Create a list of (snippet_id, code_snippet) tuples for the top n recommendations
    recommendations = [(code_ids[i], code_list[i]) for i in indices]

    return recommendations

with open('./code_model/python_snippets.pkl', 'rb') as f:
    snippet_dict = pickle.load(f)


st.title('Clean Code')
col1, col2 = st.columns(2,gap="large")

with col1:
    # Get code input from user
    code_input = st.text_area('Enter your Python code here:', height=350)

    # Initialize score and error message list
    score = 10
    error_msgs = []

    # Check code for compliance with standards
    if code_input:
        # Check for meaningful variable names
        if code_input[0].isdigit():
            score -= 1
            error_msgs.append('\nVariable names is not valid.')
        
        # Check for clean code
        if 'if' in code_input and ':' not in code_input:
            score -= 1
            error_msgs.append('\nUse a colon after the "if" statement.')
        if 'def' in code_input and ':' not in code_input:
            score -= 1
            error_msgs.append('\nUse a colon after the "def" statement.')
        
        # Check for PEP 8 compliance
        style_guide = pycodestyle.StyleGuide()
        result = style_guide.input_file(code_input)
        pep8_score = round((result) * 10, 2)
        if result <= 0:
            score -= 1
            error_msgs.append('\nYour code does not meet PEP 8 guidelines.')
        
        # Check for effective comments
        if '#' not in code_input:
            score -= 1
            error_msgs.append('\nAdd comments to explain your code.')
        
        # Check for modular code
        if 'global' in code_input:
            score -= 1
            error_msgs.append('\nTry to avoid using global variables.')
        
        # Check for error handling
        if 'try' not in code_input:
            score -= 1
            error_msgs.append('\nAdd error handling to your code.')
        
        # Check for documentation
        if '"""' not in code_input:
            score -= 1
            error_msgs.append('\nAdd documentation to your code.')
        
        # Print score and error messages
        if score == 10:
            st.success(u'\u2713'+'\t\tYour code meets all Python code standards!')
        else:
            error_message = ' '.join(error_msgs)
            st.markdown(f"### Score : **{score}**/10")
            st.warning(f'Your code does not meet these Python code standards.')
            st.warning(f'{error_message}')
    else:
        st.warning('Please enter some code to check.')

with col2 :
    st.subheader("Reccomended Code")
    if not code_input:
        st.write("write some code to reccomend")
    else:
        input_str = code_input
        recommendations = recommend_code(input_str, snippet_dict, n=5)
        for snippet_id, code_snippet in recommendations:
            st.write('Snippet ID:', snippet_id)
            st.code(code_snippet)
            st.write()