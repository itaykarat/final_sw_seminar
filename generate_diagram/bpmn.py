import os
from github import Github
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Insert your personal access token here
g = Github("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")

def extract_commits(github_project_url, num_commits=100):
    # Extracts the username and repo name from the URL
    username, repo_name = github_project_url.split('/')[-2:]

    # Gets the repository
    repo = g.get_user(username).get_repo(repo_name)

    # Gets the commits for the repository
    commits = repo.get_commits()[:num_commits]  # limit number of commits

    commit_data = []
    for commit in commits:
        committer_name = commit.commit.committer.name
        commit_message = commit.commit.message
        commit_message = ' '.join(commit_message.split())  # Removes newlines and extra spaces
        commit_data.append((committer_name, commit_message))

    return commit_data

def convert_commits_to_bpmn_format(commit_data): # still checking
    bpmn_format_text = []
    for i, (committer_name, commit_text) in enumerate(commit_data):
        if i == 0:  # start event
            bpmn_format_text.append(f"{committer_name}: {commit_text}")
        else:  # intermediate activities
            bpmn_format_text.append(f" {committer_name}: {commit_text}")

    # Add end event
    bpmn_format_text.append("The process ends with the last commit.")
    
    return "\n".join(bpmn_format_text)

def generate_bpmn_image(bpmn_text):
    # Setup WebDriver options
    webdriver_options = Options()
    webdriver_options.add_argument("--headless")  # Comment this line if you want to see the browser automation
    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver_options)

    # Open bpmn sketch miner
    driver.get("https://www.bpmn-sketch-miner.ai")

    # Wait until page loads
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "logtext")))

    # Find text input element and clear it, then send bpmn_text to it
    text_input = driver.find_element(By.ID, "logtext")
    text_input.clear()
    text_input.send_keys(bpmn_text)

    # Find the button to generate the BPMN sketch
    button = driver.find_element(By.ID, "restalk")
    button.click()
    button = driver.find_element(By.ID, "button-option-layout-orientation-horizontal")
    button.click()
    button = driver.find_element(By.ID, "button-export-png")
    button.click()

    # Wait until the image loads
    time.sleep(10)  # add sleep to give time for image to render

    # Define the base filename
    base_filename = "bpmn_output"
    file_extension = ".png"
    filename_number = 0

    # Generate unique filename
    while os.path.isfile(os.path.join(r"C:\Users\97252\PycharmProjects\final_sw_seminar", f"{base_filename}{filename_number}{file_extension}")):
        filename_number += 1

    # Take a screenshot of the "restalk" element only
    restalk_element = driver.find_element(By.ID, "restalk")
    restalk_element.screenshot(os.path.join(r"C:\Users\97252\PycharmProjects\final_sw_seminar", f"{base_filename}{filename_number}{file_extension}"))

    # Close the browser
    driver.quit()

    print(f"BPMN image saved as {base_filename}{filename_number}{file_extension}")

def generate_diagram_from_github_project():
    github_project_url = "https://github.com/yeminch/Calculate"
    commit_texts = extract_commits(github_project_url)
    bpmn_format_text = convert_commits_to_bpmn_format(commit_texts)

    generate_bpmn_image(bpmn_format_text)


if __name__ == "__main__":
    github_project_url = "https://github.com/yeminch/Calculate"
    commit_texts = extract_commits(github_project_url)
    bpmn_format_text = convert_commits_to_bpmn_format(commit_texts)

    generate_bpmn_image(bpmn_format_text)
