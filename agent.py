"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.
"""

import re
import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """A fresh session for one user interaction."""
    return {
        "query": query,
        "parsed": {},
        "search_results": [],
        "selected_item": None,
        "wardrobe": wardrobe,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """Run the loop once and return the finished session."""
    session = new_session(query, wardrobe)
    count = 0

    # 1. Parse the query
    count += 1
    trace.check_iterations(count)

    query_lower = query.lower()
    max_price = None
    size = None

    price_match = re.search(r'(?:under|less than|<)\s*\$?(\d+(?:\.\d+)?)', query_lower)
    if not price_match:
        price_match = re.search(r'\$(\d+(?:\.\d+)?)', query_lower)
    if price_match:
        max_price = float(price_match.group(1))

    size_match = re.search(r'size\s+([a-zA-Z0-9/_]+)', query_lower)
    if size_match:
        size = size_match.group(1)

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
    trace.step("parse_query", inputs={"query": query}, returned=session["parsed"])

    # 2. Call search_listings()
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
    trace.step("search_listings (via MCP)", inputs=search_inputs, returned=search_results)

    # 3. Branch Check (explicit trace for the branch evaluation)
    count += 1
    trace.check_iterations(count)
    
    branch_inputs = {"search_results_count": len(search_results)}
    if not search_results:
        session["error"] = f"No matching listings found for '{query}'."
        trace.step("branch_check", inputs=branch_inputs, note="branch: empty, stopping run")
        trace.step("final_session_state", inputs={"error": session["error"]}, returned=session)
        return session

    trace.step("branch_check", inputs=branch_inputs, note="branch: match found, continuing")

    # 4. Choose an item
    count += 1
    trace.check_iterations(count)

    session["selected_item"] = search_results[0]
    select_inputs = {"available_count": len(search_results), "choice_index": 0}
    trace.step("select_item", inputs=select_inputs, returned=session["selected_item"])

    # 5. Suggest outfit
    count += 1
    trace.check_iterations(count)

    outfit_inputs = {"selected_item": session["selected_item"], "wardrobe_keys": list(wardrobe.keys())}
    session["outfit_suggestion"] = suggest_outfit(session["selected_item"], wardrobe)
    trace.step("suggest_outfit", inputs=outfit_inputs, returned=session["outfit_suggestion"])

    # 6. Create fit card
    count += 1
    trace.check_iterations(count)

    fit_card_inputs = {"outfit_suggestion": session["outfit_suggestion"], "selected_item": session["selected_item"]}
    session["fit_card"] = create_fit_card(session["outfit_suggestion"], session["selected_item"])
    trace.step("create_fit_card", inputs=fit_card_inputs, returned=session["fit_card"])

    # 7. Observe final session state in the trace
    count += 1
    trace.check_iterations(count)
    session_inputs = {"status": "complete"}
    trace.step("final_session_state", inputs=session_inputs, returned=session, note="session populated successfully")

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== Successful Path Trace (Full Inputs) ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))
