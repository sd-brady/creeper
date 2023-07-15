from . import unit_system


class MdModel:
    def __init__(
        self,
    ):
        return

    def set_soft_salt_base_units(self):
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
        self.unit_system = unit_system.UnitSystem(
            time=unit_system.UnitTime("Seconds"),
            temperature=unit_system.UnitTemp("Kelvin"),
            stress=unit_system.UnitStress("MPa"),
        )
        return

    def set_hard_salt_base_units(self):
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
        self.unit_system = unit_system.UnitSystem(
            time=unit_system.UnitTime("Seconds"),
            temperature=unit_system.UnitTemp("Kelvin"),
            stress=unit_system.UnitStress("MPa"),
        )
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
        unit_system: unit_system.UnitSystem,
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
        self.unit_system = unit_system

    def set_default_max_values_base_units(self):
        self.a1 = 9.81e22
        self.n1 = 7.0
        self.q1divr = 12589.0
        self.a2 = 1.132e13
        self.n2 = 5.0
        self.q2divr = 5035.5
        self.b1 = 7121000.0
        self.b2 = 0.0355
        self.q = 5335.0
        self.sig0 = 20.57
        self.k0 = 40000000.0
        self.m = 4.5
        self.c = 0.009198
        self.alpha = -2.0
        self.beta = -2.0
        self.delta = 0.58
        self.mu = 12400.0
        self.unit_system = unit_system.UnitSystem(
            time=unit_system.UnitTime("Seconds"),
            temperature=unit_system.UnitTemp("Kelvin"),
            stress=unit_system.UnitStress("MPa"),
        )
        return

    def set_default_min_values_base_units(self):
        self.a1 = 1.445e22
        self.n1 = 4.5
        self.q1divr = 12589.0
        self.a2 = 1.667e12
        self.n2 = 4.0
        self.q2divr = 5035.5
        self.b1 = 104900.0
        self.b2 = 0.00523
        self.q = 5335.0
        self.sig0 = 20.57
        self.k0 = 30000.0
        self.m = 2.0
        self.c = 0.009198
        self.alpha = -35.0
        self.beta = -35.0
        self.delta = 0.58
        self.mu = 12400.0
        self.unit_system = unit_system.UnitSystem(
            time=unit_system.UnitTime("Seconds"),
            temperature=unit_system.UnitTemp("Kelvin"),
            stress=unit_system.UnitStress("MPa"),
        )
        return
