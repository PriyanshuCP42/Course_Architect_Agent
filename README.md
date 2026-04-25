<p align="center">
  <img src="assets/banner.png" alt="Course Architect — AI-Powered Course Generation Engine" width="100%"/>
</p>

<p align="center">
  <strong>Transform raw notes into production-grade, pedagogically structured courses — powered by AI agents.</strong>
</p>

<br/>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.9+-14354C?style=for-the-badge&logo=python&logoColor=yellow" alt="Python 3.9+"/></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.56-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/></a>
  <a href="https://groq.com/"><img src="https://img.shields.io/badge/Groq-Inference-F55036?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0id2hpdGUiLz48L3N2Zz4=&logoColor=white" alt="Groq"/></a>
  <a href="https://llama.meta.com/"><img src="https://img.shields.io/badge/Llama_3.1-8B_Instant-0467DF?style=for-the-badge&logo=meta&logoColor=white" alt="Llama 3.1"/></a>
  <a href="https://github.com/py-pdf/fpdf2"><img src="https://img.shields.io/badge/FPDF2-2.8-00599C?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="FPDF2"/></a>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge" alt="MIT License"/>
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-multi-agent-architecture">Architecture</a> •
  <a href="#-getting-started">Get Started</a> •
  <a href="#-deployment">Deploy</a> •
  <a href="#-project-structure">Structure</a>
</p>

---

## 📋 Overview

**Course Architect** is a multi-agent AI system that takes unstructured source material — textbook notes, lecture transcripts, research papers, or raw concepts — and synthesizes it into a **complete, structured course architecture** in seconds.

The system orchestrates **four specialized AI agents**, each responsible for a distinct pedagogical function, to produce:

- 📐 A hierarchical **curriculum** with modules, lessons, and weekly timelines
- 📖 Deep-dive **lesson content** with introductions, explanations, key takeaways, and real-world applications
- 🧪 Rigorous **assessments** — MCQs, short-answer, and scenario-based questions with answer keys
- 🏗️ Resume-worthy **capstone projects** with rubrics, deliverables, and acceptance criteria
- 📄 A professional **PDF export** of the complete architecture

> **One input → Four agents → A production-grade course.**

---

## ✨ Key Features

<table>
  <tr>
    <td width="50%">

### 🏗️ Curriculum Designer Agent
Generates a structured module-lesson hierarchy with learning goals, prerequisites, difficulty levels, and a weekly timeline — optimized for your target audience and course duration.

</td>
    <td width="50%">

### 📖 Content Generator Agent
Writes detailed lesson content for every lesson: introductions, core explanations, key takeaways, real-world applications, and summaries — each grounded in the source material.

</td>
  </tr>
  <tr>
    <td width="50%">

### 🧪 Assessment Engine Agent
Creates a comprehensive question bank: multiple-choice questions with explanations, short-answer prompts with model answers, and scenario-based assessments with scoring guides.

</td>
    <td width="50%">

### 🏆 Project Designer Agent
Designs capstone projects with problem statements, step-by-step deliverables, acceptance criteria, technical requirements, tools & technologies, and professional evaluation rubrics.

</td>
  </tr>
</table>

### Additional Capabilities

| Capability | Description |
|:---|:---|
| 📄 **PDF Export** | Professional, Claude-themed PDF document with cover page, section headers, accent colors, and complete course data |
| 🎨 **Claude-Inspired UI** | Premium light theme with warm terracotta (`#D97757`) accents, serif headings (Newsreader), and clean card-based layout |
| ⚡ **Token Optimization** | Smart content truncation and lightweight curriculum passing to stay within free-tier API limits |
| 🔄 **Retry Logic** | Built-in rate-limit handling with exponential backoff for reliable generation |
| 📊 **Interactive Dashboard** | Four-tab interface: Curriculum & Timeline, Lesson Content, Assessments, Projects |

---

## 🏛️ Multi-Agent Architecture

The system follows a sequential pipeline where each agent builds on the output of the previous one:

```
                    ┌─────────────────────────────┐
                    │       📝 USER INPUT          │
                    │  Raw Notes + Course Params   │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │  🏗️ AGENT 1: CURRICULUM      │
                    │  DESIGNER                    │
                    │                              │
                    │  → Modules & Lessons         │
                    │  → Weekly Timeline           │
                    │  → Learning Outcomes          │
                    │  → Prerequisites              │
                    │                              │
                    │  Output: Structured JSON      │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │  📖 AGENT 2: CONTENT         │
                    │  GENERATOR                   │
                    │                              │
                    │  For each lesson:             │
                    │  → Introduction               │
                    │  → Core Explanation           │
                    │  → Key Takeaways              │
                    │  → Real-World Application     │
                    │  → Summary                    │
                    │                              │
                    │  Output: Hydrated Curriculum  │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────┴───────────────┐
                    │                             │
                    ▼                             ▼
        ┌───────────────────┐       ┌───────────────────┐
        │  🧪 AGENT 3:      │       │  🏆 AGENT 4:      │
        │  ASSESSMENT       │       │  PROJECT           │
        │  ENGINE           │       │  DESIGNER          │
        │                   │       │                    │
        │  → MCQs           │       │  → Problem         │
        │  → Short Answer   │       │    Statements      │
        │  → Scenarios      │       │  → Deliverables    │
        │  → Answer Keys    │       │  → Rubrics         │
        │  → Scoring Guides │       │  → Tech Stack      │
        └─────────┬─────────┘       └─────────┬──────────┘
                  │                           │
                  └─────────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────────┐
                    │   📊 STREAMLIT DASHBOARD     │
                    │                              │
                    │  Tab 1: Curriculum & Timeline │
                    │  Tab 2: Lesson Content        │
                    │  Tab 3: Assessments           │
                    │  Tab 4: Capstone Projects     │
                    │  + Professional PDF Export     │
                    └─────────────────────────────┘
```

### Token Optimization Strategy

To operate efficiently within Groq's free-tier limits (6,000 TPM), the pipeline implements:

1. **Input Truncation** — Raw notes are capped at ~1,500 tokens to leave room for prompts and responses
2. **Lightweight Curriculum Passing** — Agents 3 & 4 receive a stripped-down curriculum (titles and descriptions only, no lesson body text) to minimize token usage
3. **Rate-Limit Retries** — Automatic 25-second cooldown and retry on 429/413 errors

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Details |
|:---|:---|
| **Python** | 3.9 or higher |
| **Groq API Key** | Free at [console.groq.com](https://console.groq.com) |
| **pip** | Python package manager |

### Installation

```bash
# Clone the repository
git clone https://github.com/PriyanshuCP42/Course_Architect_Agent.git
cd Course_Architect_Agent

# Install dependencies
pip install -r requirements.txt

# Configure your API key
cp .env.example .env
# Open .env and paste your Groq API key:
#   GROQ_API_KEY=gsk_your_key_here

# Launch the application
streamlit run app.py
```

The app opens at **`http://localhost:8501`**.

### Usage

1. **Paste** your raw content into the Source Material text area
2. **Set** your course parameters — target audience, duration, class size
3. **Specify** desired learning outcomes and pedagogical elements
4. **Click** "Generate Course" and wait for the 4-agent pipeline to complete
5. **Explore** results across four interactive tabs
6. **Download** a professional PDF of the complete course architecture

---

## 🌐 Deployment

### Option 1: Streamlit Community Cloud *(Recommended — Free)*

| Step | Action |
|:---|:---|
| **1** | Go to [share.streamlit.io](https://share.streamlit.io) → Sign in with GitHub |
| **2** | Click **"New app"** → Select repo `Course_Architect_Agent`, branch `main`, file `app.py` |
| **3** | Click **"Advanced settings"** → Add your secret in TOML format (see below) |
| **4** | Click **"Deploy!"** → App goes live at `https://your-app.streamlit.app` |

**Secrets Configuration (TOML format):**
```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
```

> ⚠️ **Never commit your `.env` file.** The `.gitignore` is already configured to exclude it.

---

### Option 2: Railway / Render

```bash
# Start Command
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

Add `GROQ_API_KEY` as an environment variable in the platform's dashboard.

---

### Option 3: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t course-architect .
docker run -p 8501:8501 -e GROQ_API_KEY=gsk_your_key course-architect
```

---

## 📁 Project Structure

```
Course_Architect_Agent/
│
├── app.py                  # Streamlit frontend — UI layout, CSS, rendering
├── agents.py               # Multi-agent LLM pipeline — 4 specialized agents
├── pdf_generator.py        # Claude-themed professional PDF export engine
├── constants.py            # Design system — colors, styles, and tokens
│
├── requirements.txt        # Python dependencies
├── .env.example            # Template for local API key configuration
├── .gitignore              # Protects .env, caches, and build artifacts
│
└── assets/
    └── banner.png          # README hero banner
```

---

## 🛠️ Tech Stack

<table>
  <tr>
    <th align="center">Technology</th>
    <th align="center">Role</th>
    <th align="center">Version</th>
    <th>Details</th>
  </tr>
  <tr>
    <td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="30"/></td>
    <td align="center"><strong>Python</strong></td>
    <td align="center"><code>3.9+</code></td>
    <td>Core language for backend logic and agent orchestration</td>
  </tr>
  <tr>
    <td align="center"><img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="30"/></td>
    <td align="center"><strong>Streamlit</strong></td>
    <td align="center"><code>1.56</code></td>
    <td>Interactive web framework for the dashboard UI</td>
  </tr>
  <tr>
    <td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="30"/></td>
    <td align="center"><strong>Groq SDK</strong></td>
    <td align="center"><code>1.2</code></td>
    <td>Ultra-fast LLM inference API with structured JSON output</td>
  </tr>
  <tr>
    <td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytorch/pytorch-original.svg" width="30"/></td>
    <td align="center"><strong>Llama 3.1</strong></td>
    <td align="center"><code>8B Instant</code></td>
    <td>Meta's open-source LLM — fast, capable, free-tier compatible</td>
  </tr>
  <tr>
    <td align="center">📄</td>
    <td align="center"><strong>FPDF2</strong></td>
    <td align="center"><code>2.8</code></td>
    <td>Lightweight PDF generation with full layout control</td>
  </tr>
  <tr>
    <td align="center">🔐</td>
    <td align="center"><strong>python-dotenv</strong></td>
    <td align="center"><code>1.2</code></td>
    <td>Secure environment variable management for API keys</td>
  </tr>
</table>

---

## 🎨 Design System

The UI follows a **Claude-inspired light theme** built for readability and premium aesthetics:

| Element | Specification |
|:---|:---|
| **Typography** | `Inter` (sans-serif body) + `Newsreader` (serif headings) via Google Fonts |
| **Accent Color** | `#D97757` — Warm terracotta/clay for CTAs, active states, and highlights |
| **Card Design** | White (`#FFFFFF`) cards with `1px` borders, `12px` radius, subtle box shadows |
| **Input Fields** | `10px` border-radius, muted placeholder text, accent focus ring |
| **Tab Navigation** | Minimal bar with `2px` accent underline on active tab |
| **Page Background** | `#FAFAFA` — Off-white for comfortable reading |
| **PDF Theme** | Matching accent colors, shaded section bars, terracotta accent stripes |

---

## ⚙️ Configuration

| Variable | Required | Description |
|:---|:---|:---|
| `GROQ_API_KEY` | ✅ | API key from [console.groq.com](https://console.groq.com) |

### Model Configuration

Edit `agents.py` to switch models:

```python
MODEL = "llama-3.1-8b-instant"   # Default — optimized for free tier
# MODEL = "llama-3.3-70b-versatile"  # Higher quality, requires paid tier
# MODEL = "gemma2-9b-it"           # Alternative open model
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository
2. **Create** a feature branch → `git checkout -b feature/your-feature`
3. **Commit** your changes → `git commit -m 'Add your feature'`
4. **Push** to the branch → `git push origin feature/your-feature`
5. **Open** a Pull Request

---

## 📝 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<p align="center">
  <sub>Built with ❤️ using Streamlit, Groq, and Llama 3.1</sub>
</p>
