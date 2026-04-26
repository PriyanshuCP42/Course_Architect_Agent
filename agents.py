import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Try Streamlit secrets first (cloud), then .env (local)
try:
    import streamlit as st
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", None) or os.getenv("GROQ_API_KEY")
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Clean the key — strip whitespace/newlines that TOML text areas can introduce
if GROQ_API_KEY:
    GROQ_API_KEY = GROQ_API_KEY.strip().replace("\n", "").replace("\r", "").replace(" ", "")

MODEL        = "llama-3.1-8b-instant"
client       = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def ask_llm(system_prompt, user_prompt, temperature=0.3) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content

def ask_llm_json(system_prompt, user_prompt, temperature=0.3, max_tokens=1500, max_retries=3) -> dict:
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            if "413" in str(e) or "rate" in str(e).lower() or "429" in str(e):
                if attempt < max_retries - 1:
                    time.sleep(25)
                    continue
            raise e

def build_curriculum(raw_notes: str, target_audience: str, course_duration: str, class_size: str, desired_outcomes: str, engaging_materials: str) -> dict:
    system_prompt = """You are an expert curriculum designer. You must design a complete curriculum.
    Respond ONLY in valid JSON matching this exact schema:
    {
      "course_title": "String",
      "course_subtitle": "String",
      "target_audience": "String",
      "difficulty_level": "String",
      "total_weeks": "Integer",
      "total_hours": "Integer",
      "prerequisites": ["String"],
      "course_outcomes": ["String"],
      "modules": [
        {
          "module_id": "String (e.g. M1)",
          "title": "String",
          "week": "Integer",
          "duration_days": "Integer",
          "module_goal": "String",
          "learning_objectives": ["String"],
          "lessons": [
             {
                "lesson_id": "String (e.g. M1L1)",
                "title": "String",
                "duration_minutes": "Integer",
                "lesson_type": "String (one of: concept, hands-on, case-study, review)",
                "description": "String"
             }
          ]
        }
      ]
    }
    """
    user_prompt = f"""Create a curriculum using these constraints:
    Notes: {raw_notes}
    Target Audience: {target_audience}
    Course Duration: {course_duration}
    Class Size: {class_size}
    Instructor Outcomes: {desired_outcomes}
    Engaging Materials: {engaging_materials}
    """
    return ask_llm_json(system_prompt, user_prompt)

def generate_module_content(module_title: str, lessons: list, raw_notes: str, engaging_materials: str) -> list:
    system_prompt = """You are an expert instructional designer. Generate detailed lesson content for EVERY lesson in the provided list.
    You MUST provide content for all lessons passed to you. Do not skip any.
    Respond ONLY in valid JSON matching this exact schema:
    {
      "lessons": [
         {
            "lesson_id": "String",
            "content": {
               "introduction": "Detailed paragraph.",
               "core_explanation": "Detailed paragraphs explaining the concept.",
               "key_points": ["String", "String"],
               "real_world_application": "Detailed scenario applying the concept.",
               "summary": "Short summary."
            }
         }
      ]
    }
    Make the content rich, engaging, and highly detailed.
    """
    user_prompt = f"Module Title: {module_title}\\nLessons to generate:\\n{json.dumps(lessons)}\\nRaw Notes:\\n{raw_notes}\\nEngaging Materials:\\n{engaging_materials}"
    response = ask_llm_json(system_prompt, user_prompt)
    return response.get("lessons", [])

def create_assessments(curriculum: dict) -> dict:
    system_prompt = """You are an expert educational assessment creator. Create quizzes and exams for the provided curriculum.
    CRITICAL INSTRUCTION: You MUST generate tough, university-level assessments. Include EXACTLY 3 challenging MCQs and 1 highly advanced, non-generic scenario question per module.
    Ensure "total_questions" accurately reflects the sum of all generated questions.
    Respond ONLY in valid JSON matching this exact schema:
    {
      "total_questions": "Integer",
      "module_assessments": [
        {
          "module_id": "String",
          "module_title": "String",
          "mcq": [
            {
              "question_text": "String",
              "difficulty": "String (Hard)",
              "options": {"A": "Option 1", "B": "Option 2", "C": "Option 3", "D": "Option 4"},
              "correct_answer": "String",
              "explanation": "String"
            }
          ],
          "short_answer": [],
          "scenario": {
             "scenario_text": "String",
             "question_text": "String",
             "difficulty": "String (Advanced)",
             "model_answer": "String",
             "scoring_guide": "String"
          }
        }
      ],
      "final_exam": {
        "duration_minutes": 60,
        "passing_score_percent": 70,
        "instructions": "String",
        "mcq": [],
        "short_answer": [],
        "capstone_question": {
             "scenario_text": "String",
             "question_text": "String",
             "difficulty": "String",
             "model_answer": "String",
             "scoring_guide": "String"
        }
      }
    }
    """
    user_prompt = f"Create highly advanced assessments for this curriculum:\\n{json.dumps(curriculum)}"
    return ask_llm_json(system_prompt, user_prompt)

def design_projects(curriculum: dict) -> list:
    system_prompt = """You are a curriculum project designer. Create hands-on, practical projects.
    CRITICAL INSTRUCTION: Do NOT generate dummy or generic projects. Produce resume-worthy, high-quality industry-level projects tailored specifically to the modules. Provide realistic timelines.
    Respond ONLY in valid JSON matching this exact schema containing a 'projects' list:
    {
      "projects": [
        {
          "project_id": "String",
          "title": "String",
          "tagline": "String",
          "assigned_week": "Integer",
          "difficulty": "String",
          "problem_statement": "String",
          "deliverables": [
             {"title": "String", "description": "String", "acceptance_criteria": ["String"]}
          ],
          "technical_requirements": ["String"],
          "tools_and_technologies": ["String"],
          "evaluation_rubric": [
             {"criterion": "String", "points": "Integer", "excellent": "String", "satisfactory": "String", "needs_work": "String"}
          ],
          "stretch_goals": ["String"],
          "submission_format": "String"
        }
      ]
    }
    """
    user_prompt = f"Design engaging, resume-worthy projects for this curriculum:\\n{json.dumps(curriculum)}"
    response = ask_llm_json(system_prompt, user_prompt)
    return response.get("projects", [])

def build_complete_course(raw_notes: str, target_audience: str, course_duration: str, class_size: str, desired_outcomes: str, engaging_materials: str, progress_callback=None) -> dict:
    # Truncate raw notes to roughly 1500 tokens (6000 chars) to aggressively stay under the 6000 TPM limit
    if len(raw_notes) > 6000:
        raw_notes = raw_notes[:6000] + "... [Content truncated to meet API rate limits]"

    # 1. Build Curriculum structure
    if progress_callback: progress_callback("🏗️ Architecting curriculum structure...")
    curriculum = build_curriculum(raw_notes, target_audience, course_duration, class_size, desired_outcomes, engaging_materials)
    
    # 2. Generate Lesson Content ITERATIVELY per module to avoid LLM laziness
    if progress_callback: progress_callback("📖 Writing detailed lesson content...")
    if "modules" in curriculum:
        for i, module in enumerate(curriculum["modules"]):
            if progress_callback: progress_callback(f"📖 Writing content for Module {i+1}: {module.get('title', '')}...")
            enriched_lessons = generate_module_content(
                module.get("title", ""),
                module.get("lessons", []),
                raw_notes,
                engaging_materials
            )
            # Merge
            for l in module.get("lessons", []):
                for el in enriched_lessons:
                    if l.get("lesson_id") == el.get("lesson_id"):
                        l["content"] = el.get("content", {})

    # 3. Create Assessments (Use a lightweight curriculum to save tokens!)
    if progress_callback: progress_callback("🧪 Engineering assessments and quizzes...")
    import copy
    light_curriculum = copy.deepcopy(curriculum)
    for m in light_curriculum.get("modules", []):
        for l in m.get("lessons", []):
            l.pop("content", None)
            
    assessments = create_assessments(light_curriculum)
    
    # Ensure total questions is correct
    t_q = 0
    for ma in assessments.get("module_assessments", []):
        t_q += len(ma.get("mcq", []))
        t_q += len(ma.get("short_answer", []))
        if ma.get("scenario"): t_q += 1
    fe = assessments.get("final_exam", {})
    t_q += len(fe.get("mcq", []))
    t_q += len(fe.get("short_answer", []))
    if fe.get("capstone_question"): t_q += 1
    assessments["total_questions"] = t_q
    
    # 4. Design Projects
    if progress_callback: progress_callback("🏆 Designing capstone projects and rubrics...")
    projects = design_projects(light_curriculum)
    
    return {
        "curriculum": curriculum,
        "assessments": assessments,
        "projects": projects
    }

if __name__ == "__main__":
    print("Agents loaded successfully")
