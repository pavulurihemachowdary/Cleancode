import streamlit as st
import pycodestyle
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os


def airbnb_javascript_style_guide(code_input):
    # Placeholder for Airbnb JavaScript style guide checks
    # You might want to integrate a JavaScript linter or style guide checker
    # For example, 'eslint' is a popular JavaScript linter

    # For this example, we assume that the code follows the Airbnb JavaScript style guide
    # You can replace this with a more comprehensive JavaScript linting or style guide check
    return True, []

# Unchanged code for Python and HTML checks
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

def html_checks(code_input):
    # Initialize score and error message list
    score = 10
    error_msgs = []

    # Check HTML code for compliance with standards
    # Example HTML checks
    if '<html' not in code_input.lower():
        score -= 1
        error_msgs.append('\nMissing <html> tag in HTML code.')

    # Add more HTML checks as needed

    return score, error_msgs

# Unchanged code for CSS and JavaScript checks
def airbnb_css_style_guide(css_code):
    # Placeholder for Airbnb CSS style guide checks
    # You might want to integrate a CSS linter or style guide checker
    # For example, 'stylelint' is a popular CSS linter

    # For this example, we assume that the code follows the Airbnb CSS style guide
    # You can replace this with a more comprehensive CSS linting or style guide check
    return True, []

def css_checks(code_input):
    # Placeholder for CSS checks
    score = 10
    error_msgs = []

    # Additional CSS checks
    airbnb_valid, airbnb_errors = airbnb_css_style_guide(code_input)
    if not airbnb_valid:
        score -= 1
        error_msgs.append('\nCSS does not follow the Airbnb Style Guide.')
        error_msgs.extend([f'\nAirbnb Error: {error}' for error in airbnb_errors])

    # Add more CSS checks as needed

    return score, error_msgs

# Unchanged code for Java checks
def java_checks(code_input):
    # Placeholder for Java checks
    score = 10
    error_msgs = []

    # Additional Java checks
    # Add your specific Java checks here

    return score, error_msgs

if __name__ == "__main__":
    # Load Python, HTML, CSS, JavaScript, and Java snippet dictionaries
    with open('./code_model/python_snippets.pkl', 'rb') as f_python, \
            open('./code_model/html_snippets.pkl', 'rb') as f_html, \
            open('./code_model/css_snippets.pkl', 'rb') as f_css, \
            open('./code_model/js_snippets.pkl', 'rb') as f_js, \
            open('./code_model/java_snippets.pkl', 'rb') as f_java:
        snippet_dict_python = pickle.load(f_python)
        snippet_dict_html = pickle.load(f_html)
        snippet_dict_css = pickle.load(f_css)
        snippet_dict_js = pickle.load(f_js)
        snippet_dict_java = pickle.load(f_java)

    # Combine all snippets into a single dictionary
    snippet_dict_combined = {
        **snippet_dict_python,
        **snippet_dict_html,
        **snippet_dict_css,
        **snippet_dict_js,
        **snippet_dict_java
    }

    st.title('Recommendation System')
    col1, col2 = st.columns(2, gap="large")

    with col1:
        # Get code input from user
        options = st.selectbox('Select a Programming Language (#Default : Python):', ('Python', 'HTML', 'CSS', 'JavaScript', 'Java'))

        code_input = st.text_area('Enter your code here:', height=350)

        # Initialize score and error message list
        score = 10
        error_msgs = []

        # Check code for compliance with standards
        if code_input:
            if options == 'Python':
                # Unchanged Python checks
                # Example Python checks
                # Check for meaningful variable names
                if code_input and code_input[0].isdigit():
                    score -= 1
                    error_msgs.append('\nVariable names are not valid.')
    
                # Check for clean code
                if code_input and 'if' in code_input and ':' not in code_input:
                    score -= 1
                    error_msgs.append('\nUse a colon after the "if" statement.')
                if code_input and 'def' in code_input and ':' not in code_input:
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
                if code_input and '#' not in code_input:
                    score -= 1
                    error_msgs.append('\nAdd comments to explain your code.')
    
                # Check for modular code
                if code_input and 'global' in code_input:
                    score -= 1
                    error_msgs.append('\nTry to avoid using global variables.')
    
                # Check for error handling
                if code_input and 'try' not in code_input:
                    score -= 1
                    error_msgs.append('\nAdd error handling to your code.')
                    
                # Check for documentation
                if code_input and '"""' not in code_input:
                    score -= 1
                    error_msgs.append('\nAdd documentation to your code.')

            elif options == 'HTML':
                # Unchanged HTML checks
                html_score, html_errors = html_checks(code_input)
                score -= html_score
                error_msgs.extend(html_errors)

            elif options == 'CSS':
                # Additional CSS checks
                css_score, css_errors = css_checks(code_input)
                score -= css_score
                error_msgs.extend(css_errors)

            elif options == 'JavaScript':
                # Unchanged JavaScript checks
                # Example JavaScript checks
                # ...
                javascript_valid, javascript_errors = airbnb_javascript_style_guide(code_input)
                if not javascript_valid:
                    score -= 1
                    error_msgs.append('\nJavaScript does not follow the Airbnb Style Guide.')
                    error_msgs.extend([f'\nAirbnb Error: {error}' for error in javascript_errors])

                # Add more JavaScript checks as needed

            elif options == 'Java':
                # Additional Java checks
                java_score, java_errors = java_checks(code_input)
                score -= java_score
                error_msgs.extend(java_errors)

            if score == 10:
                st.success(u'\u2713' + '\t\tYour code meets all code standards!')
            else:
                error_message = ' '.join(error_msgs)
                st.markdown(f"### Score : **{score}**/10")
                st.warning(f'Your code does not meet these code standards.')
                st.warning(f'{error_message}')

        else:
            st.warning('Please enter some code to check.')

    with col2:
        st.subheader("Recommended Code")
        if not code_input:
            st.write("Write some code to recommend")
        else:
            input_str = code_input
            recommendations = recommend_code(input_str, snippet_dict_combined, n=5)
            for snippet_id, code_snippet in recommendations:
                st.write('Snippet ID:', snippet_id)
                st.code(code_snippet)
                st.write()

