"""
Research Finder Agent - Core logic using Gemini API with Google Search grounding.

Supports:
- Multiple API key rotation (each free key has its own daily quota)
- Automatic model fallback
- Exponential backoff on per-minute rate limits
"""

import json
import re
import time
from google import genai
from google.genai import types
from config import AVAILABLE_MODELS, DEFAULT_MODEL, QUALITY_CRITERIA


def create_client(api_key: str) -> genai.Client:
    """Create a Gemini client with the given API key."""
    return genai.Client(api_key=api_key)


def create_clients(api_keys: list[str]) -> list[genai.Client]:
    """Create multiple Gemini clients from a list of API keys."""
    return [genai.Client(api_key=key.strip()) for key in api_keys if key.strip()]


def search_professors_materials(clients, model: str = None, status_callback=None) -> dict:
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

    return _execute_search(clients, prompt, model, _status_callback=status_callback)


def search_professors_cv(clients, model: str = None, status_callback=None) -> dict:
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

    return _execute_search(clients, prompt, model, _status_callback=status_callback)


def search_phd_students(clients, model: str = None, status_callback=None) -> dict:
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

    return _execute_search(clients, prompt, model, _status_callback=status_callback)


def search_labs(clients, model: str = None, status_callback=None) -> dict:
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

    return _execute_search(clients, prompt, model, _status_callback=status_callback)


def search_internships(clients, model: str = None, status_callback=None) -> dict:
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

    return _execute_search(clients, prompt, model, _status_callback=status_callback)


def _extract_retry_delay(error_msg: str) -> float:
    """Extract the retry delay from a rate-limit error message."""
    match = re.search(r'retry in ([\d.]+)s', error_msg)
    if match:
        return float(match.group(1))
    return 10.0  # default 10s


def _is_daily_quota_exhausted(error_msg: str) -> bool:
    """Check if the error is a DAILY quota exhaustion (not recoverable by waiting)."""
    # Daily quota errors have 'limit: 0' or 'PerDay' in the message
    return ('limit: 0' in error_msg) or ('PerDay' in error_msg)


def _get_fallback_models(primary_model: str) -> list[str]:
    """Get a list of fallback model IDs, excluding the primary."""
    all_ids = list(AVAILABLE_MODELS.values())
    return [m for m in all_ids if m != primary_model]


def _execute_search(
    clients,
    prompt: str,
    model: str = None,
    max_retries: int = 2,
    _status_callback=None,
) -> dict:
    """Execute a search query using Gemini with Google Search grounding.

    Supports:
    - Multiple API keys (clients): rotates to next key when one is exhausted
    - Model fallback: tries other models if the selected one fails
    - Exponential backoff on per-minute rate limits
    - Skips retries for daily quota exhaustion (moves to next key immediately)
    """
    # Normalize to list of clients
    if isinstance(clients, genai.Client):
        client_list = [clients]
    else:
        client_list = list(clients)

    primary_model = model or AVAILABLE_MODELS[DEFAULT_MODEL]
    models_to_try = [primary_model] + _get_fallback_models(primary_model)

    last_error = None

    for key_idx, client in enumerate(client_list):
        key_label = f"Key {key_idx + 1}/{len(client_list)}"

        for model_id in models_to_try:
            for attempt in range(max_retries):
                try:
                    # Status: starting attempt
                    if _status_callback:
                        if attempt == 0 and model_id == primary_model:
                            _status_callback(
                                f"🌐 Sending request to **{model_id}**"
                                + (f" ({key_label})" if len(client_list) > 1 else "")
                            )
                        elif attempt > 0:
                            _status_callback(
                                f"🔄 Retry {attempt}/{max_retries} on **{model_id}**"
                                + (f" ({key_label})" if len(client_list) > 1 else "")
                            )
                        elif model_id != primary_model:
                            _status_callback(
                                f"� Trying fallback model **{model_id}**"
                                + (f" ({key_label})" if len(client_list) > 1 else "")
                            )

                    response = client.models.generate_content(
                        model=model_id,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            tools=[types.Tool(google_search=types.GoogleSearch())],
                            temperature=0.3,
                        ),
                    )

                    # Status: got response
                    if _status_callback:
                        _status_callback("📥 Response received, parsing results...")

                    # Extract text from response
                    text = response.text
                    if not text:
                        if _status_callback:
                            _status_callback("⚠️ Empty response received")
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
                        parsed["_model_used"] = model_id
                        parsed["_key_used"] = key_idx + 1

                        # Count results
                        n_results = 0
                        for v in parsed.values():
                            if isinstance(v, list):
                                n_results = len(v)
                                break

                        if _status_callback:
                            _status_callback(
                                f"✅ **{n_results} results** found via {model_id}"
                                + (f" ({key_label})" if len(client_list) > 1 else "")
                                + (f" | {len(sources)} sources cited" if sources else "")
                            )
                        return parsed
                    else:
                        if _status_callback:
                            _status_callback("⚠️ Could not parse JSON from response")
                        return {"error": "Could not parse response", "raw_text": text[:2000]}

                except Exception as e:
                    error_str = str(e)
                    last_error = error_str

                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        # Daily quota exhausted → skip retries, try next key/model
                        if _is_daily_quota_exhausted(error_str):
                            if _status_callback:
                                _status_callback(
                                    f"🚫 {key_label} **daily quota exhausted** for {model_id} — skipping"
                                )
                            break  # break retry loop → try next model

                        # Per-minute rate limit → wait and retry
                        retry_delay = _extract_retry_delay(error_str)
                        wait_time = min(max(retry_delay, 10.0) * (2 ** attempt), 60.0)

                        if _status_callback:
                            _status_callback(
                                f"⏳ Rate limited on {model_id}. Waiting **{wait_time:.0f}s** before retry..."
                            )

                        time.sleep(wait_time)
                        continue
                    else:
                        if _status_callback:
                            _status_callback(f"❌ Error: {error_str[:120]}")
                        return {"error": error_str}

        # All models exhausted for this key
        if _status_callback and key_idx < len(client_list) - 1:
            _status_callback(f"🔑 {key_label} fully exhausted. **Rotating to next API key...**")

    if _status_callback:
        _status_callback("❌ All API keys and models exhausted")
    return {"error": f"All API keys and models exhausted. Last error: {last_error}"}


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


# Delay between searches to avoid hitting per-minute rate limits (seconds)
SEARCH_DELAY = 12


def run_full_search(
    clients,
    categories: list[str] = None,
    model: str = None,
    status_callback=None,
) -> dict:
    """Run searches for all or specified categories with inter-search delays."""
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
    for i, category in enumerate(categories):
        if category in search_functions:
            results[category] = search_functions[category](clients, model=model)
            # Add delay between searches to stay under rate limits
            if i < len(categories) - 1:
                if status_callback:
                    status_callback(f"⏳ Cooling down {SEARCH_DELAY}s to avoid rate limits...")
                time.sleep(SEARCH_DELAY)

    return results
