"""Build an independently calculated, versioned evaluation of the S&P workbook.

The source workbook is never overwritten. Forecasts use only earlier observations,
and model parameters are selected on the training partition only.
"""

from __future__ import annotations

import json
import math
from datetime import date
from pathlib import Path

import numpy as np
from openpyxl import load_workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "SP500_Data_Analysis Final.xlsx"
OUTPUT = ROOT / "SP500_Data_Analysis_Evaluated_2026-09-13.xlsx"
RESULTS_JSON = ROOT / "SP500_Forecast_Evaluation_2026-09-13.json"
RESULTS_MD = ROOT / "SP500_Forecast_Evaluation_2026-09-13.md"

BLUE = "1F4E78"
LIGHT_BLUE = "D9EAF7"
LIGHT_GRAY = "E7E6E6"
LIGHT_GREEN = "E2F0D9"
LIGHT_YELLOW = "FFF2CC"
WHITE = "FFFFFF"


def extract_series(ws):
    """Return contiguous rows having both observation number and price."""
    rows = []
    for row in range(4, ws.max_row + 1):
        observation = ws.cell(row, 2).value
        price = ws.cell(row, 3).value
        if observation is None or price is None:
            break
        try:
            rows.append((int(observation), float(price), row))
        except (TypeError, ValueError):
            break
    return rows


def moving_average_forecasts(y: np.ndarray, window: int) -> np.ndarray:
    forecasts = np.full(len(y), np.nan)
    csum = np.concatenate(([0.0], np.cumsum(y)))
    for t in range(window, len(y)):
        forecasts[t] = (csum[t] - csum[t - window]) / window
    return forecasts


def ses_forecasts(y: np.ndarray, alpha: float) -> tuple[np.ndarray, float]:
    forecasts = np.full(len(y), np.nan)
    level = float(y[0])
    for t in range(1, len(y)):
        forecasts[t] = level
        level = alpha * float(y[t]) + (1.0 - alpha) * level
    return forecasts, level


def holt_forecasts(y: np.ndarray, alpha: float, beta: float) -> tuple[np.ndarray, float]:
    forecasts = np.full(len(y), np.nan)
    level = float(y[0])
    initial_span = min(6, len(y))
    trend = float(np.mean(np.diff(y[:initial_span]))) if initial_span > 1 else 0.0
    for t in range(1, len(y)):
        forecasts[t] = level + trend
        previous_level = level
        level = alpha * float(y[t]) + (1.0 - alpha) * (level + trend)
        trend = beta * (level - previous_level) + (1.0 - beta) * trend
    return forecasts, level + trend


def training_mse(actual: np.ndarray, forecast: np.ndarray) -> float:
    valid = np.isfinite(forecast)
    return float(np.mean(np.square(actual[valid] - forecast[valid])))


def optimize_ses(train: np.ndarray) -> float:
    best_alpha = 0.1
    best_mse = math.inf
    for alpha in np.linspace(0.001, 0.999, 999):
        forecast, _ = ses_forecasts(train, float(alpha))
        mse = training_mse(train, forecast)
        if mse < best_mse:
            best_alpha, best_mse = float(alpha), mse
    return best_alpha


def optimize_holt(train: np.ndarray) -> tuple[float, float]:
    best = (0.2, 0.1)
    best_mse = math.inf

    # Coarse search, followed by a local fine search. No holdout observations are
    # used in parameter selection.
    for alpha in np.linspace(0.05, 0.95, 19):
        for beta in np.linspace(0.05, 0.95, 19):
            forecast, _ = holt_forecasts(train, float(alpha), float(beta))
            mse = training_mse(train, forecast)
            if mse < best_mse:
                best, best_mse = (float(alpha), float(beta)), mse

    alpha_center, beta_center = best
    alpha_values = np.unique(np.clip(np.arange(alpha_center - 0.10, alpha_center + 0.101, 0.005), 0.001, 0.999))
    beta_values = np.unique(np.clip(np.arange(beta_center - 0.10, beta_center + 0.101, 0.005), 0.001, 0.999))
    for alpha in alpha_values:
        for beta in beta_values:
            forecast, _ = holt_forecasts(train, float(alpha), float(beta))
            mse = training_mse(train, forecast)
            if mse < best_mse:
                best, best_mse = (float(alpha), float(beta)), mse
    return best


def metrics(y: np.ndarray, forecast: np.ndarray, indices: np.ndarray) -> dict[str, float | int]:
    actual = y[indices]
    predicted = forecast[indices]
    errors = actual - predicted
    actual_direction = np.sign(actual - y[indices - 1])
    predicted_direction = np.sign(predicted - y[indices - 1])
    return {
        "observations": int(len(indices)),
        "mae": float(np.mean(np.abs(errors))),
        "rmse": float(np.sqrt(np.mean(np.square(errors)))),
        "directional_accuracy": float(np.mean(actual_direction == predicted_direction)),
    }


def style_title(cell):
    cell.fill = PatternFill("solid", fgColor=BLUE)
    cell.font = Font(color=WHITE, bold=True, size=14)
    cell.alignment = Alignment(vertical="center")


def style_section(cell):
    cell.fill = PatternFill("solid", fgColor=LIGHT_BLUE)
    cell.font = Font(bold=True, color=BLUE)


def style_header_row(ws, row: int, start: int, end: int):
    for col in range(start, end + 1):
        cell = ws.cell(row, col)
        cell.fill = PatternFill("solid", fgColor=BLUE)
        cell.font = Font(color=WHITE, bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def write_evaluation_sheet(wb, results, formula_audit, next_forecasts, coverage):
    if "S&P 500 Evaluation" in wb.sheetnames:
        del wb["S&P 500 Evaluation"]
    ws = wb.create_sheet("S&P 500 Evaluation", 0)
    ws.sheet_view.showGridLines = False
    ws.merge_cells("A1:F1")
    ws["A1"] = "S&P 500 Forecast Evaluation — Independent Recalculation"
    style_title(ws["A1"])
    ws.row_dimensions[1].height = 24

    ws["A3"] = "Bottom line"
    style_section(ws["A3"])
    ws.merge_cells("B3:F3")
    ws["B3"] = results["conclusion"]
    ws["B3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[3].height = 44

    ws["A5"] = "Methodology"
    style_section(ws["A5"])
    methodology = [
        ("Usable observations", results["data_audit"]["usable_observations"]),
        ("Training observations", results["methodology"]["training_observations"]),
        ("Holdout observations", results["methodology"]["holdout_observations"]),
        ("Split", results["methodology"]["split"]),
        ("Evaluation", "Rolling one-step-ahead forecasts; every prediction uses only earlier actual observations"),
        ("Metrics", "MAE, RMSE, and exact up/flat/down directional accuracy on one common holdout window; naive predicts flat, so its direction score is expected to be near zero"),
        ("Instrument/date status", "Unverified: the workbook contains an observation index, not calendar dates or a source identifier"),
    ]
    for offset, (label, value) in enumerate(methodology, start=6):
        ws.cell(offset, 1, label).font = Font(bold=True)
        ws.merge_cells(start_row=offset, start_column=2, end_row=offset, end_column=6)
        ws.cell(offset, 2, value)
        ws.cell(offset, 2).alignment = Alignment(wrap_text=True)

    metrics_start = 15
    ws.cell(metrics_start, 1, "Holdout results")
    style_section(ws.cell(metrics_start, 1))
    headers = ["Method", "MAE", "RMSE", "Directional accuracy", "RMSE vs. naive", "Assessment"]
    for col, value in enumerate(headers, start=1):
        ws.cell(metrics_start + 1, col, value)
    style_header_row(ws, metrics_start + 1, 1, 6)
    naive_rmse = results["methods"]["Naive"]["rmse"]
    sorted_methods = sorted(results["methods"].items(), key=lambda item: item[1]["rmse"])
    for row, (name, values) in enumerate(sorted_methods, start=metrics_start + 2):
        change = (naive_rmse - values["rmse"]) / naive_rmse
        assessment = "Best holdout RMSE" if name == results["best_method"] else "Baseline" if name == "Naive" else "Comparison"
        ws.cell(row, 1, name)
        ws.cell(row, 2, values["mae"])
        ws.cell(row, 3, values["rmse"])
        ws.cell(row, 4, values["directional_accuracy"])
        ws.cell(row, 5, change)
        ws.cell(row, 6, assessment)
        ws.cell(row, 2).number_format = "0.0000"
        ws.cell(row, 3).number_format = "0.0000"
        ws.cell(row, 4).number_format = "0.0%"
        ws.cell(row, 5).number_format = "0.0%"
        if name == results["best_method"]:
            for col in range(1, 7):
                ws.cell(row, col).fill = PatternFill("solid", fgColor=LIGHT_GREEN)

    audit_start = metrics_start + 3 + len(sorted_methods)
    ws.cell(audit_start, 1, "Data and formula audit")
    style_section(ws.cell(audit_start, 1))
    audit_lines = [
        ("Valid source rows", f"Rows 4–2562 ({results['data_audit']['usable_observations']:,} observations)"),
        ("Excluded tail", f"Rows 2563–6355 ({results['data_audit']['excluded_tail_rows']:,} undated values); consecutive differences are constant, so this is synthetic/extrapolated rather than usable history"),
        ("Original chart", "Removed from this evaluated copy because it references the excluded synthetic tail; the untouched source workbook is retained separately"),
        ("Seasonal Holt-Winters", "Not scored: there are no calendar dates, verified frequency, or defensible seasonal period in the workbook"),
    ] + formula_audit
    for offset, (label, value) in enumerate(audit_lines, start=audit_start + 1):
        ws.cell(offset, 1, label).font = Font(bold=True)
        ws.merge_cells(start_row=offset, start_column=2, end_row=offset, end_column=6)
        ws.cell(offset, 2, value)
        ws.cell(offset, 2).alignment = Alignment(wrap_text=True, vertical="top")

    coverage_start = audit_start + 2 + len(audit_lines)
    ws.cell(coverage_start, 1, "Prior-20-observation band coverage")
    style_section(ws.cell(coverage_start, 1))
    ws.cell(coverage_start + 1, 1, "Band")
    ws.cell(coverage_start + 1, 2, "Holdout coverage")
    style_header_row(ws, coverage_start + 1, 1, 2)
    ws.cell(coverage_start + 2, 1, "Mean ± 2 population standard deviations")
    ws.cell(coverage_start + 2, 2, coverage["2_sigma"])
    ws.cell(coverage_start + 3, 1, "Mean ± 3 population standard deviations")
    ws.cell(coverage_start + 3, 2, coverage["3_sigma"])
    ws.cell(coverage_start + 2, 2).number_format = "0.0%"
    ws.cell(coverage_start + 3, 2).number_format = "0.0%"

    next_start = coverage_start + 5
    ws.cell(next_start, 1, "Next-observation model outputs")
    style_section(ws.cell(next_start, 1))
    ws.cell(next_start + 1, 1, "Method")
    ws.cell(next_start + 1, 2, "Forecast")
    style_header_row(ws, next_start + 1, 1, 2)
    for row, (name, value) in enumerate(next_forecasts.items(), start=next_start + 2):
        ws.cell(row, 1, name)
        ws.cell(row, 2, value)
        ws.cell(row, 2).number_format = "0.0000"

    limitations_start = next_start + 3 + len(next_forecasts)
    ws.cell(limitations_start, 1, "Interpretation guardrails")
    style_section(ws.cell(limitations_start, 1))
    guardrails = [
        "This is a course-data forecasting evaluation, not investment advice or a trading signal.",
        "A small holdout improvement over naive persistence is not evidence of a durable market-prediction edge.",
        "Before building an app, replace the unverified series with licensed, date-stamped market data and rerun walk-forward tests across multiple market regimes.",
        "Do not label the series as the S&P 500 index or SPY ETF until the symbol and source are independently verified.",
    ]
    for row, line in enumerate(guardrails, start=limitations_start + 1):
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
        ws.cell(row, 1, f"• {line}")
        ws.cell(row, 1).alignment = Alignment(wrap_text=True)

    widths = {"A": 34, "B": 20, "C": 18, "D": 22, "E": 18, "F": 28}
    for col, width in widths.items():
        ws.column_dimensions[col].width = width
    ws.freeze_panes = "A16"
    ws.auto_filter.ref = f"A{metrics_start + 1}:F{metrics_start + 1 + len(sorted_methods)}"


def write_clean_forecasts_sheet(wb, observations, y, forecasts, train_end):
    if "Clean Forecasts" in wb.sheetnames:
        del wb["Clean Forecasts"]
    ws = wb.create_sheet("Clean Forecasts", 1)
    ws.sheet_view.showGridLines = False
    headers = ["Observation", "Actual", "Partition"] + list(forecasts.keys())
    for col, value in enumerate(headers, start=1):
        ws.cell(1, col, value)
    style_header_row(ws, 1, 1, len(headers))

    for i, observation in enumerate(observations):
        row = i + 2
        ws.cell(row, 1, int(observation))
        ws.cell(row, 2, float(y[i]))
        ws.cell(row, 3, "Training" if i < train_end else "Holdout")
        for col, values in enumerate(forecasts.values(), start=4):
            value = values[i]
            if np.isfinite(value):
                ws.cell(row, col, float(value))
        for col in range(2, len(headers) + 1):
            ws.cell(row, col).number_format = "0.0000"
        if i == train_end:
            for col in range(1, len(headers) + 1):
                ws.cell(row, col).fill = PatternFill("solid", fgColor=LIGHT_YELLOW)

    ws.freeze_panes = "D2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(y) + 1}"
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 12
    for col in range(4, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 20

    # A readable final-holdout chart, instead of the original chart that used
    # the excluded synthetic tail.
    chart = LineChart()
    chart.title = "Final 120 Holdout Observations"
    chart.y_axis.title = "Workbook price units"
    chart.x_axis.title = "Observation"
    chart.height = 10
    chart.width = 22
    start_row = max(train_end + 2, len(y) + 2 - 120)
    end_row = len(y) + 1
    selected_columns = [2, 4, 6, 9]  # Actual, Naive, MA20, Holt
    for col in selected_columns:
        data = Reference(ws, min_col=col, min_row=1, max_row=end_row)
        chart.add_data(data, titles_from_data=True, from_rows=False)
    categories = Reference(ws, min_col=1, min_row=start_row, max_row=end_row)
    chart.set_categories(categories)
    # Restrict series values to the same 120-row display interval.
    for series, col in zip(chart.series, selected_columns):
        data = Reference(ws, min_col=col, min_row=start_row, max_row=end_row)
        series.val.numRef.f = data.range_string
    ws.add_chart(chart, "K3")


def write_app_scope_sheet(wb):
    if "App Scope" in wb.sheetnames:
        del wb["App Scope"]
    ws = wb.create_sheet("App Scope", 2)
    ws.sheet_view.showGridLines = False
    ws.merge_cells("A1:D1")
    ws["A1"] = "Honest Forecast-Evaluation App Scope"
    style_title(ws["A1"])
    sections = [
        ("Purpose", "Compare simple forecasting baselines on licensed, date-stamped market data; show uncertainty and out-of-sample evidence."),
        ("Inputs", "Verified symbol, source, market calendar, adjusted/unadjusted field, date range, and data-use license."),
        ("Models", "Naive persistence, moving averages, SES, nonseasonal Holt trend; seasonal models only after a documented seasonality test."),
        ("Evaluation", "Expanding-window or rolling-window backtests across multiple regimes; MAE, RMSE, direction, interval coverage, and costs where relevant."),
        ("Output", "Model leaderboard, residual diagnostics, downloadable evaluation, next-observation scenarios, and explicit limitations."),
        ("Guardrails", "No guaranteed returns, no unsupported S&P label, no training on holdout data, and no claim of durable edge from one workbook."),
        ("Recommended first build", "A local Streamlit prototype reading a clean CSV/API response, then a small hosted demo only after data licensing is confirmed."),
    ]
    row = 3
    for label, value in sections:
        ws.cell(row, 1, label)
        style_section(ws.cell(row, 1))
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=4)
        ws.cell(row, 2, value)
        ws.cell(row, 2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 45
        row += 2

    row += 1
    ws.cell(row, 1, "Current data-source decision")
    style_section(ws.cell(row, 1))
    row += 1
    source_headers = ["Source", "Useful verified facts", "Decision", "Official reference"]
    for col, value in enumerate(source_headers, start=1):
        ws.cell(row, col, value)
    style_header_row(ws, row, 1, 4)
    source_rows = [
        (
            "Twelve Data Basic",
            "SPY is cataloged as the SPDR S&P 500 ETF Trust on Basic; 8 API credits/minute and 800/day; up to 5,000 points/request.",
            "Recommended for a private/local prototype. Basic is internal non-display use, so confirm or upgrade licensing before a public data display.",
            "https://twelvedata.com/docs and https://twelvedata.com/pricing",
        ),
        (
            "Alpaca Basic",
            "Free US stock/ETF data, historical coverage since 2016, IEX real-time coverage, and 200 historical calls/minute.",
            "Good fallback for SPY testing; it is ETF data, not the official S&P 500 index, and the free IEX feed is not full-market coverage.",
            "https://docs.alpaca.markets/us/v1.1/docs/about-market-data-api",
        ),
        (
            "Alpha Vantage",
            "Free service covers most datasets at 25 requests/day; adjusted daily equity history is listed as premium.",
            "Not first choice for this app unless the selected endpoint and personal/noncommercial license fit the exact use.",
            "https://www.alphavantage.co/documentation/ and https://www.alphavantage.co/support/",
        ),
    ]
    for source_row in source_rows:
        row += 1
        for col, value in enumerate(source_row, start=1):
            ws.cell(row, col, value)
            ws.cell(row, col).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 88
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 48
    ws.column_dimensions["C"].width = 50
    ws.column_dimensions["D"].width = 48


def main():
    wb = load_workbook(SOURCE)
    source_ws = wb["HistoricalPrices"]
    rows = extract_series(source_ws)
    observations = np.array([row[0] for row in rows], dtype=int)
    y = np.array([row[1] for row in rows], dtype=float)
    if len(y) < 500:
        raise RuntimeError(f"Expected a substantial series; found only {len(y)} usable values")

    tail_values = []
    for row in range(rows[-1][2] + 1, source_ws.max_row + 1):
        if source_ws.cell(row, 2).value is None and isinstance(source_ws.cell(row, 3).value, (int, float)):
            tail_values.append(float(source_ws.cell(row, 3).value))
    tail_diffs = np.diff(tail_values) if len(tail_values) > 1 else np.array([])
    tail_is_linear = bool(len(tail_diffs) and np.max(np.abs(tail_diffs - tail_diffs[0])) < 1e-8)

    train_end = int(len(y) * 0.80)
    train = y[:train_end]
    fixed_alpha = 2.0 / 21.0
    optimized_alpha = optimize_ses(train)
    holt_alpha, holt_beta = optimize_holt(train)

    forecasts = {
        "Naive": np.concatenate(([np.nan], y[:-1])),
        "MA(5)": moving_average_forecasts(y, 5),
        "MA(20)": moving_average_forecasts(y, 20),
        "MA(60)": moving_average_forecasts(y, 60),
        "MA(200)": moving_average_forecasts(y, 200),
    }
    forecasts[f"SES fixed (alpha={fixed_alpha:.4f})"], fixed_next = ses_forecasts(y, fixed_alpha)
    forecasts[f"SES optimized (alpha={optimized_alpha:.3f})"], optimized_next = ses_forecasts(y, optimized_alpha)
    forecasts[f"Holt trend (alpha={holt_alpha:.3f}, beta={holt_beta:.3f})"], holt_next = holt_forecasts(y, holt_alpha, holt_beta)

    holdout_indices = np.arange(max(train_end, 200), len(y), dtype=int)
    method_results = {name: metrics(y, values, holdout_indices) for name, values in forecasts.items()}
    best_method = min(method_results, key=lambda name: method_results[name]["rmse"])
    naive_rmse = method_results["Naive"]["rmse"]
    best_rmse = method_results[best_method]["rmse"]
    improvement = (naive_rmse - best_rmse) / naive_rmse
    if best_method == "Naive" or improvement <= 0:
        conclusion = "No tested method beat the naive one-step persistence baseline on holdout RMSE. The defensible result is baseline performance, not a market-prediction claim."
    else:
        conclusion = (
            f"{best_method} produced the lowest holdout RMSE, {improvement:.1%} below naive persistence. "
            "This is a workbook-specific one-step result and is not evidence of a durable trading or market-prediction edge."
        )

    ma20 = forecasts["MA(20)"]
    rolling_sd = np.full(len(y), np.nan)
    for t in range(20, len(y)):
        rolling_sd[t] = float(np.std(y[t - 20:t], ddof=0))
    actual_holdout = y[holdout_indices]
    mean_holdout = ma20[holdout_indices]
    sd_holdout = rolling_sd[holdout_indices]
    coverage = {
        "2_sigma": float(np.mean((actual_holdout >= mean_holdout - 2 * sd_holdout) & (actual_holdout <= mean_holdout + 2 * sd_holdout))),
        "3_sigma": float(np.mean((actual_holdout >= mean_holdout - 3 * sd_holdout) & (actual_holdout <= mean_holdout + 3 * sd_holdout))),
    }

    next_forecasts = {
        "Naive": float(y[-1]),
        "MA(5)": float(np.mean(y[-5:])),
        "MA(20)": float(np.mean(y[-20:])),
        "MA(60)": float(np.mean(y[-60:])),
        "MA(200)": float(np.mean(y[-200:])),
        f"SES fixed (alpha={fixed_alpha:.4f})": float(fixed_next),
        f"SES optimized (alpha={optimized_alpha:.3f})": float(optimized_next),
        f"Holt trend (alpha={holt_alpha:.3f}, beta={holt_beta:.3f})": float(holt_next),
    }

    formula_audit = [
        ("Naive formula", f"D5 = {source_ws['D5'].value}; correctly shifts the prior observation"),
        ("MA(5) formula", f"E8 = {source_ws['E8'].value}; includes C8, the target row, causing look-ahead bias"),
        ("MA(20) formula", f"F24 = {source_ws['F24'].value}; uses the prior 20 observations and is correctly aligned"),
        ("MA(60) formula", f"G64 = {source_ws['G64'].value}; includes C64 and 61 values, causing look-ahead/misalignment"),
        ("MA(200) formula", f"H204 = {source_ws['H204'].value}; includes C204 and 201 values, causing look-ahead/misalignment"),
        ("SES formula", f"P5 = {source_ws['P5'].value}; one-step recursion is correctly aligned"),
    ]

    results = {
        "generated": date.today().isoformat(),
        "source_workbook": SOURCE.name,
        "output_workbook": OUTPUT.name,
        "conclusion": conclusion,
        "best_method": best_method,
        "best_rmse_improvement_vs_naive": improvement,
        "data_audit": {
            "usable_observations": int(len(y)),
            "source_rows": f"4-{rows[-1][2]}",
            "first_value": float(y[0]),
            "last_value": float(y[-1]),
            "excluded_tail_rows": int(len(tail_values)),
            "excluded_tail_linear": tail_is_linear,
            "calendar_dates_present": False,
            "instrument_source_verified": False,
        },
        "methodology": {
            "split": "First 80% training / final 20% holdout",
            "training_observations": int(train_end),
            "holdout_observations": int(len(holdout_indices)),
            "holdout_first_observation": int(observations[holdout_indices[0]]),
            "holdout_last_observation": int(observations[holdout_indices[-1]]),
            "parameter_selection": "Training partition only",
            "forecast_protocol": "Rolling one-step-ahead with prior actuals only",
        },
        "methods": method_results,
        "band_coverage": coverage,
        "next_observation_forecasts": next_forecasts,
        "original_formula_audit": dict(formula_audit),
    }

    # Remove only charts from the evaluated copy; the source file remains unchanged.
    source_ws._charts = []
    write_evaluation_sheet(wb, results, formula_audit, next_forecasts, coverage)
    write_clean_forecasts_sheet(wb, observations, y, forecasts, train_end)
    write_app_scope_sheet(wb)
    wb.save(OUTPUT)

    RESULTS_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")
    lines = [
        "# S&P 500 Workbook Forecast Evaluation",
        "",
        f"**Generated:** {results['generated']}",
        f"**Source:** `{SOURCE.name}` (preserved unchanged)",
        f"**Evaluated copy:** `{OUTPUT.name}`",
        "",
        "## Bottom line",
        "",
        conclusion,
        "",
        "## Clean holdout comparison",
        "",
        "| Method | MAE | RMSE | Directional accuracy | RMSE vs. naive |",
        "|---|---:|---:|---:|---:|",
    ]
    sorted_methods = sorted(method_results.items(), key=lambda item: item[1]["rmse"])
    for name, values in sorted_methods:
        delta = (naive_rmse - values["rmse"]) / naive_rmse
        lines.append(f"| {name} | {values['mae']:.4f} | {values['rmse']:.4f} | {values['directional_accuracy']:.1%} | {delta:+.1%} |")
    lines.extend([
        "",
        "## Data-quality findings",
        "",
        f"- Used {len(y):,} contiguous observations from source rows 4–{rows[-1][2]}.",
        f"- Excluded {len(tail_values):,} undated tail values. Constant consecutive differences: {tail_is_linear}.",
        "- The workbook does not identify the market symbol, source, adjusted-price convention, or calendar dates.",
        "- Original MA(5), MA(60), and MA(200) formulas include their target row; clean calculations use strictly earlier observations.",
        "- Seasonal Holt-Winters was not scored because the source lacks dates, verified frequency, and a defensible seasonal period.",
        "",
        "## Interpretation",
        "",
        "This is a forecasting-method evaluation, not investment advice. A useful app should emphasize backtesting, uncertainty, and data provenance rather than promise market prediction.",
    ])
    RESULTS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "output": str(OUTPUT),
        "results": str(RESULTS_JSON),
        "summary": str(RESULTS_MD),
        "best_method": best_method,
        "rmse_improvement_vs_naive": improvement,
        "usable_observations": len(y),
        "excluded_tail_rows": len(tail_values),
    }, indent=2))


if __name__ == "__main__":
    main()
