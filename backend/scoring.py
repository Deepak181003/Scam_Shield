def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def risk_level(risk_percent: int) -> str:
    if risk_percent >= 75:
        return "HIGH RISK"
    if risk_percent >= 45:
        return "SUSPICIOUS"
    return "LOW RISK"


def calculate_risk(model_probability: float, rule_count: int,
                   url_score_total: float, stage_hits: int) -> dict:
    # These are prototype weights, not calibrated probabilities.
    model_component = clamp(model_probability) * 0.55
    rule_component = min(0.35, rule_count * 0.055)
    url_component = min(0.20, max(0.0, url_score_total) / 300.0)
    stage_component = min(0.15, max(0, stage_hits) * 0.025)

    combined = clamp(
        model_component + rule_component + url_component + stage_component,
        0.01, 0.99
    )
    percent = round(combined * 100)

    return {
        "risk": percent,
        "level": risk_level(percent),
        "components": {
            "ml": round(model_component * 100, 2),
            "rules": round(rule_component * 100, 2),
            "url": round(url_component * 100, 2),
            "stage": round(stage_component * 100, 2),
        },
        "weights": {
            "ml": 0.55,
            "rules": 0.35,
            "url": 0.20,
            "stage": 0.15,
        },
    }
