import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks


class StepProcessor:

    def process(self, data):
        # extract the accelerometer x, y and z into 3 arrays
        acceleration_x_values = np.array([item[3] for item in data])
        acceleration_y_values = np.array([item[4] for item in data])
        acceleration_z_values = np.array([item[5] for item in data])

        # calculate the magnitude of this array
        magnitude = np.sqrt(acceleration_x_values**2 + acceleration_y_values**2 + acceleration_z_values**2)

        # find the peaks
        peaks, _ = find_peaks(magnitude, height=1.1)

        fig, ax = plt.subplots(1, 1)
        fig.set_figheight(7.5)
        fig.set_figwidth(15)

        fig.suptitle("Accelerometer Data with Peaks", fontsize=30)
        fig.tight_layout()

        ax.plot(magnitude, 'b')
        ax.plot(peaks, magnitude[peaks], "rx")
        ax.set_ylabel('Acceleration (m/s^2)', fontdict={'size': 20})
        ax.set_ylim(0, 7)

        plt.tight_layout()
        plt.show()

        # calculate the number of steps
        steps = len(peaks)
        print(f"Number of steps: {steps}")

        return steps