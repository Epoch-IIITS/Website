r"""Reference solution for NL-01 Regular Expressions for Text.

Splitting on whitespace and re-joining is the loop-free manual equivalent of `\s+` → space. The
number pattern makes the sign and decimal part optional with a non-capturing group so `findall`
returns whole matches. A look-behind stops `email#tag` from counting as a hashtag. The compiled
log pattern with named groups turns a valid line into a dict in one call and `fullmatch` rejects
anything else.
"""
import re


def collapse_spaces_manual(text):
    return " ".join(text.split())


def collapse_spaces(text):
    return re.sub(r"\s+", " ", text).strip()


def mask_digits(text):
    return re.sub(r"\d", "#", text)


def find_numbers(text):
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text)]


def find_hashtags(text):
    return [tag.lower() for tag in re.findall(r"(?<!\w)#(\w+)", text)]


LOG = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) "
    r"(?P<level>DEBUG|INFO|WARNING|ERROR) (?P<message>.+)"
)


def parse_log(line):
    m = LOG.fullmatch(line)
    return m.groupdict() if m else None
