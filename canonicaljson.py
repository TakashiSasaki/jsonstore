import json
import jcs


def _convert_to_es6(value):
    fvalue = float(value)
    if fvalue == 0:
        return "0"
    py_double = str(fvalue)
    if "n" in py_double:
        raise ValueError(f"Invalid JSON number: {py_double}")
    sign = ""
    if py_double.startswith("-"):
        sign = "-"
        py_double = py_double[1:]
    exp_str = ""
    exp_val = 0
    q = py_double.find("e")
    if q > 0:
        exp_str = py_double[q:]
        if exp_str[2:3] == "0":
            exp_str = exp_str[:2] + exp_str[3:]
        py_double = py_double[:q]
        exp_val = int(exp_str[1:])
    first = py_double
    dot = ""
    last = ""
    q = py_double.find(".")
    if q > 0:
        dot = "."
        first = py_double[:q]
        last = py_double[q + 1 :]
    if last == "0":
        dot = ""
        last = ""
    if exp_val > 0 and exp_val < 21:
        first += last
        last = ""
        dot = ""
        exp_str = ""
        q = exp_val - len(first)
        while q >= 0:
            q -= 1
            first += "0"
    elif exp_val < 0 and exp_val > -7:
        last = first + last
        first = "0"
        dot = "."
        exp_str = ""
        q = exp_val
        while q < -1:
            q += 1
            last = "0" + last
    return sign + first + dot + last + exp_str


def _canonicalize(obj):
    if obj is None:
        return "null"
    if obj is True:
        return "true"
    if obj is False:
        return "false"
    if isinstance(obj, (int, float)):
        return _convert_to_es6(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, (list, tuple)):
        return "[" + ",".join(_canonicalize(x) for x in obj) + "]"
    if isinstance(obj, dict):
        items = []
        for key in sorted(obj.keys()):
            if isinstance(key, str):
                key_str = json.dumps(key, ensure_ascii=False)
            elif key is None:
                key_str = "null"
            elif key is True:
                key_str = "true"
            elif key is False:
                key_str = "false"
            elif isinstance(key, (int, float)):
                key_str = _convert_to_es6(key)
            else:
                raise TypeError(f"key {key!r} is not JSON serializable")
            items.append(f"{key_str}:{_canonicalize(obj[key])}")
        return "{" + ",".join(items) + "}"
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def canonical_json(obj) -> str:
    result = _canonicalize(obj)
    jcs_result = jcs.canonicalize(obj).decode("utf-8")
    assert result == jcs_result, f"Canonical mismatch: {result} != {jcs_result}"
    return result
