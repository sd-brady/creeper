from pprint import pprint
from . import data_classes as dc


def get_localfit_dict(fit: dc.LocalFit) -> None:
    return


def export_config(save_filename: str, test_suite: dc.TestSuite) -> None:
    test_suite_dict = {
        "test_list": [],
        "num_tests": test_suite.num_tests,
    }
    for i in range(len(test_suite.test_list)):
        # Compile the local fit list
        for j in range(test_suite.test_list[i].num_localfits):
            local_fit_ = {
                "name": test_suite.test_list[i].localfit_list[j].name,
                "primary": test_suite.test_list[i].localfit_list[j].primary,
                #         self.a1 = 1.445e22
        # self.n1 = 5.5
        # self.q1divr = 12589.0
        # self.a2 = 1.667e12
        # self.n2 = 5.0
        # self.q2divr = 5035.5
        # self.b1 = 104900.0
        # self.b2 = 0.00523
        # self.q = 5335.0
        # self.sig0 = 20.57
        # self.k0 = 627500.0
        # self.m = 3.0
        # self.c = 0.009198
        # self.alpha = -17.37
        # self.beta = -7.738
        # self.delta = 0.58
        # self.mu = 12400.0
                "mdtablemodel": {
                    "val_model": {
                        "a1": test_suite.test_list[i]
                        .localfit_list[j]
                        .mdtablemodel.val_model.a1,
                        "n1": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.n1,
                        "q1divr": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.q1divr,
                        "a2": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.a2,
                        "n2": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.n2,
                        "q2divr": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.q2divr,
                        "b1": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.b1,
                        "b2": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.b2,
                        "q": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.q,
                        "sig0": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.sig0,
                        "k0": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.k0,
                        "m": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.m,
                        "c": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.c,
                        "alpha": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.alpha,
                        "beta": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.beta,
                        "delta": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.delta,
                        "mu": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.mu,
                        "gamma": test_suite.test_list[i].localfit_list[j].mdtablemodel.val_model.gamma
                    }
                },
            }

        # Compile the test dictionary
        test_dict = {
            "name": test_suite.test_list[i].name,
            "stress": test_suite.test_list[i].stress,
            "color": test_suite.test_list[i].color,
            "active": test_suite.test_list[i].active_state,
            "test_data": {
                "time": test_suite.test_list[i].test_data.time,
                "stress": test_suite.test_list[i].test_data.stress,
                "temperature": test_suite.test_list[i].test_data.temperature,
                "strain": test_suite.test_list[i].test_data.strain,
            },
            "localfits": {},
        }

        test_suite_dict["test_list"].append(test_dict)

    pprint(test_suite_dict)

    return
