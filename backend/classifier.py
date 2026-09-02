REFERENCE_RANGES = {
    "glucose": {
        "unit": "mg/dL",
        "normal_min": 70,
        "normal_max": 140,
        "critical_low": 40,
        "critical_high": 300
    },

    "hemoglobin": {
        "unit": "g/dL",
        "normal_min": 12,
        "normal_max": 17.5,
        "critical_low": 7,
        "critical_high": 20
    },

    "wbc": {
        "unit": "10^3/uL",
        "normal_min": 4,
        "normal_max": 11,
        "critical_low": 2,
        "critical_high": 30
    },

    "platelet count": {
        "unit": "10^3/uL",
        "normal_min": 150,
        "normal_max": 450,
        "critical_low": 50,
        "critical_high": 1000
    },

    "creatinine": {
        "unit": "mg/dL",
        "normal_min": 0.6,
        "normal_max": 1.3,
        "critical_low": 0.3,
        "critical_high": 5
    },

    "cholesterol": {
        "unit": "mg/dL",
        "normal_min": 0,
        "normal_max": 200,
        "critical_low": 0,
        "critical_high": 400
    }
}


def classify_lab(test_name: str, value: float):
    key = test_name.strip().lower()

    if key not in REFERENCE_RANGES:
        raise ValueError(f"Unknown laboratory test: {test_name}")

    reference = REFERENCE_RANGES[key]

    if (
        value < reference["critical_low"]
        or value > reference["critical_high"]
    ):
        status = "Critical"

    elif (
        value < reference["normal_min"]
        or value > reference["normal_max"]
    ):
        status = "Warning"

    else:
        status = "Normal"

    return {
        "status": status,
        "reference_range": {
            "min": reference["normal_min"],
            "max": reference["normal_max"]
        }
    }