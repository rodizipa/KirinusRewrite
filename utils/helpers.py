
def checkdigitarguments(args, default):
    for item in args:
        if item.isdigit():
            return int(item)
    return default
