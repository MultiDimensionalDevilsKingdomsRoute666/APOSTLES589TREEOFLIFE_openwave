# M8.16.1: the freeze block

## The terms

- The filed terms, `run/m8_16_task_details.md`: SHA-256 `9d16712982e5388970fca33de59958721109e09f9d88dec7a2a088489ad3efd6`.
- The go: https://github.com/openwave-labs/openwave/pull/650#issuecomment-6385959498
- `run/FROZEN.json` written 2026-10-25T01:40:57Z.

## The instrument

- The solver commit: MIT `d1c0ec889b09b4a93d5f08e63280080e25e83e2e`.
- The manifest: 48 files, SHA-256 `8cc2d7e2d01a72fc3572adabf917656abf36cbddd70ed35532b73ae5451790dd`; `run/MANIFEST_PIN` holds `8cc2d7e2d01a72fc3572adabf917656abf36cbddd70ed35532b73ae5451790dd`.
- The freeze pin, `run/FROZEN_PIN`: `c258e299b8f0268e805712b4f087b3533c6e0cd3c37e237bf3d0639540c52a2d`.

| file | SHA-256 |
| --- | --- |
| `instrument/__init__.py` | `ebb8d0440edae25ee0755fa962d24061fbebb502bf5176d3084a422188d2dcdc` |
| `instrument/basis.py` | `5728c5e8c9532bc4764dd5b9d111f693e5ba86c415d4a2b4f880e8196c66616b` |
| `instrument/branches.py` | `4e32a8cfd1cd7db4ced242ecddf5e22c9319134029877b78eae74b13b3d1a55f` |
| `instrument/certified.py` | `1f5dde36bde7edfc3257e7581b2538ab7853693ab8ed1b48dae6dc0e2de343d1` |
| `instrument/convergence.py` | `02404ab43313eb4d67cb336edbed364d9071187da66dec44bbd4f997cf66bd51` |
| `instrument/devtools.py` | `3a2d0f7d2c5bd74bdedf2a673989a67cadef25c508424ad25501745c7adb7d0f` |
| `instrument/functional.py` | `f8f9329f1fa5d2bb1f7e3718d5e5bdfa94e86f9e0dcc4dda308a7f86c0f00d79` |
| `instrument/group2i.py` | `0a9732afe32b3509976de2e519c0f8da3d4f773d2495c5c2d58d27fe5aaa85f0` |
| `instrument/linear.py` | `e0fce88f3ed8374f94f6ba329813cfb639f05a2407f9a313f66cbe79744f11c2` |
| `instrument/newton.py` | `36bd989fe10891ba49757025a908b95569cb7b7ee1901f87299dede2a10fe00f` |
| `instrument/quadrature.py` | `6c9baf9d1bd3bc8741006490f88fd4a1e134f0cd3a6ffd8f9b7f1a6074e30a71` |
| `instrument/su2.py` | `60c4f8088a089341e76fb159847784336f4ad6a886a72a1c7683ef86a63b75f6` |
| `reference/m815/branch_C2a_R4.json` | `c5266378170a2f425eb9423b0886f2a7e9db1628d4c5f80e0f70ac5aba888fde` |
| `reference/m815/branch_C2b_R2.json` | `25bcee62a88a05d03703c0a523621ac1e812ce09f8b7d0792d1ebd9fc129a716` |
| `reference/m815/branch_C3_R4.json` | `61c9d81899a80a8179582a60f52eb17fd36f71a42476374df275e28e3348d284` |
| `run/DRY.json` | `b973c86fba7966ef677cdcce9d8479687c1751817c9732db0e131b1b7ad69543` |
| `run/ENVIRONMENT.json` | `4d666fce6cddfca04d0950f6cbe3ad2524056e60f52196921a18549680ee9354` |
| `run/build_dry.py` | `34de8225eab09c8708b67e09c8bb0308e731dabee4a78b4fd57a6fca9e0cf55c` |
| `run/cases.py` | `cfc3663dc5c9ac469335ca71d8884312504362c455b6291b758d45b92ab25e9c` |
| `run/checks.py` | `c3122cd0ac692e16a5a6fb7fde178e13b27d9bb1632ad8eed32432b2c6919b84` |
| `run/driver.py` | `6fad387effeb2ac805a09f485a11037b7575f511558776d0461dd8c6f5b622f9` |
| `run/freeze_block.py` | `0de0304f237b53d61f38006e5f6f002a85213f672d3ebcff5dd3cfd99b931b1a` |
| `run/m8_16_task_details.md` | `9d16712982e5388970fca33de59958721109e09f9d88dec7a2a088489ad3efd6` |
| `run/name_targets.py` | `8b4572054cd2d6cb80352d72d2ba2805b97411d21739116ee0cb6ed9d7d4cb1d` |
| `run/next_order_values.json` | `b05fff5ddd71c29c79318b6257f940c6035d7c954f3bafa34a22080eecc00333` |
| `run/next_order_values.out` | `fc0821ecdf011190c19604ae146150a604e3ec25ac5a8ecc38a740afa84c2f55` |
| `run/next_order_values.py` | `4bf81a60beef1338c6da36b2d4c04f9d51b826322a0b1e9540769fa318f4028e` |
| `run/pin_manifest.py` | `4e7c7ab3eb36bafcb956c67751bdbc121767ba9b57bec89a8a108f5b67798580` |
| `run/record_environment.py` | `1494fb8afd942e74a646671fe16f03ad4d9b095ae62cd1be35a51b2eb3a10059` |
| `run/score_ladder.out` | `1f34ca8ab32bc303d8747a6a1fb3d35220f529243d75933c662579a61a0012c9` |
| `run/score_ladder.py` | `d4a0a083714cd201bc30ae86bbd954dc33ca87a6238fa1c7c6627bb4025e7b18` |
| `run/score_plumbing.out` | `538f9603209e5f7545d01ceb76eb435f9e8b0e6966e39544220f1b928287db8e` |
| `run/score_plumbing.py` | `93d9050b0b081fb528287274bf855034406f9b9deff961a6da8741f24b4f05a3` |
| `run/score_record.out` | `46ace07d27e2caeb592ef10fe33e3c83d70097b73a9ccdbc1810a011dc5c260c` |
| `run/score_record.py` | `01469629314e8b9ff4e8b7039ec99073926b1aa2747ce6ee5bccf952d1a5a566` |
| `run/seeds.py` | `11916c7ccd9c27583933c78b8d79f5c9ed0472c4ade946312acf4cf0bd80d87c` |
| `run/targets.json` | `6ca3854d15b5447ee2eab71670ee37b84d9bad60a4f06923d500aa72a52997af` |
| `run/test_constants.out` | `b224670fa5ed006469ec3a90d365f60823505999ea709b670df1b59857bde02b` |
| `run/test_constants.py` | `214699780f5c6fd639380c07860fb42e3b3cb474a19c9c8665bab4bd802d4385` |
| `run/test_guard.out` | `6d9f69f0b665787df7a814e7361c2597fdb40005036cdd588ef7c4d18f0fb4b3` |
| `run/test_guard.py` | `0ad237f2c9220ef14344f057ea1cc8737bd2b109ff59d27e64380e9d3f0c36a2` |
| `run/test_imports.out` | `b3b408f4e16e51fb3340adbc0fa5e3e8f482815bd6713a8deb42980c04815879` |
| `run/test_imports.py` | `f8e0c9886f2e8e422dea17546da64a2525d67095d8539f43405ec20ac417434a` |
| `run/test_k3.out` | `7d6faa272e7d180ac3baaa3f9c76f6fa2ca1c5285143ad2ecbdff4d5fe2fba4b` |
| `run/test_k3.py` | `8adccbcb7236e9a087c0e32dcf6e8d9144044d8bcedc6d8a06093a11c13246cb` |
| `run/test_verdicts.out` | `aba8d4b2c900446efa8c77aac079507d1e91b8425145881af8af5baf9195bd21` |
| `run/test_verdicts.py` | `498a700d46d195f9b4d9edb93d86fe97dc58ed976f3ca8286cb6910a3c988dae` |
| `run/write_guard.py` | `38af403dbc86ca16a3f581d5728e70fc08535a30901dae812cd848c9f26d8621` |

## The environment

- Recorded 2026-10-22T23:19:50Z, and read again when this block was built.
- Differences: none.

<details><summary>As recorded</summary>

```json
{
 "interpreter": {
  "build": "3.13.13 | packaged by conda-forge | (main, Apr  8 2026, 02:29:07) [Clang 19.1.7 ]",
  "executable": "/opt/homebrew/Caskroom/miniforge/base/bin/python3",
  "flags": {
   "dont_write_bytecode": 1,
   "isolated": 1,
   "optimize": 0
  },
  "implementation": "CPython",
  "version": "3.13.13"
 },
 "machine": {
  "arch": "arm64",
  "cores": 8,
  "cpu": "Apple M3",
  "efficiency_cores": 4,
  "model": "Mac15,13",
  "performance_cores": 4
 },
 "numpy": {
  "blas": {
   "detection method": "system",
   "found": true,
   "include directory": "unknown",
   "lib directory": "unknown",
   "name": "accelerate",
   "openblas configuration": "unknown",
   "pc file directory": "unknown",
   "version": "unknown"
  },
  "lapack": {
   "detection method": "system",
   "found": true,
   "include directory": "unknown",
   "lib directory": "unknown",
   "name": "accelerate",
   "openblas configuration": "unknown",
   "pc file directory": "unknown",
   "version": "unknown"
  },
  "version": "2.5.0"
 },
 "os": {
  "build": "24H23",
  "kernel": "24.6.0",
  "product": "macOS",
  "version": "15.8"
 },
 "recorded": "2026-10-22T23:19:50Z",
 "scipy": {
  "blas": {
   "cython blas ilp64": false,
   "detection method": "extraframeworks",
   "found": true,
   "has ilp64": false,
   "include directory": "unknown",
   "lib directory": "unknown",
   "name": "Accelerate",
   "openblas configuration": "unknown",
   "pc file directory": "unknown",
   "version": "unknown"
  },
  "lapack": {
   "detection method": "extraframeworks",
   "found": true,
   "has ilp64": false,
   "include directory": "unknown",
   "lib directory": "unknown",
   "name": "Accelerate",
   "openblas configuration": "unknown",
   "pc file directory": "unknown",
   "version": "unknown"
  },
  "version": "1.18.0"
 },
 "threading": {
  "MKL_NUM_THREADS": null,
  "OMP_NUM_THREADS": null,
  "OPENBLAS_NUM_THREADS": null,
  "VECLIB_MAXIMUM_THREADS": null
 }
}
```

</details>

<details><summary>Read again</summary>

```json
{
 "interpreter": {
  "build": "3.13.13 | packaged by conda-forge | (main, Apr  8 2026, 02:29:07) [Clang 19.1.7 ]",
  "executable": "/opt/homebrew/Caskroom/miniforge/base/bin/python3",
  "flags": {
   "dont_write_bytecode": 1,
   "isolated": 1,
   "optimize": 0
  },
  "implementation": "CPython",
  "version": "3.13.13"
 },
 "machine": {
  "arch": "arm64",
  "cores": 8,
  "cpu": "Apple M3",
  "efficiency_cores": 4,
  "model": "Mac15,13",
  "performance_cores": 4
 },
 "numpy": {
  "blas": {
   "detection method": "system",
   "found": true,
   "include directory": "unknown",
   "lib directory": "unknown",
   "name": "accelerate",
   "openblas configuration": "unknown",
   "pc file directory": "unknown",
   "version": "unknown"
  },
  "lapack": {
   "detection method": "system",
   "found": true,
   "include directory": "unknown",
   "lib directory": "unknown",
   "name": "accelerate",
   "openblas configuration": "unknown",
   "pc file directory": "unknown",
   "version": "unknown"
  },
  "version": "2.5.0"
 },
 "os": {
  "build": "24H23",
  "kernel": "24.6.0",
  "product": "macOS",
  "version": "15.8"
 },
 "scipy": {
  "blas": {
   "cython blas ilp64": false,
   "detection method": "extraframeworks",
   "found": true,
   "has ilp64": false,
   "include directory": "unknown",
   "lib directory": "unknown",
   "name": "Accelerate",
   "openblas configuration": "unknown",
   "pc file directory": "unknown",
   "version": "unknown"
  },
  "lapack": {
   "detection method": "extraframeworks",
   "found": true,
   "has ilp64": false,
   "include directory": "unknown",
   "lib directory": "unknown",
   "name": "Accelerate",
   "openblas configuration": "unknown",
   "pc file directory": "unknown",
   "version": "unknown"
  },
  "version": "1.18.0"
 },
 "threading": {
  "MKL_NUM_THREADS": null,
  "OMP_NUM_THREADS": null,
  "OPENBLAS_NUM_THREADS": null,
  "VECLIB_MAXIMUM_THREADS": null
 }
}
```

</details>

## The target records

| name | MIT commit | blob | SHA-256 |
| --- | --- | --- | --- |
| T2_R4 | `33aeb754ec8d98449346dfe27d204be79e333fa5` | `22bb03321404960b76ad568e1091f9629b4bdcb2` | `5b1758c9ec1c6566091fe9028a542f67fd6bd0ad51c927f7147d54c07d876b49` |
| T2_R5 | `33aeb754ec8d98449346dfe27d204be79e333fa5` | `2a5e77315c8c323e0c9ec8b15629fa26b6b64d98` | `a064683298ebc922ecbba06316a3af11b68a7b6193e7e04c63eaa9fc1ad931ba` |
| T3_R4 | `33aeb754ec8d98449346dfe27d204be79e333fa5` | `497301e4186b8e45d9efcb4207255d7b257f47e7` | `fe3497a3a4de45a5f3a6d2ce2a6c322feb5399610ad20d9da530acd8abdf3bc2` |
| T3_R5 | `33aeb754ec8d98449346dfe27d204be79e333fa5` | `a719df9db2b04edc06c1ec82f2d8467fc5b77c41` | `660d0322d1921bb7b6c9e7e1b71bf3c54bea63a6c17a754e22582601b49aaee4` |
| T5_R2 | `33aeb754ec8d98449346dfe27d204be79e333fa5` | `76501d58c96bec7db585dd525a09994a35f23251` | `6bcdb5cfd58980bf228b4c84271e51d1e6efa5b6052b0fd6cf98cce143a5884f` |

## The next-order values

- `run/next_order_values.json`: SHA-256 `b05fff5ddd71c29c79318b6257f940c6035d7c954f3bafa34a22080eecc00333`; its cases section `45ad237179b6c7176b4372f8b36fe6cf20ba95ebdff510f727eec1ea4a2ebeea`.
- Its script, `run/next_order_values.py`: SHA-256 `4bf81a60beef1338c6da36b2d4c04f9d51b826322a0b1e9540769fa318f4028e`.
- Its environment: python 3.13.13, sympy 1.14.0, mpmath 1.3.0, numpy 2.5.0, dps 50.

## The seeds

- The seed check, `dev/seed_check.py`: SHA-256 `c7d5d597af6d8165c48f33b8985ae6ed1863453fac0b15947ce30c4473168ea4`.

| case | Q(u) | its exact value | criticality | (k, r_u) | checked |
| --- | --- | --- | --- | --- | --- |
| C1 | 1.0000000000000016 | '1' | 1.1e-15 | (4, 2) | yes |
| C2a | 1.000777000777 | '1288/1287' | 9.0e-17 | (3, 1) | yes |
| C3 | 1.2237762237762266 | '175/143' | 2.0e-16 | (4, 4) | yes |
| P5 | 1.1846153846153862 | '77/65' | 6.8e-16 | (4, 2) | yes |
| T1/R4 | 1.0279720279720312 | '147/143' | 3.8e-17 | (3, 1) | yes |
| T2/R4 | 1.1590141125024869 | '5831/5031' | 6.4e-16 | (4, 4) | yes |
| T3/R4 | 1.35975135975136 | '1750/1287' | 4.2e-16 | (4, 4) | yes |
| T4/R4 | 1.185203461338849 | '1.1852034613388465' | 5.6e-16 | (4, 2) | yes |
| C3R/R4 | 1.184615384615388 | '77/65' | 4.2e-16 | (4, 2) | yes |
| C2a/R5 | 1.0004370629370645 | '2289/2288' | 5.3e-17 | (3, 1) | yes |
| T1/R5 | 1.015734265734266 | '581/572' | 3.3e-17 | (3, 1) | yes |
| T2/R5 | 1.0894454382826486 | '609/559' | 6.9e-16 | (4, 4) | yes |
| T3/R5 | 1.2023601398601402 | '2751/2288' | 2.8e-16 | (4, 4) | yes |
| T4/R5 | 1.1041769470031033 | '1.104176947003101' | 5.5e-16 | (4, 2) | yes |
| C2b | 1.006993006993007 | '144/143' | 8.4e-17 | (5, 1) | yes |
| T5/R2 | 1.6923076923076934 | '22/13' | 1.5e-16 | (6, 4) | yes |
| T5J/R2 | 1.6923076923076936 | '22/13' | 1.5e-16 | (6, 4) | yes |

- The files the seed check loaded, its child processes included: 12.

| file | SHA-256 | equals its manifest line |
| --- | --- | --- |
| `instrument/__init__.py` | `ebb8d0440edae25ee0755fa962d24061fbebb502bf5176d3084a422188d2dcdc` | yes |
| `instrument/basis.py` | `5728c5e8c9532bc4764dd5b9d111f693e5ba86c415d4a2b4f880e8196c66616b` | yes |
| `instrument/branches.py` | `4e32a8cfd1cd7db4ced242ecddf5e22c9319134029877b78eae74b13b3d1a55f` | yes |
| `instrument/certified.py` | `1f5dde36bde7edfc3257e7581b2538ab7853693ab8ed1b48dae6dc0e2de343d1` | yes |
| `instrument/devtools.py` | `3a2d0f7d2c5bd74bdedf2a673989a67cadef25c508424ad25501745c7adb7d0f` | yes |
| `instrument/functional.py` | `f8f9329f1fa5d2bb1f7e3718d5e5bdfa94e86f9e0dcc4dda308a7f86c0f00d79` | yes |
| `instrument/group2i.py` | `0a9732afe32b3509976de2e519c0f8da3d4f773d2495c5c2d58d27fe5aaa85f0` | yes |
| `instrument/linear.py` | `e0fce88f3ed8374f94f6ba329813cfb639f05a2407f9a313f66cbe79744f11c2` | yes |
| `instrument/newton.py` | `36bd989fe10891ba49757025a908b95569cb7b7ee1901f87299dede2a10fe00f` | yes |
| `instrument/quadrature.py` | `6c9baf9d1bd3bc8741006490f88fd4a1e134f0cd3a6ffd8f9b7f1a6074e30a71` | yes |
| `instrument/su2.py` | `60c4f8088a089341e76fb159847784336f4ad6a886a72a1c7683ef86a63b75f6` | yes |
| `run/seeds.py` | `11916c7ccd9c27583933c78b8d79f5c9ed0472c4ade946312acf4cf0bd80d87c` | yes |

## `FROZEN.json`

<details><summary>In full</summary>

```json
{
 "allowlist": [
  "C1",
  "C2a",
  "C2b",
  "C3",
  "C2a/R5",
  "P5",
  "C3R/R4",
  "T1/R4",
  "T1/R5",
  "T4/R4",
  "T4/R5",
  "T5J/R2",
  "T2/R4",
  "T2/R5",
  "T3/R4",
  "T3/R5",
  "T5/R2"
 ],
 "order": [
  "C1",
  "C2a",
  "C2b",
  "C3",
  "C2a/R5",
  "P5",
  "C3R/R4",
  "T1/R4",
  "T1/R5",
  "T4/R4",
  "T4/R5",
  "T5J/R2",
  "T2/R4",
  "T2/R5",
  "T3/R4",
  "T3/R5",
  "T5/R2"
 ],
 "cases": {
  "C1": {
   "role": "control",
   "slot": "R3",
   "level": 2,
   "lam0": 8.0,
   "orbit": "theoremD",
   "sig": null,
   "k": 4,
   "r": 2,
   "points": [
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32,
    40
   ],
   "m815": null,
   "dim": 6,
   "ranks": [
    1,
    0
   ],
   "chains": 5,
   "type": "Elliptic",
   "idx": [
    0,
    0,
    0
   ],
   "kr": 0,
   "kc": 0,
   "ki": 0,
   "Q": {
    "frac": "1/1",
    "value": 1.0
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [],
   "representative": {
    "1": [
     1.0,
     0.0
    ],
    "0": [
     0.6,
     0.3
    ],
    "-1": [
     0.0,
     -0.4
    ]
   },
   "admission": "theoremD:R3"
  },
  "C2a": {
   "role": "control",
   "slot": "R4",
   "level": 6,
   "lam0": 48.0,
   "orbit": "coherent",
   "sig": [
    0,
    0,
    10
   ],
   "k": 3,
   "r": 1,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": null,
   "dim": 4,
   "ranks": [
    1,
    0
   ],
   "chains": 3,
   "type": "Elliptic",
   "idx": [
    0,
    0,
    0
   ],
   "kr": 0,
   "kc": 0,
   "ki": 0,
   "Q": {
    "frac": "1288/1287",
    "value": 1.0007770007770007
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "28/143",
      "value": 0.1958041958041958
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "56/429",
      "value": 0.13053613053613053
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "140/99",
      "value": 1.4141414141414141
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "112/39",
      "value": 2.871794871794872
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "896/1287",
      "value": 0.6961926961926962
     },
     "mult": 1
    }
   ],
   "representative": {
    "3": [
     1.0,
     0.0
    ]
   },
   "admission": "C2a"
  },
  "C2b": {
   "role": "control",
   "slot": "R2",
   "level": 7,
   "lam0": 63.0,
   "orbit": "weight72",
   "sig": [
    0,
    0,
    10
   ],
   "k": 5,
   "r": 1,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": null,
   "dim": 6,
   "ranks": [
    1,
    0
   ],
   "chains": 5,
   "type": "Elliptic",
   "idx": [
    0,
    0,
    0
   ],
   "kr": 0,
   "kc": 0,
   "ki": 0,
   "Q": {
    "frac": "144/143",
    "value": 1.006993006993007
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "112/143",
      "value": 0.7832167832167832
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "168/143",
      "value": 1.1748251748251748
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "336/143",
      "value": 2.3496503496503496
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "504/143",
      "value": 3.5244755244755246
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "560/143",
      "value": 3.9160839160839163
     },
     "mult": 1
    }
   ],
   "representative": {
    "3.5": [
     1.0,
     0.0
    ]
   },
   "admission": "C2b"
  },
  "C3": {
   "role": "control",
   "slot": "R4",
   "level": 6,
   "lam0": 48.0,
   "orbit": "octahedron",
   "sig": [
    6,
    0,
    3
   ],
   "k": 4,
   "r": 4,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": null,
   "dim": 8,
   "ranks": [
    4,
    0
   ],
   "chains": 4,
   "type": "Hyperbolic",
   "idx": [
    6,
    3,
    3
   ],
   "kr": 3,
   "kc": 0,
   "ki": 0,
   "Q": {
    "frac": "175/143",
    "value": 1.2237762237762237
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [
    {
     "cls": "real",
     "sign": null,
     "tau": {
      "value": 0.674085679526388
     },
     "mult": 3
    }
   ],
   "representative": {
    "2": [
     1.0,
     0.0
    ],
    "-2": [
     1.0,
     0.0
    ]
   },
   "admission": "C3"
  },
  "C2a/R5": {
   "role": "R5gate",
   "slot": "R5",
   "level": 6,
   "lam0": 48.0,
   "orbit": "coherent",
   "sig": [
    0,
    0,
    10
   ],
   "k": 3,
   "r": 1,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": null,
   "dim": 4,
   "ranks": [
    1,
    0
   ],
   "chains": 3,
   "type": "Elliptic",
   "idx": [
    0,
    0,
    0
   ],
   "kr": 0,
   "kc": 0,
   "ki": 0,
   "Q": {
    "frac": "2289/2288",
    "value": 1.000437062937063
   },
   "s": {
    "frac": "9/16",
    "value": 0.5625
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "28/143",
      "value": 0.1958041958041958
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "56/429",
      "value": 0.13053613053613053
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "140/99",
      "value": 1.4141414141414141
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "112/39",
      "value": 2.871794871794872
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "896/1287",
      "value": 0.6961926961926962
     },
     "mult": 1
    }
   ],
   "representative": {
    "3": [
     1.0,
     0.0
    ]
   },
   "admission": "C2a/R5"
  },
  "P5": {
   "role": "pyramid",
   "slot": "R4",
   "level": 6,
   "lam0": 48.0,
   "orbit": "pyramid",
   "sig": [
    5,
    0,
    4
   ],
   "k": 4,
   "r": 2,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": null,
   "dim": 6,
   "ranks": [
    2,
    0
   ],
   "chains": 4,
   "type": "Hyperbolic",
   "idx": [
    5,
    1,
    4
   ],
   "kr": 0,
   "kc": 1,
   "ki": 1,
   "next_order": {
    "16": [
     {
      "s": [
       "-1.643269893669447657559704e-51",
       "0.06223486909568790724544574"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-2.502769906858040393003423e-53",
       "0.0009478635136564426746242348"
      ],
      "c_g": [
       "4.916489626638153205146562e-55",
       "-0.00001064621147000250005841326"
      ],
      "c_g_off": null,
      "under_bar": false,
      "spectrum_index": 0
     },
     {
      "s": [
       "0.04173528598376259430139185",
       "0.06091686091686091686091686"
      ],
      "mult": 1,
      "cls": "complex",
      "krein": null,
      "kappa_s": [
       "0.0006356461480653562023710027",
       "0.0009277896887803903470073557"
      ],
      "c_g": [
       "0.0001195515456890397380967572",
       "-0.0002358143032732839336240766"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-4.902349205570723022598736e-80",
       "1.095185488324669513111975"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-7.466486249081060140228799e-82",
       "0.01668014057317097391851552"
      ],
      "c_g": [
       "6.764232268557010721252782e-56",
       "-0.0000767611760516291178604035"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     }
    ],
    "24": [
     {
      "s": [
       "-1.643269893669447657559704e-51",
       "0.06223486909568790724544574"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-2.502769906858040393003423e-53",
       "0.0009478635136564426746242348"
      ],
      "c_g": [
       "4.617478195520401141526899e-55",
       "-0.00001313911766073773401189807"
      ],
      "c_g_off": null,
      "under_bar": false,
      "spectrum_index": 0
     },
     {
      "s": [
       "0.04173528598376259430139185",
       "0.06091686091686091686091686"
      ],
      "mult": 1,
      "cls": "complex",
      "krein": null,
      "kappa_s": [
       "0.0006356461480653562023710027",
       "0.0009277896887803903470073557"
      ],
      "c_g": [
       "0.0001242332455239913262308566",
       "-0.0002348453653056894878831448"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-4.902349205570723022598736e-80",
       "1.095185488324669513111975"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-7.466486249081060140228799e-82",
       "0.01668014057317097391851552"
      ],
      "c_g": [
       "9.179640923728366821050269e-56",
       "-0.0001321715189203882735231213"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     }
    ],
    "32": [
     {
      "s": [
       "-1.643269893669447657559704e-51",
       "0.06223486909568790724544574"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-2.502769906858040393003423e-53",
       "0.0009478635136564426746242348"
      ],
      "c_g": [
       "4.617478195520401141526899e-55",
       "-0.00001313911766073773401189807"
      ],
      "c_g_off": null,
      "under_bar": false,
      "spectrum_index": 0
     },
     {
      "s": [
       "0.04173528598376259430139185",
       "0.06091686091686091686091686"
      ],
      "mult": 1,
      "cls": "complex",
      "krein": null,
      "kappa_s": [
       "0.0006356461480653562023710027",
       "0.0009277896887803903470073557"
      ],
      "c_g": [
       "0.0001242332455239913262308566",
       "-0.0002348453653056894878831448"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-4.902349205570723022598736e-80",
       "1.095185488324669513111975"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-7.466486249081060140228799e-82",
       "0.01668014057317097391851552"
      ],
      "c_g": [
       "9.179640923728366821050269e-56",
       "-0.0001321715189203882735231213"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     }
    ]
   },
   "Q": {
    "frac": "77/65",
    "value": 1.1846153846153846
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 0.0622348691
     },
     "mult": 1
    },
    {
     "cls": "complex",
     "sign": null,
     "tau": {
      "re": 0.041735286,
      "im": 0.0609168609
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "value": 1.0951854883
     },
     "mult": 1
    }
   ],
   "representative": {
    "3": [
     3.4641016151377544,
     0.0
    ],
    "-2": [
     3.605551275463989,
     0.0
    ]
   },
   "admission": "P5"
  },
  "C3R/R4": {
   "role": "ray",
   "slot": "R4",
   "level": 6,
   "lam0": 48.0,
   "orbit": "c3ray",
   "sig": [
    5,
    0,
    4
   ],
   "k": 4,
   "r": 2,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": null,
   "dim": 6,
   "ranks": [
    2,
    0
   ],
   "chains": 4,
   "type": "Hyperbolic",
   "idx": [
    5,
    1,
    4
   ],
   "kr": 0,
   "kc": 1,
   "ki": 1,
   "next_order": {
    "16": [
     {
      "s": [
       "0.03556672536102731006354228",
       "0.009869528771337233982631024"
      ],
      "mult": 1,
      "cls": "complex",
      "krein": null,
      "kappa_s": [
       "0.0005416963473984859819392362",
       "0.0001503171189281290789094394"
      ],
      "c_g": [
       "0.00001638557853285604182167366",
       "0.00005721327997393224340340862"
      ],
      "c_g_off": [
       "-0.0001290926453744682420226969",
       "-0.00005206109914080668025634546"
      ],
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "2.2495847514701127814879e-52",
       "0.4538302354347943530089112"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "3.426213210986183207450137e-54",
       "0.006912027418284713557779736"
      ],
      "c_g": [
       "1.635603923170307435035513e-55",
       "-0.0001091831520530414277722538"
      ],
      "c_g_off": [
       "-9.757608770173252729187422e-56",
       "-0.0003587480448487821884433321"
      ],
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-5.238487977569249393177244e-52",
       "1.001806258005316012392248"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-7.978439888788741290922846e-54",
       "0.01525793519796645992235538"
      ],
      "c_g": [
       "7.490556479532316931037989e-55",
       "-0.00002084260886184119665569045"
      ],
      "c_g_off": [
       "5.12577814233763978609055e-55",
       "-0.00009059468220624881626274189"
      ],
      "under_bar": true,
      "spectrum_index": 2
     }
    ],
    "24": [
     {
      "s": [
       "0.03556672536102731006354228",
       "0.009869528771337233982631024"
      ],
      "mult": 1,
      "cls": "complex",
      "krein": null,
      "kappa_s": [
       "0.0005416963473984859819392362",
       "0.0001503171189281290789094394"
      ],
      "c_g": [
       "0.00001576644826655185010137049",
       "0.0000569107353835280937188124"
      ],
      "c_g_off": [
       "-0.0001253558091910067680377724",
       "-0.00004909170710414556010692469"
      ],
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "2.2495847514701127814879e-52",
       "0.4538302354347943530089112"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "3.426213210986183207450137e-54",
       "0.006912027418284713557779736"
      ],
      "c_g": [
       "1.590992533560310168437763e-55",
       "-0.0001309630754965078696466127"
      ],
      "c_g_off": [
       "-9.42181750189874749671704e-56",
       "-0.000373055397684360691873811"
      ],
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-5.238487977569249393177244e-52",
       "1.001806258005316012392248"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-7.978439888788741290922846e-54",
       "0.01525793519796645992235538"
      ],
      "c_g": [
       "7.355350858404895233743971e-55",
       "-0.00006863064912597637137821637"
      ],
      "c_g_off": [
       "5.061379648361528056092418e-55",
       "-0.000136294178335535390505815"
      ],
      "under_bar": true,
      "spectrum_index": 2
     }
    ],
    "32": [
     {
      "s": [
       "0.03556672536102731006354228",
       "0.009869528771337233982631024"
      ],
      "mult": 1,
      "cls": "complex",
      "krein": null,
      "kappa_s": [
       "0.0005416963473984859819392362",
       "0.0001503171189281290789094394"
      ],
      "c_g": [
       "0.00001576644826655185010137049",
       "0.0000569107353835280937188124"
      ],
      "c_g_off": [
       "-0.0001253558091910067680377724",
       "-0.00004909170710414556010692469"
      ],
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "2.2495847514701127814879e-52",
       "0.4538302354347943530089112"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "3.426213210986183207450137e-54",
       "0.006912027418284713557779736"
      ],
      "c_g": [
       "1.590992533560310168437763e-55",
       "-0.0001309630754965078696466127"
      ],
      "c_g_off": [
       "-9.42181750189874749671704e-56",
       "-0.000373055397684360691873811"
      ],
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-5.238487977569249393177244e-52",
       "1.001806258005316012392248"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-7.978439888788741290922846e-54",
       "0.01525793519796645992235538"
      ],
      "c_g": [
       "7.355350858404895233743971e-55",
       "-0.00006863064912597637137821637"
      ],
      "c_g_off": [
       "5.061379648361528056092418e-55",
       "-0.000136294178335535390505815"
      ],
      "under_bar": true,
      "spectrum_index": 2
     }
    ]
   },
   "Q": {
    "frac": "77/65",
    "value": 1.1846153846153846
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [
    {
     "cls": "complex",
     "sign": null,
     "tau": {
      "re": 0.03556672536102731,
      "im": 0.009869528771337234
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 0.45383023543479434
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "value": 1.001806258005316
     },
     "mult": 1
    }
   ],
   "representative": {
    "2": [
     1.0,
     0.0
    ],
    "-1": [
     2.0,
     0.0
    ]
   },
   "admission": "C3R/R4"
  },
  "T1/R4": {
   "role": "row",
   "slot": "R4",
   "level": 6,
   "lam0": 48.0,
   "orbit": "v2",
   "sig": [
    2,
    0,
    8
   ],
   "k": 3,
   "r": 1,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": null,
   "dim": 4,
   "ranks": [
    1,
    0
   ],
   "chains": 3,
   "type": "Elliptic",
   "idx": [
    2,
    0,
    2
   ],
   "kr": 0,
   "kc": 0,
   "ki": 1,
   "next_order": {
    "16": [
     {
      "s": [
       "1.5894457303110833644197e-52",
       "0.04351204351204351204351204"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "2.7896762244219591265217e-54",
       "0.000763690832261409741414218"
      ],
      "c_g": [
       "7.526769180719597978705729e-58",
       "-0.00002244098854384017931369553"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "0.0",
       "0.7832167832167832167832168"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.01374643498070537534545592"
      ],
      "c_g": [
       "4.701576097919634429959845e-57",
       "-0.00003599772439608122331887315"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "0.957264957264957264957265"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.0168011983097510143111128"
      ],
      "c_g": [
       "-3.246989148967665663728754e-55",
       "-0.0003051764629183947844546185"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "0.0",
       "1.305361305361305361305361"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.02291072496784229224242654"
      ],
      "c_g": [
       "5.957804799482451215134196e-58",
       "-0.000723591329962861222804008"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 4
     },
     {
      "s": [
       "0.0",
       "1.566433566433566433566434"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.02749286996141075069091185"
      ],
      "c_g": [
       "1.407422237170304511432112e-55",
       "-0.0004108756054299986547688377"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     }
    ],
    "24": [
     {
      "s": [
       "1.5894457303110833644197e-52",
       "0.04351204351204351204351204"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "2.7896762244219591265217e-54",
       "0.000763690832261409741414218"
      ],
      "c_g": [
       "7.526769180719597978705729e-58",
       "-0.000023443477364252014399328"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "0.0",
       "0.7832167832167832167832168"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.01374643498070537534545592"
      ],
      "c_g": [
       "7.280566465162657129361309e-57",
       "-0.00005725079872074393205200999"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "0.957264957264957264957265"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.0168011983097510143111128"
      ],
      "c_g": [
       "-3.130018245755751970272971e-55",
       "-0.0003383410969539136454785312"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "0.0",
       "1.305361305361305361305361"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.02291072496784229224242654"
      ],
      "c_g": [
       "2.071210492358289816527159e-55",
       "-0.0007572385284926777063070296"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 4
     },
     {
      "s": [
       "0.0",
       "1.566433566433566433566434"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.02749286996141075069091185"
      ],
      "c_g": [
       "1.590910542030549394758898e-55",
       "-0.0004571083973030289374447451"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     }
    ],
    "32": [
     {
      "s": [
       "1.5894457303110833644197e-52",
       "0.04351204351204351204351204"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "2.7896762244219591265217e-54",
       "0.000763690832261409741414218"
      ],
      "c_g": [
       "7.526769180719597978705729e-58",
       "-0.000023443477364252014399328"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "0.0",
       "0.7832167832167832167832168"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.01374643498070537534545592"
      ],
      "c_g": [
       "7.280566465162657129361309e-57",
       "-0.00005725079872074393205200999"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "0.957264957264957264957265"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.0168011983097510143111128"
      ],
      "c_g": [
       "-3.130018245755751970272971e-55",
       "-0.0003383410969539136454785312"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "0.0",
       "1.305361305361305361305361"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.02291072496784229224242654"
      ],
      "c_g": [
       "2.071210492358289816527159e-55",
       "-0.0007572385284926777063070296"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 4
     },
     {
      "s": [
       "0.0",
       "1.566433566433566433566434"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.02749286996141075069091185"
      ],
      "c_g": [
       "1.590910542030549394758898e-55",
       "-0.0004571083973030289374447451"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     }
    ]
   },
   "Q": {
    "frac": "147/143",
    "value": 1.027972027972028
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "frac": "56/1287",
      "value": 0.04351204351204351
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "112/143",
      "value": 0.7832167832167832
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "112/117",
      "value": 0.9572649572649573
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "224/143",
      "value": 1.5664335664335665
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "560/429",
      "value": 1.3053613053613053
     },
     "mult": 1
    }
   ],
   "representative": {
    "2": [
     1.0,
     0.0
    ]
   },
   "admission": "T1/R4"
  },
  "T1/R5": {
   "role": "row",
   "slot": "R5",
   "level": 6,
   "lam0": 48.0,
   "orbit": "v2",
   "sig": [
    2,
    0,
    8
   ],
   "k": 3,
   "r": 1,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": null,
   "dim": 4,
   "ranks": [
    1,
    0
   ],
   "chains": 3,
   "type": "Elliptic",
   "idx": [
    2,
    0,
    2
   ],
   "kr": 0,
   "kc": 0,
   "ki": 1,
   "next_order": {
    "16": [
     {
      "s": [
       "8.33061766222011076041516e-54",
       "0.02447552447552447552447552"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "1.479743679047341547699521e-55",
       "0.0004347517087271278347207446"
      ],
      "c_g": [
       "2.112838696987356963002834e-58",
       "-0.00001406762205842468734374544"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "0.0",
       "0.4405594405594405594405594"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.007825530757088301024973402"
      ],
      "c_g": [
       "-1.078041010571423762627482e-56",
       "-0.0003214474837500513015169849"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "0.5384615384615384615384615"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.00956453759199681236385638"
      ],
      "c_g": [
       "5.265496328392613607061761e-56",
       "-0.0003154919506442634452905777"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "0.0",
       "0.7342657342657342657342657"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.01304255126181383504162234"
      ],
      "c_g": [
       "-1.537644927568202268763357e-56",
       "-0.00008248680494604239833221933"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 4
     },
     {
      "s": [
       "0.0",
       "0.8811188811188811188811189"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.0156510615141766020499468"
      ],
      "c_g": [
       "-8.795857086759700701424846e-58",
       "-0.0002990434172606534149383853"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     }
    ],
    "24": [
     {
      "s": [
       "8.33061766222011076041516e-54",
       "0.02447552447552447552447552"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "1.479743679047341547699521e-55",
       "0.0004347517087271278347207446"
      ],
      "c_g": [
       "2.112838696987356963002834e-58",
       "-0.00001464217821196850767023877"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "0.0",
       "0.4405594405594405594405594"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.007825530757088301024973402"
      ],
      "c_g": [
       "3.824545785679527502762826e-56",
       "-0.000333601589230575717098612"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "0.5384615384615384615384615"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.00956453759199681236385638"
      ],
      "c_g": [
       "2.957930514714808627260293e-56",
       "-0.0003344072563731941746387781"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "0.0",
       "0.7342657342657342657342657"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.01304255126181383504162234"
      ],
      "c_g": [
       "-2.001264723542928123289454e-56",
       "-0.0001017413242805997621650564"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 4
     },
     {
      "s": [
       "0.0",
       "0.8811188811188811188811189"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.0156510615141766020499468"
      ],
      "c_g": [
       "-1.126971965725722973961297e-56",
       "-0.0003254565068009672365883763"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     }
    ],
    "32": [
     {
      "s": [
       "8.33061766222011076041516e-54",
       "0.02447552447552447552447552"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "1.479743679047341547699521e-55",
       "0.0004347517087271278347207446"
      ],
      "c_g": [
       "2.112838696987356963002834e-58",
       "-0.00001464217821196850767023877"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "0.0",
       "0.4405594405594405594405594"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.007825530757088301024973402"
      ],
      "c_g": [
       "3.824545785679527502762826e-56",
       "-0.000333601589230575717098612"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "0.5384615384615384615384615"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.00956453759199681236385638"
      ],
      "c_g": [
       "2.957930514714808627260293e-56",
       "-0.0003344072563731941746387781"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "0.0",
       "0.7342657342657342657342657"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.01304255126181383504162234"
      ],
      "c_g": [
       "-2.001264723542928123289454e-56",
       "-0.0001017413242805997621650564"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 4
     },
     {
      "s": [
       "0.0",
       "0.8811188811188811188811189"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "0.0",
       "0.0156510615141766020499468"
      ],
      "c_g": [
       "-1.126971965725722973961297e-56",
       "-0.0003254565068009672365883763"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     }
    ]
   },
   "Q": {
    "frac": "581/572",
    "value": 1.0157342657342658
   },
   "s": {
    "frac": "9/16",
    "value": 0.5625
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "frac": "56/1287",
      "value": 0.04351204351204351
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "112/143",
      "value": 0.7832167832167832
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "112/117",
      "value": 0.9572649572649573
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "224/143",
      "value": 1.5664335664335665
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "frac": "560/429",
      "value": 1.3053613053613053
     },
     "mult": 1
    }
   ],
   "representative": {
    "2": [
     1.0,
     0.0
    ]
   },
   "admission": "T1/R5"
  },
  "T4/R4": {
   "role": "row",
   "slot": "R4",
   "level": 6,
   "lam0": 48.0,
   "orbit": "outside3",
   "sig": [
    7,
    0,
    2
   ],
   "k": 4,
   "r": 2,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": null,
   "dim": 6,
   "ranks": [
    2,
    0
   ],
   "chains": 4,
   "type": "Elliptic",
   "idx": [
    7,
    1,
    6
   ],
   "kr": 0,
   "kc": 0,
   "ki": 3,
   "next_order": {
    "16": [
     {
      "s": [
       "-1.691791739876743108185433e-50",
       "0.005736859223094351705573823"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-2.575392243537360426429318e-52",
       "0.00008733145101240050550832012"
      ],
      "c_g": [
       "1.410053871390215170082864e-53",
       "-0.00001048206110242490919256803"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     },
     {
      "s": [
       "6.530848127863545995485519e-51",
       "0.1392518329643492375161716"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "9.941823934809887516860272e-53",
       "0.002119812279854689995527604"
      ],
      "c_g": [
       "-6.592836807179460173101994e-54",
       "0.00003714168119815899137041395"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "-2.421776100969072550449298e-51",
       "0.310692742361500122983186"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-3.686637804765676645711673e-53",
       "0.004729634623109431361833082"
      ],
      "c_g": [
       "-2.33994929613870534220547e-54",
       "-0.0003094939527389709984387031"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-1.942818970075171972213463e-51",
       "1.012091604894205959728147"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-2.957527683929569678677364e-53",
       "0.01540693696248758110710271"
      ],
      "c_g": [
       "1.288455257573316551381278e-54",
       "-0.00007626777955689850145987648"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "24": [
     {
      "s": [
       "-1.691791739876743108185433e-50",
       "0.005736859223094351705573823"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-2.575392243537360426429318e-52",
       "0.00008733145101240050550832012"
      ],
      "c_g": [
       "1.303155876373250699195963e-53",
       "-0.000009953348733660484493364564"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     },
     {
      "s": [
       "6.530848127863545995485519e-51",
       "0.1392518329643492375161716"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "9.941823934809887516860272e-53",
       "0.002119812279854689995527604"
      ],
      "c_g": [
       "-6.599756929252469066433429e-54",
       "0.00003211330512148688858971683"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "-2.421776100969072550449298e-51",
       "0.310692742361500122983186"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-3.686637804765676645711673e-53",
       "0.004729634623109431361833082"
      ],
      "c_g": [
       "-2.638450622803305377992096e-54",
       "-0.0003210698505576520471156753"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-1.942818970075171972213463e-51",
       "1.012091604894205959728147"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-2.957527683929569678677364e-53",
       "0.01540693696248758110710271"
      ],
      "c_g": [
       "1.307724233798739228682989e-54",
       "-0.0001235212562843326517621256"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "32": [
     {
      "s": [
       "-1.691791739876743108185433e-50",
       "0.005736859223094351705573823"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-2.575392243537360426429318e-52",
       "0.00008733145101240050550832012"
      ],
      "c_g": [
       "1.303155876373250699195963e-53",
       "-0.000009953348733660484493364564"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     },
     {
      "s": [
       "6.530848127863545995485519e-51",
       "0.1392518329643492375161716"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "9.941823934809887516860272e-53",
       "0.002119812279854689995527604"
      ],
      "c_g": [
       "-6.599756929252469066433429e-54",
       "0.00003211330512148688858971683"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "-2.421776100969072550449298e-51",
       "0.310692742361500122983186"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-3.686637804765676645711673e-53",
       "0.004729634623109431361833082"
      ],
      "c_g": [
       "-2.638450622803305377992096e-54",
       "-0.0003210698505576520471156753"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-1.942818970075171972213463e-51",
       "1.012091604894205959728147"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-2.957527683929569678677364e-53",
       "0.01540693696248758110710271"
      ],
      "c_g": [
       "1.307724233798739228682989e-54",
       "-0.0001235212562843326517621256"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ]
   },
   "Q": {
    "value": 1.1852034613388465
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "value": 1.01209160489
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 0.310692742362
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 0.139251832964
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 0.00573685922309
     },
     "mult": 1
    }
   ],
   "representative": {
    "3": [
     -0.3086472568785893,
     -0.06949329411780472
    ],
    "2": [
     0.34579154134174556,
     -0.37948776525885436
    ],
    "1": [
     0.20302636427665244,
     0.1632131521070081
    ],
    "0": [
     0.29228686825253675,
     0.09882806648613832
    ],
    "-1": [
     0.3588169781640245,
     -0.4475251820209991
    ],
    "-2": [
     0.0005102297941505528,
     0.0441294932645358
    ],
    "-3": [
     0.22297893474867425,
     -0.30425691601898186
    ]
   },
   "admission": "T4/R4"
  },
  "T4/R5": {
   "role": "row",
   "slot": "R5",
   "level": 6,
   "lam0": 48.0,
   "orbit": "outside3",
   "sig": [
    7,
    0,
    2
   ],
   "k": 4,
   "r": 2,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": null,
   "dim": 6,
   "ranks": [
    2,
    0
   ],
   "chains": 4,
   "type": "Elliptic",
   "idx": [
    7,
    1,
    6
   ],
   "kr": 0,
   "kc": 0,
   "ki": 3,
   "next_order": {
    "16": [
     {
      "s": [
       "-7.160185136497685502059357e-52",
       "0.003226983312990572834385275"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-1.169970658695319451313197e-53",
       "0.00005272874542103126692183694"
      ],
      "c_g": [
       "1.329344481921162342070699e-53",
       "0.00001232616058683281576614424"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     },
     {
      "s": [
       "6.139054330132819221255153e-52",
       "0.07832915604244644610284651"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "1.003118397285615959095325e-53",
       "0.00127989447958402176448166"
      ],
      "c_g": [
       "1.980680386313032911772464e-54",
       "-0.00007549196435959471550789545"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "2.308743382967845127757687e-51",
       "0.1747646675783438191780421"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "3.772475103696256329082133e-53",
       "0.002855645899448308927242345"
      ],
      "c_g": [
       "2.652896615578911939699727e-54",
       "0.0000487557438198699684901474"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-9.8933018395933414729422e-52",
       "0.5693015277529908523470826"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-1.616560556645374794964708e-53",
       "0.009302358398894923571101506"
      ],
      "c_g": [
       "1.270910195992155396089878e-54",
       "-0.0001835569882328996141696661"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "24": [
     {
      "s": [
       "-7.160185136497685502059357e-52",
       "0.003226983312990572834385275"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-1.169970658695319451313197e-53",
       "0.00005272874542103126692183694"
      ],
      "c_g": [
       "1.408906032540104615468062e-53",
       "0.00001265437152491790586718242"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     },
     {
      "s": [
       "6.139054330132819221255153e-52",
       "0.07832915604244644610284651"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "1.003118397285615959095325e-53",
       "0.00127989447958402176448166"
      ],
      "c_g": [
       "2.125690572063365584713881e-54",
       "-0.0000788738631454683320333208"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "2.308743382967845127757687e-51",
       "0.1747646675783438191780421"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "3.772475103696256329082133e-53",
       "0.002855645899448308927242345"
      ],
      "c_g": [
       "2.429355284444535885706282e-54",
       "0.00004098350169631699511132212"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-9.8933018395933414729422e-52",
       "0.5693015277529908523470826"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-1.616560556645374794964708e-53",
       "0.009302358398894923571101506"
      ],
      "c_g": [
       "1.209516778420864361610713e-54",
       "-0.0002149395213634538703315838"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "32": [
     {
      "s": [
       "-7.160185136497685502059357e-52",
       "0.003226983312990572834385275"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-1.169970658695319451313197e-53",
       "0.00005272874542103126692183694"
      ],
      "c_g": [
       "1.408906032540104615468062e-53",
       "0.00001265437152491790586718242"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 3
     },
     {
      "s": [
       "6.139054330132819221255153e-52",
       "0.07832915604244644610284651"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "1.003118397285615959095325e-53",
       "0.00127989447958402176448166"
      ],
      "c_g": [
       "2.125690572063365584713881e-54",
       "-0.0000788738631454683320333208"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "2.308743382967845127757687e-51",
       "0.1747646675783438191780421"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "3.772475103696256329082133e-53",
       "0.002855645899448308927242345"
      ],
      "c_g": [
       "2.429355284444535885706282e-54",
       "0.00004098350169631699511132212"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-9.8933018395933414729422e-52",
       "0.5693015277529908523470826"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-1.616560556645374794964708e-53",
       "0.009302358398894923571101506"
      ],
      "c_g": [
       "1.209516778420864361610713e-54",
       "-0.0002149395213634538703315838"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ]
   },
   "Q": {
    "value": 1.104176947003101
   },
   "s": {
    "frac": "9/16",
    "value": 0.5625
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "value": 1.01209160489
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 0.310692742362
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 0.139251832964
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 0.00573685922309
     },
     "mult": 1
    }
   ],
   "representative": {
    "3": [
     -0.3086472568785893,
     -0.06949329411780472
    ],
    "2": [
     0.34579154134174556,
     -0.37948776525885436
    ],
    "1": [
     0.20302636427665244,
     0.1632131521070081
    ],
    "0": [
     0.29228686825253675,
     0.09882806648613832
    ],
    "-1": [
     0.3588169781640245,
     -0.4475251820209991
    ],
    "-2": [
     0.0005102297941505528,
     0.0441294932645358
    ],
    "-3": [
     0.22297893474867425,
     -0.30425691601898186
    ]
   },
   "admission": "T4/R5"
  },
  "T5J/R2": {
   "role": "member",
   "slot": "R2",
   "level": 7,
   "lam0": 63.0,
   "orbit": "line72_32j",
   "sig": [
    9,
    0,
    0
   ],
   "k": 6,
   "r": 4,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": null,
   "dim": 10,
   "ranks": [
    4,
    0
   ],
   "chains": 6,
   "type": "Elliptic",
   "idx": [
    9,
    3,
    6
   ],
   "kr": 0,
   "kc": 0,
   "ki": 3,
   "next_order": {
    "16": [
     {
      "s": [
       "-5.355542066222458330181278e-52",
       "2.589888194593561825218638"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-4.983837168863778744589719e-54",
       "0.02410135311759634262654179"
      ],
      "c_g": [
       "-1.892705810963471129716856e-55",
       "-0.0005067240697424374146415444"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "-6.456039641264989876353033e-51",
       "2.904245561380119756138729"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-6.007953990451937472792771e-53",
       "0.02702674500048014251863086"
      ],
      "c_g": [
       "-2.288462226045552593276842e-55",
       "-0.000487808186961475187725176"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "-1.259487242944960154272188e-51",
       "3.014674737753705817336273"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-1.172071707678025246181632e-53",
       "0.02805439267261558002610893"
      ],
      "c_g": [
       "-5.073426246450646227434036e-56",
       "-0.0004835278080255389243353466"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     }
    ],
    "24": [
     {
      "s": [
       "-5.355542066222458330181278e-52",
       "2.589888194593561825218638"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-4.983837168863778744589719e-54",
       "0.02410135311759634262654179"
      ],
      "c_g": [
       "-1.742515700005133557974596e-55",
       "-0.0005174603992905819189626533"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "-6.456039641264989876353033e-51",
       "2.904245561380119756138729"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-6.007953990451937472792771e-53",
       "0.02702674500048014251863086"
      ],
      "c_g": [
       "-1.725538125312723346467418e-55",
       "-0.0005021846270504823574479374"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "-1.259487242944960154272188e-51",
       "3.014674737753705817336273"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-1.172071707678025246181632e-53",
       "0.02805439267261558002610893"
      ],
      "c_g": [
       "-1.712673255143663981463601e-56",
       "-0.000499114256694836164444763"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     }
    ],
    "32": [
     {
      "s": [
       "-5.355542066222458330181278e-52",
       "2.589888194593561825218638"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-4.983837168863778744589719e-54",
       "0.02410135311759634262654179"
      ],
      "c_g": [
       "-1.742515700005133557974596e-55",
       "-0.0005174603992905819189626533"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "-6.456039641264989876353033e-51",
       "2.904245561380119756138729"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-6.007953990451937472792771e-53",
       "0.02702674500048014251863086"
      ],
      "c_g": [
       "-1.725538125312723346467418e-55",
       "-0.0005021846270504823574479374"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "-1.259487242944960154272188e-51",
       "3.014674737753705817336273"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-1.172071707678025246181632e-53",
       "0.02805439267261558002610893"
      ],
      "c_g": [
       "-1.712673255143663981463601e-56",
       "-0.000499114256694836164444763"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     }
    ]
   },
   "Q": {
    "frac": "22/13",
    "value": 1.6923076923076923
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 2.9042455613801197
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 3.014674737753706
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 2.589888194593562
     },
     "mult": 1
    }
   ],
   "representative": {
    "3.5": [
     0.3872983346207417,
     0.0
    ],
    "1.5": [
     0.0,
     0.5916079783099616
    ],
    "-1.5": [
     0.5916079783099616,
     0.0
    ],
    "-3.5": [
     0.0,
     -0.3872983346207417
    ]
   },
   "admission": "T5J/R2"
  },
  "T2/R4": {
   "role": "row",
   "slot": "R4",
   "level": 6,
   "lam0": 48.0,
   "orbit": "prism",
   "sig": [
    3,
    0,
    6
   ],
   "k": 4,
   "r": 4,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.3535533905932738,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 0.7071067811865476,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 1.4142135623730951,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    },
    {
     "eps": 2.8284271247461903,
     "read": true
    },
    {
     "eps": 4.0,
     "read": true
    },
    {
     "eps": 5.656854249492381,
     "read": true
    },
    {
     "eps": 8.0,
     "read": true
    },
    {
     "eps": 11.313708498984761,
     "read": true
    },
    {
     "eps": 16.0,
     "read": false
    },
    {
     "eps": 22.627416997969522,
     "read": false
    },
    {
     "eps": 32.0,
     "read": true
    },
    {
     "eps": 45.254833995939045,
     "read": true
    },
    {
     "eps": 64.0,
     "read": true
    },
    {
     "eps": 72.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": "T2_R4",
   "dim": 8,
   "ranks": [
    4,
    0
   ],
   "chains": 4,
   "type": "Elliptic",
   "idx": [
    3,
    3,
    0
   ],
   "kr": 0,
   "kc": 0,
   "ki": 0,
   "next_order": {
    "16": [
     {
      "s": [
       "5.91946317312096718955822e-52",
       "0.2616912229309042768059204"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "9.214738035739783591194589e-54",
       "0.004073707353245128798018353"
      ],
      "c_g": [
       "-2.101704512733054842369371e-55",
       "-0.0002047836647360205219066909"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-1.173215913005572747585762e-51",
       "0.853896863913224433000144"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-1.826327317449585653956158e-53",
       "0.01329248224100626833793895"
      ],
      "c_g": [
       "2.527498839553258927150421e-55",
       "-0.0001983806108438613665992574"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "24": [
     {
      "s": [
       "5.91946317312096718955822e-52",
       "0.2616912229309042768059204"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "9.214738035739783591194589e-54",
       "0.004073707353245128798018353"
      ],
      "c_g": [
       "-4.312430091907955351181576e-55",
       "-0.0002168966941891731135946283"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-1.173215913005572747585762e-51",
       "0.853896863913224433000144"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-1.826327317449585653956158e-53",
       "0.01329248224100626833793895"
      ],
      "c_g": [
       "2.58434792024690001035604e-55",
       "-0.0002298581177368948097482866"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "32": [
     {
      "s": [
       "5.91946317312096718955822e-52",
       "0.2616912229309042768059204"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "9.214738035739783591194589e-54",
       "0.004073707353245128798018353"
      ],
      "c_g": [
       "-4.312430091907955351181576e-55",
       "-0.0002168966941891731135946283"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "-1.173215913005572747585762e-51",
       "0.853896863913224433000144"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-1.826327317449585653956158e-53",
       "0.01329248224100626833793895"
      ],
      "c_g": [
       "2.58434792024690001035604e-55",
       "-0.0002298581177368948097482866"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ]
   },
   "Q": {
    "frac": "5831/5031",
    "value": 1.1590141125024847
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "value": 0.8538968639132244
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "value": 0.2616912229309043
     },
     "mult": 2
    }
   ],
   "representative": {
    "3": [
     1.0,
     0.0
    ],
    "0": [
     1.51657508881031,
     0.0
    ],
    "-3": [
     1.0,
     0.0
    ]
   },
   "admission": "T2/R4"
  },
  "T2/R5": {
   "role": "row",
   "slot": "R5",
   "level": 6,
   "lam0": 48.0,
   "orbit": "prism",
   "sig": [
    3,
    0,
    6
   ],
   "k": 4,
   "r": 4,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.3535533905932738,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 0.7071067811865476,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 1.4142135623730951,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    },
    {
     "eps": 2.8284271247461903,
     "read": true
    },
    {
     "eps": 4.0,
     "read": true
    },
    {
     "eps": 5.656854249492381,
     "read": true
    },
    {
     "eps": 8.0,
     "read": true
    },
    {
     "eps": 11.313708498984761,
     "read": true
    },
    {
     "eps": 16.0,
     "read": true
    },
    {
     "eps": 22.627416997969522,
     "read": true
    },
    {
     "eps": 32.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": "T2_R5",
   "dim": 8,
   "ranks": [
    4,
    0
   ],
   "chains": 4,
   "type": "Elliptic",
   "idx": [
    3,
    3,
    0
   ],
   "kr": 0,
   "kc": 0,
   "ki": 0,
   "next_order": {
    "16": [
     {
      "s": [
       "-5.785418808851883403396119e-52",
       "0.1472013128986336557033302"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-9.581173679320277304836393e-54",
       "0.002437786081360051931572765"
      ],
      "c_g": [
       "-3.789464815573201095697812e-55",
       "0.000003311425320022107347720464"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "5.549726949661543959576865e-52",
       "0.480316985951188743562581"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "9.190846770877726352278152e-54",
       "0.007954481111176883279815476"
      ],
      "c_g": [
       "-1.502089014872972094865654e-55",
       "-0.00006908008142304150128078185"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "24": [
     {
      "s": [
       "-5.785418808851883403396119e-52",
       "0.1472013128986336557033302"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-9.581173679320277304836393e-54",
       "0.002437786081360051931572765"
      ],
      "c_g": [
       "-4.624339462489080515883977e-55",
       "-0.000004525213404123304639307974"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "5.549726949661543959576865e-52",
       "0.480316985951188743562581"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "9.190846770877726352278152e-54",
       "0.007954481111176883279815476"
      ],
      "c_g": [
       "-1.615689605928719998315534e-55",
       "-0.00008962848548704921335507153"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "32": [
     {
      "s": [
       "-5.785418808851883403396119e-52",
       "0.1472013128986336557033302"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "-9.581173679320277304836393e-54",
       "0.002437786081360051931572765"
      ],
      "c_g": [
       "-4.624339462489080515883977e-55",
       "-0.000004525213404123304639307974"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "5.549726949661543959576865e-52",
       "0.480316985951188743562581"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "+",
      "kappa_s": [
       "9.190846770877726352278152e-54",
       "0.007954481111176883279815476"
      ],
      "c_g": [
       "-1.615689605928719998315534e-55",
       "-0.00008962848548704921335507153"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ]
   },
   "Q": {
    "frac": "609/559",
    "value": 1.0894454382826475
   },
   "s": {
    "frac": "9/16",
    "value": 0.5625
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "value": 0.8538968639132244
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": 1,
     "tau": {
      "value": 0.2616912229309043
     },
     "mult": 2
    }
   ],
   "representative": {
    "3": [
     1.0,
     0.0
    ],
    "0": [
     1.51657508881031,
     0.0
    ],
    "-3": [
     1.0,
     0.0
    ]
   },
   "admission": "T2/R5"
  },
  "T3/R4": {
   "role": "row",
   "slot": "R4",
   "level": 6,
   "lam0": 48.0,
   "orbit": "hexagon",
   "sig": [
    9,
    0,
    0
   ],
   "k": 4,
   "r": 4,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.3535533905932738,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 0.7071067811865476,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 1.4142135623730951,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    },
    {
     "eps": 2.8284271247461903,
     "read": true
    },
    {
     "eps": 4.0,
     "read": true
    },
    {
     "eps": 5.656854249492381,
     "read": true
    },
    {
     "eps": 8.0,
     "read": true
    },
    {
     "eps": 11.313708498984761,
     "read": true
    },
    {
     "eps": 16.0,
     "read": true
    },
    {
     "eps": 22.627416997969522,
     "read": true
    },
    {
     "eps": 32.0,
     "read": false
    },
    {
     "eps": 45.254833995939045,
     "read": true
    },
    {
     "eps": 64.0,
     "read": true
    },
    {
     "eps": 72.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": "T3_R4",
   "dim": 8,
   "ranks": [
    4,
    0
   ],
   "chains": 4,
   "type": "Elliptic",
   "idx": [
    9,
    3,
    6
   ],
   "kr": 0,
   "kc": 0,
   "ki": 3,
   "next_order": {
    "16": [
     {
      "s": [
       "0.0",
       "0.9533011101877017048512916"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.01264911064067351732799557"
      ],
      "c_g": [
       "-4.059742987328553198563657e-56",
       "0.0001062705537895819840187088"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "1.212300506732372678758973"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.01608570794214541245722124"
      ],
      "c_g": [
       "2.309012403181324787713643e-56",
       "-0.0001348626140213145865003946"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "24": [
     {
      "s": [
       "0.0",
       "0.9533011101877017048512916"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.01264911064067351732799557"
      ],
      "c_g": [
       "-1.664404730895558348657655e-55",
       "0.00006204387031028789099746208"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "1.212300506732372678758973"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.01608570794214541245722124"
      ],
      "c_g": [
       "4.095170970240677263026726e-56",
       "-0.0001831826779379695065155132"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "32": [
     {
      "s": [
       "0.0",
       "0.9533011101877017048512916"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.01264911064067351732799557"
      ],
      "c_g": [
       "-1.664404730895558348657655e-55",
       "0.00006204387031028789099746208"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "1.212300506732372678758973"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.01608570794214541245722124"
      ],
      "c_g": [
       "4.095170970240677263026726e-56",
       "-0.0001831826779379695065155132"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ]
   },
   "Q": {
    "frac": "1750/1287",
    "value": 1.3597513597513597
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 1.2123005067323727
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 0.9533011101877017
     },
     "mult": 2
    }
   ],
   "representative": {
    "3": [
     1.0,
     0.0
    ],
    "-3": [
     1.0,
     0.0
    ]
   },
   "admission": "T3/R4"
  },
  "T3/R5": {
   "role": "row",
   "slot": "R5",
   "level": 6,
   "lam0": 48.0,
   "orbit": "hexagon",
   "sig": [
    9,
    0,
    0
   ],
   "k": 4,
   "r": 4,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.3535533905932738,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 0.7071067811865476,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 1.4142135623730951,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    },
    {
     "eps": 2.8284271247461903,
     "read": true
    },
    {
     "eps": 4.0,
     "read": true
    },
    {
     "eps": 5.656854249492381,
     "read": true
    },
    {
     "eps": 8.0,
     "read": true
    },
    {
     "eps": 11.313708498984761,
     "read": true
    },
    {
     "eps": 16.0,
     "read": false
    },
    {
     "eps": 22.627416997969522,
     "read": true
    },
    {
     "eps": 32.0,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": "T3_R5",
   "dim": 8,
   "ranks": [
    4,
    0
   ],
   "chains": 4,
   "type": "Elliptic",
   "idx": [
    9,
    3,
    6
   ],
   "kr": 0,
   "kc": 0,
   "ki": 3,
   "next_order": {
    "16": [
     {
      "s": [
       "0.0",
       "0.5362318744805822089788515"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.008046508041140914330785989"
      ],
      "c_g": [
       "-4.487532772239431101320946e-55",
       "-0.0003927813883688411151681436"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "0.6819190350369596318019221"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.01023263864004161097787611"
      ],
      "c_g": [
       "-9.029242481331487378445969e-56",
       "-0.0002730701557960074538328798"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "24": [
     {
      "s": [
       "0.0",
       "0.5362318744805822089788515"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.008046508041140914330785989"
      ],
      "c_g": [
       "-3.779099929010743551761802e-55",
       "-0.0004270391069306641260730705"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "0.6819190350369596318019221"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.01023263864004161097787611"
      ],
      "c_g": [
       "-9.579329336072665244359212e-56",
       "-0.0003110477786749382600200842"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ],
    "32": [
     {
      "s": [
       "0.0",
       "0.5362318744805822089788515"
      ],
      "mult": 2,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.008046508041140914330785989"
      ],
      "c_g": [
       "-3.779099929010743551761802e-55",
       "-0.0004270391069306641260730705"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     },
     {
      "s": [
       "0.0",
       "0.6819190350369596318019221"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "0.0",
       "0.01023263864004161097787611"
      ],
      "c_g": [
       "-9.579329336072665244359212e-56",
       "-0.0003110477786749382600200842"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     }
    ]
   },
   "Q": {
    "frac": "2751/2288",
    "value": 1.2023601398601398
   },
   "s": {
    "frac": "9/16",
    "value": 0.5625
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 1.2123005067323727
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 0.9533011101877017
     },
     "mult": 2
    }
   ],
   "representative": {
    "3": [
     1.0,
     0.0
    ],
    "-3": [
     1.0,
     0.0
    ]
   },
   "admission": "T3/R5"
  },
  "T5/R2": {
   "role": "row",
   "slot": "R2",
   "level": 7,
   "lam0": 63.0,
   "orbit": "line72_32",
   "sig": [
    9,
    0,
    0
   ],
   "k": 6,
   "r": 4,
   "points": [
    {
     "eps": 0.25,
     "read": true
    },
    {
     "eps": 0.3535533905932738,
     "read": true
    },
    {
     "eps": 0.5,
     "read": true
    },
    {
     "eps": 0.7071067811865476,
     "read": true
    },
    {
     "eps": 1.0,
     "read": true
    },
    {
     "eps": 1.4142135623730951,
     "read": true
    },
    {
     "eps": 2.0,
     "read": true
    },
    {
     "eps": 2.8284271247461903,
     "read": true
    },
    {
     "eps": 4.0,
     "read": true
    },
    {
     "eps": 5.656854249492381,
     "read": true
    },
    {
     "eps": 8.0,
     "read": true
    },
    {
     "eps": 11.313708498984761,
     "read": true
    },
    {
     "eps": 16.0,
     "read": true
    },
    {
     "eps": 22.627416997969522,
     "read": true
    },
    {
     "eps": 32.0,
     "read": true
    },
    {
     "eps": 45.254833995939045,
     "read": false
    },
    {
     "eps": 64.0,
     "read": true
    },
    {
     "eps": 90.50966799187809,
     "read": true
    }
   ],
   "cutoffs": [
    16,
    24,
    32
   ],
   "m815": "T5_R2",
   "dim": 10,
   "ranks": [
    4,
    0
   ],
   "chains": 6,
   "type": "Elliptic",
   "idx": [
    9,
    3,
    6
   ],
   "kr": 0,
   "kc": 0,
   "ki": 3,
   "next_order": {
    "16": [
     {
      "s": [
       "-5.297038257226489638821057e-82",
       "2.68857172135926286741336"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-4.929393854967847056065321e-84",
       "0.02501969643853000197268229"
      ],
      "c_g": [
       "-1.937902150132756234205634e-55",
       "-0.0005054866301181613849894282"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "-3.519892105428729074295261e-52",
       "2.741258741258741258741259"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-3.275591693335268045850584e-54",
       "0.02550999886701395886158583"
      ],
      "c_g": [
       "-2.388941748544467332349927e-56",
       "-0.0004902879861792438954539162"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "1.232452178978591316983793e-101",
       "3.080180112967654475804968"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "1.146913029995704886743185e-103",
       "0.02866398199096056752433741"
      ],
      "c_g": [
       "-4.756930844066413741280019e-55",
       "-0.0004816956068350579322539942"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     }
    ],
    "24": [
     {
      "s": [
       "-5.297038257226489638821057e-82",
       "2.68857172135926286741336"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-4.929393854967847056065321e-84",
       "0.02501969643853000197268229"
      ],
      "c_g": [
       "-2.023213256702529987828498e-55",
       "-0.0005172290729977108974950514"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "-3.519892105428729074295261e-52",
       "2.741258741258741258741259"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-3.275591693335268045850584e-54",
       "0.02550999886701395886158583"
      ],
      "c_g": [
       "-9.417740564627841048346329e-56",
       "-0.0005029900476979371166606276"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "1.232452178978591316983793e-101",
       "3.080180112967654475804968"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "1.146913029995704886743185e-103",
       "0.02866398199096056752433741"
      ],
      "c_g": [
       "-4.685511314596179160422582e-55",
       "-0.0004979792784536943451718762"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     }
    ],
    "32": [
     {
      "s": [
       "-5.297038257226489638821057e-82",
       "2.68857172135926286741336"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-4.929393854967847056065321e-84",
       "0.02501969643853000197268229"
      ],
      "c_g": [
       "-2.023213256702529987828498e-55",
       "-0.0005172290729977108974950514"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 2
     },
     {
      "s": [
       "-3.519892105428729074295261e-52",
       "2.741258741258741258741259"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "-3.275591693335268045850584e-54",
       "0.02550999886701395886158583"
      ],
      "c_g": [
       "-9.417740564627841048346329e-56",
       "-0.0005029900476979371166606276"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 0
     },
     {
      "s": [
       "1.232452178978591316983793e-101",
       "3.080180112967654475804968"
      ],
      "mult": 1,
      "cls": "imag",
      "krein": "-",
      "kappa_s": [
       "1.146913029995704886743185e-103",
       "0.02866398199096056752433741"
      ],
      "c_g": [
       "-4.685511314596179160422582e-55",
       "-0.0004979792784536943451718762"
      ],
      "c_g_off": null,
      "under_bar": true,
      "spectrum_index": 1
     }
    ]
   },
   "Q": {
    "frac": "22/13",
    "value": 1.6923076923076923
   },
   "s": {
    "frac": "1/1",
    "value": 1.0
   },
   "spectrum": [
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 2.7412587412587412
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 3.0801801129676543
     },
     "mult": 1
    },
    {
     "cls": "imag",
     "sign": -1,
     "tau": {
      "value": 2.688571721359263
     },
     "mult": 1
    }
   ],
   "representative": {
    "3.5": [
     0.5477225575051661,
     0.0
    ],
    "-1.5": [
     0.8366600265340756,
     0.0
    ]
   },
   "admission": "T5/R2"
  }
 },
 "values": {
  "calibration": {
   "kappa": 2.0,
   "m0": 0.2,
   "G": 3.0,
   "kappa_d": 10.0,
   "kappa_L": 200.0,
   "leak_cap": 0.0001,
   "L_cut_over_u": 1000.0,
   "G_L": 10.0,
   "D_cut": 1e-08,
   "u": 2.220446049250313e-16
  },
  "solve": {
   "accept_rel": 1e-15,
   "halving": 1e-08,
   "secant": 1e-06,
   "secant_iterations": 8,
   "seed_check": 1e-12
  },
  "checks": {
   "bar": 0.05,
   "overlap_xy": 0.9,
   "overlap_z": 0.1,
   "identity": 0.01,
   "axis": 1e-06,
   "factor": 0.1,
   "span": 1e-06,
   "left": 10000.0,
   "conditioning": 0.01,
   "idempotence": 1e-06,
   "slow_band": 2,
   "band_edge": 0.5,
   "orthonormal": 1e-06,
   "k6_eps": 2
  },
  "next_order": {
   "points": [
    0.25,
    0.5,
    1.0
   ],
   "ceiling": [
    0.1,
    0.001
   ],
   "resolution": 0.1,
   "floor": 0.1,
   "nominal_weights": [
    42.666666666666664,
    8.0,
    0.3333333333333333
   ]
  },
  "cutoffs": [
   16,
   24,
   32
  ],
  "c1": {
   "eps": [
    0.5,
    1.0,
    2.0
   ],
   "cutoffs": [
    16,
    24,
    32,
    40
   ],
   "residual": 1e-15,
   "off_level": 1e-14,
   "spectrum": 1e-10,
   "along": 1e-12
  },
  "sample": [
   0.25,
   0.5,
   1.0,
   2.0
  ]
 },
 "next_order": {
  "file": "run/next_order_values.json",
  "sha256": "b05fff5ddd71c29c79318b6257f940c6035d7c954f3bafa34a22080eecc00333",
  "cases_sha256": "45ad237179b6c7176b4372f8b36fe6cf20ba95ebdff510f727eec1ea4a2ebeea",
  "script": {
   "path": "run/next_order_values.py",
   "sha256": "4bf81a60beef1338c6da36b2d4c04f9d51b826322a0b1e9540769fa318f4028e"
  },
  "environment": {
   "python": "3.13.13",
   "sympy": "1.14.0",
   "mpmath": "1.3.0",
   "numpy": "2.5.0",
   "dps": 50
  }
 },
 "terms_sha256": "9d16712982e5388970fca33de59958721109e09f9d88dec7a2a088489ad3efd6",
 "manifest_sha256": "8cc2d7e2d01a72fc3572adabf917656abf36cbddd70ed35532b73ae5451790dd",
 "go": "https://github.com/openwave-labs/openwave/pull/650#issuecomment-6385959498",
 "targets": [
  {
   "name": "T2_R4",
   "path": "files/framework/files/working/files/scripts/soft-slot-dynamics/m8_15_solver/out/branch_T2_R4.json",
   "commit": "33aeb754ec8d98449346dfe27d204be79e333fa5",
   "blob": "22bb03321404960b76ad568e1091f9629b4bdcb2",
   "file": "reference/m815_targets/branch_T2_R4.json",
   "sha256": "5b1758c9ec1c6566091fe9028a542f67fd6bd0ad51c927f7147d54c07d876b49"
  },
  {
   "name": "T2_R5",
   "path": "files/framework/files/working/files/scripts/soft-slot-dynamics/m8_15_solver/out/branch_T2_R5.json",
   "commit": "33aeb754ec8d98449346dfe27d204be79e333fa5",
   "blob": "2a5e77315c8c323e0c9ec8b15629fa26b6b64d98",
   "file": "reference/m815_targets/branch_T2_R5.json",
   "sha256": "a064683298ebc922ecbba06316a3af11b68a7b6193e7e04c63eaa9fc1ad931ba"
  },
  {
   "name": "T3_R4",
   "path": "files/framework/files/working/files/scripts/soft-slot-dynamics/m8_15_solver/out/branch_T3_R4.json",
   "commit": "33aeb754ec8d98449346dfe27d204be79e333fa5",
   "blob": "497301e4186b8e45d9efcb4207255d7b257f47e7",
   "file": "reference/m815_targets/branch_T3_R4.json",
   "sha256": "fe3497a3a4de45a5f3a6d2ce2a6c322feb5399610ad20d9da530acd8abdf3bc2"
  },
  {
   "name": "T3_R5",
   "path": "files/framework/files/working/files/scripts/soft-slot-dynamics/m8_15_solver/out/branch_T3_R5.json",
   "commit": "33aeb754ec8d98449346dfe27d204be79e333fa5",
   "blob": "a719df9db2b04edc06c1ec82f2d8467fc5b77c41",
   "file": "reference/m815_targets/branch_T3_R5.json",
   "sha256": "660d0322d1921bb7b6c9e7e1b71bf3c54bea63a6c17a754e22582601b49aaee4"
  },
  {
   "name": "T5_R2",
   "path": "files/framework/files/working/files/scripts/soft-slot-dynamics/m8_15_solver/out/branch_T5_R2.json",
   "commit": "33aeb754ec8d98449346dfe27d204be79e333fa5",
   "blob": "76501d58c96bec7db585dd525a09994a35f23251",
   "file": "reference/m815_targets/branch_T5_R2.json",
   "sha256": "6bcdb5cfd58980bf228b4c84271e51d1e6efa5b6052b0fd6cf98cce143a5884f"
  }
 ],
 "written": "2026-10-25T01:40:57Z"
}
```

</details>

## The order

1. C1
2. C2a
3. C2b
4. C3
5. C2a/R5
6. P5
7. C3R/R4
8. T1/R4
9. T1/R5
10. T4/R4
11. T4/R5
12. T5J/R2
13. T2/R4
14. T2/R5
15. T3/R4
16. T3/R5
17. T5/R2
