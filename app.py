import streamlit as st
import pandas as pd
import os
from datetime import datetime


# -------------------------------
# App Configuration
# -------------------------------
st.set_page_config(page_title="Ethical AI & Digital Competency Assessment", layout="centered")

st.title("🧠 Ethical AI & Digital Competency Assessment (EADCA)")
st.write("""
Welcome to the **Ethical AI & Digital Competency Assessment**!  
This tool evaluates your understanding of:
- 🧩 **Digital Literacy**
- 🔐 **Cybersecurity Awareness**
- 🤖 **AI Ethics & Adoption**

All questions are **mandatory** — please answer every one before submitting.
""")

# -------------------------------
# Merged Questions Dictionary
# -------------------------------
questions = {
    "Digital Literacy": [
        {
            "q": "You find two conflicting online articles about the same topic. What should you do?",
            "options": {
                "a": "Pick the first article that looks detailed",
                "b": "Check the author, date, and credibility of both sources",
                "c": "Ask your friend which one is correct"
            },
            "answer": "b"
        },
        {
            "q": "A file download looks suspicious but claims to be a course update. What will you do?",
            "options": {
                "a": "Scan it or verify the sender before opening",
                "b": "Open it immediately to check what's inside",
                "c": "Forward it to others to confirm"
            },
            "answer": "a"
        },
        {
            "q": "Cloud files remain private even without setting permissions. (T/F)",
            "options": {"a": "True", "b": "False"},
            "answer": "b"
        },
        {
            "q": "You are working on a group document and notice conflicting edits. What is the most professional way to resolve it?",
            "options": {
                "a": "Delete others’ edits and keep yours",
                "b": "Use version history and discuss changes with your team",
                "c": "Save multiple copies and ignore differences"
            },
            "answer": "b"
        },
        {
            "q": "Which of the following represents a safe website?",
            "options": {"a": "http://example.com", "b": "https://example.com", "c": "example.txt"},
            "answer": "b"
        },
        {
            "q": "Which of the following is a productivity tool?",
            "options": {"a": "Google Docs", "b": "YouTube", "c": "Instagram"},
            "answer": "a"
        },
        {
            "q": "While sharing files online, which format is best for maintaining document structure?",
            "options": {"a": ".pdf", "b": ".txt", "c": ".doc"},
            "answer": "a"
        },
        {
            "q": "You see a trending post that looks fake but has thousands of shares. What should you do?",
            "options": {
                "a": "Share it since everyone else did",
                "b": "Report or verify it through trusted sources",
                "c": "Ignore it completely"
            },
            "answer": "b"
        }
    ],

    "Cybersecurity Awareness": [
        {
            "q": "You receive an email asking to update your account password through a link. What should you do?",
            "options": {
                "a": "Click the link immediately",
                "b": "Ignore it and verify directly from the official site",
                "c": "Forward it to friends to check"
            },
            "answer": "b"
        },
        {
            "q": "Which password is most secure?",
            "options": {"a": "Sanjana123", "b": "San@2025", "c": "!T9x#R1p$"},
            "answer": "c"
        },
        {
            "q": "You are using public Wi-Fi at a café. Which action is most secure?",
            "options": {
                "a": "Accessing your online banking account",
                "b": "Connecting via VPN before logging in anywhere",
                "c": "Turning off firewall for faster internet"
            },
            "answer": "b"
        },
        {
            "q": "Define phishing in one sentence:",
            "type": "text",
            "keywords": ["fraud", "fake", "trick", "steal", "information", "data"]
        },
        {
            "q": "A friend’s account got hacked due to a weak password. What should they do first?",
            "options": {
                "a": "Reset password and enable 2FA",
                "b": "Create a new account",
                "c": "Ignore it"
            },
            "answer": "a"
        },
        {
            "q": "Cybersecurity mainly focuses on protecting what?",
            "options": {
                "a": "Data, systems, and networks",
                "b": "Only people",
                "c": "Mobile phones"
            },
            "answer": "a"
        },
        {
            "q": "Ransomware does which of the following?",
            "options": {
                "a": "Deletes files permanently",
                "b": "Encrypts files and demands payment",
                "c": "Improves system security"
            },
            "answer": "b"
        },
        {
            "q": "Multi-factor authentication adds which layer of protection?",
            "options": {
                "a": "Additional verification like OTP or fingerprint",
                "b": "Automatic login to save time",
                "c": "Password sharing with others"
            },
            "answer": "a"
        }
    ],

    "AI Ethics & Adoption": [
        {
            "q": "An AI tool ranks students unfairly. Which ethical principle is violated?",
            "options": {"a": "Fairness", "b": "Transparency", "c": "Privacy"},
            "answer": "a"
        },
        {
            "q": "An AI algorithm predicts job candidates’ success but shows bias against certain groups. What is the ethical response?",
            "options": {
                "a": "Continue using it since accuracy is high",
                "b": "Audit and retrain the model to reduce bias",
                "c": "Hide results to avoid complaints"
            },
            "answer": "b"
        },
        {
            "q": "Which is an example of responsible AI use?",
            "options": {
                "a": "Using AI results without checking bias",
                "b": "Evaluating bias before using AI output",
                "c": "Letting AI decide everything"
            },
            "answer": "b"
        },
        {
            "q": "AI models never make mistakes if data is large enough. (T/F)",
            "options": {"a": "True", "b": "False"},
            "answer": "b"
        },
        {
            "q": "Mention one ethical risk of using ChatGPT for assignments:",
            "type": "text",
            "keywords": ["plagiarism", "bias", "misinformation", "privacy"]
        },
        {
            "q": "When creating an AI chatbot collecting user data, what must be ensured?",
            "options": {
                "a": "User consent and secure data handling",
                "b": "Collect any data freely",
                "c": "Ignore privacy"
            },
            "answer": "a"
        },
        {
            "q": "Which organization provides global AI ethics guidance (e.g., UNESCO or EU)?",
            "options": {
                "a": "UNESCO and European Union",
                "b": "Only private companies",
                "c": "No one regulates AI"
            },
            "answer": "a"
        },
        {
            "q": "What is 'algorithmic bias'?",
            "options": {
                "a": "Errors due to random system bugs",
                "b": "Bias arising from unbalanced data or design flaws",
                "c": "User input mistakes"
            },
            "answer": "b"
        }
    ]
}

# -------------------------------
# Helper Function
# -------------------------------
def evaluate_text(answer, keywords):
    answer = answer.lower()
    return 3 if any(k in answer for k in keywords) else 1

# -------------------------------
# Streamlit Form (Mandatory Answers)
# -------------------------------
with st.form("assessment_form"):
    st.header("📋 Answer all questions below")

    total_score = 0
    domain_scores = {}
    unanswered = []  # track unanswered questions

    for domain, qs in questions.items():
        st.subheader(domain)
        score = 0
        for q in qs:
            if "type" in q and q["type"] == "text":
                ans = st.text_input(q["q"], key=q["q"])
                if not ans:
                    unanswered.append(q["q"])
                else:
                    score += evaluate_text(ans, q["keywords"])
            else:
                ans = st.radio(q["q"], list(q["options"].values()), key=q["q"])
                if not ans:
                    unanswered.append(q["q"])
                else:
                    chosen = [k for k, v in q["options"].items() if v == ans][0]
                    score += 3 if chosen == q["answer"] else 1
        domain_scores[domain] = score
        total_score += score

    submitted = st.form_submit_button("Submit Assessment")

# -------------------------------
# Validation & Results
# -------------------------------
if submitted:
    if unanswered:
        st.error(f"⚠️ Please answer all questions before submitting! ({len(unanswered)} unanswered)")
    else:
        st.success("✅ Assessment Completed Successfully!")
        st.write("### 📊 Results Summary:")

        for domain, score in domain_scores.items():
            max_score = len(questions[domain]) * 3
            st.write(f"- **{domain}:** {score}/{max_score}")

        total_possible = sum(len(qs) for qs in questions.values()) * 3
        ratio = total_score / total_possible
        st.write(f"**Total Score:** {total_score}/{total_possible}")

        if ratio >= 0.75:
            level = "High Competence"
        elif ratio >= 0.5:
            level = "Moderate Competence"
        else:
            level = "Needs Improvement"

        st.subheader(f"🧾 Competency Level: {level}")
        st.progress(ratio)
        st.write("Thank you for participating in the **Ethical AI & Digital Competency Assessment!** 🎓")
        
        result_row = {
            "timestamp": datetime.now().isoformat(),
            "digital_lit_score": domain_scores.get("Digital Literacy", 0),
            "cybersec_score": domain_scores.get("Cybersecurity Awareness", 0),
            "ai_ethics_adoption_score": domain_scores.get("AI Ethics & Adoption", 0),
            "total_score": total_score,
            "total_possible": total_possible,
            "ratio": ratio,
            "level": level,
        }

        csv_path = "assessment_results.csv"
        if os.path.exists(csv_path):
            old = pd.read_csv(csv_path)
            new = pd.concat([old, pd.DataFrame([result_row])], ignore_index=True)
        else:
            new = pd.DataFrame([result_row])

        new.to_csv(csv_path, index=False)
        st.success("📁 Your results have been saved to assessment_results.csv.")
