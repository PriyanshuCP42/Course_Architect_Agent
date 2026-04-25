# constants.py

# ── Color System (Light Theme — NO neon, no dark backgrounds) ───────────
COLORS = {
    "white":          "#FFFFFF",
    "bg_page":        "#F7F8FA",        # Very light warm gray page background
    "bg_card":        "#FFFFFF",        # Pure white cards
    "bg_subtle":      "#F1F4F8",        # Slightly off-white for alternating rows
    "border":         "#E4E8EF",        # Soft gray border
    "border_strong":  "#CBD5E1",        # Slightly darker border for emphasis

    # Text
    "text_primary":   "#111827",        # Near black — main headings
    "text_secondary": "#374151",        # Dark gray — body text
    "text_muted":     "#6B7280",        # Mid gray — labels and captions
    "text_faint":     "#9CA3AF",        # Light gray — timestamps, hints

    # Accent — Warm Indigo (not neon, not electric)
    "accent":         "#4F46E5",        # Deep indigo — primary actions, active states
    "accent_light":   "#EEF2FF",        # Very light indigo — accent backgrounds
    "accent_border":  "#C7D2FE",        # Light indigo border

    # Semantic
    "success":        "#059669",        # Forest green
    "success_bg":     "#ECFDF5",
    "success_border": "#A7F3D0",

    "warning":        "#D97706",        # Warm amber
    "warning_bg":     "#FFFBEB",
    "warning_border": "#FDE68A",

    "danger":         "#DC2626",        # Standard red
    "danger_bg":      "#FEF2F2",
    "danger_border":  "#FECACA",

    "info":           "#2563EB",        # Readable blue
    "info_bg":        "#EFF6FF",
    "info_border":    "#BFDBFE",
}

# ── Lesson Type Labels and Colors ────────────────────────────────────────
LESSON_TYPE_STYLES = {
    "concept":    {"bg": "#EFF6FF", "color": "#1D4ED8", "label": "Concept"},
    "hands-on":   {"bg": "#FFFBEB", "color": "#B45309", "label": "Hands-On"},
    "case-study": {"bg": "#F0FDF4", "color": "#15803D", "label": "Case Study"},
    "review":     {"bg": "#F5F3FF", "color": "#6D28D9", "label": "Review"},
}

# ── Difficulty Colors ────────────────────────────────────────────────────
DIFFICULTY_STYLES = {
    "Guided":      {"bg": "#EFF6FF", "color": "#1D4ED8"},
    "Independent": {"bg": "#FFFBEB", "color": "#B45309"},
    "Advanced":    {"bg": "#FDF2F8", "color": "#9D174D"},
    "Beginner":    {"bg": "#F0FDF4", "color": "#15803D"},
    "Intermediate":{"bg": "#FFFBEB", "color": "#B45309"},
}

# ── Tab Labels ───────────────────────────────────────────────────────────
TABS = ["📋 Curriculum", "📖 Lessons", "🧪 Assessments", "🏗️ Projects"]

APP_TITLE    = "Course Architect"
APP_SUBTITLE = "Turn your notes into a complete, structured course — instantly"
