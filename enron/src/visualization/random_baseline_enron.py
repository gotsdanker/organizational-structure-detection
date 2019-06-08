def random_baseline_enron(levels):
    if levels == 2:
        return 0.48
    elif levels == 3:
        return 0.32
    else:
        raise Exception("Unsupported number of levels")
