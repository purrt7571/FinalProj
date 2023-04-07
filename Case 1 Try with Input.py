import numpy as np

list = np.array([])

while(True):
    magnitude = float(input("Enter the magnitude of the vector: "))
    if magnitude == 100:
        print(list)
        print(sum(list))
        break
    angle = float(input("Enter the angle of the vector with respect to +x axis: "))
    vector_array = np.array([[np.array([magnitude*np.cos(np.radians(angle))]), np.array([magnitude*np.sin(np.radians(angle))])]])
    list = np.append(vector_array, list)