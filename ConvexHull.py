import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt

coordinates = [[43.2858, 19.9884], [43.2858, 19.9884], [43.3191, 19.9884], [43.3191, 19.9786], [43.3191, 19.9786], [43.3191, 19.9786], [43.3191, 19.9688], [43.3191, 19.9688], [43.3191, 19.9786], [43.3191, 19.9688], [43.3525, 19.9688], [43.3525, 19.9688], [43.3858, 19.959], [43.4524, 19.9198], [43.4524, 19.9296], [43.4524, 19.9198], [43.4524, 19.91], [43.4857, 19.9002], [43.519, 19.91], [43.519, 19.91], [43.519, 19.9002], [43.4857, 19.8904], [43.519, 19.8904], [43.5522, 19.8806], [43.5522, 19.8708], [43.5522, 19.8512], [43.5855, 19.8512], [43.5855, 19.8414], [43.6188, 19.812], [43.6188, 19.812], [43.6188, 19.812], [43.6521, 19.812], [43.6188, 19.8022], [43.5855, 19.8218], [43.5855, 19.812], [43.6188, 19.8218], [43.5855, 19.8316], [43.5855, 19.8316], [43.5855, 19.8512], [43.5522, 19.8414], [43.5522, 19.8512], [43.519, 19.8512], [43.519, 19.861], [43.519, 19.861], [43.519, 19.8708], [43.519, 19.8708], [43.519, 19.8708], [43.519, 19.8806], [43.519, 19.8806], [43.519, 19.8708], [43.519, 19.8806], [43.5522, 19.8708], [43.5522, 19.8904], [43.5522, 19.8904], [43.5522, 19.8708], [43.5522, 19.8806], [43.5522, 19.8904], [43.5522, 19.8904], [43.5855, 19.8904], [43.5855, 19.8904], [43.5855, 19.8904], [43.5855, 19.8904], [43.5855, 19.8806], [43.6188, 19.8806], [43.5855, 19.8708], [43.6188, 19.9002], [43.5855, 19.8904], [43.6521, 19.8904], [43.6853, 19.8708]]
points = np.array(coordinates)
hull = spatial.ConvexHull(points)

Key = input("Press Y to show all the points, N to show only the corners: ")

if Key=='Y':
    plt.plot(points[:,0], points[:,1], 'o')
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'b-')

    plt.show()

else:
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'b-')

    plt.show()


