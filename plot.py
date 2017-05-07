import matplotlib.pyplot as plt
import pylab
from matplotlib.patches import Rectangle

class Plot():


    def __init__(self,x, y):
        self.x = x
        self.y = y

    def draw_graph(self, x, y):
        plt.ion()
        fig = plt.figure()
        plt.axis([0, 20, 0, 20])
        currentAxis = plt.gca()


        currentAxis.add_patch(
           Rectangle((x, y), -1, -1, facecolor="blue"))

        #plt.show()
        #plt.pause(0.0001)  # Note this correction
