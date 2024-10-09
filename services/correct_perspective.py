import cv2 as cv
import numpy as np

from services.calculate_distance_between_two_points import calculate_distance_between_2_points
from services.utils import order_points

def correct_perspective(image) :
    img = cv.imread(image)

    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    thres = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

    contours, hierarchy = cv.findContours(thres, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    image_with_all_contours = img.copy()
    cv.drawContours(image_with_all_contours, contours, -1, (0, 255, 0), 3)

    rectangular_contours = []
    for contour in contours:
        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            rectangular_contours.append(approx)
    image_with_only_rectangular_contours = img.copy()
    cv.drawContours(image_with_only_rectangular_contours, rectangular_contours, -1, (0, 255, 0), 3)

    max_area = 0
    contour_with_max_area = None
    for contour in rectangular_contours:
        area = cv.contourArea(contour)
        if area > max_area:
            max_area = area
            contour_with_max_area = contour
    gambar_setelah_contour_max = img.copy()
    cv.drawContours(gambar_setelah_contour_max, [contour_with_max_area], -1, (0, 255, 0), 3)

    contour_with_max_area_ordered = order_points(contour_with_max_area)

    existing_image_width = None

    image_with_points_plotted = img.copy()
    for point in contour_with_max_area_ordered:
        point_coordinates = (int(point[0]), int(point[1]))
        image_with_points_plotted = cv.circle(image_with_points_plotted, point_coordinates, 10, (0, 0, 255), -1)

        existing_image_width = img.shape[1]

    existing_image_width_reduced_by_10_percent = int(existing_image_width * 0.9)

    distance_between_top_left_and_top_right = calculate_distance_between_2_points(contour_with_max_area_ordered[0],
                                                                                contour_with_max_area_ordered[1])
    distance_between_top_left_and_bottom_left = calculate_distance_between_2_points(contour_with_max_area_ordered[0],
                                                                                    contour_with_max_area_ordered[3])
    aspect_ratio = distance_between_top_left_and_bottom_left / distance_between_top_left_and_top_right
    new_image_width = existing_image_width_reduced_by_10_percent
    new_image_height = int(new_image_width * aspect_ratio)

    # logika perspective transform
    pts1 = np.float32(contour_with_max_area_ordered)
    pts2 = np.float32([[0, 0], [new_image_width, 0], [new_image_width, new_image_height], [0, new_image_height]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    perspective_corrected_image = cv.warpPerspective(img, matrix, (new_image_width, new_image_height))

    return perspective_corrected_image