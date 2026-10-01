"""Reader for EQE_*.txt exports (tab separated, 27 side-by-side blocks of 6 columns).

Each 6-column block is laid out as:
    cols 0-3 : Lambda(nm), EQE (%), SR (A/W), Jsc (mA/cm^2)   (data from row 5 down)
    col  4-5 : metadata key / value pairs (Name, Mode, Range, AM1.5G, ..., Date, ...)
Row 0 holds the block number.
"""
import csv

import pandas as pd

BLOCK_WIDTH = 6
HEADER_ROW = 4  # row with the data column names
DATA_START = 5


def read_eqe(path):
    """Return (meta, df).

    meta : {sample_name: {key: value}}  numbers -> float, Date -> Timestamp
    df   : index Lambda(nm), columns MultiIndex (sample_name, quantity)
    """
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        rows = [r for r in csv.reader(f, delimiter="\t") if any(c.strip() for c in r)]

    n_blocks = len(rows[0]) // BLOCK_WIDTH
    meta, frames = {}, {}

    for b in range(n_blocks):
        c0 = b * BLOCK_WIDTH
        block = [r[c0:c0 + BLOCK_WIDTH] for r in rows]

        # metadata: key in col 4, value in col 5 (header "Infomation" has no value)
        m = {"Block": int(block[0][0])}
        for r in block[1:]:
            key, val = r[4].strip(), r[5].strip()
            if key and key != "Infomation":
                m[key] = _convert(key, val)
        # AM1.5G/D/AM0 Jsc are repeated in cols 0-1 of rows 1-3; those are the same values
        name = m.get("Name") or f"block{b + 1}"
        if name in meta:
            raise ValueError(f"duplicate sample name {name!r} (block {b + 1})")

        cols = [c.strip() for c in block[HEADER_ROW][:4]]
        data = pd.DataFrame(
            [[float(x) for x in r[:4]] for r in block[DATA_START:] if r[0].strip()],
            columns=cols,
        ).set_index(cols[0])
        meta[name], frames[name] = m, data

    df = pd.concat(frames, axis=1)
    return meta, df


def _convert(key, val):
    if key == "Date":
        return pd.to_datetime(val, format="%Y-%m-%d_%H-%M-%S")
    if key == "Range (nm)":
        return val  # e.g. "300 - 1100"
    try:
        return float(val)
    except ValueError:
        return val


if __name__ == "__main__":
    meta, df = read_eqe("EQE_2026_06_23-13_30.txt")
    print(meta["G1-3"])
    print(df.shape)
    print(df["G1-3"].head())
