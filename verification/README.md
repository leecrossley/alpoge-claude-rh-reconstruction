# Verification artifacts

The post-review edition proves the implication in Theorem 1.3. Its last
section gives two sufficient arithmetic estimates, the pointwise bound
(15.1) and the signed translate mean (15.2). The
[proof-status table](../audit/paper-proof-status.tsv) records the inputs
to the new arguments and the parts that still use the published formalization.
The [selected prime-loss checks](../lean-15-1/selected-prime-loss-verification.log),
[exceptional row comparison](../lean-15-1/exceptional-degree-verification.log)
and [height-budget checks](../lean-15-1/recorded-height-verification.log)
identify the new Lean declarations and their axioms. The signed CM
comparison, the sparse moment and the bounded-conductor intervals have
their proofs in the English manuscript.

For a paper-only verification, read Theorem 1.3, the finite sum in Section 10,
the signed Mellin transform in Section 12, and the deduction in Section 13.
Equation (15.1) fixes the common arithmetic hypothesis with its quantifiers.
Sections 2 and 3 specify the common Frobenius lifts and the marked
comparisons needed at one precision. Section 5 follows the seeds on the
actual towers, treats classical imprimitive quartic points, and gives
strict Selmer vanishings through all depths on specified families. On a jointly selected window, Corollary 5.70 reduces the full field-length budget to the remaining matching-parity sums in Cases I, II, III and V.
Section 9 computes the integral determinants at a marked CM point,
the cusp zero mode, the half-maximum bound and the principal packet
measure. Section 10 gives a signed four-twist formula and a test at
integer squares. Section 8.6 forms a direct sum over the translates
before composing the theta operators and proves one rank-normalized slope
comparison. Section 11.1 connects that comparison to (15.2) with the
original numerical budget and the selection order for one complete
window. The new comparison and its application are proved in the
English text. The [referee response](../audit/referee-response.md)
locates the individual corrections and qualifications. The final column of the
proof-status table gives the printed statement numbers and pages, and its
preceding column identifies the assumptions needed at each step.

The 22 November revision separates the generic deformation counts from
the arithmetic at the trivial target. Run the exact integer calculation
for the positive Case II length with
```sh
python verification/check_zeta_jd_example.py
```

The calculation enumerates 332 reduced ideals in three cycles and
checks the specialized rank-four level. The all-depth class-group
formula, the odd-prime opposite-parity bound, and the field and flag
calculations have their proofs in Sections 5 and 9.

Extract the [original proof-value records](zeta-count-trace.zip) to
an empty directory and run `python verify.py` there to replay the
99 serialized expression paths across 2,935 original records. Its README gives the commands for
checking the full RH dependency tree, the source files, the 99
references in 24 original compiled modules, and the original export.

The source project pins Lean 4.33.1 and Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`. The independent export checker
and the three bridge files use the native Windows binary distribution of Lean
4.36.0. These files use Mathlib `v4.36.0` at
`fc4f59e577feb1a4956671bc04ac18aaaf8cd842`.

| Windows verification tool | SHA-256 |
|---|---|
| Lean 4.36.0 release archive | `8b910f5395fe13b70f2f662831e3fdbd523686e4ec999919927b1c18b505b696` |
| `nanoda_bin.exe` 0.4.17 | `a76bed8bc1091842ea7f85996464687ca3945edc6f8194237bf6963503d2d31b` |
| `con-leche.exe` | `5dc6d10f2608e217464b92fbcf823dbff3fc82f80f2610654da5d0b5f58e8538` |

## Original export

Use the fixed [export and verification archive](https://math.mit.edu/~drew/grh/).
The extraction script uses Python 3.11 or later and the `zstandard` package.
Put the compressed export in a scratch directory with 1.6 GB of free space
for the prefix. The example uses a directory named `rh-verification` next
to this checkout. Start in the repository root with the native Lean 4.36.0
tools on the command path.

```powershell
$verification = (Resolve-Path ./verification).Path
Set-Location ../rh-verification
$export = (Resolve-Path ./solution.ndjson.zst).Path
python "$verification/extract_analytic_prefix.py" $export analytic-prefix.ndjson prefix-receipt.json
nanoda_bin "$verification/nanoda-prefix.json"
con-leche --verified --jobs=2 --progress=25000 analytic-prefix.ndjson
```

The receipt records the SHA-256 of the 1,539,032,259-byte prefix and the
original NDJSON declaration, type, and proof-value indices for its three
landmarks. These indices are serialization identifiers within this precise
export. The prefix contains every preceding record, including its prerequisites.
The native Nanoda checker completed in approximately 12 min 50 s by the
process start time and output file timestamp. The highest sampled process
peak working set was 1,602,121,728 bytes.
Read other exact qualified-name records with, for example,
`python -X utf8 "$verification/find_originals.py" analytic-prefix.ndjson Deduction.ch_core Deduction.ch_top UpperTheory.Comparison₂.core_gm`.

## Fresh bridge

In the standalone Mathlib checkout, with Lean 4.36.0's `lake` and `lean`
available, run:

```powershell
git checkout fc4f59e577feb1a4956671bc04ac18aaaf8cd842
lake exe cache get Mathlib.Analysis.SpecialFunctions.Pow.Real Mathlib.Algebra.Order.Archimedean.Basic Mathlib.Data.Finset.Card Mathlib.Tactic.FieldSimp Mathlib.Tactic.Linarith Mathlib.Tactic.Positivity Mathlib.Tactic.Ring
lake env lean "$verification/WindowBridge.lean"
```

The file has no submission imports. It prints the transitive Lean axioms of
both fresh theorems.


## Independent reconstruction and source citations

The critical-line file fixes one epsilon before the windows are selected, carries the bound across each window, and proves a scalar estimate for the Cauchy remainder. Its two mathematical inputs are the arithmetic supply and the analytic exclusion for the same real function. Run this command in the same pinned Mathlib checkout as the other bridge.

~~~powershell
lake env lean "$verification/CriticalLineBridge.lean"
~~~

The finite averaging file checks character projection along a homomorphism
from a finite group and transport of an absolute error through the normalized
mean. Run it in the same checkout.

~~~powershell
lake env lean "$verification/TranslateMean.lean"
~~~

The local results are in [the finite averaging log](translate-mean.log), [the critical-line log](critical-line-bridge.log), [the finite-window log](window-bridge.log), [the Nanoda log](nanoda-prefix.log) and [the ConLeche log](con-leche-prefix.log). Section 15 specifies the deep arithmetic statements still imported from the pinned development.

The arithmetic supplements use the original Lean 4.33.1 project. From the repository root, save the path to its verification files, then change to a built checkout of the pinned upstream project. The example uses a sibling directory named `lean`.

~~~powershell
$verification = (Resolve-Path ./verification).Path
$supplements = (Resolve-Path ./lean-15-1).Path
Set-Location ../lean
lake env python "$supplements/check_lean.py"
lake env lean "$verification/LargePrimePrecision.lean"
~~~

The [local pairing and Gram-window checks](large-prime-precision.log)
include the one-lattice test for the original rank-loss predicate and the
root counts and row divisibility used in the paper. The Smith formula
and its application to the weight-box budget are distinguished in Section 15.

The `audit/source-witnesses.tsv` table binds every manuscript citation to a source file hash, one-based line and owning declaration. `audit/root-paths.tsv` holds the corresponding edges of the classical RH dependency tree. `audit/sibling-paths.tsv` records paths for the source declarations belonging to the other advertised roots. Entries marked `source_only` point to an original declaration header, including the mean bound at line 199 of `LevelOfCongruence.lean` and several inputs to the period and slope comparisons. With the full tree argument the checker verifies their absence from the classical root's dependency walk. The original source distribution is available from the [verification archive](https://math.mit.edu/~drew/grh/). From the root of the unpacked English source bundle run the following, adjusting the path to your copy of the original project.

~~~powershell
python -X utf8 verification/check_citations.py --source ../lean --tree evidence/rh-dependency-tree.tsv.gz --archive ../lean.tar.gz
~~~

The evidence directory in the source bundle includes the full classical dependency tree and the programs used to regenerate it from the official export. To repeat the full graph calculation, extract `evidence/full-graph-source.zip` into a scratch directory with room for the expression table, then run the following there. The scan verifies the SHA-256 digests of the compressed and uncompressed export.

~~~powershell
cargo build --locked --release --manifest-path graph/Cargo.toml
python scan.py --source $export --folder full
python build_dict.py full
python report_graph.py full evidence
python verify_paths.py full evidence/rh-walk-summary.json
python report_five.py full evidence/five.tsv
~~~

The three numerical certificates accept ordinary and optimised Python. The archived binder and dependency-graph checkers use assertions and stop when Python optimisation is enabled. Run those checkers with `python -E` to ignore the `PYTHONOPTIMIZE` environment variable.

The file `verification/hOnto-proof-slice.zip` contains the term slice and its checker. Extract it and run `python verify.py` in that directory. Passing `--export` followed by the original compressed export also compares the records against their original bytes. The local binder result is in [binder.log](binder.log).

Build the article with `tectonic main.tex` from the directory containing its main source. The build reads the section files and needs no Lean installation.

The fixed-target test in Section 15 has an outward-rounded certificate
for every real point of the quartic conductor-15 window from 10,000 to
1,000,000. Run `python -X utf8 verification/prime_prefix_window.py`
from the English source directory. The script certifies the prime-only
majorant and the original retained ramp independently with their respective
centres. [Recorded bounds](prime-prefix-window.log)
