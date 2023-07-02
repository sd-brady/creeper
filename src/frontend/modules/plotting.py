from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from . import data_classes


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

    def update_plot_strain(self, test: data_classes.Test):
        self.clear_plot()
        self.ax.set_title(f"Strain vs. Time for Test: {test.name}")
        self.ax.grid(which="both")
        self.ax.set_xlabel("Time (Days)")
        self.ax.set_ylabel("Strain (-)")
        self.ax.plot(test.test_data.time, test.test_data.strain, color=test.color, label=test.name)
        self.draw()
        return

    def update_plot_strainrate(self, test: data_classes.Test):
        self.clear_plot()
        self.ax.set_title(f"Strain Rate vs. Time for Test: {test.name}")
        self.ax.grid(which="both")
        self.ax.set_xlabel("Time (Days)")
        self.ax.set_ylabel("Strain (-/day)")
        self.ax.plot(test.test_data.time[1::], test.test_data.strainrate, color=test.color, label=test.name)
        self.draw()
        return

    def update_plot_stress(self, test: data_classes.Test):
        self.clear_plot()
        self.ax.set_title(f"Applied Deviatoric Stress vs. Time for Test: {test.name}")
        self.ax.grid(which="both")
        self.ax.set_xlabel("Time (Days)")
        self.ax.set_ylabel("Applied Deviatoric Stress (MPa)")
        self.ax.plot(test.test_data.time, test.test_data.stress, color=test.color, label=test.name)
        self.draw()
        return

    def update_plot_temp(self, test: data_classes.Test):
        self.clear_plot()
        self.ax.set_title(f"Applied Temperature vs. Time for Test: {test.name}")
        self.ax.grid(which="both")
        self.ax.set_xlabel("Time (Days)")
        self.ax.set_ylabel("Temperature (K)")
        self.ax.plot(test.test_data.time, test.test_data.temperature, color=test.color, label=test.name)
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

    def update_plot(self, test_suite: data_classes.TestSuite):
        self.clear_plot()
        if test_suite.num_tests == 0:
            self.setup_initial_figure()
        else:
            self.ax.set_title(f"Strain vs. Time for All Tests")
            self.ax.grid(which="both")
            self.ax.set_xlabel("Time (Days)")
            self.ax.set_ylabel("Strain (-)")

            for i in range(test_suite.num_tests):
                self.ax.plot(
                    test_suite.test_list[i].test_data.time,
                    test_suite.test_list[i].test_data.strain,
                    color=test_suite.test_list[i].color,
                    label=test_suite.test_list[i].name,
                )

            self.ax.legend()
            self.draw()
        return
