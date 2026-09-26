"""AI-assisted care guidance by risk level — not a prescription."""

from __future__ import annotations

GUIDANCE = {
    "Low": {
        "title": "Low Risk",
        "urgency": "Routine monitoring",
        "why": "No strong abnormality signal from the AI Scan, or only low-concern findings.",
        "next_step": "Continue routine observation and keep udder hygiene clean.",
        "points": [
            "Continue routine observation",
            "Maintain clean udder hygiene",
            "Monitor the cow during the next milking",
            "Repeat screening if symptoms appear",
            "Keep normal hydration and feeding",
        ],
    },
    "Mild": {
        "title": "Mild Risk",
        "urgency": "Watch closely",
        "why": "Mild concern signals were found. This is not a diagnosis.",
        "next_step": "Inspect the udder carefully and contact a veterinarian if signs persist.",
        "points": [
            "Inspect the udder carefully",
            "Maintain strict udder hygiene",
            "Monitor swelling/redness/abnormal appearance",
            "Record the cow's condition",
            "Contact a veterinarian if symptoms persist or worsen",
        ],
    },
    "Moderate": {
        "title": "Moderate Risk",
        "urgency": "Veterinary evaluation recommended",
        "why": "Moderate concern was detected by YOLO11-assisted screening.",
        "next_step": "Arrange veterinary evaluation without long delay.",
        "points": [
            "Arrange veterinary evaluation",
            "Separate monitoring of the affected cow",
            "Maintain clean milking equipment",
            "Monitor milk appearance and udder changes",
            "Avoid delaying professional evaluation",
        ],
    },
    "High": {
        "title": "High Risk",
        "urgency": "Contact a veterinarian as soon as possible",
        "why": "High-concern indicators were detected. Do not rely only on AI screening.",
        "next_step": "Contact a veterinarian as soon as possible.",
        "points": [
            "Contact a veterinarian as soon as possible",
            "Avoid relying only on AI screening",
            "Keep the affected animal under close observation",
            "Maintain strict hygiene",
            "Follow professional veterinary instructions",
        ],
    },
    "Critical": {
        "title": "Urgent Veterinary Attention",
        "urgency": "Seek veterinary assistance immediately",
        "why": "Urgent concern indicators were detected by AI-assisted screening.",
        "next_step": "Seek veterinary assistance immediately.",
        "points": [
            "Seek veterinary assistance immediately",
            "Do not administer medication without veterinary advice",
            "Keep the animal under observation",
            "Follow the veterinarian's instructions",
        ],
    },
}

# Backward-compatible aliases from older stored values
ALIASES = {
    "Healthy": "Low",
    "Severe": "High",
}

MED_SAFETY = (
    "Medication should only be given under guidance from a qualified veterinarian."
)
DISCLAIMER = (
    "BOVIMED provides AI-assisted screening and care guidance. "
    "It is not a veterinary diagnosis and does not replace a qualified veterinarian."
)


def normalize_risk(risk_level: str | None) -> str:
    if not risk_level:
        return "Low"
    key = str(risk_level).strip()
    key = ALIASES.get(key, key)
    if key not in GUIDANCE:
        return "Low"
    return key


def get_care_guidance(risk_level: str | None) -> dict:
    level = normalize_risk(risk_level)
    data = GUIDANCE[level]
    return {
        "risk_level": level,
        "title": data["title"],
        "urgency": data["urgency"],
        "why": data["why"],
        "next_step": data["next_step"],
        "guidance": list(data["points"]),
        "medication_notice": MED_SAFETY,
        "disclaimer": DISCLAIMER,
        "label": "AI-assisted care guidance",
    }
