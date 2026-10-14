# M8.15.1: the freeze block

The items the pre-registration fixes at the freeze (§ THE FREEZE, THE GUARD AND THE RUN of [the task](../tasks/m8_15_1_task_details.md)), recorded on 2026-10-11 before any target was run. Every hash below was computed from the bytes it names.

## The terms

- **SHA-256 of [`tasks/m8_15_1_task_details.md`](../tasks/m8_15_1_task_details.md):** `fc566c0406fef33d0f2a4ef2540fc6ce841191d292e5767de28d13b617156dbf`, which governs. Since 2026-10-12 the file carries a dated note after the terms, so this is the hash of its first 39,375 bytes, the file as filed at `dcc63851`.
- The same hash is in a dated note in § VI of the author's parent page, MIT [`soft-slot-branches.md`](https://github.com/dmobius3/mode-identity-theory/blob/558f7d3d8dc1136e7c23cabe6741467e03ec4bf4/files/framework/files/working/files/soft-slot-branches.md) (`558f7d3`).
- **What the locator's code cites.** The locator's code cites "`TARGET1_TERMS.md` v7". This file is that draft, reshaped for filing. Each of v7's lines is carried verbatim, apart from three kinds of change:
  - the layout: headings in uppercase, the cross-references that name them, and The question, Standing and What this task is not as subsections of TASK PLANNING;
  - the filing's own lines: the title, the opening, Standing's first five items, the last two lines of What this task is not, Ownership and run format, and Sources of record;
  - seven edits:
    1. "What Target 1 asks" reads "What this task asks";
    2. the locator "was qualified" and was "frozen at MIT `324fde3` before any target ran", where v7 said it "is qualified ... before the freeze";
    3. the freeze's step 1 names the commit the locator was frozen at;
    4. its step 2 names this freeze block;
    5. its step 3 says the instrument's freeze check was amended at MIT `ae3ad04`, where the qualification's record was added;
    6. "§ 2's candidate cluster rule" reads "the candidate cluster rule of the memo's § 2";
    7. "§ 2's block tracking" reads "the block tracking of the memo's § 2".

## The locator

- **The commit:** MIT [`324fde3`](https://github.com/dmobius3/mode-identity-theory/tree/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1) (`324fde3eda26924f028f4b6850d2e5efa80ae6fa`), the folder `scripts/soft-slot-dynamics-m8-15x-target1/`.
- **Its manifest,** [`MANIFEST.json`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/MANIFEST.json), SHA-256 `77f5d839408d74e44a37913d3e6fce97ba9827ea1578b13d1ead1d56f4976743`, records the SHA-256 of each of the locator's files:

  | file | SHA-256 |
  | --- | --- |
  | `locate.py` | `4407dae35237828fd35e59db80f1ea3a8895239c2219054a93627d3b5d5e7376` |
  | `t1_branch.py` | `f803adebc1df96d745c2577a68870b1e026d4da260777898b82dcd36a709f949` |
  | `tests/mock.py` | `74b654f676eeee7849422c9c67c2f46083009ee662c333cd8978bc2cd02abb20` |
  | `tests/real.py` | `1c4e815a0397ea25742f83592af77cfec29cbf5f314729dc1aa75af4012b9982` |
  | `tests/synthetic.py` | `3c40771f56f1bbb099ed58632aab80df918d84f42ef4e5b524fe273654edcb1e` |
  | `record_frozen_check.py` | `a909f5885b5b25a2178a6270a411e11c24d2b956dd0edfce659ba50f2cfa9e76` |
  | `compare_run3.py` | `1806ca4ec201058e70641122ed6c9f9c625b5575a1255edc18ea9ffec200f592` |
  | `span_gate_continuum.py` | `d49783f8ef69fc5974c6d5bb028fbca219a5359d85195ede618c33f5abf99c81` |
  | `span_rank_controls.py` | `8f589f76726455bf664550913a0a786d698c6b9e9b65d787ef82e0d6c332b90d` |

- **The extracted `decide`:** SHA-256 `6c48f12a8f58ad16eddd074601fbedc8f2345fb36be4a97da4001972c872bec9`, of the source the locator reads from the instrument's `m815_branch.py` through its syntax tree.
- **Its registration,** [`REGISTER_4.md`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/REGISTER_4.md), registered `2026-10-09T21:58:26Z`: SHA-256 `d5f497ac65127bb4769038b750dfe9cb108f986f766ae4136ed7f197dd55b16a`.
- **Its tests' results,** [`RESULT_4.md`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/RESULT_4.md): SHA-256 `fe416a0ea20531545b884bc7c23ce3517c9a9bd2d3f0bfadcddc15e3817decd7`. The records give: synthetic tests: 20 of 20 pass, each arm caught; real-solver controls: 7 of 7 pass, each arm caught; record check: ALL PASS; comparison with run 3: ALL PASS.
- **`SHA256SUMS`** pins all 83 other files of the folder.

## The instrument

- **The commit:** MIT [`97a8c08`](https://github.com/dmobius3/mode-identity-theory/tree/97a8c0884c5e3a0ed25afb345f3d668340c5b537/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x) (`97a8c0884c5e3a0ed25afb345f3d668340c5b537`), the folder `scripts/soft-slot-dynamics-m8-15x/`.
- **Its manifest,** [`m8_15x_solver/out/MANIFEST.json`](https://github.com/dmobius3/mode-identity-theory/blob/97a8c0884c5e3a0ed25afb345f3d668340c5b537/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x/m8_15x_solver/out/MANIFEST.json), SHA-256 `2b9864ab185e47f98c8572500fb2468c24de9e8346aec4e1f0fb4d077fd3e70c`, which every locator run checks. The locator's manifest records each file it lists, equal to it. Keys starting `../` are read from the instrument's folder, the rest from its solver folder:

  | file | SHA-256 |
  | --- | --- |
  | `geometry.py` | `788e10eb6973668e84370c13a8bd7b16dc9e712f6fa681c7386e15e9b1d1abff` |
  | `irreps.py` | `cbc7f4481706a08d7ca0229914980e773125c642da616e867580fe1620b5a149` |
  | `fem.py` | `209fba67eecf8c2b6ecaa432aafda3c6a161024d83d14a060809b81ca2e1061d` |
  | `nonlinear.py` | `f00ca41c1406d123dac4384cd2f7336410be49e851426db15cad79da3102a060` |
  | `standing.py` | `455cfc94f4bb10b97eaf0c426c86cb933e32fd7b199b00fc153bcad88fde5efb` |
  | `linearize.py` | `7cca177bf0c8efc344cc76d2cbcee94f0a96987ae9f3c0895ae64f2f705eed58` |
  | `integrate.py` | `3c137e773f7890478b2495d6b466dc167c2aeffc4a8d179a0b7775b9b6b58096` |
  | `symmetry.py` | `c6bbb178dd9103ab5b2f168c6df8cd923b4c57bd8432215b1b9d4a5bef5aae19` |
  | `pinned.py` | `f6e03566b15063529ac65df7b96dddb0c1726f60f418bedac9a0e5f78b936b8f` |
  | `continuation.py` | `70c4c0354bbd33dfe627a4fbfc8b187bc0073513e56cb674670d27fb837260dd` |
  | `verdict.py` | `0dac34197abbf61edd8ede76a0c23d9c0691328ed606c032a9744397b6e29f05` |
  | `persistence.py` | `3d9906d8ea9ace471aec33566a5329e6d68dbf1122677f21b3690d8b9f3fb103` |
  | `m815_common.py` | `a66fdf091021098497a08f645c54b4cc60340203dcc8f53013c550df88dfafc6` |
  | `m815_controls.py` | `dfc7a3c17fa061221d1ea74291047a01cf402d348653397a0b58cabd61b6801c` |
  | `m815_branch.py` | `7db54e748dfe238bbc21b252ec959748f9354ba681837d0fa4cbf2f0145f56db` |
  | `m815_freeze.py` | `6a47bf4376aadd589243408b6d925c1910c649080dd1df85075fa5135320a866` |
  | `angle.py` | `ca557b0d81f403c20b04675e3fb9b24be754f4cbe8b181498121dbd254e212b3` |
  | `../soft-slot-dynamics/m8_15_math/outside3_krein.py` | `94ba627cfc455d20cae34ef761f191bcfbf89e170748545d30f72d3a8b7d89e5` |
  | `../soft-slot-dynamics/m8_15_math/outside3_krein.out` | `ad01a27c993793eac968ec7ccba25499f15eaf42b10ff58234ea7079313a42b1` |
  | `../soft-slot-dynamics/m8_15_math/analyse.py` | `971f1a755cc9b3b329552e299f2e6f09a8851121b3e975e30015ffac9242c5a0` |
  | `../soft-slot-dynamics/m8_15_math/core.py` | `3507004f47d3bcc248012335e4e20e70c47cae118e9aa2a87cf85f9cc62f86b3` |
  | `../soft-slot-dynamics/m8_15_math/outside3_p.npy` | `027a797c805be453c8ea0cc1ca8c9eeb4d276d7e765a7979e1daf09954e82f0d` |
  | `out/freeze_numbers.json` | `c46b102c5ded4a78667dfb0e87e1311d729b006cb1362c6aeb91cbe1b9fe369f` |
  | `out/orientations.json` | `21b1f19161058da22a074acdc12150c8650ce60c7cdc9a86bc6622fc452290a1` |

- **The environment,** as the manifest records it: Python 3.13.13 (conda-forge), numpy 2.5.0, scipy 1.18.0, BLAS from Accelerate, macOS-15.8-arm64-arm-64bit-Mach-O, one thread for every BLAS (`OMP`, `OPENBLAS`, `VECLIB` and `MKL` thread counts all 1), ARPACK starting vectors from the seed `271828`. The instrument is deterministic under the frozen environment; bit-for-bit agreement on other machines is not promised.
- **The dated note at MIT [`ae3ad04`](https://github.com/dmobius3/mode-identity-theory/tree/ae3ad04d551c078f089a6509acd35922ae01ffdf/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x)** (`ae3ad04d551c078f089a6509acd35922ae01ffdf`): the qualification's record, the guard file's exclusion from the freeze check, and the fast-spectrum defect (the task's § Standing). No instrument file changes, and the manifest does not.

## The numbers

The task's § FROZEN VALUES. The values it inherits from M8.15's freeze are read from the instrument's [`out/freeze_numbers.json`](https://github.com/dmobius3/mode-identity-theory/blob/97a8c0884c5e3a0ed25afb345f3d668340c5b537/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x/m8_15x_solver/out/freeze_numbers.json), SHA-256 `c46b102c5ded4a78667dfb0e87e1311d729b006cb1362c6aeb91cbe1b9fe369f`, hashed in the manifest above. The guard file must carry them unchanged. **Corrected (2026-10-14):** a target run reads them through the instrument's `frozen_numbers`, from that guard file, the instrument's `m8_15x_solver/out/FROZEN.json`; the values are the same.

## The order

The instrument landed on MIT `main` at `97a8c08` on 2026-10-09. The qualification's record, the guard file's exclusion and the dated note landed at `ae3ad04`, the locator at `324fde3`, and the terms-hash note at `558f7d3`, all on 2026-10-11. The pre-registration is this pull request's merge, and no target is solved before it. After the maintainer's go, the guard file `m8_15x_solver/out/FROZEN.json`, which the locator requires before any target runs, is written with the values of `out/freeze_numbers.json` unchanged, the governing terms' SHA-256 and the go.
