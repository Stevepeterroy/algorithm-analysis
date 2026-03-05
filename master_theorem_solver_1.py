import re
import math
import sys

OUTPUT_FILE = "master_theorem_solver_output.txt"
DEMO_RECURRENCES = [
    "T(n) = 3T(n/3) + n^2",
]

def parse_recurrence(expr: str):
    expr = expr.replace(" ", "").replace("*", "")
    pattern = r"[Tt]\(n\)=(\d*)T\(n/(\d+)\)([\+\-].*)?$"
    m = re.match(pattern, expr, re.IGNORECASE)
    if not m:
        raise ValueError("Cannot parse. Expected form:  T(n) = aT(n/b) + f(n)")
    a_str, b_str, fn_raw = m.group(1), m.group(2), m.group(3)
    a = int(a_str) if a_str else 1
    b = int(b_str)
    fn_str = fn_raw if fn_raw else "+1"
    fn_str = fn_str.lstrip("+")
    if a <= 0:
        raise ValueError("a must be a positive integer >= 1.")
    if b <= 1:
        raise ValueError("b must be an integer > 1.")
    return a, b, fn_str


def classify_fn(fn_str: str):
    s = fn_str.strip().lstrip("+").lower()
    if re.fullmatch(r"\d+(\.\d+)?", s):
        return 0.0, 0
    if re.fullmatch(r"sqrt\(n\)", s):
        return 0.5, 0
    if re.fullmatch(r"log\(?n\)?", s):
        return 0.0, 1
    if s == "n":
        return 1.0, 0
    if re.fullmatch(r"n\*?log\(?n\)?", s):
        return 1.0, 1
    m = re.fullmatch(r"n\^(\d+(\.\d+)?)", s)
    if m:
        return float(m.group(1)), 0
    m = re.fullmatch(r"n\^(\d+(\.\d+)?)\*?log\(?n\)?", s)
    if m:
        return float(m.group(1)), 1
    return 0.0, 0


def apply_masters_theorem(a, b, fn_str):
    result = {}
    result["a"] = a
    result["b"] = b
    result["fn"] = fn_str
    log_b_a = math.log(a, b)
    result["log_b_a"] = log_b_a
    k, p = classify_fn(fn_str)
    result["k"] = k
    result["p"] = p
    eps = 1e-9

    if k < log_b_a - eps:
        result["case"] = 1
        result["complexity"] = f"Θ(n^{log_b_a:.4g})"
        result["explanation"] = (
            f"f(n) = Θ(n^{k}) is polynomially smaller than n^log_{b}({a}) = n^{log_b_a:.4g}.\n"
            f"  T(n) = Θ(n^log_{b}({a})) = {result['complexity']}"
        )
    elif abs(k - log_b_a) < eps:
        if p >= 0:
            if p == 0:
                result["complexity"] = f"Θ(n^{log_b_a:.4g} · log n)"
            elif p == 1:
                result["complexity"] = f"Θ(n^{log_b_a:.4g} · log² n)"
            else:
                result["complexity"] = f"Θ(n^{log_b_a:.4g} · log^{p+1} n)"
            result["case"] = 2
            result["explanation"] = (
                f"f(n) = Θ(n^{k} · log^{p} n) matches n^log_{b}({a}) = n^{log_b_a:.4g}.\n"
                f"  T(n) = {result['complexity']}"
            )
        else:
            result["case"] = "2 (extended, p < 0 — theorem not directly applicable)"
            result["complexity"] = "Cannot determine with standard Master's Theorem"
            result["explanation"] = "p < 0 case requires extended Master Theorem analysis."
    elif k > log_b_a + eps:
        result["case"] = 3
        result["complexity"] = f"Θ(n^{k})" if p == 0 else f"Θ(n^{k} · log^{p} n)"
        result["explanation"] = (
            f"f(n) = Θ(n^{k}) is polynomially larger than n^log_{b}({a}) = n^{log_b_a:.4g}.\n"
            f"  Regularity condition a·f(n/b) <= c·f(n) is assumed to hold.\n"
            f"  T(n) = {result['complexity']}"
        )
    else:
        result["case"] = "Indeterminate"
        result["complexity"] = "Master's Theorem does not directly apply"
        result["explanation"] = (
            "The recurrence falls in a gap between cases. "
            "Use the Akra-Bazzi method or substitution."
        )
    return result


def format_output(recurrence_input, result):
    lines = []
    sep = "=" * 45
    lines.append(sep)
    lines.append("   MASTER'S THEOREM SOLVER ")
    lines.append(sep)
    lines.append(f"\nInput Recurrence  : {recurrence_input}")
    lines.append(f"\nExtracted Parameters")
    lines.append(f"  a               = {result['a']}")
    lines.append(f"  b               = {result['b']}")
    lines.append(f"  f(n)            = {result['fn']}")
    lines.append(f"\nComputed Values")
    lines.append(f"  log_b(a)        = log_{result['b']}({result['a']}) = {result['log_b_a']:.6f}")
    lines.append(f"  f(n) exponent k = {result['k']}")
    lines.append(f"  f(n) log power p= {result['p']}")
    lines.append(f"\nMaster's Theorem Case : {result['case']}")
    lines.append(f"\nExplanation:")
    lines.append(f"  {result['explanation']}")
    lines.append(f"\n{'─'*60}")
    lines.append(f"  Time Complexity  ->  {result['complexity']}")
    lines.append(f"{'─'*60}\n")
    return "\n".join(lines)





def main():
    all_output = []
    if len(sys.argv) > 1:
        inputs = [" ".join(sys.argv[1:])]
    else:
        print("No recurrence supplied. Running built-in demo examples.\n")
        inputs = DEMO_RECURRENCES

    for rec in inputs:
        print(f"Processing: {rec}")
        try:
            a, b, fn_str = parse_recurrence(rec)
            result = apply_masters_theorem(a, b, fn_str)
            out = format_output(rec, result)
        except ValueError as e:
            out = f"\n[ERROR] {rec}\n  -> {e}\n"
        print(out)
        all_output.append(out)

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(all_output))
    print(f"\n  All results saved to '{OUTPUT_FILE}'")


if __name__ == "__main__":
    main()
