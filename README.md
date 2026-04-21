# Agentic AI LinkedIn Poster

Daily news-based LinkedIn posting automation for Agentic AI content.

## How It Works

1. **Fetch News** - Gets daily Agentic AI news from curated sources
2. **Generate Content** - Creates LinkedIn posts based on the news
3. **Post to LinkedIn** - Automatically publishes using saved browser session

## Files

| File | Purpose |
|------|---------|
| `daily_fresh_poster.py` | Main script - orchestrates the workflow |
| `news_fetcher.py` | Fetches daily Agentic AI news |
| `agentic_ai_news_content_generator.py` | Creates LinkedIn posts from news |
| `autonomous_linkedin_poster.py` | Handles LinkedIn posting via Playwright |

## Usage

### Run with preview (manual confirmation):
```bash
python daily_fresh_poster.py
```

### Run auto-post (no confirmation):
```bash
python daily_fresh_poster.py --auto
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up LinkedIn session (run once):
```bash
python autonomous_linkedin_poster.py --login
```

## Data Files

- `daily_news_cache.json` - Today's fetched news
- `generated_posts.json` - Log of generated posts
- `autonomous_posting_log.json` - Log of published posts
- `linkedin_cookies_playwright.json` - Saved LinkedIn session
- `chrome_profile/` - Browser profile data
- `debug_screenshots/` - Posting verification screenshots

## Post Rotation

Posts rotate daily between 3 formats:
- **News Digest** - Summary of 3 top stories
- **Single Story** - Deep dive on top headline
- **Insights** - Analysis of market trends
