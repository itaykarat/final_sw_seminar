from computer_vision_service.square_detection_cv import detection_in_image
from generate_diagram.bpmn import generate_diagram_from_github_project
from read_data.read_tables import read_data_as_datafrane
if __name__ == '__main__':
    """READING THE GITHUB DATA AND GENERATING A DIAGRAM FROM IT"""
    generate_diagram_from_github_project()

    """ --------------- READING GENERATED DIAGRAM AND CALCULATING THE COMPLEXITY SCORE ---------------"""
    # image_path_bpmn = r'C:\Users\97252\PycharmProjects\final_sw_seminar\bpmn_output0.png'
    complexity_score = detection_in_image.detect_random_shaped_in_image('bpmn_output0.png',show_detection=True)

    """READ DATA FROM GITHUB ARCHIVE AND APPEND THE COMPLEXITY SCORE TO EACH PROJECT ---------------"""
    # test id for POC = 27567171398
    read_data_as_datafrane(complexity_score=complexity_score,project_id = 27567171398)

