def random_baseline_mc(levels):
    if levels == 2:
        return 0.42
    elif levels == 3:
        return 0.24
    else:
        raise Exception("Unsupported number of levels")
