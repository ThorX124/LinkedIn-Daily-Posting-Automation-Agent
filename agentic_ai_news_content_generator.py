#!/usr/bin/env python3
"""
Agentic AI News-Based Content Generator
Creates LinkedIn posts based on daily Agentic AI news
"""

import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).parent
NEWS_CACHE = SCRIPT_DIR / "daily_news_cache.json"


def fetch_daily_news():
    """Run news fetcher to get today's news"""
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "news_fetcher.py")],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )

        # Parse the news data from the JSON in the output
        output = result.stdout

        # Extract JSON between markers if present
        if "===NEWS_FETCH_COMPLETE===" in output:
            json_part = output.split("===NEWS_FETCH_COMPLETE===")[1].split("===NEWS_END===")[0].strip()
            return json.loads(json_part)

        # Otherwise try to load from cache
        if NEWS_CACHE.exists():
            with open(NEWS_CACHE, 'r', encoding='utf-8') as f:
                return json.load(f)

    except Exception as e:
        print(f"[ERROR] Could not fetch news: {e}")

    return None


def generate_news_digest_post(news_data):
    """Generate a LinkedIn post from daily news"""
    if not news_data or 'news_items' not in news_data:
        # Fallback to generic content
        return generate_fallback_post()

    date_info = datetime.now()
    date_str = date_info.strftime("%B %d, %Y")
    day_name = date_info.strftime("%A")

    news_items = news_data['news_items']
    trending = news_data.get('trending_topic', 'Agentic AI')

    # Build the post
    lines = []
    lines.append(f"📰 Agentic AI Daily Digest - {date_str}")
    lines.append("")
    lines.append("🔥 Today's top stories:")
    lines.append("")

    # Add emoji indicators for different categories
    category_emojis = {
        "Product Launch": "🚀",
        "Framework": "🛠️",
        "Enterprise": "🏢",
        "Research": "🔬",
        "Developer Tools": "💻",
        "Open Source": "📂",
        "Robotics": "🤖",
        "Platform": "🌐",
        "Funding": "💰",
        "Legal Tech": "⚖️",
        "Development": "⚡",
        "CRM": "📊",
        "Content": "📝",
        "Automation": "⚙️",
        "Collaboration": "🤝",
        "Research": "🔍"
    }

    source_links = []
    for i, item in enumerate(news_items[:3], 1):
        emoji = category_emojis.get(item.get('category', ''), '✨')
        lines.append(f"{i}. {emoji} {item['headline']}")
        lines.append(f"   {item['summary']}")
        if item.get('url'):
            source_links.append(f"   🔗 {item['headline']}: {item['url']}")
        lines.append("")

    # Add source links
    if source_links:
        lines.append("🔗 Sources:")
        lines.extend(source_links)
        lines.append("")

    # Add trending topic
    lines.append(f"📈 Trending: {trending}")
    lines.append("")

    # Add insights/commentary
    lines.append("💡 Key Takeaway:")
    lines.append(f"Agentic AI is rapidly evolving with {len(news_items)} major updates today.")
    lines.append("From autonomous coding to enterprise deployment, the landscape is shifting.")
    lines.append("")

    # Add engagement question
    engagement_questions = [
        "Which development are you most excited about?",
        "How are you using Agentic AI in your work?",
        "What agentic capability do you need most?",
        "Are you building with agents yet?",
        "What's your biggest AI agent use case?"
    ]
    lines.append(f"🤔 {engagement_questions[date_info.day % len(engagement_questions)]}")
    lines.append("")

    # Add hashtags
    hashtags = "#AgenticAI #AI #ArtificialIntelligence #AIAgents #Automation #TechNews #Innovation #FutureOfWork"
    lines.append(hashtags)

    return "\n".join(lines)


def generate_single_story_post(news_data):
    """Generate a post focused on the top story"""
    if not news_data or 'news_items' not in news_data:
        return generate_fallback_post()

    date_info = datetime.now()
    date_str = date_info.strftime("%B %d, %Y")

    top_story = news_data['news_items'][0]
    trending = news_data.get('trending_topic', 'Agentic AI')

    lines = []
    lines.append(f"🚀 Breaking: {top_story['headline']}")
    lines.append("")
    lines.append(f"📅 {date_str}")
    lines.append("")
    lines.append(top_story['summary'])
    lines.append("")
    lines.append("🔍 Why this matters:")
    lines.append(f"This represents a significant step forward in {trending.lower()}.")
    lines.append("The ability to autonomously execute tasks is transforming industries.")
    lines.append("")
    lines.append("💬 What do you think about this development?")
    lines.append("")
    lines.append(f"📰 Source: {top_story.get('source', 'Industry News')}")
    if top_story.get('url'):
        lines.append(f"🔗 Read more: {top_story['url']}")
    lines.append("")
    lines.append("#AgenticAI #AI #Innovation #TechNews #Automation #FutureOfWork")

    return "\n".join(lines)


def generate_insights_post(news_data):
    """Generate an insights/analysis post based on trends"""
    if not news_data or 'news_items' not in news_data:
        return generate_fallback_post()

    date_info = datetime.now()
    date_str = date_info.strftime("%B %d, %Y")
    trending = news_data.get('trending_topic', 'Agentic AI')

    # Get all categories from today's news
    categories = [item.get('category', 'General') for item in news_data['news_items']]
    category_text = ", ".join(set(categories))

    lines = []
    lines.append(f"💡 Agentic AI Market Insights - {date_str}")
    lines.append("")
    lines.append(f"📊 Today's focus: {trending}")
    lines.append("")
    lines.append("Key developments across the ecosystem:")
    lines.append("")

    source_links = []
    for item in news_data['news_items']:
        emoji = "✅" if "Launch" in item.get('category', '') else "🔹"
        lines.append(f"{emoji} {item['headline']}")
        if item.get('url'):
            source_links.append(f"🔗 {item['headline']}: {item['url']}")

    lines.append("")
    if source_links:
        lines.append("📚 Sources:")
        lines.extend(source_links)
        lines.append("")

    lines.append("🎯 The Big Picture:")
    lines.append(f"Activity in {category_text} shows the market maturing rapidly.")
    lines.append("Enterprise adoption is accelerating as trust in autonomous systems grows.")
    lines.append("")
    lines.append("⚡ What's next?")
    lines.append("Watch for multi-agent orchestration and safety frameworks.")
    lines.append("")
    lines.append("#AgenticAI #MarketTrends #AI #Innovation #EnterpriseAI")

    return "\n".join(lines)


def generate_fallback_post():
    """Generate a generic post if news fetch fails"""
    date_info = datetime.now()
    date_str = date_info.strftime("%B %d, %Y")

    return f"""📰 Agentic AI Update - {date_str}

The agentic AI landscape continues to evolve rapidly:

✅ New frameworks emerging weekly
✅ Enterprise adoption accelerating
✅ Safety and alignment improving
✅ Tool integration expanding

The shift toward autonomous AI systems is transforming how we work.

What agentic AI tools are you exploring?

#AgenticAI #AI #Innovation #FutureOfWork"""


def select_post_format(day_of_month):
    """Select which post format to use based on day"""
    # Rotate through different formats
    formats = [
        generate_news_digest_post,      # Day 1, 4, 7, 10...
        generate_single_story_post,     # Day 2, 5, 8, 11...
        generate_insights_post,         # Day 3, 6, 9, 12...
    ]
    return formats[(day_of_month - 1) % len(formats)]


def save_generated_post(post_content):
    """Save the generated post for reference"""
    try:
        content_db = SCRIPT_DIR / "generated_posts.json"
        posts = []

        if content_db.exists():
            with open(content_db, 'r', encoding='utf-8') as f:
                posts = json.load(f)

        posts.append({
            "date": datetime.now().isoformat(),
            "content": post_content
        })

        # Keep only last 30 posts
        posts = posts[-30:]

        with open(content_db, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2)
    except:
        pass


def main():
    print("=" * 60)
    print("AGENTIC AI NEWS CONTENT GENERATOR")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    # Step 1: Fetch daily news
    print("[*] Fetching daily Agentic AI news...")
    news_data = fetch_daily_news()

    if news_data:
        print("[OK] News fetched successfully!")
        print(f"    - {len(news_data.get('news_items', []))} stories")
        print(f"    - Trending: {news_data.get('trending_topic', 'N/A')}")
    else:
        print("[!] Using fallback content")
    print()

    # Step 2: Select post format based on day
    day = datetime.now().day
    post_format = select_post_format(day)
    print(f"[*] Using post format: {post_format.__name__.replace('generate_', '')}")
    print()

    # Step 3: Generate the post
    print("[*] Generating LinkedIn post...")
    post = post_format(news_data)

    print("[OK] Post generated!")
    print()

    # Display the post
    print("=" * 60)
    print("GENERATED POST:")
    print("=" * 60)
    print(post)
    print("=" * 60)
    print()

    # Save for reference
    save_generated_post(post)

    return post


if __name__ == '__main__':
    post = main()
    print("\n===POST_CONTENT_START===")
    print(post)
    print("===POST_CONTENT_END===")
