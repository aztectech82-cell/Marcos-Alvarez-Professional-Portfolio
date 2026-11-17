# Market Forecast Baseline Evaluation — Honest Out-of-Sample Testing

This case study repaired and completed an unfinished forecasting workbook before considering an app. The work focused on data provenance, look-ahead leakage, chronological testing, and a defensible conclusion.

## Data Audit

- 2,559 contiguous observations were usable.
- 3,793 later values had no date or observation index and formed a perfectly linear tail; they were excluded as synthetic/extrapolated data.
- The workbook did not identify a market symbol, provider, calendar dates, or adjusted-price convention.
- Original MA(5), MA(60), and MA(200) formulas included the value on the row they were supposed to predict, creating look-ahead bias or misalignment.

Because the instrument is unverified, this project does not claim that the workbook contains either the official S&P 500 index or the SPY ETF.

## Method

- First 80% of valid observations for training; final 20% for holdout evaluation.
- Rolling one-step-ahead forecasts using only earlier actual observations.
- Model parameters selected from the training partition only.
- Common holdout window of 512 observations.
- Metrics: MAE, RMSE, and exact up/flat/down directional accuracy.

## Holdout Results

| Method | MAE | RMSE | Directional accuracy |
|---|---:|---:|---:|
| Naive persistence | 3.8096 | **5.0355** | 0.2% |
| Optimized SES | 3.8800 | 5.0782 | 51.2% |
| Holt linear trend | 3.8650 | 5.0959 | 51.0% |
| MA(5) | 5.6079 | 7.2122 | 51.8% |
| Fixed SES | 8.4496 | 10.5098 | 49.4% |
| MA(20) | 9.8984 | 12.2032 | 48.2% |
| MA(60) | 14.2536 | 17.3994 | 48.6% |
| MA(200) | 27.8134 | 32.8598 | 45.7% |

Naive persistence predicts no change, so its exact direction score is expected to be near zero. Directional accuracy and price-error accuracy answer different questions.

## Conclusion

No tested method beat naive persistence on holdout RMSE. That is the result—not a failure to be hidden. The project demonstrates that a model can produce more active-looking directional predictions while still making worse price forecasts.

This is a forecasting-method evaluation, not investment advice or evidence of a durable trading edge.

## App Decision

The first app should be a local model-comparison tool using licensed, date-stamped `SPY` ETF data. Twelve Data is the current prototype recommendation, but its Basic plan is for internal non-display use; a public hosted display requires a licensing review. SPY must remain labeled as an ETF rather than the official index.

## Artifacts

- [Evaluation summary](SP500_Forecast_Evaluation_2026-09-13.md)
- [Machine-readable results](SP500_Forecast_Evaluation_2026-09-13.json)
- [Reproducible evaluator](evaluate_sp500_forecasts.py)
- [Market-data API decision](MARKET_DATA_API_DECISION_2026-09-13.md)

The original workbook and raw series are not published because their market-data provenance and redistribution rights are unresolved.
