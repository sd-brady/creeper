from frontend.modules import ui_mdwidget
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from . import mdmodel
from . import unit_system


class MdWidget(qtw.QWidget, ui_mdwidget.Ui_Form):
    def __init__(self, parent=None):
        super(MdWidget, self).__init__(parent)
        self.setupUi(self)

        self.lineedit_widget_list = [
            self.a1_value,
            self.n1_value,
            self.q1divr_value,
            self.a2_value,
            self.n2_value,
            self.q2divr_value,
            self.b1_value,
            self.b2_value,
            self.q_value,
            self.sig0_value,
            self.k0_value,
            self.m_value,
            self.c_value,
            self.alpha_value,
            self.beta_value,
            self.delta_value,
            self.mu_value,
            self.a1_min,
            self.n1_min,
            self.q1divr_min,
            self.a2_min,
            self.n2_min,
            self.q2divr_min,
            self.b1_min,
            self.b2_min,
            self.q_min,
            self.sig0_min,
            self.k0_min,
            self.m_min,
            self.c_min,
            self.alpha_min,
            self.beta_min,
            self.delta_min,
            self.mu_min,
            self.a1_max,
            self.n1_max,
            self.q1divr_max,
            self.a2_max,
            self.n2_max,
            self.q2divr_max,
            self.b1_max,
            self.b2_max,
            self.q_max,
            self.sig0_max,
            self.k0_max,
            self.m_max,
            self.c_max,
            self.alpha_max,
            self.beta_max,
            self.delta_max,
            self.mu_max,
        ]

        self.value_widget_list = [
            self.a1_value,
            self.n1_value,
            self.q1divr_value,
            self.a2_value,
            self.n2_value,
            self.q2divr_value,
            self.b1_value,
            self.b2_value,
            self.q_value,
            self.sig0_value,
            self.k0_value,
            self.m_value,
            self.c_value,
            self.alpha_value,
            self.beta_value,
            self.delta_value,
            self.mu_value,
        ]

        self.min_widget_list = [
            self.a1_min,
            self.n1_min,
            self.q1divr_min,
            self.a2_min,
            self.n2_min,
            self.q2divr_min,
            self.b1_min,
            self.b2_min,
            self.q_min,
            self.sig0_min,
            self.k0_min,
            self.m_min,
            self.c_min,
            self.alpha_min,
            self.beta_min,
            self.delta_min,
            self.mu_min,
        ]

        self.max_widget_list = [
            self.a1_max,
            self.n1_max,
            self.q1divr_max,
            self.a2_max,
            self.n2_max,
            self.q2divr_max,
            self.b1_max,
            self.b2_max,
            self.q_max,
            self.sig0_max,
            self.k0_max,
            self.m_max,
            self.c_max,
            self.alpha_max,
            self.beta_max,
            self.delta_max,
            self.mu_max,
        ]

        self.time_widget_list = [
            self.a1_value,
            self.a2_value,
            self.b1_value,
            self.b2_value,
            self.a1_max,
            self.a2_max,
            self.b1_max,
            self.b2_max,
            self.a1_min,
            self.a2_min,
            self.b1_min,
            self.b2_min,
        ]

        self.stress_widget_list = [
            self.sig0_value,
            self.sig0_min,
            self.sig0_max,
            self.mu_value,
            self.mu_min,
            self.mu_max,
        ]
        self.temp_widget_list = [
            self.q1divr_value,
            self.q1divr_min,
            self.q1divr_max,
            self.q2divr_value,
            self.q2divr_min,
            self.q2divr_max,
        ]
        self.invtemp_widget_list = [self.c_value, self.c_min, self.c_max]

        self.time_unit_widget_list = [
            self.a1_unit,
            self.a2_unit,
            self.b1_unit,
            self.b2_unit,
        ]
        self.stress_unit_widget_list = [self.sig0_unit, self.mu_unit]
        self.temp_unit_widget_list = [self.q1divr_unit, self.q2divr_unit]
        self.invtemp_unit_widget_list = [self.c_unit]

        self.set_lineedit_validators()

        self.unit_system = unit_system.UnitSystem(
            time=unit_system.UnitTime("Seconds"),
            temperature=unit_system.UnitTemp("Kelvin"),
            stress=unit_system.UnitStress("MPa"),
        )

        return

    def set_lineedit_validators(self):
        for i in range(len(self.lineedit_widget_list)):
            self.lineedit_widget_list[i].setValidator(
                qtg.QDoubleValidator(
                    bottom=-1e35,
                    decimals=10,
                    notation=qtg.QDoubleValidator.ScientificNotation,
                    top=1.0e35,
                )
            )
        return

    # Formatting Function
    @staticmethod
    def format_value_to_string(value):
        print("Value: ", value)
        if abs(value) == "":
            return abs(value)
        elif abs(value) >= 1.0e10:
            fmt = "{:.3e}"
        elif abs(value) < 1.0e10 and abs(value) >= 1.0e4:
            fmt = "{:.0f}"
        elif abs(value) < 1.0e4 and abs(value) >= 1.0e2:
            fmt = "{:.2f}"
        elif abs(value) < 1.0e2 and abs(value) >= 1.0e1:
            fmt = "{:.4f}"
        else:
            fmt = "{:.6f}"

        print("Format: ", fmt)
        formatted_value = fmt.format(value)
        return str(formatted_value)

    def place_mdmodel(self, md_model: mdmodel.MdModel):
        # Set all the widgets to the md_model values
        self.a1_value.setText(self.format_value_to_string(md_model.a1))
        self.n1_value.setText(self.format_value_to_string(md_model.n1))
        self.q1divr_value.setText(self.format_value_to_string(md_model.q1divr))
        self.a2_value.setText(self.format_value_to_string(md_model.a2))
        self.n2_value.setText(self.format_value_to_string(md_model.n2))
        self.q2divr_value.setText(self.format_value_to_string(md_model.q2divr))
        self.b1_value.setText(self.format_value_to_string(md_model.b1))
        self.b2_value.setText(self.format_value_to_string(md_model.b2))
        self.q_value.setText(self.format_value_to_string(md_model.q))
        self.sig0_value.setText(self.format_value_to_string(md_model.sig0))
        self.k0_value.setText(self.format_value_to_string(md_model.k0))
        self.m_value.setText(self.format_value_to_string(md_model.m))
        self.c_value.setText(self.format_value_to_string(md_model.c))
        self.alpha_value.setText(self.format_value_to_string(md_model.alpha))
        self.beta_value.setText(self.format_value_to_string(md_model.beta))
        self.delta_value.setText(self.format_value_to_string(md_model.delta))
        self.mu_value.setText(self.format_value_to_string(md_model.mu))

        # Set Unit System
        self.unit_system = md_model.unit_system
        return

    def clear_table(self):
        for i in range(len(self.lineedit_widget_list)):
            self.lineedit_widget_list[i].clear()
        return

    def validate(self) -> bool:
        for i in range(len(self.value_widget_list)):
            if self.value_widget_list[i].text() == "":
                return False
        return True

    def get_table_mdmodel(self, usys: unit_system.UnitSystem):
        table_mdmodel = mdmodel.MdModel()
        table_mdmodel.set_custom_vals_units(
            a1=float(self.a1_value.text()),
            n1=float(self.n1_value.text()),
            q1divr=float(self.q1divr_value.text()),
            a2=float(self.a2_value.text()),
            n2=float(self.n2_value.text()),
            q2divr=float(self.q2divr_value.text()),
            b1=float(self.b1_value.text()),
            b2=float(self.b2_value.text()),
            q=float(self.q_value.text()),
            sig0=float(self.sig0_value.text()),
            k0=float(self.k0_value.text()),
            m=float(self.m_value.text()),
            c=float(self.c_value.text()),
            alpha=float(self.alpha_value.text()),
            beta=float(self.beta_value.text()),
            delta=float(self.delta_value.text()),
            mu=float(self.mu_value.text()),
            usys=usys,
        )
        print(table_mdmodel.a1)
        return table_mdmodel

    def convert_usys(self, to_unit: unit_system.UnitSystem):
        self.convert_invtime_usys(to_unit.time)
        self.convert_stress_usys(to_unit.stress)
        self.convert_temp_usys(to_unit.temperature)
        self.convert_invtemp_usys(to_unit.temperature)

        self.unit_system = to_unit

        return

    def convert_invtime_usys(self, to_unit: unit_system.UnitTime):
        # Set the unit labels on the form
        for i in range(len(self.time_unit_widget_list)):
            self.time_unit_widget_list[i].setText(self.get_time_unit_string(to_unit))

        # Convert the time parameter QLineEdit widgets
        for i in range(len(self.time_widget_list)):
            # Get value from widget
            value = self.time_widget_list[i].text()

            if value == "":
                pass
            else:
                value = float(value)
                value = unit_system.convert_invtime_to_base(
                    value, self.unit_system.time
                )
                value = unit_system.convert_invtime_from_base(value, to_unit)

                # Format the value
                value = self.format_value_to_string(value)

                # Set the value in the widget
                self.time_widget_list[i].setText(value)

        return

    def convert_stress_usys(self, to_unit: unit_system.UnitStress):
        # Set the unit labels on the form
        for i in range(len(self.stress_unit_widget_list)):
            self.stress_unit_widget_list[i].setText(
                self.get_stress_unit_string(to_unit)
            )

        # Convert the time parameter QLineEdit widgets
        for i in range(len(self.stress_widget_list)):
            # Get value from widget
            value = self.stress_widget_list[i].text()

            if value == "":
                pass
            else:
                value = float(value)
                value = unit_system.convert_stress_to_base(
                    value, self.unit_system.stress
                )
                value = unit_system.convert_stress_from_base(value, to_unit)

                # Format the value
                value = self.format_value_to_string(value)

                # Set the value in the widget
                self.stress_widget_list[i].setText(value)

        return

    def convert_temp_usys(self, to_unit: unit_system.UnitTemp):
        for i in range(len(self.temp_unit_widget_list)):
            self.temp_unit_widget_list[i].setText(self.get_temp_unit_string(to_unit))

        # Convert the time parameter QLineEdit widgets
        for i in range(len(self.temp_widget_list)):
            # Get value from widget
            value = self.temp_widget_list[i].text()

            if value == "":
                pass
            else:
                value = float(value)
                value = unit_system.convert_temp_to_base(
                    value, self.unit_system.temperature
                )
                value = unit_system.convert_temp_from_base(value, to_unit)

                # Format the value
                value = self.format_value_to_string(value)

                # Set the value in the widget
                self.temp_widget_list[i].setText(value)

        return

    def convert_invtemp_usys(self, to_unit: unit_system.UnitTemp):
        for i in range(len(self.invtemp_unit_widget_list)):
            self.invtemp_unit_widget_list[i].setText(
                self.get_invtemp_unit_string(to_unit)
            )

        # Convert the time parameter QLineEdit widgets
        for i in range(len(self.invtemp_widget_list)):
            # Get value from widget
            value = self.invtemp_widget_list[i].text()

            if value == "":
                pass
            else:
                value = float(value)
                value = unit_system.convert_invtemp_to_base(
                    value, self.unit_system.temperature
                )
                value = unit_system.convert_invtemp_from_base(value, to_unit)

                # Format the value
                value = self.format_value_to_string(value)

                # Set the value in the widget
                self.invtemp_widget_list[i].setText(value)

        return

    @staticmethod
    def get_time_unit_string(time_unit: unit_system.UnitTime):
        if time_unit.name == "SECONDS":
            return "sec<html><sup>-1</sup></html>"
        elif time_unit.name == "DAYS":
            return "day<html><sup>-1</sup></html>"
        elif time_unit.name == "YEARS":
            return "year<html><sup>-1</sup></html>"
        return

    @staticmethod
    def get_stress_unit_string(stress_unit: unit_system.UnitStress):
        if stress_unit.name == "MPA":
            return "MPa"
        elif stress_unit.name == "PSI":
            return "psi"

    @staticmethod
    def get_temp_unit_string(temp_unit: unit_system.UnitTemp):
        if temp_unit.name == "KELVIN":
            return "K"
        elif temp_unit.name == "CELSIUS":
            return "<html>&deg;</html>C"
        elif temp_unit.name == "FAHRENHEIT":
            return "<html>&deg;</html>F"
        elif temp_unit.name == "RANKINE":
            return "R"

    @staticmethod
    def get_invtemp_unit_string(temp_unit: unit_system.UnitTemp):
        if temp_unit.name == "KELVIN":
            return "K<html><sup>-1</sup></html>"
        elif temp_unit.name == "CELSIUS":
            return "<html>&deg;</html>C<html><sup>-1</sup></html>"
        elif temp_unit.name == "FAHRENHEIT":
            return "<html>&deg;</html>F<sup>-1</sup>"
        elif temp_unit.name == "RANKINE":
            return "R<html><sup>-1</sup></html>"
