# Open the one-page Power BI report

1. Extract the complete project ZIP. In `powerbi/`, double-click **`Unicorn_Market_Intelligence.pbip`**.
2. The semantic model references the **four public source CSV files** using `Web.Contents`. On first refresh, select **Anonymous** access to `raw.githubusercontent.com` if prompted. Internet is required for the first refresh.
3. Verify the all-country and all-industry default context: **732 new unicorns (2019–2021)**, **400 in the top three**, **54.6% top-three share**. The native Power BI version and the separate HTML visual don't use identical layout components.
4. Use **File → Save As → Power BI file (.pbix)** after the data source refresh succeeds. Check the two main charts and the Continent / Industry slicers.
5. Export a real screenshot from Desktop only after checking the layout. The existing `charts/LinkedIn_Dashboard_Preview.png` is a *standalone data-driven design preview*, NOT a screenshot from Power BI Desktop.

**Why only one page?** Executive visual storytelling works better for LinkedIn and a recruiter-first portfolio. The SQL, Python notebook, source caveats and quality checks supply technical depth without extra report tabs.

**If your installed Desktop build rejects PBIP:** The intended query logic and visuals are documented in `dax_measures.dax` and `power_bi_theme.json`. Some installations require enabling PBIP in Options > Preview features. This source project has been generated and structurally checked, not runtime-tested on Windows.

**Important interpretation:** Valuations are historical *snapshot* attributes. `Year_Joined` is the date cohort, not the date when the snapshot valuation was observed. No financial-return claim is implied.
