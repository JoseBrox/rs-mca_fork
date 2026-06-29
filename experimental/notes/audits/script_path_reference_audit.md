# Script Path Reference Audit

- **Status:** AUDIT.
- **Agent/model:** Codex acting through Jose Brox (@JoseBrox).
- **Scope:** Distinguish missing easy computational targets from scripts that
  already exist under another path, especially after the move to
  `experimental/scripts/`.

## Claim

The next easy computational target is not a new quotient-profile or q=17
implementation. Those artifacts already exist. The reproducibility gap is that
some Markdown references still use pre-cleanup script paths such as
`experimental/foo.py` or old planned names such as `scripts/locator_fiber_scan.py`.

## Artifact

`experimental/scripts/script_path_reference_audit.py` deterministically scans:

```text
agents.md
readme.md
experimental/README.md
experimental/scripts/README.md
experimental/notes/**/*.md
```

It checks every `experimental/*.py` and `scripts/*.py` style reference against
actual scripts under:

```text
scripts/**/*.py
experimental/scripts/**/*.py
experimental/notes/certificate_scanner/**/*.py
```

If an exact reference is missing but a script with the same basename exists, the
report classifies it as a stale path and prints candidate actual locations.

## Reproduction

From the repository root:

```bash
python3 experimental/scripts/script_path_reference_audit.py
python3 experimental/scripts/script_path_reference_audit.py --include-triage
python3 experimental/scripts/script_path_reference_audit.py --format json
```

The default scan skips historical PR triage notes; `--include-triage` includes
them for a fully exhaustive audit.

## Current Triage Result

The audit confirms that the originally easy targets have moved from "missing
implementation" to "audit or extension" status:

- quotient profile and dither scanner:
  `experimental/scripts/quotient_profile.py`,
  `experimental/scripts/quotient_profile_dither.py`;
- entropy reserve: `experimental/scripts/entropy_margin.py`;
- q=17 locator/MCA check for `rho=1/2,1/4`:
  `experimental/scripts/verify_q17_locator_mca.py` with certificate data under
  `experimental/data/certificates/q17-locator-mca/`;
- extension-line sweep: `experimental/scripts/f1_extension_slope_sweep.py`;
- Lean starter: `experimental/lean/rs_mca_formalization/`.

The next theoretical targets remain the main open local-limit and transfer
problems, not these starter artifacts.
