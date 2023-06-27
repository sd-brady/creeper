def get_strain_rate(time_list, strain_list):
    sr_time_list = []
    strain_rate_list = []

    for i in range(1, len(time_list)):
        sr_time_list.append(time_list[i])
        strain_rate_list.append(
            (strain_list[i] - strain_list[i - 1]) / (time_list[i] - time_list[i - 1])
        )

    return strain_rate_list
