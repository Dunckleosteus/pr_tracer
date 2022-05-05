# this file contains the functions needed in the pytracer program
import math
import numpy
def closest(x1,y1,route):
    m_value = 0
    result = []
    listx = (x[0] for x in route)            # list of all the x values
    listy = (x[1] for x in route)            # list of all the y values
    distance = list(math.dist((x[0],x[1]),(x1,y1)) for x in route)      # creates list of all the distcance values
    m_value = numpy.min(distance)
    print ("distance between estimated pr is {} meters".format(m_value))                                                # find the smallest distance value
    result = distance.index(m_value)
    return result, m_value
