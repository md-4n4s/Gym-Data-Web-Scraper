# Fitness Club Scraper

A small Python script that crawls the [Titan Fitness Club website](https://titan-fitness-club-website.vercel.app/), downloads every image it finds, and extracts subscription plan pricing from the site's `Plan.html` page.

## What it does

1. Fetches the homepage and collects every link (`<a href="...">`) found on it.
2. Visits each of those linked pages.
3. On every page visited, collects all `<img>` tags and downloads the images into a local `images/` folder.
4. If the page is `Plan.html`, it looks for elements with the class `box` (assumed to represent a subscription plan), and for each one:
   - Reads the plan name from an `<h1>` (or `<h2>` if no `<h1>` is present).
   - Reads the price from the plan's `<button>` text, stripping everything except digits and `$`.
5. Prints a dictionary of `{plan_name: price}` to the console.
6. Saves all downloaded images to `./images/`.

## Requirements

- Python 3.7+
- Packages:
  - `requests`
  - `beautifulsoup4`

Install dependencies:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the script directly:

```bash
python scraper.py
```

Output:
- Console: a dictionary of subscription plan names and prices, e.g.
  ```
  Available Subscriptions:
  {'Basic': '$29', 'Premium': '$59', 'Elite': '$99'}
  ```
- Disk: an `images/` folder (created if it doesn't exist) containing every image downloaded from the crawled pages.

## How it works (code walkthrough)

| Step | Code | Purpose |
|---|---|---|
| Fetch homepage | `requests.get(url, ...)` | Downloads the site's HTML |
| Parse HTML | `BeautifulSoup(response.text, "html.parser")` | Enables tag/element searching |
| Collect links | `soup.find_all("a")` → `pages` set | Builds the list of pages to crawl |
| Crawl each page | `urljoin(url, page)` | Resolves relative links to absolute URLs |
| Collect images | `soup.find_all("img")` → `img_urls` set | Gathers every image URL site-wide |
| Extract plans | `soup.find_all(class_="box")` on `Plan.html` | Locates subscription plan blocks |
| Clean price | `re.sub(r"[^\d$]", "", ...)` | Strips non-numeric/non-`$` characters from price text |
| Download images | Loop over `img_urls`, write bytes to file | Saves each image locally |
