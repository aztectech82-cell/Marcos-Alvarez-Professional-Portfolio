# S&P 500 Workbook Forecast Evaluation

**Generated:** 2026-09-13
**Source:** `SP500_Data_Analysis Final.xlsx` (preserved unchanged)
**Evaluated copy:** `SP500_Data_Analysis_Evaluated_2026-09-13.xlsx`

## Bottom line

No tested method beat the naive one-step persistence baseline on holdout RMSE. The defensible result is baseline performance, not a market-prediction claim.

## Clean holdout comparison

| Method | MAE | RMSE | Directional accuracy | RMSE vs. naive |
|---|---:|---:|---:|---:|
| Naive | 3.8096 | 5.0355 | 0.2% | +0.0% |
| SES optimized (alpha=0.868) | 3.8800 | 5.0782 | 51.2% | -0.8% |
| Holt trend (alpha=0.870, beta=0.010) | 3.8650 | 5.0959 | 51.0% | -1.2% |
| MA(5) | 5.6079 | 7.2122 | 51.8% | -43.2% |
| SES fixed (alpha=0.0952) | 8.4496 | 10.5098 | 49.4% | -108.7% |
| MA(20) | 9.8984 | 12.2032 | 48.2% | -142.3% |
| MA(60) | 14.2536 | 17.3994 | 48.6% | -245.5% |
| MA(200) | 27.8134 | 32.8598 | 45.7% | -552.6% |

## Data-quality findings

- Used 2,559 contiguous observations from source rows 4–2562.
- Excluded 3,793 undated tail values. Constant consecutive differences: True.
- The workbook does not identify the market symbol, source, adjusted-price convention, or calendar dates.
- Original MA(5), MA(60), and MA(200) formulas include their target row; clean calculations use strictly earlier observations.
- Seasonal Holt-Winters was not scored because the source lacks dates, verified frequency, and a defensible seasonal period.

## Interpretation

This is a forecasting-method evaluation, not investment advice. A useful app should emphasize backtesting, uncertainty, and data provenance rather than promise market prediction.
