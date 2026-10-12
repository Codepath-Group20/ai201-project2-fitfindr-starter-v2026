# FitFindr

## What This Does
FitFindr is an AI-powered fashion assistant agent that takes a user's natural language style query (including desired items, size constraints, and price ceilings) alongside a digital wardrobe. It searches clothing listings across platforms, selects a matching piece, generates personalized outfit combinations using the user's existing wardrobe items, and produces an engaging, persuasive "fit card" summarizing the look. If no items match the user's criteria, the agent halts early and provides actionable guidance on how to adjust the search parameters.

---

## Tool Inventory

* **`search_listings(description: str, size: str = None, max_price: float = None)`**
  * **Inputs:** `description` (string keywords), `size` (optional string), `max_price` (optional float).
  * **Returns:** A list of matching listing dictionaries from the catalog.
  * **On Empty:** Returns an empty list (`[]`) if no listings match the criteria.

* **`suggest_outfit(listing: dict, wardrobe: dict)`**
  * **Inputs:** `listing` (dictionary of the selected clothing item), `wardrobe` (dictionary representing the user's closet).
  * **Returns:** A formatted string containing two distinct outfit combinations pairing the listing with wardrobe items, complete with styling notes.
  * **On Empty/Missing Wardrobe:** Returns a structured fallback message guiding the user to add wardrobe items.

* **`create_fit_card(outfit_description: str, listing: dict)`**
  * **Inputs:** `outfit_description` (string of suggested outfits), `listing` (dictionary of the selected clothing item).
  * **Returns:** A persuasive, engaging text summary card ("fit card") marketing the item and outfit combination.

---

## Planning Loop

* **Branch Rule:** If `search_listings` returns an empty list (`[]`), the agent halts execution early, sets `session["error"]` to a helpful message explaining what the user can change (such as broadening keywords, increasing price, or removing size filters), leaves `fit_card` as `None`, and returns the session without calling `suggest_outfit` or `create_fit_card`. If listings are found, it selects the first result and proceeds through the rest of the workflow.
* **Location:** `agent.py::run_agent`

---

## Sample Run

### Per-Tool Terminal Tests

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

### Full Agent Execution Run

<pre><code>(.venv) [leo@precision ai201-project2-fitfindr-starter-v2026]$ python agent.py
=== A query the data can match ===
  found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop
  outfit:   Based on the items currently in your wardrobe, here are two outfit combinations featuring the **Y2K Baby Tee — Butterfly Print**:

**1. Casual Y2K Everyday Look**
* **Top:** Y2K Baby Tee — Butterfly Print ($18.0)
* **Bottoms:** Item (bottoms, size N/A)
* **Shoes:** Item (shoes, size N/A)
* **Accessories:** Item (accessories, size N/A)
* *Why it works:* A classic, effortless Y2K aesthetic. Pairing a fitted baby tee with your bottoms creates a balanced silhouette, and accessorizing with your accessory piece ties the nostalgic look together.

**2. Layered Streetwear Vibe**
* **Top:** Y2K Baby Tee — Butterfly Print ($18.0)
* **Outerwear:** Item (outerwear, size N/A)
* **Bottoms:** Item (bottoms, size N/A)
* **Shoes:** Item (shoes, size N/A)
* *Why it works:* Perfect for transitional weather. Tossing your outerwear piece over the baby tee adds dimension and texture to the outfit while keeping the butterfly print as the focal point.
  fit card: Channel your inner 2000s pop star with this gorgeous Y2K Baby Tee — Butterfly Print for just $18.0 on Depop! Whether you're keeping it casual for everyday wear or throwing on some outerwear for an edgy streetwear vibe, this piece is about to become your new wardrobe MVP. Run, don't walk, to snag this nostalgic steal!

=== A query it can't ===
  stopped: No matching listings found for 'designer ballgown size XXS under $5'. Try broadening your search keywords, increasing your maximum price, or removing size restrictions.
  fit_card is None — it should still be None here
</code></pre>

---

## How I Used AI

1. **Query Parsing Logic:** I asked Claude to help design the query parsing logic in `agent.py` using regular expressions to extract price ceilings (like "under $30") and sizes from natural language text. It returned a regex pattern, but I modified it to handle alternative phrasing (such as explicit dollar signs or less-than symbols) so that edge cases in user input were handled robustly.
2. **Tool Empty-State Design:** I provided Claude with my `search_listings` tool spec to check how it handled empty results. It initially suggested returning a static error string on no matches, but I changed it to return an empty list `[]` instead. This ensured that the planning loop's conditional branch could cleanly evaluate the result and provide actionable guidance to the user rather than failing silently.
