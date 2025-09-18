import random
import numpy as np
import math
import matplotlib.pyplot as plt

LEFT_X_BOUNDS = (-17.135, -3.0)
RIGHT_X_BOUNDS = (3.0, 17.135)
Y_BOUNDS = (-17.135, 17.135)
MIN_DIST = 11
MIN_POINTS = 230
ANGLE_RANGE = (90, 130)
NUM_CIRCLE_POINTS = 1000
MAX_ATTEMPTS = 100

def squareCoordinates(x_bounds, y_bounds):
    for i in range(MAX_ATTEMPTS):
        p3 = None
        circle_coordinates = []

        # loops until length of potential coordinates is greater than 230
        while (len(circle_coordinates) <= 230): 
            p1, p2 = get_random_coordinates(x_bounds, y_bounds)
            dist = math.dist(p1, p2)
            pointsList = get_circle_points(p1, dist) # gets coordinates on circle with radius = distance btwn the first two points at center = coordinate1
            circle_coordinates = get_points_in_bounds(pointsList, x_bounds, y_bounds) # gets coordinates on circle that are within the area bounds     

        for point in reversed(circle_coordinates):
            RTangle = get_angle(p1, p2, point) # gets angle at first coordinate relative to the other two
            if RTangle >= 90 and RTangle <= 130:
                p3 = point 
                break
        
        if (p1 and p2 and p3):
            return (p1, p2, p3)

def get_random_coordinates(x_bounds, y_bounds):
    p1 = np.random.uniform(x_bounds[0], x_bounds[1]), np.random.uniform(y_bounds[0], y_bounds[1])
    x, y = p1
    test_y = 0
    while (abs(test_y - y) < MIN_DIST):
        test_y = np.random.uniform(y_bounds[0], y_bounds[1])
    p2 = x, test_y
    return(p1, p2)

# returns list of x and y coordinates on circle around first coordinate with radius = dist between first two points
def get_circle_points(point1,radius):
    originX = point1[0]
    originY = point1[1]
    x = []
    y = []
    for i in range(NUM_CIRCLE_POINTS): # how many points are plotted
        angle = random.uniform(0,1)*(math.pi*2)
        x.append(math.cos(angle) * radius + originX)
        y.append(math.sin(angle) * radius + originY)
    return [x,y]

# takes in list of circle of points around first coordinate, returns list of coordinates within the spatial bounds
def get_points_in_bounds(pointsList, x_bounds, y_bounds):
    coordinates = []
    xmin, xmax = x_bounds
    ymin, ymax = y_bounds
    for i in range(len(pointsList[0])):
        p3 = (pointsList[0][i], pointsList[1][i])
        if (p3[0] >= xmin and p3[0] <= xmax) and (p3[1] >= ymin and p3[1] <= ymax):
            coordinates.append(p3)
    return coordinates

# helper for get_angle()
def lengthSquare(a, b):
    xDiff = a[0] - b[0]
    yDiff = a[1] - b[1]
    return (xDiff * xDiff) + (yDiff * yDiff)
     
# returns angle at first coordinate
def get_angle(point1, point2, point3):
    # Square of lengths be a2, b2, c2
    a2 = lengthSquare(point2, point3)
    b2 = lengthSquare(point1, point3)
    c2 = lengthSquare(point1, point2)
    
    # length of sides be a, b, c
    a = math.sqrt(a2)
    b = math.sqrt(b2)
    c = math.sqrt(c2)
    
    # From Cosine law
    alpha = math.acos((b2 + c2 - a2) / (2 * b * c))
    beta = math.acos((a2 + c2 - b2) / (2 * a * c))
    gamma = math.acos((a2 + b2 - c2) / (2 * a * b))
    
    # Converting to degree
    alpha = alpha * 180 / math.pi; # angle at first point
    beta = beta * 180 / math.pi; 
    gamma = gamma * 180 / math.pi; 
    
    return alpha

def plot_points(left_coordinates, right_coordinates):
    fig, ax = plt.subplots()
    ax.set_aspect(1)
    plt.grid()
    plt.plot([0,0],[0,20],linewidth=2,color="k")
    plt.plot([0,0],[0,-20],linewidth=2,color="k")
    square = plt.Rectangle((-20.135,-20.135), 40.27, 40.27, edgecolor = 'black', facecolor = None, fill = False)
    plt.gca().add_patch(square)

    for x, y in left_coordinates:
        plt.scatter(x, y)
    
    for x, y in right_coordinates:
        plt.scatter(x, y)

    plt.axis('equal')
    plt.show()


def main():
    left_triangle = np.round(squareCoordinates(LEFT_X_BOUNDS, Y_BOUNDS), decimals=2)
    right_triangle = np.round(squareCoordinates(RIGHT_X_BOUNDS, Y_BOUNDS), decimals=2)
    plot_points(left_triangle, right_triangle)