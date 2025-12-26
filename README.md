# AeroPulse  

### An Interpretability-First Analysis of Airline Experience Drivers

---

## Overview

**AeroPulse** is an exploratory analysis of approximately **5,000 airline customer reviews**, designed to answer a single, sharply defined question:

> **When customers express sentiment about a specific aspect of their airline experience, how strongly is that sentiment associated with their overall satisfaction?**

The core insight is deliberately counter-intuitive:

> **The aspects customers talk about most are not necessarily the aspects that matter most.**

This project separates **frequency** (visibility) from **influence** (impact), and focuses on the latter.

---

## What This Project Is

AeroPulse is an **influence analysis**, not a predictive system.

It is intentionally scoped to:
- prioritize interpretability over automation  
- ground text analysis in observable rating behavior  
- surface *high-leverage experience dimensions* without black-box models  

The work is exploratory and explanatory by design, closer in spirit to an applied research notebook than a production ML pipeline.

---

## What This Project Is *Not*

To avoid over-claiming or false rigor, AeroPulse explicitly does **not**:

- Claim causality  
- Build satisfaction or churn prediction models  
- Auto-discover aspects using embeddings or topic models  
- Optimize metrics such as accuracy or AUC  
- Generalize findings beyond the analyzed airline  

All conclusions are framed as **observed associations**, not causal effects.

---

## Dataset

The analysis uses ~5,100 customer reviews scraped from `airlinequality.com` for **United Airlines**.  
Each review includes:

- Free-text narrative feedback  
- Aspect-level ratings:
  - Seat comfort  
  - Cabin staff  
  - Food & beverage  
  - Ground service  
  - Value for money  
- An overall satisfaction score  
- A binary recommendation flag  

### Known Biases (Explicitly Acknowledged)

This dataset is **not representative of the full passenger population**.  
Key biases include:

- Self-selection bias  
- Negativity bias  
- Non-uniform aspect rating completion  

Rather than attempting to “correct” these biases, the analysis treats them as part of the signal and focuses on **relative influence**, not absolute satisfaction levels.

---

## Methodological Principles

Several design choices are central to the validity of the analysis:

### 1. Aspect Anchoring
All text analysis is explicitly anchored to the airline’s **existing rating dimensions**.  
No additional aspects are introduced, even if mentioned in text.

This preserves alignment between:
- what customers say  
- what customers score  
- what conclusions are drawn  

### 2. Interpretation of Missing Ratings
Missing aspect ratings are treated as **non-salience**, not neutrality.

- No rating imputation is performed  
- Aspect sentiment is computed **only when the aspect is explicitly mentioned in text**  

All influence estimates are therefore **conditional on aspect mention** and should be interpreted as *within-aspect contrasts*, not population-wide effects.

### 3. Sentiment Extraction
Sentiment is computed using **rule-based VADER**, applied at the **sentence level** and restricted to **aspect-relevant sentences only**.

This avoids:
- sentiment dilution across unrelated topics  
- hallucinated signal  
- opaque model behavior  

### 4. Influence Measurement
Influence is measured using **directional lift**:

> the change in mean overall satisfaction when aspect sentiment shifts from negative to positive

Spearman correlation is reported only as supporting evidence, not as the primary signal.

---

## Key Findings

A consistent hierarchy of influence emerges:

- **Food & beverage quality** is discussed relatively infrequently, yet exhibits the **largest marginal impact** on overall satisfaction  
- **Cabin staff behavior** acts as an emotional amplifier, contributing to polarized experiences  
- **Seat comfort** functions as a baseline requirement, where failures are heavily penalized  
- **Value for money** reflects retrospective judgment rather than a directly actionable operational lever  

Some dimensions operate as **“silent killers”**—low visibility, high impact.

---

## Repository Structure

- `notebook/` — Primary narrative artifact (analysis + explanation)  
- `src/` — Scrapping script 
- `data/` — Pre-processed review dataset  
- `assets/` — Supporting visuals  

---

## Limitations and Extensions

This analysis does not claim causality and does not generalize beyond the studied airline.

Potential extensions include:
- Temporal trend analysis  
- Cross-airline comparison  
- Controlled embedding-based aspect discovery  

Any extension should preserve the interpretability constraints used here.
