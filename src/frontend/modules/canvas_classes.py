from PyQt5 import QtChart as qtch
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=75):
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(
            self, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding
        )
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class SinglePlot_Strain_Canvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.setup_initial_figure()
        return

    def setup_initial_figure(self):
        self.clear_plot()
        self.ax.set_title("Test: None Selected")
        self.ax.grid(which="both")

        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, 0.001)

        self.draw()
        return

    def clear_plot(self):
        self.ax.cla()
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        return

    def update_plot_strain(self, testdict):
        self.clear_plot()
        self.ax.set_title(f"Strain vs. Time for Test: {testdict['name']}")
        self.ax.grid(which="both")
        self.ax.set_xlabel("Time (Days)")
        self.ax.set_ylabel("Strain (-)")
        self.ax.plot(testdict["time"], testdict["strain"])
        self.draw()
        return

    def update_plot_strainrate(self, testdict):
        self.clear_plot()
        self.ax.set_title(f"Strain Rate vs. Time for Test: {testdict['name']}")
        self.ax.grid(which="both")
        self.ax.set_xlabel("Time (Days)")
        self.ax.set_ylabel("Strain Rate (-/day)")
        self.ax.plot(testdict["time"][1::], testdict["strain_rate"])
        self.draw()
        return

    def update_plot_stress(self, testdict):
        self.clear_plot()
        self.ax.set_title(
            f"Applied Deviatoric Stress vs. Time for Test: {testdict['name']}"
        )
        self.ax.grid(which="both")
        self.ax.set_xlabel("Time (Days)")
        self.ax.set_ylabel("Applied Deviatoric Stress (MPa)")
        self.ax.plot(testdict["time"], testdict["stress"])
        self.draw()
        return

    def update_plot_temp(self, testdict):
        self.clear_plot()
        self.ax.set_title(f"Applied Temperature vs. Time for Test: {testdict['name']}")
        self.ax.grid(which="both")
        self.ax.set_xlabel("Time (Days)")
        self.ax.set_ylabel("Applied Temperature (K)")
        self.ax.plot(testdict["time"], testdict["temperature"])
        self.draw()
        return


class MultiPlot_Strain_Canvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.setup_initial_figure()
        return

    def setup_initial_figure(self):
        self.clear_plot()
        self.ax.set_title("Test: None Imported")
        self.ax.grid(which="both")
        self.ax.set_xlabel("Time (Day)")
        self.ax.set_ylabel("Strain (-)")

        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, 0.001)

        self.draw()
        return

    def clear_plot(self):
        self.ax.cla()
        return

    def update_plot(self, testlist: list[dict]):
        self.clear_plot()
        if len(testlist) == 0:
            self.setup_initial_figure()
        else:
            self.ax.set_title(f"Strain vs. Time for All Tests")
            self.ax.grid(which="both")
            self.ax.set_xlabel("Time (Days)")
            self.ax.set_ylabel("Strain (-)")

            for i in range(len(testlist)):
                self.ax.plot(
                    testlist[i]["time"], testlist[i]["strain"], label=testlist[i]["name"]
                )

            self.ax.legend()
            self.draw()
        return


# class TestSuite_SinglePlot(qtch.QChartView):
#     def __init__(self):
#         super().__init__()

#         self.chart = qtch.QChart()  # type: ignore
#         self.setChart(self.chart)

#         # Set up the axis
#         self.chart.createDefaultAxes()
#         self.chart.legend().hide()

#         self.setRenderHint(qtg.QPainter.Antialiasing)

#         return

#     def add_curve(self, title, x_data, y_data):
#         # Remove any existing series and axis
#         if len(self.chart.series()) > 0:
#             series_list = self.chart.series()
#             for i in range(len(self.chart.series())):
#                 self.chart.removeSeries(series_list[i])

#             axis_list = self.chart.axes()
#             for j in range(len(axis_list)):
#                 self.chart.removeAxis(axis_list[j])

#         # Get x-axis limits and ticks
#         min_x, max_x, numticks_x = get_lims_ticks([x_data])

#         # QChart Cannot resolve small values. Need to convert strain to microstrain
#         y_data = [i * 1e6 for i in y_data]
#         # Get y-axis limits and ticks
#         min_y, max_y, numticks_y = get_lims_ticks([y_data])

#         self.series = qtch.QLineSeries()
#         self.chart.addSeries(self.series)

#         for i in range(len(x_data)):
#             self.series.append(qtc.QPoint(x_data[i], y_data[i]))

#         self.x_axis = qtch.QValueAxis()
#         self.x_axis.setRange(min_x, max_x)
#         self.x_axis.setTickCount(numticks_x)
#         self.chart.setAxisX(self.x_axis, self.series)

#         self.y_axis = qtch.QValueAxis()
#         self.y_axis.setRange(min_y, max_y)
#         self.y_axis.setTickCount(numticks_y)
#         self.chart.setAxisY(self.y_axis, self.series)

#         # Set the chart title
#         self.chart.setTitle(title)

#         return


def lim_modulus_values():
    modulus_value_list = [
        1e-15,
        2e-15,
        2.5e-15,
        5e-15,
        1e-14,
        2e-14,
        2.5e-14,
        5e-14,
        1e-13,
        2e-13,
        2.5e-13,
        5e-13,
        1e-12,
        2e-12,
        2.5e-12,
        5e-12,
        1e-11,
        2e-11,
        2.5e-11,
        5e-11,
        1e-10,
        2e-10,
        2.5e-10,
        5e-10,
        1e-9,
        2e-9,
        2.5e-9,
        5e-9,
        1e-8,
        2e-8,
        2.5e-8,
        5e-8,
        1e-7,
        2e-7,
        2.5e-7,
        5e-7,
        1e-6,
        2e-6,
        2.5e-6,
        5e-6,
        1e-5,
        2e-5,
        2.5e-5,
        5e-5,
        1e-4,
        2e-4,
        2.5e-4,
        5e-4,
        1e-3,
        2e-3,
        2.5e-3,
        5e-3,
        1e-2,
        2e-2,
        2.5e-2,
        5e-2,
        1e-1,
        2e-1,
        2.5e-1,
        5e-1,
        1e0,
        2e0,
        2.5e0,
        5e0,
        1e1,
        2e1,
        2.5e1,
        5e1,
        1e2,
        2e2,
        2.5e2,
        5e2,
        1e3,
        2e3,
        2.5e3,
        5e3,
        1e4,
        2e4,
        2.5e4,
        5e4,
        1e5,
        2e5,
        2.5e5,
        5e5,
        1e6,
        2e6,
        2.5e6,
        5e6,
        1e7,
        2e7,
        2.5e7,
        5e7,
        1e8,
        2e8,
        2.5e8,
        5e8,
        1e9,
        2e9,
        2.5e9,
        5e9,
        1e10,
        2e10,
        2.5e10,
        5e10,
        1e11,
        2e11,
        2.5e11,
        5e11,
        1e12,
        2e12,
        2.5e12,
        5e12,
    ]
    return modulus_value_list


def get_lims_ticks(data_list: list[list[float]], allowable_ticks: int = 6):
    """
    @param data_list: list of data
    @return: tuple of (min, max, tick)
    """

    min_value = data_list[0][0]
    max_value = data_list[0][0]
    for i in range(len(data_list)):
        for j in range(len(data_list[i])):
            if data_list[i][j] < min_value:
                min_value = data_list[i][j]
            if data_list[i][j] > max_value:
                max_value = data_list[i][j]

    data_range = max_value - min_value

    # Figure out the correct tick value to be under the allowable ticks based on the range
    test_modulus = data_range / allowable_ticks

    tick_value = lim_modulus_values()[0]
    for modvalue in lim_modulus_values():
        if modvalue >= test_modulus:
            tick_value = modvalue
            break

    # Figure out the correct min and max values based on the tick value
    min_bound = (min_value // tick_value) * tick_value
    max_bound = (max_value // tick_value) * tick_value + (
        tick_value if max_value % tick_value != 0 else 0
    )
    # tick_count = int((max_bound - min_bound) / tick_value) + 1
    return min_bound, max_bound, tick_value
