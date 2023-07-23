from . import unit_system


class MdModel:
    def __init__(self):
        return

    def set_soft_salt(self, usys: unit_system.UnitSystem):
        self.unit_system = unit_system.UnitSystem(
            time=unit_system.UnitTime("Seconds"),
            temperature=unit_system.UnitTemp("Kelvin"),
            stress=unit_system.UnitStress("MPa"),
        )
        self.a1 = 9.81e22
        self.n1 = 5.5
        self.q1divr = 12589.0
        self.a2 = 1.132e13
        self.n2 = 5.0
        self.q2divr = 5035.5
        self.b1 = 7121000.0
        self.b2 = 0.0355
        self.q = 5335.0
        self.sig0 = 20.57
        self.k0 = 627500.0
        self.m = 3.0
        self.c = 0.009198
        self.alpha = -17.37
        self.beta = -7.738
        self.delta = 0.58
        self.mu = 12400.0
        self.convert_usys(usys)
        self.unit_system = usys
        return

    def set_hard_salt(self, usys: unit_system.UnitSystem):
        self.unit_system = unit_system.UnitSystem(
            time=unit_system.UnitTime("Seconds"),
            temperature=unit_system.UnitTemp("Kelvin"),
            stress=unit_system.UnitStress("MPa"),
        )
        self.a1 = 1.445e22
        self.n1 = 5.5
        self.q1divr = 12589.0
        self.a2 = 1.667e12
        self.n2 = 5.0
        self.q2divr = 5035.5
        self.b1 = 104900.0
        self.b2 = 0.00523
        self.q = 5335.0
        self.sig0 = 20.57
        self.k0 = 627500.0
        self.m = 3.0
        self.c = 0.009198
        self.alpha = -17.37
        self.beta = -7.738
        self.delta = 0.58
        self.mu = 12400.0

        self.convert_usys(usys)
        self.unit_system = usys
        return

    def set_custom_vals_units(
        self,
        a1,
        n1,
        q1divr,
        a2,
        n2,
        q2divr,
        b1,
        b2,
        q,
        sig0,
        k0,
        m,
        c,
        alpha,
        beta,
        delta,
        mu,
        usys: unit_system.UnitSystem,
    ):
        self.a1 = a1
        self.n1 = n1
        self.q1divr = q1divr
        self.a2 = a2
        self.n2 = n2
        self.q2divr = q2divr
        self.b1 = b1
        self.b2 = b2
        self.q = q
        self.sig0 = sig0
        self.k0 = k0
        self.m = m
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.delta = delta
        self.mu = mu
        self.unit_system = usys
        return

    # def default_max_vals_base_units(self):
    #     self.a1 = 9.81e22
    #     self.n1 = 7.0
    #     self.q1divr = 12589.0
    #     self.a2 = 1.132e13
    #     self.n2 = 5.0
    #     self.q2divr = 5035.5
    #     self.b1 = 7121000.0
    #     self.b2 = 0.0355
    #     self.q = 5335.0
    #     self.sig0 = 20.57
    #     self.k0 = 40000000.0
    #     self.m = 4.5
    #     self.c = 0.009198
    #     self.alpha = -2.0
    #     self.beta = -2.0
    #     self.delta = 0.58
    #     self.mu = 12400.0
    #     self.unit_system = unit_system.UnitSystem(
    #         time=unit_system.UnitTime("Seconds"),
    #         temperature=unit_system.UnitTemp("Kelvin"),
    #         stress=unit_system.UnitStress("MPa"),
    #     )
    #     return
    #
    # def default_min_vals_base_units(self):
    #     self.a1 = 1.445e22
    #     self.n1 = 4.5
    #     self.q1divr = 12589.0
    #     self.a2 = 1.667e12
    #     self.n2 = 4.0
    #     self.q2divr = 5035.5
    #     self.b1 = 104900.0
    #     self.b2 = 0.00523
    #     self.q = 5335.0
    #     self.sig0 = 20.57
    #     self.k0 = 30000.0
    #     self.m = 2.0
    #     self.c = 0.009198
    #     self.alpha = -35.0
    #     self.beta = -35.0
    #     self.delta = 0.58
    #     self.mu = 12400.0
    #     self.unit_system = unit_system.UnitSystem(
    #         time=unit_system.UnitTime("Seconds"),
    #         temperature=unit_system.UnitTemp("Kelvin"),
    #         stress=unit_system.UnitStress("MPa"),
    #     )
    #     return

    def convert_usys(self, usys: unit_system.UnitSystem):
        self.convert_invtime_usys(usys.time)
        self.convert_stress_usys(usys.stress)
        self.convert_temp_usys(usys.temperature)
        self.convert_invtemp_usys(usys.temperature)
        self.unit_system = usys
        return

    def convert_usys_to_base(self):
        base_usys = unit_system.UnitSystem(
            time=unit_system.UnitTime("Seconds"),
            temperature=unit_system.UnitTemp("Kelvin"),
            stress=unit_system.UnitStress("MPa"),
        )

        self.convert_invtime_usys(base_usys.time)
        self.convert_stress_usys(base_usys.stress)
        self.convert_temp_usys(base_usys.temperature)
        self.convert_invtemp_usys(base_usys.temperature)
        self.unit_system = base_usys
        return

    def convert_invtime_usys(self, to_unit: unit_system.UnitTime):
        self.a1 = unit_system.convert_invtime_to_base(self.a1, self.unit_system.time)
        self.a1 = unit_system.convert_invtime_from_base(self.a1, to_unit)

        self.a2 = unit_system.convert_invtime_to_base(self.a2, self.unit_system.time)
        self.a2 = unit_system.convert_invtime_from_base(self.a2, to_unit)

        self.b1 = unit_system.convert_invtime_to_base(self.b1, self.unit_system.time)
        self.b1 = unit_system.convert_invtime_from_base(self.b1, to_unit)

        self.b2 = unit_system.convert_invtime_to_base(self.b2, self.unit_system.time)
        self.b2 = unit_system.convert_invtime_from_base(self.b2, to_unit)
        return

    def convert_stress_usys(self, to_unit: unit_system.UnitStress):
        self.sig0 = unit_system.convert_stress_to_base(
            self.sig0, self.unit_system.stress
        )
        self.sig0 = unit_system.convert_stress_from_base(self.sig0, to_unit)

        self.mu = unit_system.convert_stress_to_base(self.mu, self.unit_system.stress)
        self.mu = unit_system.convert_stress_from_base(self.mu, to_unit)
        return

    def convert_temp_usys(self, to_unit: unit_system.UnitTemp):
        self.q1divr = unit_system.convert_temp_to_base(
            self.q1divr, self.unit_system.temperature
        )
        self.q1divr = unit_system.convert_temp_from_base(self.q1divr, to_unit)

        self.q2divr = unit_system.convert_temp_to_base(
            self.q2divr, self.unit_system.temperature
        )
        self.q2divr = unit_system.convert_temp_from_base(self.q2divr, to_unit)
        return

    def convert_invtemp_usys(self, to_unit: unit_system.UnitTemp):
        self.c = unit_system.convert_invtemp_to_base(
            self.c, self.unit_system.temperature
        )
        self.c = unit_system.convert_invtemp_from_base(self.c, to_unit)
        return

    def validate_mdmodel(self):
        return


class MdModelFlags:
    def __init__(
        self,
        a1_flag: bool,
        n1_flag: bool,
        q1divr_flag: bool,
        a2_flag: bool,
        n2_flag: bool,
        q2divr_flag: bool,
        b1_flag: bool,
        b2_flag: bool,
        q_flag: bool,
        sig0_flag: bool,
        k0_flag: bool,
        m_flag: bool,
        c_flag: bool,
        alpha_flag: bool,
        beta_flag: bool,
        delta_flag: bool,
        mu_flag: bool,
    ):
        self.a1_flag = a1_flag
        self.n1_flag = n1_flag
        self.q1divr_flag = q1divr_flag
        self.a2_flag = a2_flag
        self.n2_flag = n2_flag
        self.q2divr_flag = q2divr_flag
        self.b1_flag = b1_flag
        self.b2_flag = b2_flag
        self.q_flag = q_flag
        self.sig0_flag = sig0_flag
        self.k0_flag = k0_flag
        self.m_flag = m_flag
        self.c_flag = c_flag
        self.alpha_flag = alpha_flag
        self.beta_flag = beta_flag
        self.delta_flag = delta_flag
        self.mu_flag = mu_flag
        return


class MdTableModel:
    def __init__(
        self,
        val_model: MdModel,
        min_model: MdModel,
        max_model: MdModel,
        flag_model: MdModelFlags,
    ):
        self.val_model = val_model
        self.min_model = min_model
        self.max_model = max_model
        self.flag_model = flag_model
        return

    def convert_usys_to_base(self):
        self.val_model.convert_usys_to_base()
        self.min_model.convert_usys_to_base()
        self.max_model.convert_usys_to_base()
        return
