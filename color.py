import numpy as np
import pandas as pd
import cv2
import imutils

# Initialize camera and global variables
camera = cv2.VideoCapture(0)
r = g = b = xpos = ypos = 0
correct_predictions = 0
total_predictions = 0

# Load color dataset
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv('colors.csv', names=index, header=None)

# Function to get the color name from RGB values
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, 'color_name'] + '   Hex=' + df.loc[i, 'hex']
    return cname

# Mouse callback function to identify the color
def identify_color(event, x, y, flags, param):
    global b, g, r, xpos, ypos
    xpos = x
    ypos = y
    b, g, r = frame[y, x]
    b = int(b)
    g = int(g)
    r = int(r)

# Setup OpenCV window
cv2.namedWindow('image')
cv2.setMouseCallback('image', identify_color)

# Main loop
while True:
    (grabbed, frame) = camera.read()
    frame = imutils.resize(frame, width=900)
    kernal = np.ones((5, 5), "uint8")
    
    # Draw a rectangle and display color details
    cv2.rectangle(frame, (20, 20), (800, 60), (b, g, r), -1)
    text = getColorName(b, g, r) + '   R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
    cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Adjust text color for light backgrounds
    if r + g + b >= 600:
        cv2.putText(frame, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    
    # Accuracy validation snippet
    if cv2.waitKey(20) & 0xFF == ord('v'):  # Press 'v' to validate
        ground_truth = input("Enter the ground truth color name: ")
        detected_color = getColorName(b, g, r)
        total_predictions += 1
        if ground_truth.lower() in detected_color.lower():
            correct_predictions += 1
        accuracy = (correct_predictions / total_predictions) * 100
        print(f"Accuracy: {accuracy:.2f}%")
    
    # Show the frame
    cv2.imshow('image', frame)
    
    # Break the loop on 'Esc' key press
    if cv2.waitKey(20) & 0xFF == 27:
        break

# Release resources
camera.release()
cv2.destroyAllWindows()
