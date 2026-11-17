# Market-Data API Decision for the Forecast-Evaluation App

**Decision date:** 2026-09-13
**Scope:** data for a private/local prototype first; no public market-data display until the applicable license is confirmed.

## Recommendation

Use **Twelve Data with `SPY` at a one-day interval** for the first local prototype.

- Twelve Data's official catalog identifies `SPY` as **SPDR S&P 500 ETF Trust** and lists it on the Basic access tier.
- Its Basic plan currently lists 8 API credits per minute and 800 requests per day.
- The historical endpoint supports up to 5,000 observations per request; longer ranges can be requested by bounded date windows.
- The Basic plan is described as **internal non-display usage**. A public hosted chart or downloadable data product needs a separate license/plan review before release.

This recommendation is for **SPY ETF data**, not the official S&P 500 index. The app and portfolio must keep that distinction visible.

Official references:

- [Twelve Data API documentation](https://twelvedata.com/docs)
- [Twelve Data pricing](https://twelvedata.com/pricing)
- [Twelve Data historical-data guidance](https://support.twelvedata.com/en/articles/5214728-getting-historical-data)

## Alternatives

### Alpaca Basic

Alpaca's Basic plan covers U.S. stocks and ETFs, lists historical coverage since 2016, and permits 200 historical API calls per minute. The free real-time equity feed is IEX rather than all U.S. exchanges. It is a credible fallback for a SPY prototype, but it still does not turn SPY into the official index.

Official reference: [Alpaca Market Data API plans](https://docs.alpaca.markets/us/v1.1/docs/about-market-data-api)

### Alpha Vantage

Alpha Vantage currently states that its free service covers most datasets at 25 requests per day. Its documentation labels daily adjusted equity history as premium, and its general terms describe personal, non-commercial use unless otherwise agreed. It is suitable only after checking that the exact endpoint and intended use fit the plan and license.

Official references:

- [Alpha Vantage API documentation](https://www.alphavantage.co/documentation/)
- [Alpha Vantage support and limits](https://www.alphavantage.co/support/)
- [Alpha Vantage terms](https://www.alphavantage.co/terms_of_service/)

## Minimum data contract

Every imported dataset should persist:

1. Provider and endpoint.
2. Exact symbol and instrument name.
3. Exchange/MIC when supplied.
4. UTC retrieval time and exchange-local observation date.
5. Raw versus adjusted close convention.
6. Requested and returned date range.
7. Missing-session and duplicate checks.
8. Provider-plan/license note.
9. SHA-256 hash of the immutable raw response.

## App boundary

The first app should compare models, visualize errors, and export a backtest report. It should not recommend trades, promise returns, or relabel an ETF as an index. The current course workbook cannot be an app data source because it lacks calendar dates, a verified symbol/provider, and a documented price convention.
