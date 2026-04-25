import streamlit as st
import json
import textwrap
import re
from constants import *
from agents import build_complete_course
from pdf_generator import generate_course_pdf

st.set_page_config(
    page_title="Course Architect",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Theme definitions
c_bg_page = "#FAFAFA"
c_bg_card = "#FFFFFF"
c_input_bg = "#FFFFFF"
c_border = "#E5E7EB"
c_text_primary = "#0F172A"
c_text_secondary = "#475569"
c_text_muted = "#94A3B8"
c_accent = "#D97757"
c_accent_hover = "#C46243"
c_accent_bg = "#FDF4F1"
c_accent_border = "#F2D5CB"
c_item_bg = "#F8FAFC"
c_item_border = "#E2E8F0"

# Claude-inspired CSS Theme
css = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&display=swap');

* {{ 
    font-family: 'Inter', system-ui, sans-serif; 
}}

.stApp {{ 
    background-color: {c_bg_page}; 
}}

/* Push header upward */
.block-container {{
    padding-top: 2rem !important;
}}

/* Hide Streamlit default elements */
#MainMenu, footer, header {{ visibility: hidden; }}

h1, h2, h3, .serif {{
    font-family: 'Newsreader', serif !important;
}}

/* Primary button - Claude Clay */
.stButton > button[kind="primary"] {{
    background: {c_accent};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 500;
    font-size: 15px;
    transition: background 0.2s ease;
}}
.stButton > button[kind="primary"]:hover {{
    background: {c_accent_hover};
    color: white;
}}

/* Text area & Selectbox */
.stTextArea textarea, .stSelectbox > div > div, .stTextInput input {{
    border-radius: 10px;
    border: 1px solid {c_border};
    font-size: 15px;
    line-height: 1.6;
    background: {c_input_bg} !important;
    color: {c_text_primary} !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}}
.stTextArea textarea::placeholder, .stTextInput input::placeholder {{
    color: {c_text_muted} !important;
    opacity: 1;
}}
.stTextArea textarea:focus, .stSelectbox > div > div:focus-within, .stTextInput input:focus {{
    border-color: {c_accent} !important;
    box-shadow: 0 0 0 1px {c_accent} !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    background: transparent;
    border-bottom: 1px solid {c_border};
    gap: 24px;
    padding-bottom: 0px;
}}
.stTabs [data-baseweb="tab"] {{
    font-weight: 500;
    color: {c_text_secondary};
    padding: 12px 0px;
    border-bottom: 2px solid transparent;
}}
.stTabs [aria-selected="true"] {{
    color: {c_text_primary} !important;
    border-bottom: 2px solid {c_accent} !important;
    background: transparent !important;
}}

/* Expander */
.streamlit-expanderHeader {{
    background: {c_bg_card};
    border-radius: 8px;
    font-weight: 500;
    color: {c_text_primary};
    border: 1px solid {c_border};
}}

/* Cards */
.claude-card {{
    background: {c_bg_card};
    border: 1px solid {c_border};
    border-radius: 12px;
    padding: 32px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.01), 0 4px 6px rgba(0,0,0,0.01);
}}
"""
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# SECTION 1: HEADER
col_title, col_badges = st.columns([2, 1])

with col_title:
    st.markdown(f"""
    <div style="padding: 12px 0 12px 0;">
      <div class="serif" style="font-size: 36px; font-weight: 500; color: {c_text_primary}; letter-spacing: -0.5px;">
        Course Architect
      </div>
      <div style="font-size: 16px; color: {c_text_secondary}; margin-top: 4px; font-weight: 400;">
        Design structurally sound, pedagogically rich learning experiences.
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_badges:
    st.markdown(f"""
    <div style="display: flex; gap: 8px; justify-content: flex-end; align-items: center; padding-top: 24px; margin-bottom: 8px;">
      <span style="background: {c_accent_bg}; color: {c_accent}; font-size: 12px;
                   font-weight: 500; padding: 4px 12px; border-radius: 6px; border: 1px solid {c_accent_border};">
        Powered by Groq
      </span>
      <span style="background: {c_item_bg}; color: {c_text_secondary}; font-size: 12px;
                   font-weight: 500; padding: 4px 12px; border-radius: 6px; border: 1px solid {c_item_border};">
        Llama 3.1
      </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"<div style='height: 1px; background: {c_border}; margin: 8px 0 32px 0;'></div>", unsafe_allow_html=True)


# SECTION 2: INPUT PANEL
with st.container():
    st.markdown(f"""
    <div class="claude-card" style="margin-bottom: 24px;">
      <div style="font-size: 18px; font-weight: 600; color: {c_text_primary}; margin-bottom: 8px;">
        Source Material
      </div>
      <div style="font-size: 14px; color: {c_text_secondary}; margin-bottom: 16px;">
        Provide the foundational text, textbook chapters, or raw concepts you wish to synthesize into a structured course.
      </div>
    """, unsafe_allow_html=True)

    raw_notes = st.text_area(
        label="Raw Content",
        label_visibility="collapsed",
        height=200,
        placeholder="Paste your raw content here...",
        key="raw_notes_input"
    )

    st.markdown(f"<div style='font-size: 16px; font-weight: 600; color: {c_text_primary}; margin-top: 24px; margin-bottom: 16px;'>Course Parameters</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        target_audience = st.selectbox(
            "Target Audience",
            ["Beginners", "Intermediate Learners", "Advanced Professionals", "College Students", "Corporate Teams", "Hobbyists"]
        )
    with col2:
        course_duration = st.selectbox(
            "Course Duration",
            ["1 Week", "2 Weeks", "1 Month", "2 Months", "3 Months", "6 Months", "1 Year"]
        )
    with col3:
        class_size = st.selectbox(
            "Class Size",
            ["1-10 (Small Group)", "10-30 (Classroom)", "30-100 (Lecture)", "100+ (Massive Online)"]
        )
        
    col4, col5 = st.columns(2)
    with col4:
        desired_outcomes = st.text_area("Learning Outcomes", placeholder="What specific skills or knowledge should students acquire?", height=80)
    with col5:
        engaging_materials = st.text_area("Pedagogical Elements", placeholder="e.g. Case studies, role-playing, interactive coding, Socratic questioning...", height=80)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    col_btn, col_hint = st.columns([1, 3])
    with col_btn:
        run_button = st.button("Generate Course", type="primary", key="run_btn", use_container_width=True)
    with col_hint:
        st.markdown(f"""
        <div style="padding-top: 10px; font-size: 14px; color: {c_text_muted};">
          Synthesizing curriculum structure, pedagogical lessons, cognitive assessments, and practical projects...
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# SECTION 3: SESSION STATE INIT
def init_state():
    defaults = {
        "course":        None,
        "is_running":    False,
        "is_complete":   False,
        "active_module": 0,
        "active_lesson": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def clean_html(html_str):
    return re.sub(r'^[ \t]+', '', html_str, flags=re.MULTILINE)

# RENDER FUNCTIONS
def render_course_hero(curriculum: dict):
    modules = curriculum.get("modules", [])
    total_lessons = sum(len(m.get("lessons", [])) for m in modules)

    st.markdown(f"""
    <div class="claude-card" style="margin-bottom: 32px; border-top: 4px solid {c_accent}; padding: 40px;">
      <div style="font-size: 12px; font-weight: 600; color: {c_accent}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">
        Course Overview
      </div>
      <div class="serif" style="font-size: 32px; font-weight: 500; color: {c_text_primary}; margin-bottom: 8px;">
        {curriculum.get('course_title', 'Untitled Course')}
      </div>
      <div style="font-size: 18px; color: {c_text_secondary}; margin-bottom: 32px;">
        {curriculum.get('course_subtitle', '')}
      </div>

      <div style="display: flex; gap: 40px; flex-wrap: wrap; margin-bottom: 24px;">
        <div>
          <div style="font-size: 28px; font-weight: 600; color: {c_text_primary};">{curriculum.get('total_weeks', '?')}</div>
          <div style="font-size: 12px; color: {c_text_muted}; text-transform: uppercase; letter-spacing: 0.5px;">Weeks</div>
        </div>
        <div style="width: 1px; background: {c_border};"></div>
        <div>
          <div style="font-size: 28px; font-weight: 600; color: {c_text_primary};">{curriculum.get('total_hours', '?')}</div>
          <div style="font-size: 12px; color: {c_text_muted}; text-transform: uppercase; letter-spacing: 0.5px;">Hours</div>
        </div>
        <div style="width: 1px; background: {c_border};"></div>
        <div>
          <div style="font-size: 28px; font-weight: 600; color: {c_text_primary};">{len(modules)}</div>
          <div style="font-size: 12px; color: {c_text_muted}; text-transform: uppercase; letter-spacing: 0.5px;">Modules</div>
        </div>
        <div style="width: 1px; background: {c_border};"></div>
        <div>
          <div style="font-size: 28px; font-weight: 600; color: {c_text_primary};">{total_lessons}</div>
          <div style="font-size: 12px; color: {c_text_muted}; text-transform: uppercase; letter-spacing: 0.5px;">Lessons</div>
        </div>
      </div>

      <div style="display: flex; gap: 12px; flex-wrap: wrap; align-items: center; border-top: 1px solid {c_border}; padding-top: 24px;">
        <span style="background: {c_item_bg}; color: {c_text_secondary}; font-size: 13px; font-weight: 500; padding: 6px 14px; border-radius: 6px;">
          Difficulty: {curriculum.get('difficulty_level', '')}
        </span>
        <span style="background: {c_item_bg}; color: {c_text_secondary}; font-size: 13px; font-weight: 500; padding: 6px 14px; border-radius: 6px;">
          Audience: {curriculum.get('target_audience', '')}
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

def render_curriculum_tab(curriculum: dict):
    col_left, col_right = st.columns([1, 2])
    with col_left:
        outcomes_html = "".join(f"<li style='margin-bottom: 8px;'>{outcome}</li>" for outcome in curriculum.get("course_outcomes", []))
        prereqs = ", ".join(curriculum.get("prerequisites", ["None required"]))
        st.markdown(f"""
        <div class="claude-card">
          <div class="serif" style="font-size: 20px; font-weight: 500; color: {c_text_primary}; margin-bottom: 16px;">
            Expected Outcomes
          </div>
          <ul style="color: {c_text_secondary}; font-size: 15px; padding-left: 20px; line-height: 1.6;">
            {outcomes_html}
          </ul>
          <div style="border-top: 1px solid {c_border}; margin: 24px 0;"></div>
          <div class="serif" style="font-size: 20px; font-weight: 500; color: {c_text_primary}; margin-bottom: 12px;">
            Prerequisites
          </div>
          <div style="color: {c_text_secondary}; font-size: 15px; line-height: 1.6;">
            {prereqs}
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_right:
        modules = curriculum.get("modules", [])
        for i, module in enumerate(modules):
            lessons = module.get("lessons", [])
            total_time = sum(l.get("duration_minutes", 0) for l in lessons)
            
            lessons_html = ""
            for l in lessons:
                lessons_html += f"<div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px; font-size: 14px; padding: 12px; background: {c_item_bg}; border-radius: 8px; border: 1px solid {c_item_border};'><span style='font-weight: 600; color: {c_text_secondary}; width: 50px;'>{l.get('lesson_id', '')}</span><span style='color: {c_text_primary}; font-weight: 500;'>{l.get('title', '')}</span><span style='color: {c_text_muted}; margin-left: auto;'>{l.get('duration_minutes', 0)} mins</span></div>"
                
            block = f"""
            <div class="claude-card" style="margin-bottom: 24px; padding: 32px; border-left: 4px solid {c_item_border};">
              <div style="display: flex; gap: 12px; margin-bottom: 16px; align-items: center;">
                <span style="background: {c_item_bg}; color: {c_text_secondary}; font-size: 12px; padding: 4px 10px; border-radius: 4px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Week {module.get('week', '')}</span>
                <span style="color: {c_text_muted}; font-size: 13px; font-weight: 500;">Module {module.get('module_id', '')}</span>
              </div>
              <div class="serif" style="font-size: 22px; font-weight: 600; color: {c_text_primary}; margin-bottom: 8px;">{module.get('title', '')}</div>
              <div style="font-size: 15px; color: {c_text_secondary}; margin-bottom: 24px; line-height: 1.6;">{module.get('module_goal', '')}</div>
              <div style="margin-bottom: 24px;">
                {lessons_html}
              </div>
              <div style="font-size: 14px; color: {c_text_muted}; font-weight: 500; border-top: 1px solid {c_item_bg}; padding-top: 16px;">
                {len(lessons)} lessons · {total_time} mins
              </div>
            </div>
            """
            st.markdown(clean_html(block), unsafe_allow_html=True)


def render_lessons_tab(curriculum: dict):
    col_left, col_right = st.columns([1, 2.5])
    modules = curriculum.get("modules", [])
    if not modules:
        return
    
    with col_left:
        st.markdown(f"<div style='font-weight: 600; color: {c_text_primary}; margin-bottom: 16px; font-size: 16px;'>Course Navigator</div>", unsafe_allow_html=True)
        for m_idx, module in enumerate(modules):
            with st.expander(f"{module.get('module_id', '')}: {module.get('title', '')}", expanded=(m_idx == st.session_state.get('active_module', 0))):
                for l_idx, lesson in enumerate(module.get("lessons", [])):
                    if st.button(f"{lesson.get('lesson_id')} - {lesson.get('title', '')}", key=f"btn_{m_idx}_{l_idx}", use_container_width=True):
                        st.session_state.active_module = m_idx
                        st.session_state.active_lesson = l_idx

    active_m = st.session_state.get("active_module", 0)
    active_l = st.session_state.get("active_lesson", 0)
    if active_m < len(modules) and active_l < len(modules[active_m].get("lessons", [])):
        lesson = modules[active_m]["lessons"][active_l]
        module = modules[active_m]
        with col_right:
            block = f"""
            <div style="margin-bottom: 32px;">
              <div style="display: flex; gap: 8px; margin-bottom: 16px;">
                <span style="background: {c_item_bg}; color: {c_text_secondary}; font-size: 12px; padding: 4px 10px; border-radius: 4px; font-weight: 600;">{lesson.get('lesson_id', '')}</span>
                <span style="background: {c_item_bg}; color: {c_text_secondary}; font-size: 12px; padding: 4px 10px; border-radius: 4px; font-weight: 600; text-transform: capitalize;">{lesson.get('lesson_type', 'concept')}</span>
              </div>
              <div class="serif" style="font-size: 32px; font-weight: 600; color: {c_text_primary}; margin-bottom: 12px;">{lesson.get('title', '')}</div>
              <div style="font-size: 15px; color: {c_text_muted};">{lesson.get('duration_minutes', 0)} min · Part of: {module.get('title', '')}</div>
            </div>
            
            <div class="claude-card" style="margin-bottom: 24px; padding: 32px;">
              <div class="serif" style="font-size: 20px; font-weight: 600; color: {c_text_primary}; margin-bottom: 16px;">Introduction</div>
              <div style="font-size: 16px; color: {c_text_secondary}; line-height: 1.7;">{lesson.get('content', {}).get('introduction', 'No introduction provided.')}</div>
            </div>

            <div class="claude-card" style="margin-bottom: 24px; padding: 32px;">
              <div class="serif" style="font-size: 20px; font-weight: 600; color: {c_text_primary}; margin-bottom: 16px;">Core Explanation</div>
              <div style="font-size: 16px; color: {c_text_secondary}; line-height: 1.7; white-space: pre-wrap;">{lesson.get('content', {}).get('core_explanation', 'No core explanation provided.')}</div>
            </div>

            <div class="claude-card" style="margin-bottom: 24px; padding: 32px;">
              <div class="serif" style="font-size: 20px; font-weight: 600; color: {c_text_primary}; margin-bottom: 16px;">Key Takeaways</div>
              <ul style="color: {c_text_secondary}; font-size: 16px; padding-left: 20px; line-height: 1.7;">
                {"".join(f"<li style='margin-bottom: 8px;'>{pt}</li>" for pt in lesson.get('content', {}).get("key_points", []))}
              </ul>
            </div>

            <div class="claude-card" style="margin-bottom: 24px; padding: 32px; background: {c_bg_page}; border: 1px solid {c_border};">
              <div class="serif" style="font-size: 20px; font-weight: 600; color: {c_text_primary}; margin-bottom: 16px;">Real-World Application</div>
              <div style="font-size: 16px; color: {c_text_secondary}; line-height: 1.7;">{lesson.get('content', {}).get('real_world_application', 'No real-world application provided.')}</div>
            </div>

            <div class="claude-card" style="margin-bottom: 24px; padding: 32px; border-left: 4px solid {c_accent};">
              <div class="serif" style="font-size: 20px; font-weight: 600; color: {c_text_primary}; margin-bottom: 16px;">Lesson Summary</div>
              <div style="font-size: 16px; color: {c_text_secondary}; line-height: 1.7;">{lesson.get('content', {}).get('summary', 'No summary provided.')}</div>
            </div>
            """
            st.markdown(clean_html(block), unsafe_allow_html=True)


def render_assessments_tab(assessments: dict):
    total_q = assessments.get("total_questions", 0)
    total_mq = len(assessments.get("module_assessments", []))
    final_e = 1 if "final_exam" in assessments else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='claude-card' style='text-align: center; padding: 24px;'><div style='font-size: 32px; font-weight: 600; color: {c_text_primary};'>{total_q}</div><div style='font-size: 14px; color: {c_text_muted};'>Total Questions</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='claude-card' style='text-align: center; padding: 24px;'><div style='font-size: 32px; font-weight: 600; color: {c_text_primary};'>{total_mq}</div><div style='font-size: 14px; color: {c_text_muted};'>Module Quizzes</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='claude-card' style='text-align: center; padding: 24px;'><div style='font-size: 32px; font-weight: 600; color: {c_text_primary};'>{final_e}</div><div style='font-size: 14px; color: {c_text_muted};'>Final Exam</div></div>", unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)

    module_assessments = assessments.get("module_assessments", [])
    if module_assessments:
        module_names = [mq.get("module_title", f"Module {i+1}") for i, mq in enumerate(module_assessments)]
        selected_mod_name = st.selectbox("Select Assessment to View", module_names)
        selected_mq = next((mq for mq in module_assessments if mq.get("module_title") == selected_mod_name), None)
        
        if selected_mq:
            st.markdown(f"<div class='serif' style='font-size: 24px; font-weight: 600; color: {c_text_primary}; margin: 32px 0 24px 0;'>{selected_mq.get('module_title')} Quiz</div>", unsafe_allow_html=True)
            
            questions = []
            for q in selected_mq.get("mcq", []):
                q["type"] = "mcq"
                questions.append(q)
            for q in selected_mq.get("short_answer", []):
                q["type"] = "short_answer"
                questions.append(q)
            if selected_mq.get("scenario"):
                q = selected_mq.get("scenario")
                q["type"] = "scenario"
                questions.append(q)

            for i, q in enumerate(questions):
                q_type = q.get("type", "mcq")
                difficulty = q.get("difficulty", "Medium")
                
                border_left = f"border-left: 4px solid {c_accent};" if q_type == "scenario" else f"border-left: 4px solid {c_border};"
                block = f"""
                <div class="claude-card" style="padding: 24px; margin-bottom: 16px; {border_left}">
                  <div style="display: flex; gap: 8px; margin-bottom: 16px;">
                    <span style="background: {c_item_bg}; color: {c_text_secondary}; font-size: 12px; padding: 4px 10px; border-radius: 4px; font-weight: 600;">Q{i+1}</span>
                    <span style="background: {c_item_bg}; color: {c_text_secondary}; font-size: 12px; padding: 4px 10px; border-radius: 4px; font-weight: 500;">{difficulty}</span>
                    <span style="background: {c_item_bg}; color: {c_text_secondary}; font-size: 12px; padding: 4px 10px; border-radius: 4px; font-weight: 500; text-transform: uppercase;">{q_type.replace('_', ' ')}</span>
                  </div>
                """
                st.markdown(clean_html(block), unsafe_allow_html=True)
                
                if q_type == "scenario":
                    st.markdown(f"<div style='font-size: 15px; color: {c_text_secondary}; margin-bottom: 16px; background: {c_bg_page}; padding: 16px; border-radius: 8px;'><strong>Scenario:</strong> {q.get('scenario_text', '')}</div>", unsafe_allow_html=True)
                
                st.markdown(f"<div style='font-size: 17px; font-weight: 500; color: {c_text_primary}; margin-bottom: 20px; line-height: 1.5;'>{q.get('question_text', '')}</div>", unsafe_allow_html=True)
                
                if q_type == "mcq":
                    options = q.get("options", {})
                    if isinstance(options, list):
                        options = {chr(65+k): v for k, v in enumerate(options)}
                    for key, val in options.items():
                        st.markdown(f"<div style='font-size: 15px; color: {c_text_secondary}; padding: 12px 16px; border: 1px solid {c_item_border}; border-radius: 8px; margin-bottom: 8px; background: {c_bg_page};'><strong>{key}</strong>. {val}</div>", unsafe_allow_html=True)
                    with st.expander("Show Answer & Explanation"):
                        st.markdown(f"**Correct Answer:** {q.get('correct_answer', '')}")
                        st.markdown(f"**Explanation:** {q.get('explanation', '')}")
                elif q_type in ["short_answer", "scenario"]:
                    with st.expander("Show Ideal Model Answer"):
                        st.markdown(q.get("model_answer", ""))
                    with st.expander("Show Evaluator Scoring Guide"):
                        st.markdown(q.get("scoring_guide", ""))
                
                st.markdown("</div>", unsafe_allow_html=True)


def render_projects_tab(projects: list):
    for project in projects:
        difficulty = project.get("difficulty", "Guided")
        
        deliv_html = ""
        for d in project.get("deliverables", []):
            ac_list = "".join(f"<li style='margin-bottom: 4px;'>{c}</li>" for c in d.get("acceptance_criteria", []))
            deliv_html += f"<div style='border: 1px solid {c_item_border}; border-radius: 8px; padding: 20px; background: {c_bg_page};'><div style='font-size: 16px; font-weight: 600; color: {c_text_primary}; margin-bottom: 8px;'>{d.get('title', '')}</div><div style='font-size: 15px; color: {c_text_secondary}; margin-bottom: 12px;'>{d.get('description', '')}</div><div style='font-size: 13px; font-weight: 600; color: {c_text_secondary}; margin-bottom: 6px;'>Acceptance Criteria:</div><ul style='font-size: 14px; color: {c_text_secondary}; padding-left: 20px; margin: 0;'>{ac_list}</ul></div>"
        
        reqs_html = "".join(f"<li style='margin-bottom: 6px;'>{req}</li>" for req in project.get("technical_requirements", []))
        tools_html = "".join(f"<span style='background: {c_item_bg}; color: {c_text_secondary}; font-size: 13px; padding: 6px 12px; border-radius: 6px; border: 1px solid {c_item_border};'>{tool}</span>" for tool in project.get("tools_and_technologies", []))
        
        rubric_html = ""
        total_pts = 0
        for r in project.get("evaluation_rubric", []):
            pts = r.get("points", 0)
            total_pts += pts
            rubric_html += f"<tr style='border-bottom: 1px solid {c_item_border};'><td style='padding: 16px; color: {c_text_primary}; font-weight: 500;'>{r.get('criterion', '')}</td><td style='padding: 16px; color: {c_accent}; font-weight: 600;'>{pts}</td><td style='padding: 16px; color: {c_text_secondary};'>{r.get('excellent', '')}</td><td style='padding: 16px; color: {c_text_secondary};'>{r.get('satisfactory', '')}</td><td style='padding: 16px; color: {c_text_secondary};'>{r.get('needs_work', '')}</td></tr>"

        block = f"""
        <div class="claude-card" style="margin-bottom: 32px; padding: 0; overflow: hidden;">
          <div style="background: {c_item_bg}; padding: 32px; border-bottom: 1px solid {c_item_border};">
            <div style="display: flex; gap: 8px; margin-bottom: 16px;">
              <span style="background: {c_item_border}; color: {c_text_secondary}; font-size: 12px; padding: 4px 10px; border-radius: 4px; font-weight: 600;">{project.get('project_id', 'Project')}</span>
              <span style="background: {c_item_border}; color: {c_text_secondary}; font-size: 12px; padding: 4px 10px; border-radius: 4px; font-weight: 600;">{difficulty}</span>
              <span style="background: {c_item_border}; color: {c_text_secondary}; font-size: 12px; padding: 4px 10px; border-radius: 4px; font-weight: 600;">Assigned Week: {project.get('assigned_week', '')}</span>
            </div>
            <div class="serif" style="font-size: 28px; font-weight: 600; color: {c_text_primary}; margin-bottom: 8px;">{project.get('title', '')}</div>
            <div style="font-size: 16px; color: {c_text_secondary};">{project.get('tagline', '')}</div>
          </div>
          
          <div style="padding: 32px;">
            <div style="background: {c_bg_card}; border: 1px solid {c_item_border}; border-radius: 8px; padding: 24px; margin-bottom: 32px;">
              <div class="serif" style="font-size: 18px; font-weight: 600; color: {c_text_primary}; margin-bottom: 12px;">Problem Statement</div>
              <div style="font-size: 16px; color: {c_text_secondary}; line-height: 1.6;">{project.get('problem_statement', '')}</div>
            </div>
            
            <div class="serif" style="font-size: 20px; font-weight: 600; color: {c_text_primary}; margin-bottom: 20px;">Deliverables</div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 32px;">
              {deliv_html}
            </div>
            
            <div style="display: flex; gap: 32px; margin-bottom: 32px; flex-wrap: wrap;">
              <div style="flex: 1; min-width: 300px;">
                <div class="serif" style="font-size: 20px; font-weight: 600; color: {c_text_primary}; margin-bottom: 16px;">Technical Requirements</div>
                <ul style="font-size: 15px; color: {c_text_secondary}; padding-left: 20px; line-height: 1.6;">
                  {reqs_html}
                </ul>
              </div>
              <div style="flex: 1; min-width: 300px;">
                <div class="serif" style="font-size: 20px; font-weight: 600; color: {c_text_primary}; margin-bottom: 16px;">Tools & Technologies</div>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                  {tools_html}
                </div>
              </div>
            </div>
            
            <div class="serif" style="font-size: 20px; font-weight: 600; color: {c_text_primary}; margin-bottom: 16px;">Evaluation Rubric</div>
            <div style="overflow-x: auto;">
              <table style="width: 100%; border-collapse: collapse; font-size: 15px; margin-bottom: 32px; text-align: left; min-width: 600px;">
                <thead>
                  <tr style="background: {c_item_bg}; border-bottom: 2px solid {c_item_border};">
                    <th style="padding: 16px; color: {c_text_secondary}; font-weight: 600;">Criterion</th>
                    <th style="padding: 16px; color: {c_text_secondary}; font-weight: 600;">Points</th>
                    <th style="padding: 16px; color: {c_text_secondary}; font-weight: 600;">Excellence Standard</th>
                    <th style="padding: 16px; color: {c_text_secondary}; font-weight: 600;">Satisfactory</th>
                    <th style="padding: 16px; color: {c_text_secondary}; font-weight: 600;">Needs Work</th>
                  </tr>
                </thead>
                <tbody>
                  {rubric_html}
                  <tr style="background: {c_item_bg}; font-weight: 600; border-top: 2px solid {c_item_border};">
                    <td style="padding: 16px; color: {c_text_primary};">Total Points</td>
                    <td style="padding: 16px; color: {c_accent};">{total_pts}</td>
                    <td colspan="3"></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        """
        st.markdown(clean_html(block), unsafe_allow_html=True)

def render_download_section(course: dict, curriculum: dict):
    st.markdown(f"<div style='height: 1px; background: {c_border}; margin: 40px 0;'></div>", unsafe_allow_html=True)
    col_dl, col_info = st.columns([1, 2])

    with col_dl:
        try:
            pdf_bytes = generate_course_pdf(course)
            st.download_button(
                label="⬇ Download Course Architecture (PDF)",
                data=pdf_bytes,
                file_name=f"{curriculum.get('course_title', 'course').replace(' ', '_')}.pdf",
                mime="application/pdf",
                key="download_btn",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Could not generate PDF. Please try again.")

    with col_info:
        st.markdown(f"""
        <div style="padding-top: 8px; font-size: 14px; color: {c_text_muted};">
          Export the entire project architecture in a structured PDF for future reference, including the complete curriculum, lesson texts, assessment banks, and resume-worthy projects.
        </div>
        """, unsafe_allow_html=True)

def render_results(curriculum: dict, assessments: dict, projects: list):
    render_course_hero(curriculum)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Curriculum & Timeline",
        "Lesson Content",
        "Assessments",
        "Projects"
    ])

    with tab1:
        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        render_curriculum_tab(curriculum)

    with tab2:
        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        render_lessons_tab(curriculum)

    with tab3:
        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        render_assessments_tab(assessments)

    with tab4:
        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        render_projects_tab(projects)

    render_download_section(st.session_state.course, curriculum)


# 6. Run logic
if run_button:
    if not raw_notes or len(raw_notes.strip()) < 50:
        st.warning("Please paste at least a few sentences of content to generate a meaningful course.")
    else:
        st.session_state.is_running  = True
        st.session_state.is_complete = False
        st.session_state.course      = None

        with st.spinner("Synthesizing curriculum structure..."):
            try:
                result = build_complete_course(
                    raw_notes=raw_notes,
                    target_audience=target_audience,
                    course_duration=course_duration,
                    class_size=class_size,
                    desired_outcomes=desired_outcomes,
                    engaging_materials=engaging_materials
                )
                st.session_state.course      = result
                st.session_state.is_complete = True
            except Exception as e:
                st.error(f"Something went wrong. Please check your API key and try again. ({str(e)})")
            finally:
                st.session_state.is_running = False

        if st.session_state.is_complete:
            st.rerun()


# 7. Render full results
if st.session_state.is_complete and st.session_state.course:
    course      = st.session_state.course
    curriculum  = course.get("curriculum", {})
    assessments = course.get("assessments", {})
    projects    = course.get("projects", [])

    render_results(curriculum, assessments, projects)
