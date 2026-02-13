[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/lJ7aMHjD)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22674279&assignment_repo_type=AssignmentRepo)
# Assignment 04 — Simple Linear Regression (REIT Annual Returns and Predictors)

**Due:** Week 4 (Friday, February 13, 2026, 11:59 PM)

## What to Do
1. Estimate **three** simple OLS regressions of REIT *annual* returns on different predictors:
   - **ret (annual) ~ div12m_me** (dividend yield)
   - **ret (annual) ~ prime_rate** (prime loan rate)
   - **ret (annual) ~ ffo_at_reit** (FFO to assets — fundamental performance)
2. Create a scatter plot with the fitted line for each regression.
3. Write an interpretation memo comparing the coefficients.
4. Complete the AI Audit Appendix.

## Instructions
From the repo root:

1. **Get interest rate data** (one-time setup): Run `fetch_interest_rates.py` to download FRED data. Add your FRED API key at the top of the script (free at [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html)).
2. **Run the assignment:**
   ```bash
   python assignment04_regression.py
   ```

This will:
- Estimate all three regressions
- Save outputs to `Results/regression_*.txt` (div12m_me, prime_rate, ffo_at_reit)
- Create scatter plots: `Results/scatter_*.png`

## Required Files
- `assignment04_regression.py` (complete the TODO sections)
- `assignment04_report.md` (use the template; compare all three regressions—div12m_me, prime_rate, ffo_at_reit)
- `AI_AUDIT_APPENDIX.md` (use the template in this repo)
- `Results/regression_div12m_me.txt`, `regression_prime_rate.txt`, `regression_ffo_at_reit.txt`
- `Results/scatter_div12m_me.png`, `scatter_prime_rate.png`, `scatter_ffo_at_reit.png`

## Dataset
**REIT annual data** (one observation per REIT per year) in:
```
data/REIT_sample_annual_YYYY_YYYY.csv
```
Pre-built file included: `REIT_sample_annual_2004_2024.csv`

**Interest rate data** in:
```
data/interest_rates_monthly.csv
```
Run `fetch_interest_rates.py` to download from FRED (uses same sample period as REIT data). The assignment merges **December** (year-end) interest rates by year.

**Key columns (rename in your load function):**
- `ret12` → `ret`: Annual return (12-month cumulative return, Y variable)

**X variables used in this assignment:** `div12m_me`, `prime_rate`, `ffo_at_reit`

## Grading (50 points)
**Autograding (50 pts, partial credit):** Each pytest test is worth points. Pass more tests → more points. Tests check: script runs, each regression/plot file exists, and regression output has valid content.

**Manual grading (memo + AI audit):** The interpretation memo and AI Audit Appendix are graded separately (see course LMS). These are not autograded.

## Submission
Push your work to GitHub Classroom by the deadline. Then submit your GitHub repository link via the Blackboard assignment dropbox.

## Lab Notebook

The file `week4_simple_regression_lab.ipynb` is the Wednesday lab notebook. It walks through every step of fitting and interpreting an OLS regression using the same dataset. Work through it before starting the assignment -- everything you need is demonstrated there.

## Tips
- Use `statsmodels.formula.api.ols` for the regression
- Interpret slopes: compare **dividend yield** (div12m_me), **prime rate**, and **FFO/Assets** (ffo_at_reit) as predictors of annual return
- Check that each plot has a title, axis labels, and legend
- Make sure all file paths are relative (no hardcoded paths)
- The report template (`assignment04_report.md`) guides you to compare all three regressions; fill in values from your `Results/` outputs
- Paths: The repo uses `config_paths.py` for `DATA_DIR` and `RESULTS_DIR`; the script falls back to inline paths if config_paths is unavailable

---

## Extra: Other Variables in the Data (Optional Reference)

The REIT dataset includes additional columns you may explore if interested. For this assignment, you only need `ret`, `div12m_me`, `prime_rate`, and `ffo_at_reit`.

| Category | Columns |
|----------|---------|
| REIT-specific | `ffo`, `ffo_yld_reit`, `ffo_at_reit`, `roic_ffo_reit` |
| Revenue | `sales`, `sale_me` |
| Dividend | `div12m_me`, `div1m_me` |
| Profitability | `roe`, `op_new`, `ocf_me`, `ebitda_me`, `ebitda_sale` |
| Risk | `beta`, `ivol_capm_21d`, `rvol_21d`, `realizedvol` |
| Value | `btm`, `be_me` |
| Size | `lnmcap`, `market_equity`, `mcap` |
| Momentum | `ret1`, `ret_6_1` |
| Liquidity | `dolvol` |
| Other | `age`, `f_score` |
