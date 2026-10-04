# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> <pre><code>python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'</code></pre>
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

## What This Does

FitFindr is an AI-powered personal styling agent that bridges your personal wardrobe with secondhand marketplace listings. A user can ask natural-language styling or outfit-building queries (e.g., matching items they already own with new pieces to buy). The agent autonomously parses the intent, queries structured inventory databases using dedicated tools, executes a multi-step planning loop, and formats a final curated outfit recommendation.

---

## Tool Inventory

### `search_listings`

- **What it does:** Searches and filters the external secondhand marketplace catalog (`data/listings.json`) based on criteria like search text, maximum price, category, size, and style tags.
- **Inputs:** `query` (str), `max_price` (float), `category` (str), `size` (str), `style_tags` (list)
- **Returns:** A list of listing dictionaries, each containing `id` (str), `title` (str), `price` (float), `category` (str), `size` (str), `platform` (str), and `style_tags` (list).
- **When it has nothing:** Returns an empty list `[]`.

### `suggest_outfit`

- **What it does:** Generates one or two custom outfit combinations by taking a newly considered thrift item and matching it against the user's existing wardrobe items, or provides general styling and occasion advice if the wardrobe is empty.
- **Inputs:** `new_item` (dict), `wardrobe` (dict)
- **Returns:** A non-empty text string containing outfit combination ideas, styling notes, and rationale.
- **When it has nothing:** Returns a fallback text string with general styling and occasion guidance for the new item if the wardrobe items list is empty.

---

### `create_fit_card`

- **What it does:** Crafts a short, engaging 2-to-4 sentence social media caption or "fit card" for a specific curated outfit find, highlighting the item title, price, platform, and overall vibe.
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** A descriptive string representing the styled social media caption.
- **When it has nothing:** Returns an explicit error/fallback message string indicating that the outfit suggestion input was empty or whitespace.

---

## Sample Run

<pre><code>(.venv) [leo@precision ai201-project2-fitfindr-starter-v2026]$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]</code></pre>

<pre><code>(.venv) [leo@precision ai201-project2-fitfindr-starter-v2026]$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Here are two versatile outfit combinations you can create using your existing wardrobe items paired with the Vintage Levi's 501 Jeans:

**Outfit 1: Casual & Classic**
* **Bottoms:** Vintage Levi's 501 Jeans ($38)
* **Top:** Item (tops, size N/A)
* **Outerwear:** Item (outerwear, size N/A)
* **Shoes:** Item (shoes, size N/A)
* **Accessories:** Item (accessories, size N/A)
* *Why it works:* The medium-wash Levi's 501s serve as the ultimate timeless base. Pairing them with your everyday top and layering with your outerwear creates an effortless, well-balanced look that works for almost any casual day out. Complete the outfit with your go-to shoes and accessory.

**Outfit 2: Elevated Everyday**
* **Bottoms:** Vintage Levi's 501 Jeans ($38)
* **Top:** Item (tops, size N/A)
* **Shoes:** Item (shoes, size N/A)
* **Accessories:** Item (accessories, size N/A)
* *Why it works:* Vintage 501s have a great structured fit that can easily be dressed up. Tucking in your second top creates a defined silhouette, while your second pair of shoes and accessory add a polished finish to the vintage wash.</code></pre>

<pre><code>(.venv) [leo@precision ai201-project2-fitfindr-starter-v2026]$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Every closet needs that *one* perfect pair of worn-in denim, and these Vintage Levi's 501 Jeans in a timeless medium wash are the ultimate holy grail. Just toss them on with some fresh white sneakers for that effortlessly cool, off-duty model aesthetic. Grab this absolute steal for only $38.0 over on depop before I change my mind and keep them!</code></pre>

