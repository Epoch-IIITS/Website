r"""Reference solution for PY-17 Functions as Values.

`pipeline` returns a closure that remembers `funcs`. The sort key is a tuple, so ties in length
fall back to alphabetical order. `format_record` treats `*scores` as a tuple and `**extra` as a
dict, sorting the latter so the output is deterministic. The decorator stores its counter on the
wrapper itself and forwards every argument with `*args, **kwargs`.
"""
import functools


def pipeline(*funcs):
    def run(x):
        for f in funcs:
            x = f(x)
        return x
    return run


def sort_words(words):
    return sorted(words, key=lambda w: (len(w), w))


def format_record(name, *scores, sep=", ", **extra):
    text = f"{name}: " + sep.join(str(s) for s in scores)
    if extra:
        text += " | " + ", ".join(f"{k}={v}" for k, v in sorted(extra.items()))
    return text


def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper
