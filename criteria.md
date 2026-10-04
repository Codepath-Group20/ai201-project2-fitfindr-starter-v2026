# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed[cite: 2].

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion[cite: 2].
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion[cite: 2].

Under each one, write a sentence or two on **why that target** and not a
stricter one[cite: 2]. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not[cite: 2].

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does[cite: 2].

**Two are written for you. You write three[cite: 2].**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries[cite: 2].

**Why this target:**
My keyword search parser can occasionally miss nuances or alternate phrasings if the user uses synonyms not present in the catalog tags, so 4 of 5 allows for realistic natural language variation while still demanding high reliability.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries[cite: 2].

**Why this target:**
This path relies on a hard programmatic branch rule rather than model generation. Since it's deterministic code checking for an empty list, it should succeed 100% of the time without exception.

---

## 3. Something about state

In 5 of 5 test runs, the `listing_id` selected and stored in the session state by `search_listings` precisely matches the `listing_id` passed as an argument to `suggest_outfit`.

**Why this target:**
State tracking is prone to silent bugs where a dictionary key mismatch passes data as `None` or drops it entirely. Demanding 5 of 5 ensures that data integrity is maintained perfectly across tool boundaries without intermediate state corruption.

---

## 4. Something about the fit card

For any valid query resulting in a generated fit card, the output string explicitly contains the correct item price and platform name matching the source data — in at least 5 of 5 tries.

**Why this target:**
Because the fit card relies on an LLM to write descriptive prose, it can occasionally hallucinate or omit numbers. Requiring the explicit price and platform ensures the model remains grounded in the structured tool data rather than making up details.

---

## 5. Your choice

When a query specifies a strict maximum price ceiling (e.g., "under $30"), every listing returned by `search_listings` and evaluated by the agent has a price less than or equal to that threshold — in 5 of 5 tries.

**Why this target:**
Price constraints are a primary user filter. If the search or filtering logic leaks items above the specified ceiling, the user's core budget constraint is violated, making strict enforcement necessary.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit[cite: 2]. But never delete or edit the original
     line[cite: 2]. Add the revision underneath it, like this[cite: 2]:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED[cite: 2].

     Lowering a target because you missed it is not a revision, and it costs
     you the point[cite: 2]:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are[cite: 2].
     ───────────────────────────────────────────────────────────────────────── -->
