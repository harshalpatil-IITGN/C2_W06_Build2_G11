# Which AI chats did we use, and what did we keep?

**Owner:** Data Lead. One row per file in this folder. Files are named `YYYYMMDD_role_tool_purpose.md` and hold the share link and the pasted text.

| File | Role | Tool | Artifact it fed | What we kept | What we discarded |
|---|---|---|---|---|---|
| `ai_logs/20261111_client-lead_gemini_grill-charter.md` (Grill run 1) | Client Lead | Gemini / Antigravity | `docs/grill_01_charter.md` | Nightly pooling unit, euro cost metric, walk ceiling constraint, corrected 37.04% baseline, non-refundable deposit insight | Per-booking intervention, 95% accuracy metric, 25% brief baseline assumption |
| `ai_logs/20261112_build-lead_claude_grill-prd.md` (Grill run 2) | Build Lead | Claude / Antigravity | `docs/grill_02_prd.md`, `docs/BUILD_PLAN.md` | Strict Bin 1 zero leakage, negative buffer asymmetric loss mechanics, graceful degradation fallback | Forcing b >= 0, premature multi-night dynamic programming in MVP |
| `karpathy_effect.md` (required) | Build Lead | | `AGENTS.md` | | |
| AI benchmark chat (required) | Data Lead | | `ai-benchmark` branch | | |
| `20261111_model-lead_claude_planning.md` | Model Lead | Claude | `docs/DECISIONS.md`, `src/backtest.py` | Commit plan, review method | Pre-made Data Lead files |
| 2026-11-17 | Model Lead (Vysag) | Gemini | Audited Bin 1 features, fixed Choose-split model selection + AUC/MAE (`388de3e`), added nightly volatility status (`3a500b6`) | `ai_logs/20261117_model-lead_gemini_audit-and-build.md` |