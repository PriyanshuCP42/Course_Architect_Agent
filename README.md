<p align="center">
  <img src="assets/banner.png" alt="Course Architect Banner" width="100%"/>
</p>

<p align="center">
  <strong>Transform raw notes into production-grade, pedagogically structured courses — powered by AI agents.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Groq-API-F55036?style=for-the-badge&logo=groq&logoColor=white" alt="Groq"/>
  <img src="https://img.shields.io/badge/Llama_3.1-8B-0467DF?style=for-the-badge&logo=meta&logoColor=white" alt="Llama 3.1"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-deployment">Deployment</a> •
  <a href="#-tech-stack">Tech Stack</a>
</p>

---

## 🧠 What is Course Architect?

**Course Architect** is a multi-agent AI system that transforms unstructured raw content (textbook notes, research papers, lecture transcripts) into a complete, structured course architecture — including curriculum design, detailed lesson content, cognitive assessments, and resume-worthy capstone projects.

It uses a pipeline of specialized AI agents, each responsible for a distinct pedagogical task, orchestrated to produce a holistic learning experience in seconds.

> **One input. Four expert agents. A complete course.**

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏗️ **Curriculum Designer** | Generates a structured module-lesson hierarchy with learning goals, prerequisites, and weekly timelines |
| 📖 **Content Generator** | Produces detailed lesson content: introductions, core explanations, key takeaways, real-world applications, and summaries |
| 🧪 **Assessment Engine** | Creates MCQs, short-answer questions, and scenario-based assessments with answer keys and scoring guides |
| 🏆 **Project Designer** | Designs capstone projects with problem statements, deliverables, acceptance criteria, technical requirements, and evaluation rubrics |
| 📄 **PDF Export** | Professional, Claude-themed PDF document with cover page, structured sections, and complete course architecture |
| 🎨 **Claude-Inspired UI** | Clean, premium light theme with warm terracotta accents, serif headings, and polished card-based layout |

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT                           │
│  Raw Notes + Audience + Duration + Outcomes + Methods   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│              AGENT 1: CURRICULUM DESIGNER                │
│  Generates: Modules → Lessons → Weekly Timeline          │
│  Output: Structured JSON curriculum map                  │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│              AGENT 2: CONTENT GENERATOR                  │
│  For each lesson → Introduction, Core Explanation,       │
│  Key Points, Real-World Application, Summary             │
│  Output: Hydrated curriculum with full lesson content    │
└──────────────────────┬───────────────────────────────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
┌─────────────────────┐  ┌─────────────────────┐
│  AGENT 3: ASSESSOR  │  │  AGENT 4: PROJECT   │
│  MCQs, Short Answer │  │  DESIGNER           │
│  Scenario Questions  │  │  Capstone Projects  │
│  Answer Keys         │  │  Rubrics & Criteria │
└─────────┬───────────┘  └─────────┬───────────┘
          │                        │
          └────────┬───────────────┘
                   ▼
┌──────────────────────────────────────────────────────────┐
│                 STREAMLIT DASHBOARD                       │
│  Curriculum Tab │ Lessons Tab │ Assessments │ Projects    │
│                    + PDF Export                           │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Groq API Key** — Get one free at [console.groq.com](https://console.groq.com)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/PriyanshuCP42/Course_Architect_Agent.git
cd Course_Architect_Agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your API key
cp .env.example .env
# Edit .env and add your Groq API key:
# GROQ_API_KEY=gsk_your_key_here

# 4. Run the application
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📁 Project Structure

```
Course_Architect_Agent/
├── app.py                 # Streamlit frontend — UI, CSS, rendering logic
├── agents.py              # Multi-agent LLM pipeline — 4 specialized agents
├── pdf_generator.py       # Professional PDF export with Claude theme
├── constants.py           # Design system tokens and style constants
├── requirements.txt       # Python dependencies
├── .env.example           # Template for API key configuration
├── .gitignore             # Protects .env and caches
└── assets/
    └── banner.png         # README banner image
```

---

## 🛠️ Tech Stack

<table>
  <tr>
    <td align="center" width="120">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="48" height="48" alt="Python"/>
      <br/><strong>Python</strong>
      <br/><sub>Core Language</sub>
    </td>
    <td align="center" width="120">
      <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="48" height="48" alt="Streamlit"/>
      <br/><strong>Streamlit</strong>
      <br/><sub>Web Framework</sub>
    </td>
    <td align="center" width="120">
      <img src="https://cdn.prod.website-files.com/6614831e77e9646455248094/6614831e77e96464552480ed_groq-logo-icon.png" width="48" height="48" alt="Groq"/>
      <br/><strong>Groq</strong>
      <br/><sub>LLM Inference</sub>
    </td>
    <td align="center" width="120">
      <img src="https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg" width="48" height="48" alt="LLM"/>
      <br/><strong>Llama 3.1</strong>
      <br/><sub>AI Model</sub>
    </td>
    <td align="center" width="120">
      <img src="https://pyfpdf.github.io/fpdf2/fpdf2-logo.png" width="48" height="48" alt="FPDF2"/>
      <br/><strong>FPDF2</strong>
      <br/><sub>PDF Generation</sub>
    </td>
  </tr>
</table>

---

## 🎨 UI Design

The interface follows a **Claude-inspired light theme** with:

- **Typography:** Inter (sans-serif) for body, Newsreader (serif) for headings
- **Accent Color:** `#D97757` — Warm terracotta/clay
- **Cards:** White cards with subtle borders and box shadows
- **Inputs:** Rounded 10px borders with accent focus states
- **Tabs:** Minimal tab bar with accent underline for active state

---

## 🌐 Deployment

### Option 1: Streamlit Community Cloud (Recommended — Free)

This is the easiest and fastest way to deploy:

**Step 1:** Push your code to GitHub (already done ✅)

**Step 2:** Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.

**Step 3:** Click **"New app"** and configure:

| Field | Value |
|---|---|
| Repository | `PriyanshuCP42/Course_Architect_Agent` |
| Branch | `main` |
| Main file path | `app.py` |

**Step 4:** Click **"Advanced settings"** and add your secret:

```toml
[general]

GROQ_API_KEY = "gsk_your_actual_key_here"
```

**Step 5:** Click **"Deploy!"** — Your app will be live at:
```
https://course-architect-agent.streamlit.app
```

> ⚠️ **Important:** Never commit your `.env` file. On Streamlit Cloud, use the **Secrets** panel instead. Update `agents.py` line 8 to also read from Streamlit secrets:
> ```python
> GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
> ```

---

### Option 2: Railway / Render (Free Tier Available)

**Step 1:** Sign up at [railway.app](https://railway.app) or [render.com](https://render.com).

**Step 2:** Connect your GitHub repository.

**Step 3:** Set the **Start Command**:
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

**Step 4:** Add the environment variable:
```
GROQ_API_KEY=gsk_your_key_here
```

**Step 5:** Deploy. The platform will auto-detect Python and install dependencies from `requirements.txt`.

---

### Option 3: Docker (Self-Hosted)

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

## ⚙️ Configuration

| Environment Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Your Groq API key from [console.groq.com](https://console.groq.com) |

### Model Configuration

The default model is `llama-3.1-8b-instant` (optimized for Groq free tier). To change it, edit `agents.py`:

```python
MODEL = "llama-3.1-8b-instant"  # Change to any Groq-supported model
```

---

## 📊 How It Works

1. **Paste** your raw content (notes, textbook excerpts, research material)
2. **Configure** course parameters: audience, duration, class size, learning outcomes
3. **Generate** — The 4-agent pipeline processes your content:
   - 🏗️ Agent 1 designs the curriculum structure
   - 📖 Agent 2 writes detailed lesson content for each lesson
   - 🧪 Agent 3 creates assessments and quizzes
   - 🏆 Agent 4 designs capstone projects with rubrics
4. **Explore** the results across four interactive tabs
5. **Export** a professional PDF document of the complete course

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Priyanshu Agrahari**

- GitHub: [@PriyanshuCP42](https://github.com/PriyanshuCP42)

---

<p align="center">
  <sub>Built with ❤️ using Streamlit, Groq, and Llama 3.1</sub>
</p>
