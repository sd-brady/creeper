from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from frontend.modules import unit_system

from . import data_classes
from . import unit_system


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
    def __init__(
        self,
        usys: data_classes.UnitSystem,
        plot_type: data_classes.PlotType,
        *args,
        **kwargs,
    ):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.setup_initial_figure(usys, plot_type)
        return

    def setup_initial_figure(
        self, usys: unit_system.UnitSystem, plot_type: data_classes.PlotType
    ):
        self.clear_plot()
        self.ax.set_title("Test: None Selected")
        self.ax.grid(which="both")

        self.ax.set_xlabel(f"Time ({usys.time.value})")
        if plot_type.name == "STRAIN":
            self.ax.set_ylabel(f"Strain (-)")
        elif plot_type.name == "STRAINRATE":
            self.ax.set_ylabel(f"Strain Rate (-/{usys.time.value})")
        elif plot_type.name == "TEMPERATURE":
            self.ax.set_ylabel(f"Temperature ({usys.temperature.value})")
        elif plot_type.name == "STRESS":
            self.ax.set_ylabel(f"Deviatoric Stress ({usys.stress.value})")

        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, 0.001)

        self.draw()
        return

    def clear_plot(self):
        self.ax.cla()
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        return

    def update_plot(
        self,
        test: data_classes.Test,
        usys: unit_system.UnitSystem,
        plot_type: data_classes.PlotType,
    ):
        self.clear_plot()
        self.ax.set_title(f"{plot_type.value} vs. Time for Test: {test.name}")
        self.ax.grid(which="both")
        self.ax.set_xlabel(f"Time ({usys.time.value})")
        if plot_type.name == "STRAIN":
            self.ax.set_ylabel(f"Strain (-)")
            self.ax.plot(
                test.test_data.time,
                test.test_data.strain,
                color=test.color.value,
                label=test.name,
            )
        elif plot_type.name == "STRAINRATE":
            self.ax.set_ylabel(f"Strain Rate (-/{usys.time.value})")
            self.ax.plot(
                test.test_data.time[1::],
                test.test_data.strainrate,
                color=test.color.value,
                label=test.name,
            )
        elif plot_type.name == "TEMPERATURE":
            self.ax.set_ylabel(f"Temperature ({usys.temperature.value})")
            self.ax.plot(
                test.test_data.time,
                test.test_data.temperature,
                color=test.color.value,
                label=test.name,
            )
        elif plot_type.name == "STRESS":
            self.ax.set_ylabel(f"Deviatoric Stress ({usys.stress.value})")
            self.ax.plot(
                test.test_data.time,
                test.test_data.stress,
                color=test.color.value,
                label=test.name,
            )
        self.draw()
        return


class MultiPlot_Strain_Canvas(MyMplCanvas):
    def __init__(
        self,
        usys: data_classes.UnitSystem,
        plot_type: data_classes.PlotType,
        *args,
        **kwargs,
    ):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.setup_initial_figure(usys, plot_type)
        return

    def setup_initial_figure(
        self, usys: unit_system.UnitSystem, plot_type: data_classes.PlotType
    ):
        self.clear_plot()
        self.ax.set_title("Test: None Selected")
        self.ax.grid(which="both")

        self.ax.set_xlabel(f"Time ({usys.time.value})")
        if plot_type.name == "STRAIN":
            self.ax.set_ylabel(f"Strain (-)")
        elif plot_type.name == "STRAINRATE":
            self.ax.set_ylabel(f"Strain Rate (-/{usys.time.value})")
        elif plot_type.name == "TEMPERATURE":
            self.ax.set_ylabel(f"Temperature ({usys.temperature.value})")
        elif plot_type.name == "STRESS":
            self.ax.set_ylabel(f"Deviatoric Stress ({usys.stress.value})")

        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, 0.001)

        self.draw()
        return

    def clear_plot(self):
        self.ax.cla()
        return

    def update_plot(
        self,
        test_suite: data_classes.TestSuite,
        usys: unit_system.UnitSystem,
        plot_type: data_classes.PlotType,
    ):
        self.clear_plot()
        if test_suite.num_tests == 0:
            self.setup_initial_figure(usys, plot_type)
        else:
            self.ax.set_title(f"{plot_type.value} vs. Time")
            self.ax.grid(which="both")
            self.ax.set_xlabel(f"Time ({usys.time.value})")
            for i in range(len(test_suite.test_list)):
                if test_suite.test_list[i].active_state.value == "On":
                    if plot_type.name == "STRAIN":
                        self.ax.set_ylabel(f"Strain (-)")
                        self.ax.plot(
                            test_suite.test_list[i].test_data.time,
                            test_suite.test_list[i].test_data.strain,
                            color=test_suite.test_list[i].color.value,
                            label=test_suite.test_list[i].name,
                        )
                    elif plot_type.name == "STRAINRATE":
                        self.ax.set_ylabel(f"Strain Rate (-/{usys.time.value})")
                        self.ax.plot(
                            test_suite.test_list[i].test_data.time[1::],
                            test_suite.test_list[i].test_data.strainrate,
                            color=test_suite.test_list[i].color.value,
                            label=test_suite.test_list[i].name,
                        )
                    elif plot_type.name == "TEMPERATURE":
                        self.ax.set_ylabel(f"Temperature ({usys.temperature.value})")
                        self.ax.plot(
                            test_suite.test_list[i].test_data.time,
                            test_suite.test_list[i].test_data.temperature,
                            color=test_suite.test_list[i].color.value,
                            label=test_suite.test_list[i].name,
                        )
                    elif plot_type.name == "STRESS":
                        self.ax.set_ylabel(f"Deviatoric Stress ({usys.stress.value})")
                        self.ax.plot(
                            test_suite.test_list[i].test_data.time,
                            test_suite.test_list[i].test_data.stress,
                            color=test_suite.test_list[i].color.value,
                            label=test_suite.test_list[i].name,
                        )
            self.ax.legend()
            self.draw()
        return
