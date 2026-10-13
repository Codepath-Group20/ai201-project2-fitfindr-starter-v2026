"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import re
import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.
    """
    session = new_session(query, wardrobe)
    count = 0

    # 1. Parse the query into description, size, and max_price
    count += 1
    trace.check_iterations(count)

    query_lower = query.lower()
    max_price = None
    size = None

    # Extract price ceiling (e.g. "under $30", "$30")
    price_match = re.search(r'(?:under|less than|<)\s*\$?(\d+(?:\.\d+)?)', query_lower)
    if not price_match:
        price_match = re.search(r'\$(\d+(?:\.\d+)?)', query_lower)
    if price_match:
        max_price = float(price_match.group(1))

    # Extract size (e.g. "size M", "size XXS")
    size_match = re.search(r'size\s+([a-zA-Z0-9/_]+)', query_lower)
    if size_match:
        size = size_match.group(1)

    # Extract description by stripping out price and size phrases
    desc = query_lower
    if price_match:
        desc = re.sub(r'(?:under|less than|<)?\s*\$?\d+(?:\.\d+)?', '', desc)
    if size_match:
        desc = re.sub(r'size\s+[a-zA-Z0-9/_]+', '', desc)

    for filler in ['looking for a', 'looking for', 'want a', 'want', 'i want', 'a ']:
        desc = desc.replace(filler, ' ')
    desc = ' '.join(desc.split())
    if not desc:
        desc = query_lower

    session["parsed"] = {
        "description": desc,
        "size": size,
        "max_price": max_price,
    }

    # 2. Call search_listings() with parsed parameters
    count += 1
    trace.check_iterations(count)

    from mcp_client import call_tool
    search_inputs = {
        "description": session["parsed"]["description"],
        "size": session["parsed"]["size"],
        "max_price": session["parsed"]["max_price"],
    }
    search_results = call_tool("search_listings", search_inputs)
    session["search_results"] = search_results
    trace.step("search_listings", search_inputs, search_results)

    # ⚠️ BRANCH: If nothing came back, halt and explain what to change
    if not search_results:
        session["error"] = (
            f"No matching listings found for '{query}'. "
            f"Try broadening your search keywords, increasing your maximum price, or removing size restrictions."
        )
        return session

    # 3. Choose an item (first result) and store in session state
    count += 1
    trace.check_iterations(count)

    selected_item = search_results[0]
    session["selected_item"] = selected_item

    # 4. Call suggest_outfit() with the selected item and wardrobe
    count += 1
    trace.check_iterations(count)

    outfit_inputs = {"selected_item": selected_item, "wardrobe": wardrobe}
    outfit_suggestion = suggest_outfit(selected_item, wardrobe)
    session["outfit_suggestion"] = outfit_suggestion
    trace.step("suggest_outfit", outfit_inputs, outfit_suggestion)

    # 5. Call create_fit_card() with the outfit and item
    count += 1
    trace.check_iterations(count)

    fit_card_inputs = {"outfit_suggestion": outfit_suggestion, "selected_item": selected_item}
    fit_card = create_fit_card(outfit_suggestion, selected_item)
    session["fit_card"] = fit_card
    trace.step("create_fit_card", fit_card_inputs, fit_card)

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )

"""

---

### How to test your trace:
Run a query with the `--trace` flag
```bash python app.py ask 'vintage graphic tee under $30' --trace
"""
