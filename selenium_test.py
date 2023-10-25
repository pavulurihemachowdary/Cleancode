import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up the Selenium driver
driver = webdriver.Chrome('./webdriver/chromedriver')

# Start the Streamlit app
driver.get("https://pavulurihemac-cleancode-saslyelfjbx.ws-us105.gitpod.io/")

# Define a function to run the tests for each file and store the results
def run_tests(filename):
    # Load the file
    with open(filename, "r") as f:
        code = f.read()

    # Find the textarea element and paste the code into it
    textarea = driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/div/div/section/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div[1]/div/div[1]/div/div/textarea")
    textarea.send_keys(Keys.CONTROL + "a")
    textarea.send_keys(Keys.DELETE)
    textarea.send_keys(code)

    # Click the "Run" button
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()

    # Wait for the results to load
    time.sleep(1)

    # Find the score element and extract the text
    score_element = driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/div/div/section/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div[2]/div/div/div/h3/div/span")
    score = float(score_element.text.split(":")[1])

    # Store the results in a Pandas DataFrame
    results = pd.DataFrame({
        "filename": [filename],
        "score": [score]
    })

    return results

# Create an empty DataFrame to store the results
all_results = pd.DataFrame(columns=["filename", "score"])

# Run the tests for each file and store the results in the DataFrame
for filename in os.listdir("path/to/python/files"):
    if filename.endswith(".py"):
        results = run_tests(os.path.join("path/to/python/files", filename))
        all_results = pd.concat([all_results, results], ignore_index=True)

# Print the results
print(all_results)
