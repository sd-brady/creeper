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