import os

import anthropic
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── Persona Pattern ──────────────────────────────────────────────────────────
PERSONAS = {
    "🏢 FAANG Technical Recruiter": {
        "description": (
            "You are a senior technical recruiter at a top-tier tech company (Google, Meta, "
            "Amazon, Apple, Netflix). You have reviewed thousands of resumes and know exactly "
            "what separates a callback from a rejection. You value quantified impact, technical "
            "depth, system-scale experience, and clear evidence of ownership."
        ),
        "focus": "technical metrics, system scale, measurable impact, and engineering depth",
    },
    "🚀 Startup Hiring Manager": {
        "description": (
            "You are a hiring manager at a well-funded Series A/B startup. You have a small, "
            "high-output team and need people who can wear many hats, move fast, and take "
            "full ownership. You value versatility, bias to action, and entrepreneurial mindset "
            "over pedigree."
        ),
        "focus": "ownership, breadth of skills, execution speed, and startup culture fit",
    },
    "💼 Finance / Consulting HR": {
        "description": (
            "You are an HR director at a top finance firm or management consulting company "
            "(Goldman Sachs, McKinsey, BCG). Your standards are exacting: formal presentation, "
            "structured analytical thinking, client-facing polish, and precisely chosen language "
            "signal whether a candidate fits the culture."
        ),
        "focus": "analytical rigor, formal language, client-facing experience, and structured problem-solving",
    },
}

# ── Few-Shot Pattern (embedded in system prompt) ─────────────────────────────
SYSTEM_PROMPT_TEMPLATE = """{persona_description}

## Your Review Format
Always structure your response with these exact sections:

### 📊 ATS Score: X/100
One sentence explaining the score — be specific about what drove it up or down.

### 🔑 Keyword Analysis
**Matched Keywords:** comma-separated list of keywords from the JD found in the resume
**Missing Keywords:** comma-separated list of important JD keywords absent from the resume

### ✍️ Bullet Point Rewrites
Identify 3–5 weak bullets and rewrite each one. For every suggestion use this format:
**Original:** [exact text from resume]
**Issue:** [one-sentence diagnosis]
**Rewritten:** [stronger version — add metrics, active verbs, and specificity]

### 💡 Overall Assessment
3–4 sentences covering the top strengths and the most critical gaps specifically for this role,
focusing on {focus}.

### 🔗 LinkedIn About Section
Write a 3-sentence LinkedIn summary tailored to this job description. Professional tone, first person.

---

## Few-Shot Examples of Weak → Strong Bullets

Weak:  "Responsible for managing a team of engineers"
Strong: "Led and mentored 8 engineers across 3 time zones, cutting average PR review time by 40% and shipping 2 major features ahead of schedule"

Weak:  "Worked on improving website performance"
Strong: "Reduced page load time by 62% (8.2 s → 3.1 s) via lazy loading and CDN optimization, lifting conversion rate 18% and saving $120K/yr in server costs"

Weak:  "Helped with customer support and issue resolution"
Strong: "Resolved 150+ tickets weekly with a 4.9/5 CSAT score; authored internal FAQ that cut repeat tickets by 30%, freeing 10 hrs/week of engineering time"

Weak:  "Built internal tools"
Strong: "Designed and shipped 4 internal React dashboards used by 200+ ops employees daily, replacing a legacy Excel workflow and saving an estimated 6 hrs/employee/week"

Always be direct and specific. Reference exact lines from the resume and exact requirements
from the job description. No generic advice."""


def build_system_prompt(persona_key: str) -> str:
    persona = PERSONAS[persona_key]
    return SYSTEM_PROMPT_TEMPLATE.format(
        persona_description=persona["description"],
        focus=persona["focus"],
    )


def stream_review(resume_text: str, job_description: str, persona_key: str):
    system_prompt = build_system_prompt(persona_key)
    user_message = (
        "Please review this resume against the job description below.\n\n"
        f"## Job Description\n{job_description}\n\n"
        f"## Resume\n{resume_text}\n\n"
        "Follow your format exactly. Be specific — quote real lines from the resume "
        "and real requirements from the job description."
    )

    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=4000,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            yield text


# ── UI ───────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="AI Resume Reviewer",
        page_icon="📄",
        layout="wide",
    )

    st.title("📄 AI Resume Reviewer")
    st.markdown(
        "*Get recruiter-specific feedback in seconds — powered by Claude*"
    )

    st.divider()

    # Persona selector
    st.subheader("👤 Choose Your Reviewer")
    persona_key = st.selectbox(
        "Who is reviewing your resume?",
        options=list(PERSONAS.keys()),
        help="Each reviewer prioritizes different signals. Pick the one closest to your target role.",
    )
    st.info(
        f"**{persona_key}** focuses on: *{PERSONAS[persona_key]['focus']}*"
    )

    st.divider()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("📋 Your Resume")
        resume_text = st.text_area(
            "Paste your resume text",
            height=420,
            placeholder="Paste the full plain text of your resume here…",
            label_visibility="collapsed",
        )

    with col2:
        st.subheader("💼 Job Description")
        job_description = st.text_area(
            "Paste the job description",
            height=420,
            placeholder="Paste the job description you are applying to…",
            label_visibility="collapsed",
        )

    st.divider()

    analyze_btn = st.button(
        "🔍 Analyze My Resume", type="primary", use_container_width=True
    )

    if analyze_btn:
        if not resume_text.strip():
            st.error("Please paste your resume.")
            return
        if not job_description.strip():
            st.error("Please paste the job description.")
            return
        if not os.getenv("ANTHROPIC_API_KEY"):
            st.error(
                "ANTHROPIC_API_KEY is not set. Add it to your .env file and restart the app."
            )
            return

        st.divider()
        st.subheader(f"📊 Review by {persona_key}")

        output = st.empty()
        full_text = ""

        with st.spinner("Analyzing…"):
            for chunk in stream_review(resume_text, job_description, persona_key):
                full_text += chunk
                output.markdown(full_text)


if __name__ == "__main__":
    main()
