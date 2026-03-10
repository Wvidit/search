"""
Configuration for the Research Finder Agent.
"""

# Gemini Model Configuration
AVAILABLE_MODELS = {
    "Gemini 3 Flash (Preview)": "gemini-3-flash-preview",
    "Gemini 3 Pro (Preview)": "gemini-3-pro-preview",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
}
DEFAULT_MODEL = "Gemini 3 Flash (Preview)"

# Search Categories
SEARCH_CATEGORIES = {
    "professors_materials": {
        "title": "🔬 Professors: AI in Materials / Ceramics",
        "description": "Professors working on AI/ML integration in materials science, specifically ceramic materials",
        "icon": "🔬",
    },
    "professors_cv": {
        "title": "👁️ Professors: Computer Vision (Interdisciplinary)",
        "description": "Computer Vision professors who accept interdisciplinary students",
        "icon": "👁️",
    },
    "phd_students": {
        "title": "🎓 Exceptional PhD Students",
        "description": "Outstanding PhD students in AI+Materials or Computer Vision",
        "icon": "🎓",
    },
    "labs": {
        "title": "🏛️ Renowned Research Labs",
        "description": "Top research labs in AI+Materials and Computer Vision",
        "icon": "🏛️",
    },
    "internships": {
        "title": "📋 Research Internship Opportunities",
        "description": "Open research internship positions and application links",
        "icon": "📋",
    },
}

# Quality filters
QUALITY_CRITERIA = """
IMPORTANT QUALITY CRITERIA:
- Professors MUST be from QS World Ranking Top 100 universities OR be in Stanford's Top 2% researchers list
- Focus on researchers with strong publication records (h-index, citations)
- Prioritize researchers who are actively publishing (last 2-3 years)
- Include researchers who explicitly welcome interdisciplinary applicants
"""
