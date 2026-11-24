# Dispatch Ledger

Compare Halifax police service demand by agency, reporting channel and period. [Open the tool](https://coolcode.ca/dispatchledger/).

<!-- coolcode:guide -->
Compare public-generated calls, proactive calls and online reports from January through June in two years. Switch between regional police, the RCMP Halifax Regional Detachment and the published combined figures. The district table counts recorded crime in 2025 and uses a different unit from the service table.
<!-- /coolcode:guide -->

## Sources and interpretation

Figure 1 compares public-generated calls, officer proactive calls and online reports. The combined online line differs from the sum of the two published agency lines in both years. This tool retains those figures as printed. Figures 15 and 16 provide a geographic breakdown of crime only. Call priority and calls by patrol area are unavailable in these tables.

The collector reads Figure 1 and Figures 15–16 of the September 3, 2025 Board of Police Commissioners report. Each run reads the reviewed document from Halifax, verifies the agency labels, checks published changes and validates the district subtotals. The schedule rechecks that report. Adding another board edition requires reviewing its tables. A future data request could ask Halifax for monthly counts by service, patrol division, priority at dispatch and status with definitions, suppression rules and no incident identifiers.

[Board report · Figures 1, 15 and 16](https://www.halifax.ca/media/91695). 

## Data and maintenance

The page reports the retrieval date in UTC separately from the periods of observation. The offline build uses the last validated snapshot committed in `web/data/edition.json`. The monthly Actions workflow also supports manual runs. A failed refresh exits before replacing the published edition. All filtering runs in the browser. The page downloads the edition from CoolCode and stores no selections.

Run `python3 scripts/refresh.py` to rebuild the data from source. Install Poppler for pdftotext first.

Run `node --test tests/*.test.mjs`, `python3 -m unittest discover -s tests` and `python3 scripts/build.py`. Serve the generated `dist/` directory to preview. The Pages workflow tests desktop and mobile browser views before deployment.

<!-- schedule-reliability -->
## Schedule reliability

Public GitHub repositories can have scheduled workflows disabled after 60 days of inactivity. A separate weekly [schedule guard](.github/workflows/schedule-guard.yml) calls GitHub's enable-workflow API for an explicit list of refresh workflows and itself. It can restore workflows disabled for inactivity, preserves manually disabled workflows, and runs independently of collection failures.

This is an interim mitigation, not a scheduling guarantee: GitHub does not document active-workflow renewal as a permanent exemption, and scheduled runs can be delayed or dropped. A scheduler on our own Linux server is the planned independent trigger. The guard does not collect data, create dummy commits, or change source/check timestamps; successful collection and published data freshness still need monitoring.
<!-- /schedule-reliability -->
