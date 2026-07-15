# 🏦 FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform

An intelligent, AI-assisted web platform that helps distressed borrowers
understand their debt, calculate financial stress, predict settlement
outcomes, and generate professional, lender-ready negotiation letters —
all from a single dashboard.

**Status:** Implemented | **Backend:** FastAPI | **Frontend:** React + Vite |
**Database:** SQLite / SQLAlchemy | **AI:** Google Gemini 2.5 Flash

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Brainstorming & Idea Prioritization](#2-brainstorming--idea-prioritization)
3. [Requirement Analysis](#3-requirement-analysis)
4. [Project Design Phase](#4-project-design-phase)
5. [Project Planning Phase](#5-project-planning-phase)
6. [Project Development Phase](#6-project-development-phase)
7. [Project Testing](#7-project-testing)
8. [Repository Structure](#8-repository-structure)
9. [Getting Started Locally](#9-getting-started-locally)
10. [Deployment (Render)](#10-deployment-render)
11. [Scalability & Future Roadmap](#11-scalability--future-roadmap)
12. [Conclusion](#12-conclusion)
13. [Summary](#13-summary)

---

## 1. Introduction

Millions of borrowers fall behind on credit card and loan payments every
year, but very few of them have access to the legal vocabulary, financial
modeling tools, or negotiation experience needed to reach a fair
settlement with a lender. Lenders, on the other hand, rely on rigid
recovery grids and third-party collection channels that rarely account
for a borrower's real repayment capacity.

**FinRelief AI** bridges this gap by giving borrowers a self-service,
AI-assisted platform that:
- Analyzes their real financial situation (income, expenses, existing debt)
- Calculates objective financial stress and debt-to-income metrics
- Predicts a realistic settlement percentage per loan
- Generates a personalized negotiation strategy
- Drafts a professional, lender-specific settlement request letter

---

## 2. Brainstorming & Idea Prioritization

During ideation, the team evaluated several approaches to debt relief
automation (chatbot-only advisory, static calculators, full negotiation
automation) and prioritized building a platform that combines:

- **Data-driven decisioning** — rule-based financial engine as the
  foundation, so the platform always works even without an AI key
- **Generative AI as an enhancement layer** — Google Gemini is used to
  produce polished, human-readable negotiation content on top of the
  calculated numbers, not to replace the underlying logic
- **Borrower-first UX** — a clean, dashboard-driven interface instead of
  a purely conversational chatbot, so users can see their numbers clearly

This prioritization ensures the platform is reliable (rule-based core)
while still feeling intelligent and personalized (AI-generated content).

---

## 3. Requirement Analysis

**Functional Requirements**
- Secure user registration/login (JWT-based)
- Borrower financial profile management (income, expenses, savings)
- Loan portfolio management (add/view/delete loan accounts)
- Real-time financial health metrics (EMI ratio, DTI ratio, stress level)
- AI-powered settlement percentage prediction per loan
- AI-generated negotiation strategy and lender-specific letters
- Debt repayment timeline simulation
- Borrower rights & financial guidance content
- History of all AI-generated content per user

**Non-Functional Requirements**
- Secure password hashing and JWT session management
- Stable operation even without an active Gemini API key (fallback)
- Modular, maintainable full-stack architecture
- Fast API responses suitable for real-time dashboard updates

---

## 4. Project Design Phase

**Entity Relationship Design** — Five core entities: `Users`, `Loans`,
`Financial Profile` (embedded in Users), `Settlement Records` (computed
on demand), and `AI History`, connected through `user_id` foreign keys.

**System Architecture**

```
React (Vite) Frontend  <--- Axios/JWT --->  FastAPI Backend  <--->  SQLite (SQLAlchemy ORM)
                                                    |
                                                    v
                                        Google Gemini API (optional)
                                          + Rule-based Fallback Engine
```

---

## 5. Project Planning Phase

The project was broken down into 6 Epics, aligned with the internship's
tracked workflow:

| Epic | Focus |
|---|---|
| 1 | Application Development & System Setup |
| 2 | AI Integration & Financial Processing Setup |
| 3 | Database Management & Financial Data Storage |
| 4 | Frontend Integration & UI Development |
| 5 | Testing, Debugging & Performance Optimization |
| 6 | Version Control, Finalization & Deployment Readiness |

---

## 6. Project Development Phase

Key modules implemented:

- **`app/services/financial_engine.py`** — EMI ratio, debt-to-income
  ratio, financial stress classification (Low/Medium/High), loan
  priority ranking, and debt repayment timeline simulation
- **`app/services/settlement_engine.py`** — rule-based settlement
  percentage calculation (clamped 40-75%) with risk scoring
- **`app/services/ai_engine.py`** — Google Gemini 2.5 Flash integration
  for negotiation strategy and letter generation, with an automatic
  rule-based fallback when no API key is configured
- **`app/main.py`** — all REST API endpoints (auth, loans, dashboard,
  settlement predictor, AI negotiation, history)
- **React frontend** — Login, Dashboard, Financial Health, Settlement
  Predictor, Negotiation Email Generator, Know Your Rights, and History
  pages, built with a custom dark-themed design system

---

## 7. Project Testing

- Verified financial calculations across multiple loan types and
  borrower profiles (single loan, multiple loans, zero income edge case)
- Tested settlement prediction with varying overdue durations, interest
  rates, and debt-to-income ratios
- Verified AI fallback activates correctly when `GOOGLE_API_KEY` is empty
  or the Gemini API call fails
- Validated JWT authentication flow (expired token, invalid token, missing
  token scenarios)
- Verified frontend <-> backend integration for all endpoints via
  FastAPI's Swagger UI (`/docs`) and the live React dashboard

---

## 8. Repository Structure

```
FinReliefAI_/
├── app/
│   ├── services/
│   │   ├── financial_engine.py
│   │   ├── settlement_engine.py
│   │   └── ai_engine.py
│   ├── utils/
│   │   ├── auth.py
│   │   └── schemas.py
│   ├── database.py
│   ├── models.py
│   └── main.py
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
├── render.yaml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 9. Getting Started Locally

### Backend Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Rename `.env.example` to `.env` and fill in your values (`SECRET_KEY`,
and optionally `GOOGLE_API_KEY`).

```powershell
uvicorn app.main:app --reload --port 8000
```

API docs available at: http://127.0.0.1:8000/docs

### Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

App available at: http://localhost:5173

---

## 10. Deployment (Render)

This project includes a `render.yaml` Blueprint for one-click deployment:

1. Push this repository to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/) → **New** →
   **Blueprint**
3. Connect this repository — Render auto-detects `render.yaml`
4. Fill in the secret environment variables in the Render dashboard:
   - `GOOGLE_API_KEY` (backend)
   - `ALLOWED_ORIGINS` (backend, set after frontend deploys)
   - `VITE_API_URL` (frontend, set to your deployed backend URL)

---

## 11. Scalability & Future Roadmap

- Migrate from SQLite to PostgreSQL for concurrent multi-user production use
- Add multi-language negotiation letter generation
- Integrate SMS/email delivery of negotiation letters directly to lenders
- Add a credit score impact estimator for post-settlement guidance
- Role-based access for financial advisors reviewing multiple borrowers
- Add automated test suite (pytest) for CI/CD via GitHub Actions

---

## 12. Conclusion

FinRelief AI demonstrates how a modular full-stack architecture combined
with generative AI can make debt negotiation more accessible, transparent,
and borrower-friendly — without depending entirely on a third-party AI
service, thanks to its rule-based fallback design.

---

## 13. Summary

FinRelief AI is a full-stack, AI-assisted debt relief platform built with
React.js, FastAPI, SQLite, and Google Gemini API. It calculates financial
health metrics, predicts settlement percentages, and generates
personalized negotiation strategies and lender-specific letters — all
while remaining fully functional even without an active AI API key
through its rule-based fallback engine.
