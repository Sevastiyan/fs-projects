from turtle import left
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import time


class CenterOfPressure:
    """Data needs to be passed in as a list of dataframes
    where each dataframe is a side of the leg"""

    def __init__(self, data, positions=None, drop_sensors=None):
        """Create an instance of COP for both legs

        Args:
            data: Both sides - Array [pd.df(left), pd.df(right)] sensors
            positions: Dictionary with left and right sensor positions { left: {[x], [y]}, right: {[x], [y]} }
            drop_sensors: Array [[left sensors], [right sensors]]
        """
        self.left_data = data[0].iloc[:, 1:15]  # Left side data
        self.right_data = data[1].iloc[:, 1:15]  # Right side data

        # self.left_data.values[self.left_data < 20] = 0    # Set all the values below 20 to 0
        # self.right_data.values[self.right_data < 20] = 0  # Set all the values below 20 to 0

        if positions is None:
            self.positions = self.default_positions()
        else:
            self.positions = positions

        if drop_sensors is None:
            self.drop_columns = []
            # self.offset = 0
        else:
            # drop = [[1,2,3,4,5,7,8,9],
            #         [5,6,7,2,1,3,9,10]]
            self.drop_columns = drop_sensors
            idx = [
                [False if i in drop_sensors[0] else True for i in range(14)],
                [False if i in drop_sensors[1] else True for i in range(14)],
            ]

            # drop positions:
            # d_c = self.drop_columns[0] + [x + 14 for x in self.drop_columns[1]]
            # self.x_pos = [x for i, x in enumerate(self.x_pos) if i not in d_c]
            # self.y_pos = [y for i, y in enumerate(self.y_pos) if i not in d_c]
            self.positions = {
                "left": {
                    "x": positions["left"]["x"][idx[0]],
                    "y": positions["left"]["y"][idx[0]],
                },
                "right": {
                    "x": positions["right"]["x"][idx[1]],
                    "y": positions["right"]["y"][idx[1]],
                },
            }

            # drop data
            self.left_data = self.left_data.drop(
                self.left_data.columns[drop_sensors[0]], axis=1
            )
            self.right_data = self.right_data.drop(
                self.right_data.columns[drop_sensors[1]], axis=1
            )
            # self.offset = len(self.drop_columns[0])

    # Data ---------------------------------------------------------------------------------------------
    def normalise(self):
        """Normalise the data using min max scaling for each column"""
        normalized_data = pd.DataFrame()
        pass

    def calculate_cop_butterfly(self):
        data = pd.concat([self.left_data, self.right_data], axis=1)
        x_pos = np.concatenate(
            [self.positions["left"]["x"], self.positions["right"]["x"]], axis=1
        )
        y_pos = np.concatenate(
            [self.positions["left"]["y"], self.positions["right"]["y"]], axis=1
        )
        data_sum = data.sum(axis=1)  # Sum of all the data
        cop_x = data * x_pos  # Multiply the data with the x_pos
        cop_y = data * y_pos  # Multiply the data with the y_pos

        self.cop_x = cop_x.sum(axis=1) / data_sum  # Sum the x_pos and divide by the sum
        self.cop_y = cop_y.sum(axis=1) / data_sum  # Sum the y_pos and divide by the sum
        # print(f'COPX data: \n {cop_x.head()}')
        # print(data_sum)

        return self.cop_x, self.cop_y

    def get_cop_foot(self, side):
        """Calculate the COP per side

        Args:
            side: the side for calculation
        Returns:
            cop_x, cop_y : center of pressure for x and y directions
        """

        if side == "left":
            data_sum = self.left_data.sum(axis=1)  # Sum of all the data
            # cop_x = self.left_data * self.x_pos[:14 - self.offset]    # Multiply the data with the x_pos
            # cop_y = self.left_data * self.y_pos[:14 - self.offset]    # Multiply the data with the y_pos

            cop_x = self.left_data * self.positions["left"]["x"]
            cop_y = self.left_data * self.positions["left"]["y"]

        if side == "right":
            data_sum = self.right_data.sum(axis=1)  # Sum of all the data
            # cop_x = self.right_data * self.x_pos[14 - self.offset:]   # Multiply the data with the x_pos
            # cop_y = self.right_data * self.y_pos[14 - self.offset:]   # Multiply the data with the y_pos
            cop_x = self.right_data * self.positions["right"]["x"]
            cop_y = self.right_data * self.positions["right"]["y"]

        d_cop_x = cop_x.sum(axis=1) / data_sum  # Sum the x_pos and divide by the sum
        d_cop_y = cop_y.sum(axis=1) / data_sum  # Sum the y_pos and divide by the sum

        return d_cop_x, d_cop_y

    # Plot ---------------------------------------------------------------------------------------------
    def plot_foot(self, side):
        data = self.get_cop_foot(side)  # Get the COP data for the foot
        plt.figure(figsize=(4, 4))  # Set the size of the graph
        plt.plot(data[0], data[1])  # Plot the COP
        plt.plot(self.positions[side]['x'], self.positions[side]['y'], "ro")  # Plot the markers
        if side == "left":  # Set the boundry of the foot
            plt.xlim(-200, 0)
        else:
            plt.xlim(0, 200)
        plt.title(f"{side} foot COP")
        plt.xlabel("Position [mm]")
        plt.ylabel("Position [mm]")

        time_now = time.strftime("%Y%m%d-%H%M%S")  # Current time
        filename = f"_{side}_COP_{time_now}.png"  # Name of the graph
        self.save_graph(plt, filename)  # Save the graph


    def plot_both_feet(self):
        left_x, left_y = self.get_cop_foot('left')
        right_x, right_y = self.get_cop_foot('right')
        
        plt.figure(figsize=(4, 4))
        plt.plot(left_x, left_y) 
        plt.plot(self.positions['left']['x'], self.positions['left']['y'], "ro")
        plt.plot(right_x, right_y)
        plt.plot(self.positions['right']['x'], self.positions['right']['y'], "ro")

        plt.title(f"Both feet COP")
        plt.xlabel("Position [mm]")
        plt.ylabel("Position [mm]")

        time_now = time.strftime("%Y%m%d-%H%M%S")  # Current time
        filename = f"both_COP_{time_now}.png"  # Name of the graph
        self.save_graph(plt, filename)  # Save the graph
        
        pass



    def plot_butterfly(self, session):
        plt.figure(figsize=(5, 5))  # Set the size of the graph
        plt.plot(self.cop_x, self.cop_y)  # Plot the COP
        plt.plot(self.x_pos, self.y_pos, "ro")  # Plot the markers

        plt.title("Butterfly COP")
        plt.xlabel("Position [mm]")
        plt.ylabel("Position [mm]")

        time_now = time.strftime("%Y%m%d-%H%M%S")  # Current time
        filename = f"{session}_Butterfly_COP_{time_now}.png"  # Name of the graph
        self.save_graph(plt, filename)  # Save the graph


    # Save ---------------------------------------------------------------------------------------------
    def save_graph(self, graph, filename):
        path = os.path.join(".", "results", "graphs")  # Path to save the graph
        if not os.path.exists(path):  # Create the path if it doesn't exist
            os.makedirs(path)
        graph.savefig("\\".join([path, filename]))  # Save the graph


    def save_data(self, session):
        """Save the DataFrame in a csv file

        Args:
            param data: DataFrame with the data
        """
        cop_x_left, cop_y_left = self.get_cop_foot("left")
        cop_x_right, cop_y_right = self.get_cop_foot("right")
        mean_cop_x = pd.Series(self.cop_x.mean())
        mean_cop_y = pd.Series(self.cop_y.mean())
        left_mean_cop_x = pd.Series(cop_x_left.mean())
        left_mean_cop_y = pd.Series(cop_y_left.mean())
        right_mean_cop_x = pd.Series(cop_x_right.mean())
        right_mean_cop_y = pd.Series(cop_y_right.mean())
        left_std_cop_x = pd.Series(cop_x_left.std())
        left_std_cop_y = pd.Series(cop_y_left.std())
        right_std_cop_x = pd.Series(cop_x_right.std())
        right_std_cop_y = pd.Series(cop_y_right.std())
        stats = pd.Series(
            [
                mean_cop_x,
                mean_cop_y,
                left_mean_cop_x,
                left_mean_cop_y,
                right_mean_cop_x,
                right_mean_cop_y,
                left_std_cop_x,
                left_std_cop_y,
                right_std_cop_x,
                right_std_cop_y,
            ]
        )
        labels = pd.Series(
            [
                "mean_cop_x",
                "mean_cop_y",
                "left_mean_cop_x",
                "left_mean_cop_y",
                "right_mean_cop_x",
                "right_mean_cop_y",
                "left_std_cop_x",
                "left_std_cop_y",
                "right_std_cop_x",
                "right_std_cop_y",
            ]
        )
        data = pd.concat(
            [
                self.cop_x,
                self.cop_y,
                cop_x_left,
                cop_y_left,
                cop_x_right,
                cop_y_right,
                labels,
                stats,
            ],
            axis=1,
        )
        data.columns = [
            "total_cop_x",
            "total_cop_y",
            "left_cop_x",
            "left_cop_y",
            "right_cop_x",
            "right_cop_y",
            "Labels",
            "Values",
        ]

        path = os.path.join(".", "results", "data")  # Path to save the filtered data
        time_now = time.strftime("%Y%m%d-%H%M%S")  # Current time
        filename = f"{session}_COP_data_{time_now}.csv"  # Name of the file
        if not os.path.exists(path):  # Create the path if it doesn't exist
            os.makedirs(path)
        data.round(decimals=3).to_csv("\\".join([path, filename]), index=False)

    def default_positions(self):
        return {
        "left": {
            "x": np.asarray(
                [
                    -149,
                    -133,
                    -115,
                    -112,
                    -96,
                    -117,
                    -101,
                    -126,
                    -146,
                    -161,
                    -140,
                    -159,
                    -158,
                    -156,
                ]
            ),
            "y": np.asarray(
                [-95, -114, -92, -16, 50, 56, 97, 101, 87, 62, 55, 25, -10, -41]
            ),
        },
        "right": {
            "x": np.asarray(
                [
                    149,
                    133,
                    115,
                    112,
                    96,
                    117,
                    101,
                    126,
                    146,
                    161,
                    140,
                    159,
                    158,
                    156,
                ]
            ),
            "y": np.asarray(
                [-95, -114, -92, -16, 50, 56, 97, 101, 87, 62, 55, 25, -10, -41]
            ),
        },
    }