#!/usr/bin/env python3
###############################################################################################
#                    ____                 ____  _           _                                 #
#                   |  _ \ __ _ _ __ __ _| __ )| | __ _  __| | ___                            #
#                   | |_) / _` | '__/ _` |  _ \| |/ _` |/ _` |/ _ \                           #
#                   |  __/ (_| | | | (_| | |_) | | (_| | (_| |  __/                           #
#                   |_|   \__,_|_|  \__,_|____/|_|\__,_|\__,_|\___|                           #
#                                                                                             #
###############################################################################################

################################# FILE NAME: PlotMoveSurface.py ###############################
#=============================================================================================#
# author: Murillo Pereira Neto                                                                |
#    :PhD Candidate,                                                                          |
#    :Mechanical Engineering,                                                                 |
#    :University of São Paulo,                                                                |
#    :Brazil                                                                                  |
#                                                                                             |
#                                                                                             |
# Description:                                                                                |
#                                                                                             |
#=============================================================================================#

#---------------------------------------------------------------------------------------------#
# Importing general packages
#---------------------------------------------------------------------------------------------#
import sys
import numpy as np
import matplotlib.pyplot as plt

#---------------------------------------------------------------------------------------------#
# Main function
#---------------------------------------------------------------------------------------------#
def main():
    # Check if filename was provided
    if len(sys.argv) != 2:
        print("Usage: PlotMoveSurface.py data.txt")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        # Load tab-separated file
        data = np.loadtxt(filename, delimiter="\t")
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

    if data.shape[1] < 4:
        print("Error: File must contain at least 4 columns (point_id, x, y, z)")
        sys.exit(1)

    x = data[:, 1]
    y = data[:, 2]
    z = data[:, 3]

    # Create 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x, y, z, s=5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(f"3D Point Cloud from {filename}")

    plt.show()

#---------------------------------------------------------------------------------------------#
# Only run in terminal
#---------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    main()