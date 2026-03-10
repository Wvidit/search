"""
Research Finder Agent - Core logic using Gemini API with Google Search grounding.

Uses Gemini 2.0 Flash (free tier) with Google Search to find:
- Professors in AI+Materials/Ceramics and Computer Vision
- PhD students, Labs, and Internship opportunities
"""

import json
import re
from google import genai
from google.genai import types
from config import GEMINI_MODEL, QUALITY_CRITERIA


def create_client(api_key: str) -> genai.Client:
    """Create a Gemini client with the given API key."""
    return genai.Client(api_key=api_key)


def search_professors_materials(client: genai.Client) -> dict:
    """Search for professors working on AI integration in materials/ceramics."""

    prompt = f"""
You are a research assistant helping find professors for potential research internship applications.

Search the web thoroughly and find 8-10 professors who are working on **AI/Machine Learning integration in Materials Science, specifically ceramic materials**. 

{QUALITY_CRITERIA}

For each professor, provide the following information in a STRICT JSON format:
{{
    "professors": [
        {{
            "name": "Full Name",
            "title": "Academic Title (e.g., Associate Professor)",
            "university": "University Name",
            "department": "Department Name",
            "email": "email@university.edu (if publicly available, else 'Not publicly listed')",
            "website": "Personal/lab website URL",
            "google_scholar": "Google Scholar profile URL if available",
            "research_areas": ["Area 1", "Area 2", "Area 3"],
            "notable_projects": [
                "Brief description of project 1",
                "Brief description of project 2"
            ],
            "recent_publications": [
                "Title of recent relevant paper 1",
                "Title of recent relevant paper 2"
            ],
            "why_notable": "Why this professor is notable (Stanford top 2%, QS ranking of university, h-index, etc.)",
            "accepts_interns": "Yes/Possibly/Unknown - any info about accepting research interns",
            "internship_link": "Link to apply for internship if available, else 'Check university website'"
        }}
    ]
}}

Focus specifically on:
1. Machine learning for ceramic material design and discovery
2. AI-driven materials characterization 
3. Computational materials science with ML for ceramics
4. Deep learning for materials property prediction
5. Computer vision for materials microstructure analysis

Search Google Scholar, university websites, and research group pages to find accurate and current information.
Return ONLY valid JSON, no additional text before or after the JSON.
"""

    return _execute_search(client, prompt)


def search_professors_cv(client: genai.Client) -> dict:
    """Search for Computer Vision professors who accept interdisciplinary students."""

    prompt = f"""
You are a research assistant helping find professors for potential research internship applications.

Search the web thoroughly and find 8-10 prominent professors working in **Computer Vision** who are known to accept **interdisciplinary students** (students from non-CS backgrounds like materials science, physics, mechanical engineering, etc.).

{QUALITY_CRITERIA}

For each professor, provide the following information in a STRICT JSON format:
{{
    "professors": [
        {{
            "name": "Full Name",
            "title": "Academic Title",
            "university": "University Name",
            "department": "Department Name", 
            "email": "email@university.edu (if publicly available, else 'Not publicly listed')",
            "website": "Personal/lab website URL",
            "google_scholar": "Google Scholar profile URL if available",
            "research_areas": ["Area 1", "Area 2", "Area 3"],
            "notable_projects": [
                "Brief description of project 1",
                "Brief description of project 2"
            ],
            "recent_publications": [
                "Title of recent relevant paper 1",
                "Title of recent relevant paper 2"
            ],
            "why_notable": "Why this professor is notable (Stanford top 2%, QS ranking of university, h-index, etc.)",
            "interdisciplinary_info": "Evidence that they accept interdisciplinary students",
            "accepts_interns": "Yes/Possibly/Unknown",
            "internship_link": "Link to research internship application if available"
        }}
    ]
}}

Focus on professors who:
1. Have published on applying CV to scientific domains (materials, medical, physical sciences)
2. Have lab members from diverse backgrounds
3. Are at top universities (MIT, Stanford, CMU, ETH Zurich, Oxford, etc.)
4. Have active research groups with internship programs
5. Work on applied computer vision (not just theory)

Search Google Scholar, university websites, and research group pages for accurate information.
Return ONLY valid JSON, no additional text before or after the JSON.
"""

    return _execute_search(client, prompt)


def search_phd_students(client: genai.Client) -> dict:
    """Search for exceptional PhD students in AI+Materials and Computer Vision."""

    prompt = f"""
You are a research assistant. Search the web and find 6-8 exceptional PhD students who are doing groundbreaking work in either:
1. AI/ML applied to Materials Science (especially ceramics)
2. Computer Vision with interdisciplinary applications

These should be students who:
- Have published in top venues (NeurIPS, ICML, Nature, Science, Acta Materialia, etc.)
- Are at top universities (QS Top 100)
- Have won awards or fellowships
- Are actively working on innovative research

Provide the following in STRICT JSON format:
{{
    "phd_students": [
        {{
            "name": "Full Name",
            "university": "University Name",
            "advisor": "PhD Advisor Name",
            "year": "PhD Year (e.g., 3rd year)",
            "research_focus": "Brief description of their research",
            "email": "email if publicly available",
            "website": "Personal website URL",
            "google_scholar": "Google Scholar profile URL if available",
            "notable_work": [
                "Description of notable paper/project 1",
                "Description of notable paper/project 2"
            ],
            "awards": ["Award 1", "Award 2"],
            "why_exceptional": "Why this student stands out"
        }}
    ]
}}

Return ONLY valid JSON, no additional text before or after.
"""

    return _execute_search(client, prompt)


def search_labs(client: genai.Client) -> dict:
    """Search for renowned research labs in AI+Materials and Computer Vision."""

    prompt = f"""
You are a research assistant. Search the web and find 8-10 renowned research labs working in:
1. AI/ML for Materials Science (especially ceramics and advanced materials)
2. Computer Vision with applied/interdisciplinary focus

Labs should be at QS Top 100 universities or national labs with strong reputations.

Provide the following in STRICT JSON format:
{{
    "labs": [
        {{
            "name": "Lab Name",
            "university": "University / Institution Name",
            "director": "Lab Director / PI Name",
            "website": "Lab website URL",
            "research_focus": ["Focus Area 1", "Focus Area 2"],
            "notable_projects": [
                "Description of notable project 1",
                "Description of notable project 2"
            ],
            "team_size": "Approximate team size if known",
            "accepts_interns": "Yes/Possibly/Unknown",
            "internship_info": "How to apply for internships at this lab",
            "internship_link": "Direct link to internship application if available",
            "why_renowned": "Why this lab is considered top-tier"
        }}
    ]
}}

Include labs like:
- MIT CSAIL groups, Stanford AI labs, CMU Robotics Institute groups
- Materials informatics labs (e.g., Citrine, Materials Project related groups)
- National lab AI/materials groups (LBNL, ORNL, Argonne, etc.)
- European/Asian top labs (ETH Zurich, Max Planck, KAIST, etc.)

Return ONLY valid JSON, no additional text before or after.
"""

    return _execute_search(client, prompt)


def search_internships(client: genai.Client) -> dict:
    """Search for research internship opportunities."""

    prompt = f"""
You are a research assistant. Search the web for current and upcoming research internship opportunities in:
1. AI/ML for Materials Science
2. Computer Vision
3. Computational Materials Science
4. Applied AI research

Focus on programs that:
- Are at renowned institutions (QS Top 100 universities, national labs, top companies)
- Accept undergraduate or early graduate students
- Welcome interdisciplinary applicants
- Are currently accepting applications or will open soon

Provide the following in STRICT JSON format:
{{
    "internships": [
        {{
            "program_name": "Internship Program Name",
            "institution": "Institution Name",
            "description": "Brief description of the program",
            "research_areas": ["Area 1", "Area 2"],
            "eligibility": "Who can apply",
            "duration": "Duration of the program",
            "stipend": "Stipend information if available",
            "application_deadline": "Deadline if known",
            "application_link": "Direct URL to apply",
            "contact_email": "Contact email if available",
            "notes": "Any additional relevant information"
        }}
    ]
}}

Include programs like:
- SURF at Caltech, MIT UROP/MSRP, Stanford CURIS/SURPS
- NSF REU programs in relevant fields
- National lab internships (DOE SULI, Argonne, LBNL, ORNL)
- European programs (CERN, Max Planck, ETH Student Research Projects)
- Industry research internships (Google Research, Microsoft Research, DeepMind)
- DAAD WISE (Germany), MITACS Globalink (Canada)

Return ONLY valid JSON, no additional text before or after.
"""

    return _execute_search(client, prompt)


def _execute_search(client: genai.Client, prompt: str) -> dict:
    """Execute a search query using Gemini with Google Search grounding."""
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.3,
            ),
        )

        # Extract text from response
        text = response.text
        if not text:
            return {"error": "Empty response from Gemini API"}

        # Parse JSON from response
        parsed = _extract_json(text)

        # Extract grounding sources if available
        sources = []
        if response.candidates and response.candidates[0].grounding_metadata:
            gm = response.candidates[0].grounding_metadata
            if gm.grounding_chunks:
                for chunk in gm.grounding_chunks:
                    if chunk.web:
                        sources.append(
                            {"title": chunk.web.title or "", "url": chunk.web.uri or ""}
                        )

        if parsed:
            parsed["_sources"] = sources
            return parsed
        else:
            return {"error": "Could not parse response", "raw_text": text[:2000]}

    except Exception as e:
        return {"error": str(e)}


def _extract_json(text: str) -> dict | None:
    """Extract JSON from model response, handling markdown code blocks."""
    # Try to find JSON in code blocks first
    code_block_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if code_block_match:
        try:
            return json.loads(code_block_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try to find JSON object directly
    json_match = re.search(r"\{[\s\S]*\}", text)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    # Try the entire text
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return None


def run_full_search(client: genai.Client, categories: list[str] = None) -> dict:
    """Run searches for all or specified categories."""
    search_functions = {
        "professors_materials": search_professors_materials,
        "professors_cv": search_professors_cv,
        "phd_students": search_phd_students,
        "labs": search_labs,
        "internships": search_internships,
    }

    if categories is None:
        categories = list(search_functions.keys())

    results = {}
    for category in categories:
        if category in search_functions:
            results[category] = search_functions[category](client)

    return results
