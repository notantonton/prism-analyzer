#!/usr/bin/env python3
"""Structural checks for a Prism Analyzer Kill Matrix (response.md).

Usage: python3 check_matrix.py <response.md> [--cycle N]
Prints JSON with parsed relief-map rows, formula checks and threat-index checks.
"""
import json
import re
import sys

VEC_RE = re.compile(r"^\s*\|?\s*\**\s*([1-4]\.[12])\b")


def parse_relief_rows(text):
    rows = {}
    for line in text.splitlines():
        if "|" not in line:
            continue
        m = VEC_RE.match(line)
        if not m:
            continue
        cells = [c.strip().strip("*") for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        vid = m.group(1)
        nums = []
        for c in cells[1:]:
            mm = re.fullmatch(r"-?\d+(?:[.,]\d+)?", c)
            nums.append(float(mm.group(0).replace(",", ".")) if mm else None)
        # expected column order: E, S, L, [Модификаторы], P, ...
        e, s, l = nums[0], nums[1], nums[2]
        p = None
        mods = None
        if len(cells) > 5 and nums[3] is None:
            mods = cells[4]
            p = nums[4]
        else:
            p = nums[3]
        decision = " ".join(cells[5:7]) if len(cells) > 5 else ""
        if vid not in rows:
            rows[vid] = {"E": e, "S": s, "L": l, "mods": mods, "P": p, "decision": decision, "raw": line.strip()}
    return rows


def check_formula(rows):
    out = []
    for vid, r in sorted(rows.items()):
        if None in (r["E"], r["S"], r["L"], r["P"]):
            out.append({"vector": vid, "ok": None, "note": "unparsed"})
            continue
        base = (r["E"] + 2 * r["S"]) * r["L"]
        out.append({"vector": vid, "base": base, "P": r["P"], "mods": r["mods"], "ok_base": abs(base - r["P"]) < 1e-6})
    return out


def check_indices(text):
    res = []
    for m in re.finditer(r"I\s*(\d)\s*[×x*]\s*T\s*(\d)\s*[×x*]\s*D\s*(\d)\s*=\s*(\d+)", text):
        i, t, d, tot = map(int, m.groups())
        res.append({"expr": m.group(0), "ok": i * t * d == tot})
    return res


def main():
    path = sys.argv[1]
    text = open(path, encoding="utf-8").read()
    rows = parse_relief_rows(text)
    activated = [v for v, r in rows.items() if re.search(r"АКТИВИРОВАН(?!\w)|ПЕРЕПРОВЕРКА|РУЧНОЙ", r["raw"]) and not re.search(r"не\s+актив|НЕ\s+АКТИВ", r["raw"], re.I)]
    out = {
        "rows_found": sorted(rows),
        "all_8": len(rows) == 8,
        "formula": check_formula(rows),
        "indices": check_indices(text),
        "activated_from_map": sorted(activated),
        "cycle_line": re.findall(r"\[ЦИКЛ:\s*([^\]]+)\]", text),
        "isolation_line": re.findall(r"\[ИЗОЛЯЦИЯ:\s*([^\]]+)\]", text),
        "not_activated_line": bool(re.search(r"\[НЕ АКТИВИРОВАНЫ:", text)),
        "vector_blocks": re.findall(r"\[ВЕКТОР\s+([1-4]\.[12])", text),
        "laws_used": re.findall(r"Применённый закон:\s*([1-4]\.[12]\.\d+)", text),
        "advice_words": re.findall(r"\b(рекоменд\w*|следует|стоит\s+\w+|нужно\s+\w+|советуем)\b", text, re.I),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
