from computer_vision_service.square_detection_cv import detection_in_image
from generate_diagram.bpmn import generate_diagram_from_github_project
from generate_diagram.bpmn import extract_commits
from read_data.read_tables import read_data_as_datafrane
import repos_urls
import cv2
import os
import requests
import plotly.figure_factory as ff

import pandas as pd
if __name__ == '__main__':

    """READING THE GITHUB DATA AND GENERATING A DIAGRAM FROM IT"""
    my_dict={}
    base_url = "https://data.gharchive.org/2015-01-01-{}.json.gz"
    urls_list = repos_urls.func(base_url)

    base_filename = "bpmn_output"
    file_extension = ".png"
    filename_numberr = 1

    i = 0
    created_at= ''
    num_pulls=0
    for url in urls_list:
        if i < 110:
            generate_diagram_from_github_project(url)
            while os.path.isfile(os.path.join(r'C:/Users/jawad/Downloads/seminar/seminar/seminar/seminar', f"{base_filename}{filename_numberr}{file_extension}")):
                filename_numberr += 1
            file_path = os.path.join(r'C:/Users/jawad/Downloads/seminar/seminar/seminar/seminar', f"{base_filename}{filename_numberr-1}{file_extension}")
            complexity_score = detection_in_image.detect_random_shaped_in_image(file_path,show_detection=True)
            commets_num = len(extract_commits(url))
            pullsurl = f"{url}/pulls"
            response1 = requests.get(pullsurl)
            data1 = response1.json()
            num_pulls= len(data1)

            response = requests.get(url)
            if response.status_code == 200:
             data = response.json()
             created_at = data.get('created_at', None)
             pullsurl = data.get('pulls_url')
             print(pullsurl)
             response1 = requests.get(pullsurl)

            my_dict[url] = {
            'url' : url,
            'complexity_score': complexity_score,
            'commits_num': commets_num,
            'created at' : created_at,
            'num_pulls': num_pulls
            }
            i=i+1


    data_rows = []
    for repo, values in my_dict.items():
     created_at = values['created at']
     complexity_score = values['complexity_score']
     commits_num = values['commits_num']
     push_num = values['commits_num']
     num_pulls = values['num_pulls']
     data_rows.append([repo, created_at, complexity_score, commits_num,push_num,num_pulls])

    columns = ['Repository', 'created at', 'Complexity_Score', 'Commits_Num','push_num','num_pulls']

    print(my_dict)
    # df = pd.DataFrame(my_dict)
    df = pd.DataFrame(data_rows, columns=columns)

    df.to_csv('my_dataframe.csv', index=False)
    df1= pd.read_csv(r'C:/Users/jawad/Downloads/seminar/my_dataframe.csv')
    df1 = df1.drop(columns=['Repository'])
    df1 = df1.drop(columns=['created at'])
    numeric_df = df1.select_dtypes(include=['float64', 'int64'])
    crr_matrix = numeric_df.corr()

    # crr_matrix = df1.corr()
    fig = ff.create_annotated_heatmap(
       z=crr_matrix.values,
       x=list(crr_matrix.index),
       annotation_text=crr_matrix.round(2).values,
       showscale=True,
       colorscale="Viridis"
    )
    fig.update_layout(title="Correlation matrix")
    fig.show()
    """ --------------- READING GENERATED DIAGRAM AND CALCULATING THE COMPLEXITY SCORE ---------------"""
    # image_path_bpmn = r'C:\Users\97252\PycharmProjects\final_sw_seminar\bpmn_output0.png'
    #complexity_score = detection_in_image.detect_random_shaped_in_image('bpmn_output0.png',show_detection=True)


    """READ DATA FROM GITHUB ARCHIVE AND APPEND THE COMPLEXITY SCORE TO EACH PROJECT ---------------"""
    # test id for POC = 27567171398
    read_data_as_datafrane(complexity_score=complexity_score,project_id = 27567171398)
