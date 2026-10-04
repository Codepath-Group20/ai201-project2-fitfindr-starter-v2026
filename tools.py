"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str
"""

import config  # noqa: F401
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.
    """
    listings = load_listings()
    filtered = []
    
    desc_words = set(description.lower().split())
    
    for item in listings:
        # 1. Price filter
        if max_price is not None:
            price = item.get("price")
            if price is None or price > max_price:
                continue
                
        # 2. Size filter (with robust token matching to avoid substring traps like "l" in "xl")
        if size is not None:
            item_size = str(item.get("size", "")).lower()
            target_size = size.lower()
            item_size_tokens = set(
                item_size.replace('/', ' ').replace(',', ' ').replace('-', ' ').split()
            )
            if target_size != item_size and target_size not in item_size_tokens:
                continue
                
        # 3. Keyword overlap scoring
        text_corpus = f"{item.get('title', '')} {item.get('description', '')} {item.get('category', '')} " + " ".join(item.get('style_tags', []))
        corpus_words = set(text_corpus.lower().split())
        
        score = len(desc_words.intersection(corpus_words))
        if score > 0:
            filtered.append((score, item))
            
    # Sort by score highest first
    filtered.sort(key=lambda x: x[0], reverse=True)
    
    limit = getattr(config, "SEARCH_RESULT_LIMIT", 5)
    return [item for score, item in filtered[:limit]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.
    """
    wardrobe_items = wardrobe.get("items", [])
    
    item_title = new_item.get("title", "this item")
    item_category = new_item.get("category", "clothing")
    item_price = new_item.get("price", "unknown price")
    item_platform = new_item.get("platform", "unknown platform")
    
    if not wardrobe_items:
        prompt = (
            f"The user is considering purchasing the following secondhand item:\n"
            f"- Title: {item_title}\n"
            f"- Category: {item_category}\n"
            f"- Price: ${item_price}\n"
            f"- Platform: {item_platform}\n\n"
            f"The user's wardrobe is currently empty. Provide general styling advice, "
            f"suggest what types of basic pieces or colors would pair well with this item, "
            f"and describe a couple of occasions where it would fit."
        )
    else:
        wardrobe_desc = "\n".join(
            [f"- {w.get('title', 'Item')} ({w.get('category', 'general')}, size {w.get('size', 'N/A')})" for w in wardrobe_items]
        )
        prompt = (
            f"The user is considering purchasing this secondhand item:\n"
            f"- Title: {item_title}\n"
            f"- Category: {item_category}\n"
            f"- Price: ${item_price}\n\n"
            f"The user already owns these items in their wardrobe:\n{wardrobe_desc}\n\n"
            f"Suggest one or two specific outfit combinations pairing the new item with pieces "
            f"from the user's wardrobe. Name the specific items they already own."
        )
        
    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.
    """
    if not outfit or not outfit.strip():
        return "Error: Unable to generate fit card because the outfit suggestion is empty."
        
    item_title = new_item.get("title", "this piece")
    item_price = new_item.get("price", "N/A")
    item_platform = new_item.get("platform", "secondhand")
    
    prompt = (
        f"Write a short, engaging 2-to-4 sentence social media caption or fit card for the following outfit find:\n"
        f"- Item: {item_title}\n"
        f"- Price: ${item_price}\n"
        f"- Platform: {item_platform}\n"
        f"- Outfit Details/Styling: {outfit}\n\n"
        f"Guidelines:\n"
        f"- Read like a real post, not a dry product description.\n"
        f"- Mention the item title, its price (${item_price}), and the platform ({item_platform}) exactly once.\n"
        f"- Be specific about the vibe."
    )
    
    return generate(prompt)
