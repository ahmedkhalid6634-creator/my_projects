# Mostaql Data Extraction — Streamlit Training Project

A mock/training project built to learn the fundamentals of **Streamlit**, structured around a real use case: scraping job listings from [Mostaql](https://mostaql.com) (an Arabic freelance marketplace), refining the raw data, and visualizing it through an interactive dashboard.

> This project is primarily a learning exercise in Streamlit fundamentals — session state, fragments, forms, and building interactive dashboards — using web scraping as the practical vehicle to generate real data to work with.

---

## Project Structure

| File | Role |
|---|---|
| `Jobs_Mostaql.py` | **Scraper (backend).** Uses Playwright (via `patchright` + `playwright-stealth`) to asynchronously scrape job listings from Mostaql — title, description, budget, status, posted date, client name, acceptance rating, skill sets, proposal counts, and more. Paginates through all result pages and scrapes listing details concurrently (bounded by a semaphore) for each job's detail page. Returns a raw `pandas.DataFrame`. |
| `Mostaql_data_refinement.py` | **Data refinement layer.** Cleans and transforms the raw scraped data: strips hidden/invisible Unicode characters, parses budget ranges into numeric min/max columns, normalizes Arabic proposal-count text into numbers, converts dates/times, fills missing values, and derives new columns (`Average Budget`, `Fin. Urgency`). Also separates out URLs, descriptions, and skill sets/badges for use in the UI. |
| `scraping_app.py` | **Frontend (Streamlit UI).** Ties the scraper and refinement layer together into an interactive web app — a search bar to trigger scraping, a scrape/cancel control, and a dashboard with sortable data tables (by payment, acceptance rate, recency, financial urgency) plus Plotly visualizations (line charts, bar charts, heatmaps). |

---

## Frameworks & Libraries Used

- 🐍 **Python**
- ⛵ **Streamlit** — UI framework
- 🐼 **Pandas** — data processing
- 🎭 **Playwright** (`patchright` + `playwright-stealth`) — browser automation / scraping
- 📊 **Plotly** — data visualization

---

## How It Works

1. User enters an optional search term and clicks **SCRAPE**.
2. The scraper launches a headless Chromium browser, navigates Mostaql's project listings, and paginates through all available pages.
3. For each listing, a detail page is opened (up to 5 concurrent detail scrapes via `asyncio.Semaphore`) to pull in deeper info (budget, description, status, skills, etc.).
4. The raw scraped DataFrame is passed through the refinement module to produce a clean, analysis-ready dataset.
5. The Streamlit UI unlocks a dashboard: sortable/selectable data tables and visual analytics (line charts for job volume over time, bar charts for financial urgency and skill frequency, heatmaps for skill/proposal correlation).

---

## Known Issues & Limitations

This project surfaced some real architectural challenges — documented here rather than hidden, since they were the main learning outcome of the project.

### 1. Scrape cancellation doesn't work reliably
The intended behavior is for the **CANCEL** button in the UI to stop an in-progress scrape. In practice, this doesn't work as expected:
- The scraper runs on a background `threading.Thread` (with the async Playwright event loop inside it), while the Streamlit UI runs on the main thread/process.
- Because there's no real communication layer (API) between the scraping backend and the Streamlit frontend, the two can't reliably talk to each other mid-execution — the cancel signal (a `threading.Event`) doesn't reach the scraper in time to interrupt work already in flight (e.g. an in-progress `page.goto()` or paginated loop).
- Using threads was an attempt to make this controllable, but it turned out to be the wrong tool for the job here — a thread can carry a flag, but it can't be *forced* to stop, and cooperative checks weren't sufficient given how the scraping loop is structured (async tasks running under `asyncio.gather`, blocking Playwright calls, etc).

**Root cause, in short:** the scraper (backend) and the UI (frontend) are tightly coupled inside the same process via threading, instead of being decoupled, independently-running components that communicate through a proper interface (e.g. a REST API). Without that separation, there's no clean way to signal, monitor, or interrupt a long-running scrape (which can take 40–90+ minutes) from the UI.

### 2. Scraper doesn't consistently deliver expected results when run through the app
Related to the above — running `Jobs_Mostaql.py` as a standalone script works reliably. Running it *through* the Streamlit app (threaded) does not consistently deliver the same outcome. This points to the same underlying issue: mixing a long-running async Playwright job with Streamlit's rerun-based execution model via raw threading is fragile.

---

## What I'd Do Differently / Next Steps

- **Decouple the scraper from the UI entirely.** Run the scraper as an independent process/service, and have the Streamlit app communicate with it through a lightweight API (e.g. Flask/FastAPI) — polling for status/progress/results instead of directly threading the scraping function into the UI process.
- **Implement proper cancellation** via a shared status endpoint that the scraper checks between checkpoints (e.g. between pages/listings), rather than relying on an in-process thread flag.
- **Learn more about APIs**, since the lack of familiarity with this was the main blocker for building the decoupled architecture above.
- **Evolve this from a mock project into something more purposeful** — the long-term idea is to turn this into a tool that actually helps freelancers evaluate and choose the best jobs available (e.g. by financial urgency, acceptance likelihood, skill match) rather than just being a scraping/visualization demo.

---

## Disclaimer

This is a training/learning project. It was built to practice Streamlit, async web scraping with Playwright, and data wrangling with Pandas — not as a production tool. Scraping any website should respect that site's Terms of Service and `robots.txt`.

For more projects, see: https://github.com/ahmedkhalid6634-creator/my_projects
