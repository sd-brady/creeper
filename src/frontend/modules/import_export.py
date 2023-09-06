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
            {
                "name": test_suite.test_list[i].localfit_list[j].name,
                "primary": test_suite.test_list[i].localfit_list[j].primary,
                "mdtablemodel": {
                    "val_model": {
                        "a1": test_suite.test_list[i]
                        .localfit_list[j]
                        .mdtablemodel.val_model.a1,
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
