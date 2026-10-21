# AI Resume Reviewer — CS4680 Prompt Engineering (Assignment 3)

## Overview

An AI-powered resume reviewer that gives you recruiter-specific feedback in seconds. Paste your resume and a job description, pick a reviewer persona, and get an ATS score, keyword gap analysis, inline bullet rewrites, and a tailored LinkedIn summary — all streamed live.

**Problem Statement:** Job seekers get generic resume advice that doesn't account for the specific role or the recruiter's priorities. A FAANG tech recruiter and a startup hiring manager care about completely different things.

**Solution:** Use Claude with recruiter-specific personas and few-shot rewrite examples to deliver targeted, actionable feedback that mirrors what a real human reviewer would say.

---

## Features

- **ATS Score Simulator** — scores your resume 0–100 against the job description with a specific explanation
- **Keyword Gap Analysis** — shows matched vs. missing keywords from the JD
- **Inline Bullet Rewrites** — flags weak bullets and shows before/after rewrites with metrics
- **Reviewer Persona Selector** — choose FAANG Recruiter, Startup Hiring Manager, or Finance/Consulting HR
- **LinkedIn About Section** — generates a tailored 3-sentence summary
- **Streaming output** — results appear token-by-token so you're never staring at a blank screen

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Generative AI API | Anthropic Claude API |
| Model | `claude-opus-4-7` |
| UI | Streamlit |

---

## Prompt Engineering Techniques

This application uses two prompt engineering patterns from CS4680:

1. **Persona Pattern** — The system prompt assigns a specific recruiter identity (FAANG, Startup, or Finance/Consulting) that shapes every judgment the model makes. The same resume gets meaningfully different feedback depending on who is "reading" it. This is defined per-persona in `PERSONAS` and injected into `SYSTEM_PROMPT_TEMPLATE`.

2. **Few-Shot Pattern** — The system prompt includes four concrete weak→strong bullet rewrite examples. This anchors the model's rewrites to a specific style and quality bar (quantified, active-verb, impact-focused) rather than generic improvement suggestions.

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- An Anthropic API key ([get one here](https://console.anthropic.com))

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment

```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

### Run the application

```bash
streamlit run main.py
```

The app opens at `http://localhost:8501`.

---

## Usage

1. **Choose a reviewer** — pick the persona closest to your target role
2. **Paste your resume** — plain text works best
3. **Paste the job description** — the more complete, the better the keyword analysis
4. **Click Analyze** — watch the review stream in live

---

## Project Structure

```
AI-Assistant-PE/
├── main.py               # Streamlit app + Claude integration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
└── README.md
```

---

## Demo

**Video:** _Coming soon_

---

## Grading Checklist

- [x] Problem identified and clearly described
- [x] Working MVP implemented
- [x] Persona Pattern used and explained
- [x] Few-Shot Pattern used and explained
- [x] User interface (Streamlit web app) present and functional
- [ ] Live demo ready for presentation
- [ ] GitHub repo link submitted via Google Form
- [ ] Short demo video (<2 min) published and submitted
- [ ] (Bonus) Application deployed publicly

---

## Course Info

**Course:** CS4680 — Prompt Engineering  
**Assignment:** Assignment 3 — AI Assistant Project  
**Points:** 50
