# -*- coding: utf-8 -*-
"""Generate remaining Eighth Schedule locale JSON files from flat key maps."""
import json
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "src" / "i18n" / "locales"
en = json.loads((DIR / "en.json").read_text(encoding="utf-8"))


def flatten(obj, p=""):
    o = {}
    for k, v in obj.items():
        nk = f"{p}.{k}" if p else k
        if isinstance(v, dict):
            o.update(flatten(v, nk))
        else:
            o[nk] = v
    return o


def unflatten(flat):
    root = {}
    for k, v in flat.items():
        parts = k.split(".")
        cur = root
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = v
    return root


EN = flatten(en)


def write_locale(code, overrides):
    out = dict(EN)
    out.update(overrides)
    out["appName"] = "BOVIMED"
    missing = [k for k in EN if k not in out]
    if missing:
        raise SystemExit(f"{code}: missing {len(missing)} keys e.g. {missing[:8]}")
    text = json.dumps(unflatten(out), ensure_ascii=False, indent=2) + "\n"
    (DIR / f"{code}.json").write_text(text, encoding="utf-8")
    print(f"wrote {code}.json ({len(overrides)} overrides)")


# Shared brand defaults applied after language-specific maps
BRAND = {
    "appName": "BOVIMED",
    "history.live": "LIVE",
    "history.demo": "Demo",
}


def apply(code, d):
    d = {**d, **BRAND}
    # Ensure every EN key present: fill from d only; caller must supply all non-brand
    write_locale(code, d)


if __name__ == "__main__":
    print("loader ready", len(EN))
