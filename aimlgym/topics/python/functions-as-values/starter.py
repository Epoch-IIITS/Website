import functools


def pipeline(*funcs):
    def run(x):
        # TODO: apply each function in order
        return x
    return run


def sort_words(words):
    # TODO: sorted with key=lambda ...
    return list(words)


def format_record(name, *scores, sep=", ", **extra):
    # TODO
    return name


def count_calls(func):
    # TODO: return a wrapper with a .calls counter
    return func
