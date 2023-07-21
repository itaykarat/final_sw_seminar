from square_detection_cv import detection_in_image

class calculate_complexity_score():
    def __init__(self,image):
        self.score_type = 'Number of classes'
        self.image = image
        self.numebr_of_classes = None



    def calculate_complexiy(self):
        image = self.image
        num_of_classes = detection_in_image(image)
        print(f'num_of_classes {num_of_classes}')
        return num_of_classes




