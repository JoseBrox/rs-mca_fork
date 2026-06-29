# PR Triage, 2026-06-18 Round 3

Status: AUDIT / EXPERIMENTAL.

This note records the manual review and integration decision for the new open
PRs after commit `c2e8c45`.  Papers A--D were left unchanged; accepted material
was copied into `experimental/` and logged in `experimental/agents-log.md`.

| PR | Decision | Reason |
|---|---|---|
| #79, Add M1 depth-two Kummer saturation wall | Add | Useful M1 slack-two depth-two material.  It extends the residual-depth scanner with quotient-window lift reductions, lift-limited ceilings, fixed-window and union Kummer saturation certificates, exact `R=2`/`R=3` quotient Fourier L1 terms, and a separate Kummer-Weil import contract.  The integration keeps the result conditional on the `16p` Kummer estimate rather than promoting it to a proved MCA theorem. |
| #80, Add L1 arbitrary-fiber repair note | Add | Useful L1 correction.  It proves the raw support-fiber multiplicity identity, shows the literal arbitrary raw-fiber polynomial bound is false for `U=0`, and proposes `ImgFib_U(s)`, maximal-support, and canonical-selector repairs that match actual list size.  This is a route repair, not a list-decoding counterexample. |
| #81, Add A0 external import source check | Add | Useful A0 audit.  It records reproducible source-reachability metadata for the Paper D import chain and keeps CS25/ABF checks open where ePrint PDFs were not directly reachable.  The probe script is source availability tooling only and does not upgrade theorem status. |

## Integration Notes

- PR-provided `agents-log.md` fragments were not copied verbatim because the
  local log had newer entries.  A consolidated integration entry was added
  instead.
- PR #79 is mathematically valuable but conditional.  The exact next target is
  the standalone algebraic-geometry proof or citation for the normal-crossing
  Kummer estimate used by the certificates.
- PR #80 should inform future Paper B edits: arbitrary-word L1 statements
  should not use raw support counts without a multiplicity ledger.
- PR #81 should inform future Paper D/A0 edits: do not mark the CS25 or ABF
  imports closed until the primary source PDFs or equivalent theorem text are
  checked directly.

## Accepted Files

```text
experimental/a0_external_import_source_check_20260618.md
experimental/scripts/a0_import_source_probe.py
experimental/l1_arbitrary_fiber_repair.md
experimental/m1_depth_two_lift_window_theorem.md
experimental/m1_kummer_weil_import_contract.md
experimental/m1_support_coefficient_test.md
experimental/m1_support_occupancy_scan.md
experimental/scripts/m1_support_occupancy_scan.py
experimental/scripts/verify_l1_arbitrary_fiber_repair.py
experimental/scripts/verify_m1_kummer_divisor_geometry.py
experimental/scripts/verify_m1_slack_two_depth_two_kummer_saturation.py
```
