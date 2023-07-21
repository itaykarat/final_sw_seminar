import cv2


class detection_in_image:
    def __init__(self):
        self.self.img = None


    @staticmethod
    def detect_random_shaped_in_image(image_path_bpmn = r'C:\Users\97252\PycharmProjects\final_sw_seminar\bpmn_output0.png',show_detection=True):
        # Read in image
        image = cv2.imread(image_path_bpmn)

        # Read and preprocess the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)

        # Find contours with RETR_TREE mode
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Analyze and draw contours
        for i in range(len(contours)):
            # Analyze contour properties
            perimeter = cv2.arcLength(contours[i], True)
            area = cv2.contourArea(contours[i])
            approx = cv2.approxPolyDP(contours[i], 0.03 * perimeter, True)

            # Draw contours on the image
            cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)

        # Print the number of shapes detected
        print("Number of shapes detected:", len(contours))

        if show_detection:
            # Display the result
            cv2.imshow('Shapes Detected', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return len(contours) # returns the complexity

    @staticmethod
    def detect_squares_in_image(img,show_detection=False):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        # blur = cv2.GaussianBlur(gray, (5, 5), 0)
        blur = gray

        # Adaptive threshold
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)

        # Find contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        classes = 0
        # Check each contour for squareness
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                area = cv2.contourArea(contour)
                x, y, w, h = cv2.boundingRect(contour)
                rect_area = w * h
                ratio = float(area) / rect_area
                if ratio > 0.7:
                    cv2.drawContours(img, [contour], 0, (0, 255, 0), 3)
                    classes +=1

        # Display image with squares detecte
        if show_detection:
            cv2.imshow('Squares Detected', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        classes = classes/3
        return classes
