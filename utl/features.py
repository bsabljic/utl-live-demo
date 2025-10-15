"""
Feature extraction skeletons for UTL (24 features for crisis chat).
These are stubs with simple heuristics so the repo remains runnable
without private datasets. Replace with your production extractors.
"""
from typing import Dict, Any, List, Optional
import json
import re
from pathlib import Path

# Defaults (fallback mini-lexicon) – will be overridden if lexicon.json is found.
DEFAULT_LEXICON = {
    "suicidal_keywords": ["kill myself","suicide","end my life","want to die","end it all"],
    "method_nouns": ["pills","rope","gun","knife","jump","overdose","hanging"],
    "finality_phrases": ["goodbye","last time","won't see you again","take care"],
    "isolation_markers": ["alone","nobody cares","isolated","no friends","no one understands"],
    "implicit_ideation": ["sleep forever","not wake up","find peace","end the struggle"]
}

def load_lexicon(path: Optional[str] = "data/lexicon.json") -> dict:
    p = Path(path) if path else None
    if p and p.exists():
        try:
            return json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT_LEXICON
    return DEFAULT_LEXICON

_LEX = load_lexicon()

SUICIDAL_KEYWORDS = set(x.lower() for x in _LEX.get("suicidal_keywords", []))
METHOD_NOUNS = set(x.lower() for x in _LEX.get("method_nouns", []))
FINALITY = set(x.lower() for x in _LEX.get("finality_phrases", []))
ISOLATION = set(x.lower() for x in _LEX.get("isolation_markers", []))
IMPLICIT = set(x.lower() for x in _LEX.get("implicit_ideation", []))

def extract_turn_features(text: str, turn_index: int, session_minutes: float = 0.0) -> Dict[str, float]:
    """
    Return a minimal dict of 24 features (many are simplified placeholders).
    """
    t = (text or "").lower()

    # Linguistic (8) – counts normalized to [0,1] range with simple caps
    suicidal_kw = sum(1 for kw in SUICIDAL_KEYWORDS if kw in t)
    method_inq = 1.0 if ("how to" in t and any(m in t for m in METHOD_NOUNS)) else 0.0
    hopelessness = 1.0 if any(x in t for x in ["no hope","hopeless","pointless"]) else 0.0
    finality = sum(1 for p in FINALITY if p in t)
    isolation = sum(1 for p in ISOLATION if p in t)
    self_harm_verbs = 1.0 if re.search(r"i('m| am)? (going to|will) (hurt|cut|kill) (myself|me)?", t) else 0.0
    temporal_urgency = 1.0 if any(x in t for x in ["tonight","right now","today"]) else 0.0
    help_rejection = 1.0 if any(x in t for x in ["won't work","tried that","no point"]) else 0.0

    # Behavioral (5) – simplified placeholders
    turn_count = float(max(1, turn_index))
    response_latency = 0.0  # unknown without timestamps
    topic_fixation = 0.0    # unknown without previous turn; placeholder
    disclosure_depth = min(1.0, len(t.split()) / 100.0)
    escalation_rate = 0.0   # requires hazard history

    # Temporal (3)
    tod = 0.0    # normalized hour if available
    dow = 0.0    # binary if weekend, placeholder
    session_dur = min(1.0, float(session_minutes) / 120.0)

    # Protective (6) – crude heuristics
    social_support = 1.0 if "friend" in t or "family" in t else 0.0
    future_plan = 1.0 if any(x in t for x in ["next week","tomorrow","plan to"]) else 0.0
    coping = 1.0 if any(x in t for x in ["meditation","walk","breathing","exercise"]) else 0.0
    help_seeking = 1.0 if any(x in t for x in ["can you recommend","where can i get help","help line"]) else 0.0
    reasons_living = 1.0 if any(x in t for x in ["my kids","responsibilities","job"]) else 0.0
    pos_emotion = 1.0 if any(x in t for x in ["grateful","thankful","hopeful"]) else 0.0

    def cap01(x, cap=3.0):
        return min(1.0, float(x)/cap)

    return {
        # Linguistic (8)
        "ling_suicidal_keywords": cap01(suicidal_kw),
        "ling_method_inquiries": method_inq,
        "ling_hopelessness": hopelessness,
        "ling_finality": cap01(finality),
        "ling_isolation": cap01(isolation),
        "ling_self_harm_verbs": self_harm_verbs,
        "ling_temporal_urgency": temporal_urgency,
        "ling_help_rejection": help_rejection,
        # Behavioral (5)
        "beh_turn_count": min(1.0, turn_count/30.0),
        "beh_response_latency": response_latency,
        "beh_topic_fixation": topic_fixation,
        "beh_disclosure_depth": disclosure_depth,
        "beh_escalation_rate": escalation_rate,
        # Temporal (3)
        "tmp_time_of_day": tod,
        "tmp_day_of_week": dow,
        "tmp_session_duration": session_dur,
        # Protective (6)
        "pro_social_support": social_support,
        "pro_future_oriented": future_plan,
        "pro_coping": coping,
        "pro_help_seeking": help_seeking,
        "pro_reasons_living": reasons_living,
        "pro_positive_affect": pos_emotion,
    }
