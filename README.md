# AeroPulse

## What This Project Is

AeroPulse is an exploratory analysis of ~5,000 airline customer reviews designed to answer a single, precise question:

> **When customers mention a specific aspect of their experience, how much does that sentiment actually influence their overall satisfaction?**

The insight: **the most talked-about issues are not always the most impactful ones.**

### Why This Matters

Airlines receive massive volumes of feedback. Conventional analysis defaults to "people complain about X, so fix X." This project challenges that logic by separating **frequency** (how often something is discussed) from **influence** (how much it actually matters).

The result: actionable, defensible priorities grounded in data, not intuition.

---

## Key Findings

* **Food & beverage quality** is discussed rarely but drives disproportionate satisfaction gains
* **Cabin staff** acts as an emotional amplifier—critical for experience consistency
* **Seat comfort** functions as a baseline requirement, not a differentiator
* **Value for money** reflects overall judgment, not a direct operational lever

---

## What This Project Does (and Doesn't)

✅ **Does:**
* Identify high-leverage experience dimensions
* Use interpretable, rating-anchored analysis
* Ground conclusions in actual customer scores

❌ **Does Not:**
* Claim causality
* Build prediction models
* Auto-discover aspects
* Generalize across airlines

---

## Approach

**Sentiment Extraction:** Rule-based VADER applied only to aspect-specific sentences (not whole reviews)

**Influence Measurement:** Directional lift—how much overall satisfaction improves when sentiment about an aspect shifts from negative to positive

**Aspect Anchoring:** Analysis restricted to five airline-defined dimensions (seat comfort, cabin staff, food & beverage, ground service, value for money)

This restraint preserves clarity over complexity.

