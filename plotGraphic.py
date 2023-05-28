from Game import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def plotGraphic(N_range, values, xLabel, yLabel):
	# строим график функции ценности
	plt.plot(N_range, values)
	plt.xlabel(xLabel)
	plt.ylabel(yLabel)
	plt.show()

def plot_state_values(V: dict):
	x_range = np.arange(0, 22)
	y_range = np.arange(1, 11)
	X, Y = np.meshgrid(x_range, y_range)

	fig = plt.figure(figsize=(15,20))
	ax = fig.add_subplot(projection='3d')
	Z = np.zeros((len(y_range), len(x_range)))
	for y in y_range:
		for x in x_range:
			value = V.get(State(x, y))
			if value is not None:
				Z[y-y_range[0]][x-x_range[0]] = value

	surf = ax.plot_surface(
		X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, vmin=-1.0, vmax=1.0, edgecolor='w', linewidth=0.5
	)
	ax.set_xlabel("Player's Current Sum")
	ax.set_ylabel("Dealer's Showing Card")
	ax.set_zlabel("Value")
	ax.view_init(ax.elev, -120)

	plt.show()
