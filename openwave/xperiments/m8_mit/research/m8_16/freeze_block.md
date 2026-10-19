# M8.16: the freeze block

The items the pre-registration fixes at the freeze (§ FIXED AT THE FREEZE of [the task](../tasks/m8_16_task_details.md)), recorded on 2026-10-18 after the maintainer's go and before any sealed case was run. Every hash below was computed from the bytes it names.

## The terms

- **SHA-256 of [`tasks/m8_16_task_details.md`](../tasks/m8_16_task_details.md):** `86992a5f7a278d639042adad2576c666979fa20f3cb53071daa62c614e83d5cf`, which governs. Since 2026-10-19 the file carries a dated note after the terms, so this is the hash of its first 48,450 bytes. They were merged in `9f1b5d7b` ([#637](https://github.com/openwave-labs/openwave/pull/637)), byte for byte the file the manifest pin covers, `run/m8_16_task_details.md`.
- The same hash is in a dated note in § V of the author's [census page](https://github.com/dmobius3/mode-identity-theory/blob/c1ea8f2e4ce3f8e61592d859b31d7fc641a6100d/files/framework/files/working/files/slot-dynamics-census.md), at MIT `c1ea8f2`.
- **The maintainer's go:** [#637, comment 6253316435](https://github.com/openwave-labs/openwave/pull/637#issuecomment-6253316435), posted 2026-10-18T18:07:09Z. It covers the instrument pinned at `c1ea8f2`, and it is recorded in `FROZEN.json`.

## The instrument

- **The commit:** MIT [`c1ea8f2`](https://github.com/dmobius3/mode-identity-theory/blob/c1ea8f2e4ce3f8e61592d859b31d7fc641a6100d/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16/REPRODUCE.md) (`c1ea8f2e4ce3f8e61592d859b31d7fc641a6100d`), in `scripts/soft-slot-dynamics-m8-16/`, with `REPRODUCE.md` and `SHA256SUMS`.
- **The manifest pin,** `run/MANIFEST_PIN`: `a5f4517360672bd6812b3f9bf79639df07304bbde19479391006ea03cd15c53a`. This is the SHA-256 of the manifest's text: one line `sha256  path` per file under `instrument/`, `run/` and `reference/m815/`, sorted by path, without `run/dry/`, `run/out/`, the pins and `FROZEN.json`. The 36 files:

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
  | `run/DRY.json` | `e7db81fe8484b9080612021e1a656cdd80a07cd5266e03aa054788971fccd4bc` |
  | `run/ENVIRONMENT.json` | `69135130896341b8ba8c56cd867c2f3254fddc7e19d01734f10c31a1e49b62ca` |
  | `run/build_dry.py` | `342553c3f06cf3f17934536b479cba789d554d68dca92bdeee74cb28f204a054` |
  | `run/cases.py` | `e5e4396c748e8055b9679c84b52236ff16d9016c30d306c85f369e54a936504a` |
  | `run/checks.py` | `31dc884bea7d9274949c00cc795073bb10519e8188e8a718c8c3f31ce31b8c83` |
  | `run/driver.py` | `315df5646de2cc4332e9d2d3fbeef810f528d953e807bf368477475e1ba0727a` |
  | `run/m8_16_task_details.md` | `86992a5f7a278d639042adad2576c666979fa20f3cb53071daa62c614e83d5cf` |
  | `run/name_targets.py` | `8b4572054cd2d6cb80352d72d2ba2805b97411d21739116ee0cb6ed9d7d4cb1d` |
  | `run/pin_manifest.py` | `4e7c7ab3eb36bafcb956c67751bdbc121767ba9b57bec89a8a108f5b67798580` |
  | `run/record_environment.py` | `1494fb8afd942e74a646671fe16f03ad4d9b095ae62cd1be35a51b2eb3a10059` |
  | `run/score_dry.out` | `dd66aaa4edc5725844cc9d93c1e239549605ad68e0af6b582d2d5eef25587462` |
  | `run/score_dry.py` | `54831523820626dc847e2ba9246a031b4efeb9270227579a2cd140e649130420` |
  | `run/targets.json` | `6ca3854d15b5447ee2eab71670ee37b84d9bad60a4f06923d500aa72a52997af` |
  | `run/test_claims.out` | `13785a763e5f17102129ed7fd08a2c11e1d991a84ff404848d1b4f9eca0c132d` |
  | `run/test_claims.py` | `0a43d5bbc75a17d479add2bb34764b935117b0951abc2fafbe2423e5526f508e` |
  | `run/test_guard.out` | `e1d49f0aa6a739d1c7724cab57531c7ba9735a28553a77b744b2dedc32c61bd7` |
  | `run/test_guard.py` | `b700f100d48006680930d5882e0a99c4cab179d1ff99d2982f55637da62f7720` |
  | `run/test_k3.out` | `6ef7b89eee740037fc9ed1e6c638477ddc67f135a4f95968df4ff927b90b7fde` |
  | `run/test_k3.py` | `b769c6bb0c6a396b30e77382e90186b42632c3e6f1d1f0109415f6502ca5be7c` |
  | `run/test_k3_synthetic.out` | `b26e7e2a2a1f819083bfd5bf6bc004a74a5751395e697c06355c85fa07f773f9` |
  | `run/write_guard.py` | `f3534ab61f54fd7642c540475801e63e8915139477510b1519c4057317cf364f` |

- **The freeze pin,** `run/FROZEN_PIN`: `ce685c8336b43fad28f279ce3198be654c712c60c9b38fac0e3bc357af56c852`, the SHA-256 of `run/FROZEN.json` (below). `write_guard.py` wrote both once, by exclusive create, at 2026-10-18T19:15:37Z. The driver refuses a sealed case unless:
  - the freeze file's SHA-256 equals its pin;
  - its manifest equals the tree's and `run/MANIFEST_PIN`;
  - its terms SHA-256 equals `run/m8_16_task_details.md`'s.
- **The environment,** as `run/ENVIRONMENT.json` records it, within the manifest:
  - Python 3.13.13 (conda-forge's build), NumPy 2.5.0 and SciPy 1.18.0, on Accelerate's BLAS and LAPACK, with no threading variable set;
  - macOS 15.8 (24H23), on a Mac15,13 with an Apple M3.
- **The environment, read again at the freeze** by `python3 -I -B run/record_environment.py --check`: no difference. Both readings, as it printed them:

  <details><summary>the recorded and the live readings</summary>

  ```text
  recorded: {
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
  live: {
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
  differences: none
  ```

  </details>

- **M8.15's target records,** copied by `write_guard.py` after the go from MIT at their named commit. Each was copied only once its git blob id equalled the one named before the freeze, in `run/targets.json`, into `reference/m815_targets/`:

  | record | commit | blob | SHA-256 |
  | --- | --- | --- | --- |
  | `T2_R4` | `33aeb75` | `22bb03321404960b76ad568e1091f9629b4bdcb2` | `5b1758c9ec1c6566091fe9028a542f67fd6bd0ad51c927f7147d54c07d876b49` |
  | `T2_R5` | `33aeb75` | `2a5e77315c8c323e0c9ec8b15629fa26b6b64d98` | `a064683298ebc922ecbba06316a3af11b68a7b6193e7e04c63eaa9fc1ad931ba` |
  | `T3_R4` | `33aeb75` | `497301e4186b8e45d9efcb4207255d7b257f47e7` | `fe3497a3a4de45a5f3a6d2ce2a6c322feb5399610ad20d9da530acd8abdf3bc2` |
  | `T3_R5` | `33aeb75` | `a719df9db2b04edc06c1ec82f2d8467fc5b77c41` | `660d0322d1921bb7b6c9e7e1b71bf3c54bea63a6c17a754e22582601b49aaee4` |
  | `T5_R2` | `33aeb75` | `76501d58c96bec7db585dd525a09994a35f23251` | `6bcdb5cfd58980bf228b4c84271e51d1e6efa5b6052b0fd6cf98cce143a5884f` |

## The seeds

Each case's representative on the lowest level, at `N = 16`, against the Result's values (§ BEFORE THE FREEZE). Sealed seeds were checked on the lowest level only (BOUNDARY.md's amendment 2), with no solve and no spectrum.
- **The source:** `dev/seed_check.py`, DEVLOG entry 269, its output kept as `dev/runs/269_seed_check.out`.
- **Its currency:** the instrument files it reads, `basis.py`, `branches.py`, `certified.py`, `functional.py`, `group2i.py`, `quadrature.py`, `su2.py`, are unchanged in the pinned tree. **Corrected (2026-10-19):** the seed check imports eleven instrument files, these seven and `__init__.py`, `devtools.py`, `newton.py` and `linear.py`. Of them only `linear.py` changed after the seed check, by one line in `record()` that the seed values never reach, as the approval of [#639](https://github.com/openwave-labs/openwave/pull/639) and the run record's § 6 record.

| case | slot | sealed | `Q(u)` | the Result's | relative | criticality | `(k, r_u)` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | `R3` | no | 1.000000000000002 | 1 | 1.6e-15 | 1.1e-15 | (4, 2), as the Result's |
| C2a | `R4` | no | 1.000777000777000 | 1288/1287 | 6.7e-16 | 9.0e-17 | (3, 1), as the Result's |
| C3 | `R4` | no | 1.223776223776227 | 175/143 | 2.4e-15 | 2.0e-16 | (4, 4), as the Result's |
| P5 | `R4` | yes | 1.184615384615386 | 77/65 | 1.3e-15 | 6.8e-16 | (4, 2), as the Result's |
| T1/R4 | `R4` | yes | 1.027972027972031 | 147/143 | 3.2e-15 | 3.8e-17 | (3, 1), as the Result's |
| T2/R4 | `R4` | yes | 1.159014112502487 | 5831/5031 | 1.9e-15 | 6.4e-16 | (4, 4), as the Result's |
| T3/R4 | `R4` | yes | 1.359751359751360 | 1750/1287 | 1.6e-16 | 4.2e-16 | (4, 4), as the Result's |
| T4/R4 | `R4` | yes | 1.185203461338849 | 1.1852034613388465 | 2.1e-15 | 5.6e-16 | (4, 2), as the Result's |
| C2a/R5 | `R5` | no | 1.000437062937064 | 2289/2288 | 1.6e-15 | 5.3e-17 | (3, 1), as the Result's |
| T1/R5 | `R5` | yes | 1.015734265734266 | 581/572 | 2.2e-16 | 3.3e-17 | (3, 1), as the Result's |
| T2/R5 | `R5` | yes | 1.089445438282649 | 609/559 | 1.0e-15 | 6.9e-16 | (4, 4), as the Result's |
| T3/R5 | `R5` | yes | 1.202360139860140 | 2751/2288 | 3.7e-16 | 2.8e-16 | (4, 4), as the Result's |
| T4/R5 | `R5` | yes | 1.104176947003103 | 1.104176947003101 | 2.0e-15 | 5.5e-16 | (4, 2), as the Result's |
| C2b | `R2` | no | 1.006993006993007 | 144/143 | 0.0e+00 | 8.4e-17 | (5, 1), as the Result's |
| T5/R2 | `R2` | yes | 1.692307692307693 | 22/13 | 6.6e-16 | 1.5e-16 | (6, 4), as the Result's |

## `FROZEN.json`

In full: 1937 lines, SHA-256 `ce685c8336b43fad28f279ce3198be654c712c60c9b38fac0e3bc357af56c852`. It holds:
- the allowlist and order of the 15 cases;
- every case, with its slot, representative, `Q`, `(k, r_u)`, expected `V₀`, expected type and indices, frozen spectrum and points;
- the frozen values;
- the terms' and the manifest's SHA-256;
- the go;
- the target records' SHA-256.

<details><summary><code>run/FROZEN.json</code></summary>

```json
{
 "allowlist": [
  "C1",
  "C2a",
  "C2b",
  "C3",
  "C2a/R5",
  "P5",
  "T1/R4",
  "T1/R5",
  "T4/R4",
  "T4/R5",
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
  "T1/R4",
  "T1/R5",
  "T4/R4",
  "T4/R5",
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
   "factor": 0.1,
   "span": 1e-06,
   "left": 10000.0,
   "conditioning": 0.01,
   "idempotence": 1e-06
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
   ]
  },
  "sample": [
   0.25,
   0.5,
   1.0,
   2.0
  ]
 },
 "terms_sha256": "86992a5f7a278d639042adad2576c666979fa20f3cb53071daa62c614e83d5cf",
 "manifest_sha256": "a5f4517360672bd6812b3f9bf79639df07304bbde19479391006ea03cd15c53a",
 "go": "https://github.com/openwave-labs/openwave/pull/637#issuecomment-6253316435",
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
 "written": "2026-10-18T19:15:37Z"
}
```

</details>

## The order

- **The instrument** landed on MIT `main` at `805ddbc` on 2026-10-18, and its revision after review at `c1ea8f2` the same day, before the go.
- **The terms** were merged in `9f1b5d7b`, and the maintainer's go followed at 18:07:09Z.
- **`write_guard.py`** wrote `FROZEN.json` at 2026-10-18T19:15:37Z.
- **This block** follows it, and the run follows this block. No sealed case has run.
