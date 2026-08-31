# Lab 2: The Complexity Profiler

Full assignment: `Lab_02_The_Complexity_Profiler.md` (Blackboard / course repo).

## Setup
```bash
git clone <your-repo-url>
cd <your-repo-folder>
pip install matplotlib
```

## Run
```bash
python profile_curves.py
```

Complete `algorithms.py` until every check prints `PASS`. The script
profiles your three functions across increasing input sizes, checks
the measured growth against the expected complexity class, and saves
`curves.png`. The Success Token only appears once every check passes.

## Submit
1. `Lab2_Theory.pdf` (or `.md`)
2. `algorithms.py`
3. The Success Token

## Troubleshooting

- **No token, but every check reads PASS?** Keep scrolling. Growth-rate checks run *after* correctness checks and can still fail on their own.
- **`curves.png` never appears?** Run `pip install matplotlib`. A missing matplotlib doesn't block the Success Token, but Part A has nothing to reference.
- **An exponent way off (`bubble_sort` reading ~0.9)?** Check for an accidental `sorted()`/`.sort()` call hiding somewhere. It silently makes `bubble_sort` look linear-ish at small n.
- **Script pauses for a while near n = 1600?** Expected. Real O(n²) work at that size takes several seconds; it isn't frozen.
