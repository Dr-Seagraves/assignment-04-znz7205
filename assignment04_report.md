# Assignment 04 Interpretation Memo

**Student Name:** [Your Name]
**Date:** [Submission Date]
**Assignment:** REIT Annual Returns and Predictors (Simple Linear Regression)

---

## 1. Regression Overview

You estimated **three** simple OLS regressions of REIT *annual* returns on different predictors:

| Model | Y Variable | X Variable | Interpretation Focus |
|-------|------------|------------|----------------------|
| 1 | ret (annual) | div12m_me | Dividend yield |
| 2 | ret (annual) | prime_rate | Interest rate sensitivity |
| 3 | ret (annual) | ffo_at_reit | FFO to assets (fundamental performance) |

For each model, summarize the key results in the sections below.

---

## 2. Coefficient Comparison (All Three Regressions)

**Model 1: ret ~ div12m_me**
- Intercept (β₀): 0.1082 (SE: 0.0060, p-value: 0.0000)
- Slope (β₁): -0.0687 (SE: 0.0325, p-value: 0.0346)
- R²: 0.00177 | N: 2527

**Model 2: ret ~ prime_rate**
- Intercept (β₀): 0.1998 (SE: 0.0158, p-value: 0.0000)
- Slope (β₁): -0.0194 (SE: 0.0030, p-value: 0.0000)
- R²: 0.01639 | N: 2527

**Model 3: ret ~ ffo_at_reit**
- Intercept (β₀): 0.0973 (SE: 0.0092, p-value: 0.0000)
- Slope (β₁): 0.5770 (SE: 0.5675, p-value: 0.3093)
- R²: 0.00041 | N: 2518

*Note: Model 3 may have fewer observations if ffo_at_reit has missing values; statsmodels drops those rows.*

---

## 3. Slope Interpretation (Economic Units)

**Dividend Yield (div12m_me):**
- A 1 percentage point increase in dividend yield (12-month dividends / market equity) is associated with a -0.0687 change in annual return (or -6.87 percentage points).
- **Interpretation:** Higher dividend yield is associated with *lower* subsequent annual returns. This may reflect a valuation effect: high-yielding REITs are already cheap (priced to offer high current income), so they offer lower capital appreciation. Alternatively, it could reflect that mature, lower-growth REITs pay out more in dividends but have lower price appreciation.

**Prime Loan Rate (prime_rate):**
- A 1 percentage point increase in the year-end prime rate is associated with a -0.0194 change in annual return (or -1.94 percentage points).
- **Interpretation:** REIT returns are negatively sensitive to interest rates. Higher borrowing costs reduce REIT profitability and also increase the discount rate that investors apply to future cash flows, both of which lower valuations. This relationship is economically meaningful and statistically significant.

**FFO to Assets (ffo_at_reit):**
- A 1 unit increase in FFO/Assets (fundamental performance) is associated with a 0.5770 change in annual return (or 57.7 percentage points).
- **Interpretation:** REITs with higher FFO-to-assets ratios show a positive but *not statistically significant* relationship with returns (p=0.309). The large coefficient estimate has a wide confidence interval due to sampling variability. We cannot reliably conclude that fundamental performance (as measured by FFO/Assets) predicts returns in this simple regression.

---

## 4. Statistical Significance

For each slope, at the 5% significance level:
- **div12m_me:** Significant (p=0.0346) — Higher dividend yield predicts significantly lower subsequent returns.
- **prime_rate:** Significant (p<0.0001) — Higher interest rates predict significantly lower returns; this relationship is the most statistically robust.
- **ffo_at_reit:** Not significant (p=0.3093) — Fundamental performance (FFO/Assets) shows no statistically reliable link to returns in this simple regression.

**Which predictor has the strongest statistical evidence of a relationship with annual returns?** The prime rate (t-stat: -6.487, p<0.0001) shows the strongest statistical evidence. Its coefficient is both precisely estimated and substantially larger in magnitude than the dividend yield coefficient.

---

## 5. Model Fit (R-squared)

Compare R² across the three models:
- **Prime rate explains the most variation** (R² = 0.0164, or 1.64%), followed by dividend yield (R² = 0.00177, or 0.177%), and FFO/Assets (R² = 0.00041, or 0.041%). **All three R² values are very low**, meaning these single predictors explain less than 2% of the variation in annual returns. This suggests that REIT returns are driven primarily by other factors not captured here: market-wide equity returns, REIT-specific sentiment, sector rotation, supply/demand dynamics, macroeconomic shocks, and idiosyncratic firm-level risks. A multiple regression including several predictors simultaneously would likely capture more of this variation.

---

## 6. Omitted Variables

By using only one predictor at a time, we might be omitting:
- **Broad equity market returns (S&P 500):** REIT returns are correlated with overall stock market performance. If market returns are correlated with interest rates (e.g., during recessions), omitting them may bias the prime_rate coefficient.
- **Mortgage rates (30-year fixed):** We use the prime rate, but REITs finance with mortgages. If mortgage rates move differently than prime rates and affect REIT leverage differently, this omission could bias our estimates.
- **REIT leverage / debt-to-assets:** REITs with higher leverage are both more affected by interest rates and may have different dividend policies and fundamental performance. Omitting leverage creates omitted-variable bias.

**Potential bias:** If omitted variables are correlated with both the X variable and ret, our slope estimates may be biased. For example, if high-leverage REITs have both higher dividend yields and higher interest-rate sensitivity, the dividend slope coefficient might partially capture a leverage effect rather than a pure dividend-yield effect. Similarly, if broad equity market strength is omitted, both the prime_rate and div12m_me coefficients may be biased (in magnitude or sign) depending on how market returns correlate with interest rates and dividend yields.

---

## 7. Summary and Next Steps

**Key Takeaway:**
REIT annual returns are significantly negatively related to interest rates (prime_rate), with a 1% increase in rates predicting a 1.94% decline in returns. Dividend yield also shows a significant negative relationship, suggesting that high-yielding REITs are already "priced in" and offer lower forward returns. Fundamental performance (FFO/Assets) shows no statistically significant link to returns in this simple model. Taken together, these findings suggest that REITs are interest-rate-sensitive and that current valuation (dividend yield) is a stronger predictor of future returns than current profitability. All three models have very low R² values, indicating that most of the variation in REIT returns is driven by other, unmeasured factors.

**What we would do next:**
- Extend to multiple regression (include prime_rate, dividend yield, and leverage simultaneously to isolate each effect)
- Add broad market index returns as a control variable to account for equity market movements
- Test for heteroskedasticity and other OLS assumption violations (especially given low R²)
- Examine whether relationships vary by time period (e.g., pre/post 2008 crisis) or REIT sector (residential, office, industrial, etc.)
- Investigate lag effects: Does lagged dividend yield or lagged interest rates predict returns better than contemporaneous values?

---

## Reproducibility Checklist
- [ ] Script runs end-to-end without errors
- [ ] Regression output saved to `Results/regression_div12m_me.txt`, `regression_prime_rate.txt`, `regression_ffo_at_reit.txt`
- [ ] Scatter plots saved to `Results/scatter_div12m_me.png`, `scatter_prime_rate.png`, `scatter_ffo_at_reit.png`
- [ ] Report accurately reflects regression results
- [ ] All interpretations are in economic units (not just statistical jargon)
