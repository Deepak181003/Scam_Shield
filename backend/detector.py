from ml.model_service import load_or_train
from backend.rules import RULES, SCAM_TYPES, STAGES
from backend.url_analyzer import analyze_urls
from backend.stage_detector import detect_stage
from backend.scoring import calculate_risk
from backend.recommendations import recommendation_for, explanation_for
from backend.validation import validate_input_type, validate_text

MODEL = load_or_train()


def normalize(text: str) -> str:
    import re
    return re.sub(r"\s+", " ", text.lower()).strip()


def detect_rules(text: str) -> list[dict]:
    t = normalize(text)
    matches = []
    for category, words in RULES.items():
        found = [w for w in words if w in t]
        if found:
            matches.append({
                "category": category,
                "matches": found[:6],
                "hit_count": len(found),
            })
    return matches


def detect_scam_type(text: str) -> dict:
    t = normalize(text)
    scores = {
        name: sum(word in t for word in words)
        for name, words in SCAM_TYPES.items()
    }
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    name, score = ranked[0]
    return {
        "name": name if score else "General / Unclassified Scam",
        "score": score,
        "ranking": [{"type": n, "hits": s} for n, s in ranked if s],
    }


def model_probability(text: str) -> float:
    probs = MODEL.predict_proba([text])[0]
    classes = list(MODEL.classes_)
    if "scam" in classes:
        return float(probs[classes.index("scam")])
    return float(max(probs))


def analyze_text(text: str, input_type: str = "message") -> dict:
    text = validate_text(text)
    input_type = validate_input_type(input_type)

    rule_hits = detect_rules(text)
    urls = analyze_urls(text)
    stage, stage_hits, stage_matches, stage_ranking = detect_stage(text)
    scam_type = detect_scam_type(text)
    ml_probability_value = model_probability(text)

    risk_data = calculate_risk(
        ml_probability_value,
        len(rule_hits),
        sum(u["score"] for u in urls),
        stage_hits,
    )

    flags = [x["category"] for x in rule_hits]
    for url in urls:
        flags.extend(url["flags"])
    if not flags:
        flags = ["No major red flags detected"]

    risk = risk_data["risk"]

    return {
        **risk_data,
        "scam_probability": round(ml_probability_value * 100, 2),
        "input_type": input_type.title(),
        "scam_type": scam_type["name"],
        "scam_type_score": scam_type["score"],
        "scam_type_ranking": scam_type["ranking"],
        "stage": stage,
        "stage_hits": stage_hits,
        "stage_matches": stage_matches,
        "stage_ranking": stage_ranking,
        "rule_hits": rule_hits,
        "red_flags": list(dict.fromkeys(flags)),
        "urls": urls,
        "recommendation": recommendation_for(risk),
        "explanation": explanation_for(rule_hits, urls, stage),
        "model": {
            "name": "TF-IDF + Logistic Regression",
            "version": "baseline-week3",
        },
    }


def analyze_batch(items: list[dict]) -> list[dict]:
    return [
        analyze_text(item.get("content", ""), item.get("input_type", "message"))
        for item in items
    ]


def backend_metadata() -> dict:
    return {
        "service": "ScamShield Detection API",
        "model": "TF-IDF + Logistic Regression",
        "supported_inputs": ["message", "email", "conversation", "url"],
        "scam_types": list(SCAM_TYPES.keys()),
        "stages": [stage for stage, _ in STAGES],
    }
