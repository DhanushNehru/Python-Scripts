import cv2
import numpy as np

def canny_edge_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return edges

def detect_road_region(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_gray = np.array([0, 0, 50])  # Lower bound for gray
    upper_gray = np.array([180, 50, 200])  # Upper bound for gray

    mask = cv2.inRange(hsv, lower_gray, upper_gray)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        polygon = cv2.approxPolyDP(largest_contour, epsilon, True)

        road_mask = np.zeros_like(mask)
        if len(polygon) >= 3:  
            cv2.fillPoly(road_mask, [polygon], 255)

        return road_mask
    return None

def hough_transform(masked_edges):
    lines = cv2.HoughLinesP(masked_edges, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    return lines

def display_lines(frame, lines):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
    return line_image

def combine_images(frame, line_image):
    combined_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return combined_image

def process_frame(frame):
    edges = canny_edge_detection(frame)

    road_mask = detect_road_region(frame)

    if road_mask is not None:
        masked_edges = cv2.bitwise_and(edges, edges, mask=road_mask)
    else:
        masked_edges = edges

    lines = hough_transform(masked_edges)

    line_image = display_lines(frame, lines)

    result = combine_images(frame, line_image)

    return result

vds = ['lane5.mp4']#add more of your own videos here

cap = cv2.VideoCapture('videos/'+vds[0])
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    result = process_frame(frame)
    cv2.imshow('Lane Detection', result)
    road_cont_mask = detect_road_region(frame)
    cv2.imshow('Lane Detection2', road_cont_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()