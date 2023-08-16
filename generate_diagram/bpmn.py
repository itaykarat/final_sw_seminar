import os
import requests
from github import Github
import github
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
    try:


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
    except github.UnknownObjectException:
            print(f"Repository {username}/{repo_name} not found.")
            return []
    except Exception as e:
            print(f"An error occurred: {e}")
            return []



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
def remove_non_bmp_characters(text):
      return ''.join(c for c in text if 0x0000 <= ord(c) <= 0xFFFF)

def generate_bpmn_image(bpmn_text):
    # Setup WebDriver options
    webdriver_options = Options()
    webdriver_options.add_argument("--headless")  # Comment this line if you want to see the browser automation
    # Setup WebDriver
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver_options)

    CHROME_VERSION = "115.0.5790.171"  # Update this if you use a different version
    DASHBOARD_ENDPOINT = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

    response = requests.get(DASHBOARD_ENDPOINT)
    response_data = response.json()
    # print(response_data)
    chromedriver_url = response_data['channels']['Dev']['downloads']['chromedriver'][0]['url']

   # chromedriver_url = response_data['C:/Users/hasan/Downloads/chromedriver-win64/chromedriver-win64']  # Adjust based on the actual JSON structure

    # Now, instead of using ChromeDriverManager, directly use the downloaded ChromeDriver
    chromedriver_url = "C:/Users/jawad/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
   # driver = webdriver.Chrome(executable_path=driver_path)
    service = Service(executable_path=chromedriver_url)



# Create a Chrome driver instance using the service
    driver = webdriver.Chrome(service=service)
    # Open bpmn sketch miner
    driver.get("https://www.bpmn-sketch-miner.ai")

    # Wait until page loads
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "logtext")))

    # Find text input element and clear it, then send bpmn_text to it
    text_input = driver.find_element(By.ID, "logtext")
    text_input.clear()
    filtered_bpmn_text = remove_non_bmp_characters(bpmn_text)
    text_input.send_keys(filtered_bpmn_text)


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
    filename_number2 = 1

    # Generate unique filename
    while os.path.isfile(os.path.join(r'C:/Users/jawad/Downloads/seminar/seminar/seminar/seminar', f"{base_filename}{filename_number2}{file_extension}")):
        filename_number2 += 1

    # Take a screenshot of the "restalk" element only
    restalk_element = driver.find_element(By.ID, "restalk")
    restalk_element.screenshot(os.path.join(r'C:/Users/jawad/Downloads/seminar/seminar/seminar/seminar', f"{base_filename}{filename_number2}{file_extension}"))

    # Close the browser
    driver.quit()

    print(f"BPMN image saved as {base_filename}{filename_number2}{file_extension}")

def generate_diagram_from_github_project(url):
    github_project_url = url
    commit_texts = extract_commits(github_project_url)
    bpmn_format_text = convert_commits_to_bpmn_format(commit_texts)

    generate_bpmn_image(bpmn_format_text)


if __name__ == "__main__":
    github_project_url = "https://github.com/yeminch/Calculate"
    commit_texts = extract_commits(github_project_url)
    bpmn_format_text = convert_commits_to_bpmn_format(commit_texts)

    generate_bpmn_image(bpmn_format_text)
