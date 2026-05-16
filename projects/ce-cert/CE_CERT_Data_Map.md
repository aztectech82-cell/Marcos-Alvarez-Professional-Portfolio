# CE-CERT Data Map (OneDrive → AI-TOOL)

**Source folder:** `C:\Users\aztec\OneDrive\CE-CERT`

The CE-CERT folder now has an explicit ingestion path so it can feed the automation stack and the CE-CERT business offers outlined in `CE-CERT-addendum.md`.

## What to capture
- Lab reliability/maintenance analytics
- Lab curricula and experiment walkthroughs
- KPI definitions and measurement frameworks
- Safety/compliance modules and checklists
- Career/portfolio materials from CE-CERT projects

## How to make it actionable
1. **Surface changes nightly:** Run `python automation/daily_onedrive_summary.py` so new/modified files in `OneDrive\CE-CERT` appear in `OneDrive\AI-TOOL\Morning-Briefs\work-summary-YYYY-MM-DD.md`.
2. **Auto-tag goals/projects:** The auto goal tracker (`automation/auto_goal_tracker.py`) already scans OneDrive. Keep the `CE-CERT` folder name intact so activity is tagged to CE-CERT initiatives and shows up in the morning briefing.
3. **Convert to offers:**
   - Reliability analytics → `projects/vdhatta-business/COMPREHENSIVE_BUSINESS_PLAN_2025-12-26.md` (consulting & SaaS light KPIs).
   - Compliance modules → Pair with tax/legal checklists from `tax-planning/` when you build bundles.
   - Career materials → Feed into the career track in `CE-CERT-addendum.md` and future Creator School assets.
4. **Drop-in processing (if unsure):** Add files to `OneDrive\1_Summary\Input-Dump\` with `CE-CERT` in the filename/folder. `automation/auto_goal_tracker.py` will pick them up even if you are not inside the CE-CERT folder.

## Quick checklist
- [ ] Verify `C:\Users\aztec\OneDrive\CE-CERT` exists and is syncing.
- [ ] Place any new PDFs/notes/spreadsheets there (or in Input-Dump with `CE-CERT` in the name).
- [ ] Run `TEST_AUTOMATION.bat` to confirm OneDrive scan + morning brief still pass.
- [ ] Review the next morning’s `work-summary-YYYY-MM-DD.md` to confirm CE-CERT items are listed.
- [ ] Move summarized insights into the CE-CERT offers in `CE-CERT-addendum.md` as you process them.
