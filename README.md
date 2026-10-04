# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
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

- **What it does:** Compares available user wardrobe items with marketplace listings to generate cohesive outfit pairings based on aesthetic compatibility and user preferences.
- **Inputs:** `wardrobe_item_id` (str), `listing_id` (str), `occasion` (str)
- **Returns:** A dictionary containing `outfit_id` (str), `base_item` (dict), `matched_listing` (dict), `compatibility_score` (float), and `styling_notes` (str).
- **When it has nothing:** Returns `None` and an error string message.

### `create_fit_card`

- **What it does:** Compiles the final verified outfit components and styling notes into a nicely formatted Markdown fit card ready for user presentation.
- **Inputs:** `outfit_data` (dict), `user_notes` (str)
- **Returns:** A formatted Markdown string representing the complete fit card, including item titles, prices, platforms, and total cost.
- **When it has nothing:** Returns a fallback string: `"Error: Unable to generate fit card due to missing outfit data."`.

---

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, put a message in the session and stop. Otherwise, take the first result and go to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Using regex and explicit keyword splitting to extract filters like price ceilings and category terms.

**What moves through the session:** User query text -> extracted filters -> search results list -> selected listing ID -> outfit suggestion payload -> final markdown fit card string.

---

## Sample Run

**One full query**

<pre><code>$ python app.py ask 'vintage graphic tee under $30'
[Stub output pending milestone completion]</code></pre>

**The three tools, tested one at a time**

<pre><code>$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"</code></pre>

<pre><code>$ python -c "from tools import suggest_outfit; print(suggest_outfit('w_001', 'lst_002', 'casual'))"</code></pre>

<pre><code>$ python -c "from tools import create_fit_card; print(create_fit_card({'outfit_id': 'out_01'}, 'Looks great!'))"</code></pre>

---

## How I Used AI

**Moment 1**

- *What I asked for:* Help defining the precise dictionary return keys for `search_listings` so the branch rule wouldn't fail on missing keys.
- *What came back:* Suggested including explicit `id`, `price`, and `platform` keys in every returned list item.
- *What I changed:* Adopted the explicit key schema in the Tool Inventory spec above.

**Moment 2**

- *What I asked for:* Reviewing the branching condition rule for logical completeness when handling empty outputs.
- *What came back:* Recommended adding a clear session message assignment before breaking out of the loop.
- *What I changed:* Incorporated the explicit instruction to append a message to the session state when `search_listings` returns empty.

---

## What's Still Broken

*Milestone 2 implementation is complete; proceeding to code execution and tool coding in Milestone 3.*

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
