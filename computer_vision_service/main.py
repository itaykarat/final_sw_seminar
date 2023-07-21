import cv2

# Read in image
image_path_bpmn = r'/bpmn_output0.png'

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

# Display the result
cv2.imshow('Shapes Detected', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
