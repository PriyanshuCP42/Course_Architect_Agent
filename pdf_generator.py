import json
from fpdf import FPDF

# ─── Claude Light Theme Colors ───
C_ACCENT     = (217, 119, 87)   # #D97757 — Clay/Terracotta
C_PRIMARY    = (15, 23, 42)     # #0F172A — Deep ink
C_SECONDARY  = (71, 85, 105)    # #475569 — Muted text
C_MUTED      = (148, 163, 184)  # #94A3B8 — Subtle labels
C_BG_LIGHT   = (248, 250, 252)  # #F8FAFC — Card background
C_BORDER     = (226, 232, 240)  # #E2E8F0 — Dividers
C_WHITE      = (255, 255, 255)


def sanitize(text):
    """Clean text for latin-1 PDF encoding."""
    if not text:
        return ""
    text = str(text)
    replacements = {
        '\u201c': '"', '\u201d': '"', '\u2018': "'", '\u2019': "'",
        '\u2013': '-', '\u2014': '--', '\u2026': '...', '\u2022': '-',
        '\u00b7': '-', '\u2019': "'",
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    return text.encode('latin-1', 'replace').decode('latin-1')


class CoursePDF(FPDF):
    """Professional PDF with Claude-inspired light theme."""

    def header(self):
        if self.page_no() == 1:
            return  # Cover page has no header
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*C_MUTED)
        self.cell(95, 6, self._header_title, 0, 0, 'L')
        self.cell(95, 6, 'Course Architecture Reference', 0, 0, 'R')
        self.ln(4)
        # Accent line
        self.set_draw_color(*C_ACCENT)
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*C_MUTED)
        self.cell(0, 10, f'Page {self.page_no() - 1}', 0, 0, 'C')

    # ─── Helper Methods ───

    def accent_bar(self, y=None):
        """Draw a thin accent bar across the page."""
        if y is None:
            y = self.get_y()
        self.set_draw_color(*C_ACCENT)
        self.set_line_width(0.4)
        self.line(10, y, 200, y)
        self.ln(6)

    def subtle_divider(self):
        """Draw a light gray divider."""
        self.set_draw_color(*C_BORDER)
        self.set_line_width(0.2)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def section_heading(self, title):
        """Large section heading with accent underline."""
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(*C_PRIMARY)
        self.cell(190, 10, sanitize(title), ln=True)
        self.accent_bar()
        self.ln(2)

    def module_heading(self, label, title):
        """Module heading with colored label chip."""
        # Label chip
        self.set_fill_color(*C_ACCENT)
        self.set_text_color(*C_WHITE)
        self.set_font('Helvetica', 'B', 9)
        label_text = sanitize(label)
        label_w = self.get_string_width(label_text) + 10
        self.cell(label_w, 7, label_text, 0, 0, 'C', fill=True)
        self.ln(10)
        # Title
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(*C_PRIMARY)
        self.cell(190, 8, sanitize(title), ln=True)
        self.ln(2)

    def sub_heading(self, title):
        """Sub-section heading."""
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(*C_PRIMARY)
        self.cell(190, 7, sanitize(title), ln=True)
        self.ln(2)

    def label_text(self, label):
        """Small bold label like 'Introduction:' or 'Key Takeaways:'."""
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*C_ACCENT)
        self.cell(190, 6, sanitize(label), ln=True)
        self.ln(1)

    def body(self, text):
        """Standard body text."""
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*C_SECONDARY)
        self.multi_cell(190, 5.5, sanitize(text))
        self.ln(3)

    def bullet(self, text):
        """Indented bullet point."""
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*C_SECONDARY)
        x = self.get_x()
        self.cell(6, 5.5, '-', 0, 0)
        self.multi_cell(184, 5.5, sanitize(text))
        self.ln(1)

    def info_row(self, label, value):
        """Key-value row for metadata."""
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*C_PRIMARY)
        self.cell(45, 6, sanitize(label), 0, 0)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*C_SECONDARY)
        self.cell(145, 6, sanitize(str(value)), 0, 1)


# ─── PDF Generation ───

def generate_course_pdf(course: dict) -> bytes:
    pdf = CoursePDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    curriculum  = course.get("curriculum", {})
    assessments = course.get("assessments", {})
    projects    = course.get("projects", [])
    modules     = curriculum.get("modules", [])
    total_lessons = sum(len(m.get("lessons", [])) for m in modules)

    course_title = sanitize(curriculum.get("course_title", "Untitled Course"))
    pdf._header_title = course_title

    # ════════════════════════════════════════════
    #  COVER PAGE
    # ════════════════════════════════════════════
    pdf.add_page()

    # Top accent stripe
    pdf.set_fill_color(*C_ACCENT)
    pdf.rect(0, 0, 210, 6, 'F')

    # Vertical spacer
    pdf.ln(55)

    # Small label
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*C_ACCENT)
    pdf.cell(190, 6, 'COURSE ARCHITECTURE', 0, 1, 'C')
    pdf.ln(4)

    # Course title
    pdf.set_font('Helvetica', 'B', 30)
    pdf.set_text_color(*C_PRIMARY)
    pdf.multi_cell(190, 13, course_title, align='C')
    pdf.ln(4)

    # Subtitle
    pdf.set_font('Helvetica', 'I', 14)
    pdf.set_text_color(*C_SECONDARY)
    pdf.multi_cell(190, 8, sanitize(curriculum.get("course_subtitle", "")), align='C')
    pdf.ln(16)

    # Stats row
    pdf.set_draw_color(*C_BORDER)
    pdf.set_line_width(0.3)
    y_top = pdf.get_y()
    pdf.line(50, y_top, 160, y_top)
    pdf.ln(6)

    stats = [
        (str(curriculum.get("total_weeks", "?")), "Weeks"),
        (str(curriculum.get("total_hours", "?")), "Hours"),
        (str(len(modules)), "Modules"),
        (str(total_lessons), "Lessons"),
    ]
    col_w = 190 / len(stats)
    for val, label in stats:
        pdf.set_font('Helvetica', 'B', 22)
        pdf.set_text_color(*C_PRIMARY)
        pdf.cell(col_w, 10, val, 0, 0, 'C')
    pdf.ln(10)
    for val, label in stats:
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(*C_MUTED)
        pdf.cell(col_w, 6, label, 0, 0, 'C')
    pdf.ln(8)

    y_bot = pdf.get_y()
    pdf.line(50, y_bot, 160, y_bot)
    pdf.ln(14)

    # Difficulty & audience chips
    diff_text = f"Difficulty: {curriculum.get('difficulty_level', '?')}    |    Audience: {curriculum.get('target_audience', '?')}"
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*C_SECONDARY)
    pdf.cell(190, 6, sanitize(diff_text), 0, 1, 'C')

    # Bottom accent stripe
    pdf.set_fill_color(*C_ACCENT)
    pdf.rect(0, 291, 210, 6, 'F')

    # ════════════════════════════════════════════
    #  SECTION 1: OUTCOMES & PREREQUISITES
    # ════════════════════════════════════════════
    pdf.add_page()
    pdf.section_heading("Expected Outcomes")

    for outcome in curriculum.get("course_outcomes", []):
        pdf.bullet(outcome)
    pdf.ln(6)

    pdf.sub_heading("Prerequisites")
    prereqs = curriculum.get("prerequisites", [])
    if prereqs:
        for req in prereqs:
            pdf.bullet(req)
    else:
        pdf.body("No specific prerequisites required.")
    pdf.ln(8)

    # ════════════════════════════════════════════
    #  SECTION 2: CURRICULUM & LESSON CONTENT
    # ════════════════════════════════════════════
    pdf.add_page()
    pdf.section_heading("Curriculum & Lesson Content")

    for m in modules:
        pdf.module_heading(
            f"MODULE {m.get('module_id', '')}  |  WEEK {m.get('week', '')}",
            m.get('title', '')
        )

        if m.get('module_goal'):
            pdf.label_text("Module Goal")
            pdf.body(m.get('module_goal', ''))

        for l in m.get("lessons", []):
            # Lesson header card
            pdf.set_fill_color(*C_BG_LIGHT)
            pdf.rect(10, pdf.get_y(), 190, 8, 'F')
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(*C_PRIMARY)
            lesson_header = f"{l.get('lesson_id', '')}: {l.get('title', '')}  ({l.get('duration_minutes', 0)} min)"
            pdf.cell(190, 8, sanitize(lesson_header), ln=True)
            pdf.ln(3)

            content = l.get("content", {})
            if content:
                if content.get("introduction"):
                    pdf.label_text("Introduction")
                    pdf.body(content["introduction"])

                if content.get("core_explanation"):
                    pdf.label_text("Core Explanation")
                    pdf.body(content["core_explanation"])

                if content.get("key_points"):
                    pdf.label_text("Key Takeaways")
                    for pt in content["key_points"]:
                        pdf.bullet(pt)
                    pdf.ln(2)

                if content.get("real_world_application"):
                    pdf.label_text("Real-World Application")
                    pdf.body(content["real_world_application"])

                if content.get("summary"):
                    pdf.label_text("Summary")
                    pdf.body(content["summary"])

            pdf.subtle_divider()

        pdf.ln(4)

    # ════════════════════════════════════════════
    #  SECTION 3: ASSESSMENTS
    # ════════════════════════════════════════════
    if assessments:
        pdf.add_page()
        pdf.section_heading("Assessments & Quizzes")

        total_q = assessments.get("total_questions", 0)
        pdf.body(f"Total questions across all modules: {total_q}")
        pdf.ln(4)

        for mq in assessments.get("module_assessments", []):
            pdf.sub_heading(f"{mq.get('module_title', 'Module')} Quiz")
            pdf.ln(2)

            q_num = 0

            # MCQs
            for q in mq.get("mcq", []):
                q_num += 1
                diff = q.get("difficulty", "Medium")

                # Question header bar
                pdf.set_fill_color(*C_BG_LIGHT)
                pdf.rect(10, pdf.get_y(), 190, 7, 'F')
                pdf.set_font('Helvetica', 'B', 10)
                pdf.set_text_color(*C_PRIMARY)
                pdf.cell(140, 7, sanitize(f"Q{q_num}. {q.get('question_text', '')}"), ln=False)
                pdf.set_font('Helvetica', '', 8)
                pdf.set_text_color(*C_MUTED)
                pdf.cell(50, 7, sanitize(f"MCQ  |  {diff}"), 0, 1, 'R')
                pdf.ln(3)

                options = q.get("options", {})
                if isinstance(options, list):
                    options = {chr(65 + k): v for k, v in enumerate(options)}
                elif isinstance(options, str):
                    options = {"A": options}

                if isinstance(options, dict):
                    for key, val in options.items():
                        pdf.set_font('Helvetica', '', 10)
                        pdf.set_text_color(*C_SECONDARY)
                        pdf.cell(190, 5.5, sanitize(f"    {key}. {val}"), ln=True)
                    pdf.ln(2)

                pdf.set_font('Helvetica', 'B', 9)
                pdf.set_text_color(46, 125, 50)  # Green for answer
                pdf.cell(190, 5, sanitize(f"Answer: {q.get('correct_answer', '')}"), ln=True)
                pdf.set_font('Helvetica', 'I', 9)
                pdf.set_text_color(*C_SECONDARY)
                pdf.multi_cell(190, 5, sanitize(f"Explanation: {q.get('explanation', '')}"))
                pdf.ln(5)

            # Short answer
            for q in mq.get("short_answer", []):
                q_num += 1
                pdf.set_fill_color(*C_BG_LIGHT)
                pdf.rect(10, pdf.get_y(), 190, 7, 'F')
                pdf.set_font('Helvetica', 'B', 10)
                pdf.set_text_color(*C_PRIMARY)
                pdf.cell(140, 7, sanitize(f"Q{q_num}. {q.get('question_text', '')}"), ln=False)
                pdf.set_font('Helvetica', '', 8)
                pdf.set_text_color(*C_MUTED)
                pdf.cell(50, 7, "SHORT ANSWER", 0, 1, 'R')
                pdf.ln(3)

                if q.get("model_answer"):
                    pdf.set_font('Helvetica', 'I', 9)
                    pdf.set_text_color(*C_SECONDARY)
                    pdf.multi_cell(190, 5, sanitize(f"Model Answer: {q.get('model_answer', '')}"))
                    pdf.ln(4)

            # Scenario
            scenario = mq.get("scenario")
            if scenario:
                q_num += 1
                # Accent left bar for scenario
                pdf.set_fill_color(*C_ACCENT)
                pdf.rect(10, pdf.get_y(), 3, 30, 'F')

                pdf.set_x(16)
                pdf.set_font('Helvetica', 'B', 10)
                pdf.set_text_color(*C_ACCENT)
                pdf.cell(184, 6, "SCENARIO QUESTION", ln=True)

                pdf.set_x(16)
                pdf.set_font('Helvetica', 'I', 10)
                pdf.set_text_color(*C_SECONDARY)
                pdf.multi_cell(184, 5.5, sanitize(scenario.get("scenario_text", "")))
                pdf.ln(2)

                pdf.set_x(16)
                pdf.set_font('Helvetica', 'B', 10)
                pdf.set_text_color(*C_PRIMARY)
                pdf.multi_cell(184, 5.5, sanitize(f"Q: {scenario.get('question_text', '')}"))
                pdf.ln(2)

                if scenario.get("model_answer"):
                    pdf.set_x(16)
                    pdf.set_font('Helvetica', 'I', 9)
                    pdf.set_text_color(*C_SECONDARY)
                    pdf.multi_cell(184, 5, sanitize(f"Model Answer: {scenario.get('model_answer', '')}"))
                pdf.ln(6)

            pdf.subtle_divider()

    # ════════════════════════════════════════════
    #  SECTION 4: CAPSTONE PROJECTS
    # ════════════════════════════════════════════
    if projects:
        pdf.add_page()
        pdf.section_heading("Capstone Projects")

        for p in projects:
            # Project header card
            pdf.set_fill_color(*C_BG_LIGHT)
            pdf.rect(10, pdf.get_y(), 190, 22, 'F')
            pdf.set_draw_color(*C_ACCENT)
            pdf.set_line_width(0.8)
            pdf.line(10, pdf.get_y(), 10, pdf.get_y() + 22)

            pdf.set_x(16)
            pdf.set_font('Helvetica', '', 8)
            pdf.set_text_color(*C_MUTED)
            badges = f"{p.get('project_id', 'Project')}   |   {p.get('difficulty', 'Guided')}   |   Week {p.get('assigned_week', '?')}"
            pdf.cell(180, 6, sanitize(badges), ln=True)

            pdf.set_x(16)
            pdf.set_font('Helvetica', 'B', 15)
            pdf.set_text_color(*C_PRIMARY)
            pdf.cell(180, 8, sanitize(p.get('title', '')), ln=True)

            pdf.set_x(16)
            pdf.set_font('Helvetica', 'I', 10)
            pdf.set_text_color(*C_SECONDARY)
            pdf.cell(180, 6, sanitize(p.get('tagline', '')), ln=True)
            pdf.ln(6)

            # Problem Statement
            pdf.label_text("Problem Statement")
            pdf.body(p.get('problem_statement', ''))

            # Deliverables
            deliverables = p.get("deliverables", [])
            if deliverables:
                pdf.label_text("Deliverables")
                for d in deliverables:
                    pdf.set_font('Helvetica', 'B', 10)
                    pdf.set_text_color(*C_PRIMARY)
                    pdf.cell(190, 6, sanitize(f"- {d.get('title', '')}"), ln=True)
                    pdf.set_font('Helvetica', '', 9)
                    pdf.set_text_color(*C_SECONDARY)
                    pdf.multi_cell(190, 5, sanitize(f"  {d.get('description', '')}"))

                    for ac in d.get("acceptance_criteria", []):
                        pdf.set_font('Helvetica', '', 9)
                        pdf.set_text_color(*C_MUTED)
                        pdf.cell(190, 5, sanitize(f"    > {ac}"), ln=True)
                    pdf.ln(2)
                pdf.ln(2)

            # Technical Requirements
            tech_reqs = p.get("technical_requirements", [])
            if tech_reqs:
                pdf.label_text("Technical Requirements")
                for req in tech_reqs:
                    pdf.bullet(req)
                pdf.ln(2)

            # Tools & Technologies
            tools = p.get("tools_and_technologies", [])
            if tools:
                pdf.label_text("Tools & Technologies")
                pdf.body(", ".join(str(t) for t in tools))

            # Evaluation Rubric
            rubric = p.get("evaluation_rubric", [])
            if rubric:
                pdf.label_text("Evaluation Rubric")
                pdf.ln(2)

                # Table header
                pdf.set_fill_color(*C_BG_LIGHT)
                pdf.set_font('Helvetica', 'B', 8)
                pdf.set_text_color(*C_SECONDARY)
                pdf.cell(50, 7, "  Criterion", 0, 0, 'L', fill=True)
                pdf.cell(15, 7, "Pts", 0, 0, 'C', fill=True)
                pdf.cell(45, 7, "Excellent", 0, 0, 'L', fill=True)
                pdf.cell(45, 7, "Satisfactory", 0, 0, 'L', fill=True)
                pdf.cell(35, 7, "Needs Work", 0, 1, 'L', fill=True)

                total_pts = 0
                for r in rubric:
                    pts = r.get("points", 0)
                    total_pts += pts
                    pdf.set_font('Helvetica', '', 8)
                    pdf.set_text_color(*C_PRIMARY)
                    pdf.cell(50, 6, sanitize(f"  {r.get('criterion', '')}"), 0, 0)
                    pdf.set_text_color(*C_ACCENT)
                    pdf.set_font('Helvetica', 'B', 8)
                    pdf.cell(15, 6, str(pts), 0, 0, 'C')
                    pdf.set_font('Helvetica', '', 8)
                    pdf.set_text_color(*C_SECONDARY)
                    pdf.cell(45, 6, sanitize(str(r.get('excellent', ''))[:40]), 0, 0)
                    pdf.cell(45, 6, sanitize(str(r.get('satisfactory', ''))[:40]), 0, 0)
                    pdf.cell(35, 6, sanitize(str(r.get('needs_work', ''))[:35]), 0, 1)

                # Total row
                pdf.set_fill_color(*C_BG_LIGHT)
                pdf.set_font('Helvetica', 'B', 9)
                pdf.set_text_color(*C_PRIMARY)
                pdf.cell(50, 7, "  Total", 0, 0, 'L', fill=True)
                pdf.set_text_color(*C_ACCENT)
                pdf.cell(15, 7, str(total_pts), 0, 0, 'C', fill=True)
                pdf.cell(125, 7, "", 0, 1, 'L', fill=True)
                pdf.ln(4)

            pdf.subtle_divider()
            pdf.ln(4)

    # ─── Output ───
    out = pdf.output(dest='S')
    if isinstance(out, str):
        return out.encode('latin-1', 'replace')
    return bytes(out)
