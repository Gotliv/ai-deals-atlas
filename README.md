# AI-Deals | AI ATLAS

Mapping the landscape of the AI economy: deals, partnerships, investments, compute, manufacturing and financing.

An interactive company network with English company names, locally cached logos, Hebrew deal explanations and proper right-to-left layout. Research snapshot: **6 November 2026**.

[Open the interactive map](https://gotliv.github.io/ai-deals-atlas/) · [Source repository](https://github.com/Gotliv/ai-deals-atlas)

## Explore

- Click a company to highlight its connections and read its agreements.
- Hover over a company or an edge for a summary. Click an edge for complete Hebrew details and source links.
- Filter by relationship type, announcement year or search text. Switch between the full ecosystem and exactly 14 tech-review companies: Amazon, Google, Meta, Microsoft, Apple, NVIDIA, TSMC, Applied Materials, SpaceX, Tesla, OpenAI, Anthropic, Intel and Oracle. The review view only includes relationships whose two endpoints belong to that list.
- Open the deal ledger for every record. Export filtered CSV, the full JSON dataset, or the requested-company coverage matrix.
- Share a URL preserving the chosen company, agreement and filters.
- Use the visible dark/light buttons at the top. Your choice is saved locally.
- Historical, cancelled and superseded records are hidden by default. The history control includes them.

## Research and limitations

The dataset includes 217 documented records, 71 companies/entities and 199 distinct sources at initial publication. This is a reviewed collection of public records, **not a guarantee of every agreement or confidential contract**. A missing edge is not evidence that no relationship exists.

Most records use primary sources; two separately labelled media-reported connections use Reuters and the Financial Times. The sources tab distinguishes these tiers.

Each record includes the announcement or disclosure date, a source-supported status, a Hebrew summary, amount qualification, transaction direction and sources. Where an announcement date differs from the original contract date, the disclosure basis is explained. Dates disclosed only to month precision stay month-only.

Equity, compute purchases, contingent guarantees, credit facilities, warrants, joint ventures and nonbinding plans are distinct. A funding-round total is never assigned to every participant. Unknown individual checks stay null. Do not sum the displayed figures: several are cumulative or overlap, and guarantees are not cash investments. Indirect SPV relationships are marked in the detail panel. Bubble sizes use sourced public market capitalizations and disclosed private valuations. Dates and source links appear in each company card. Radius is sqrt(26² + (value / maximum value) × (100² - 26²)), with a minimum footprint for readability, so visible areas are not exact value ratios. Unknown valuations have a small dashed bubble. A private valuation is not a live market quote. Line width does not represent money.

Examples of corrections included: Microsoft’s €15 million Mistral convertible-bond investment, the April 2026 Microsoft/OpenAI amendment, current Anthropic compute obligations from the November 2026 S-1/A, contingent NVIDIA guarantees, and Tesla’s completed SpaceX investment.

This is a manually reviewed snapshot. Hosting or refreshing the page does not automatically research new deals. Update research and the cutoff before changing the displayed verification date. Sources can subsequently change or disappear.

## Run locally

No npm installation, paid API, server backend or external logo service is required at runtime. D3 7.9.0, the Hebrew font and brand assets are included locally.

```bash
python3 -m http.server 4173 --directory public
```

Open `http://localhost:4173/`. Do not open `index.html` through `file://`, because browsers restrict loading the JSON dataset from local files.

## Update research

1. Edit or add a reviewed array in `research/*.json`. Keep deal IDs stable.
2. Use the schema in `docs/DATA_SCHEMA.md`, include evidence for all amounts and distinguish source publication from announcement dates.
3. Add new company metadata to `scripts/build_data.py` and a local logo under `public/assets/logos/`.
4. Run the checks below and inspect the rendered Hebrew details.

```bash
python3 scripts/build_data.py
node --check public/app.js
python3 scripts/validate_data.py
```

GitHub Actions runs these checks on pushes and pull requests, and rejects stale generated data. `scripts/fetch_assets.py` is an optional asset-refresh helper that requires Pillow and network access; it is not used at runtime or in CI.

## Deploy

The `public/` directory is a complete static website. It can be hosted on GitHub Pages, Cloudflare Pages, Netlify or another static host, including under a repository subpath. The public repository Gotliv/ai-deals-atlas publishes the public/ folder through GitHub Actions on each main push. The workflow validates data and JavaScript before deploying. There is no expiring preview session or runtime dependency on ChatGPT.

The original private Gotliv/AI-Deals repository is preserved as a source mirror. The GitHub Pages repository is the public deployment destination.

## Structure

| Path | Purpose |
| --- | --- |
| `public/index.html` | Application shell and accessible controls |
| `public/app.js` | Graph, search, filters, Hebrew details and exports |
| `public/styles.css` | Responsive dark/light themes and RTL layout |
| `public/data/atlas.json` | Generated, portable research dataset |
| `research/` | Reviewed source records and research notes |
| `scripts/build_data.py` | Reproducible dataset compiler |
| `scripts/validate_data.py` | Provenance, date, endpoint and accounting checks |
| `public/vendor/` | Vendored D3 and third-party license notices |

Brand names and logos belong to their respective owners and are used for identification. Third-party software and font licenses are included separately.
