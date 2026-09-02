# Reference ranges and classification rules for supported laboratory tests.

REFERENCE_RANGES = {
    # Existing tests
    "glucose": {
        "display_name": "Glucose",
        "unit": "mg/dL",
        "normal_min": 70,
        "normal_max": 140,
        "critical_low": 40,
        "critical_high": 300,
        "type": "numeric",
    },
    "hemoglobin": {
        "display_name": "Hemoglobin",
        "unit": "g/dL",
        "normal_min": 12,
        "normal_max": 15,
        "critical_low": 7,
        "critical_high": 20,
        "type": "numeric",
    },
    "wbc": {
        "display_name": "WBC",
        "unit": "10^3/uL",
        "normal_min": 5,
        "normal_max": 10.6,
        "critical_low": 2,
        "critical_high": 30,
        "type": "numeric",
    },
    "platelet count": {
        "display_name": "Platelet Count",
        "unit": "10^3/uL",
        "normal_min": 150,
        "normal_max": 450,
        "critical_low": 50,
        "critical_high": 1000,
        "type": "numeric",
    },
    "creatinine": {
        "display_name": "Creatinine",
        "unit": "mg/dL",
        "normal_min": 0.6,
        "normal_max": 1.3,
        "critical_low": 0.3,
        "critical_high": 5,
        "type": "numeric",
    },
    "cholesterol": {
        "display_name": "Cholesterol",
        "unit": "mg/dL",
        "normal_min": 0,
        "normal_max": 200,
        "critical_low": 0,
        "critical_high": 400,
        "type": "numeric",
    },

    # Kaggle dataset - quantitative tests
    "ferritin": {
        "display_name": "Ferritin",
        "unit": "ug/L",
        "normal_min": 15,
        "normal_max": 150,
        "type": "numeric",
    },
    "glycosylated hemoglobin (hba1c)": {
        "display_name": "Glycosylated Hemoglobin (HbA1c)",
        "unit": "%",
        "normal_min": 4.0,
        "normal_max": 6.0,
        "type": "numeric",
    },
    "total ige": {
        "display_name": "Total IgE",
        "unit": "KU/L",
        "normal_min": 0.1,
        "normal_max": 100,
        "type": "numeric",
    },
    "insulin": {
        "display_name": "Insulin",
        "unit": "mU/L",
        "normal_min": 2.6,
        "normal_max": 24.9,
        "type": "numeric",
    },
    "free t4": {
        "display_name": "Free T4",
        "unit": "ng/dL",
        "normal_min": 0.87,
        "normal_max": 1.70,
        "type": "numeric",
    },
    "leukocyte": {
        "display_name": "Leukocyte",
        "unit": "10^3/uL",
        "normal_min": 5,
        "normal_max": 10.6,
        "type": "numeric",
    },
    "rbc": {
        "display_name": "RBC",
        "unit": "10^6/uL",
        "normal_min": 3.8,
        "normal_max": 5.2,
        "type": "numeric",
    },
    "rdw-sd": {
        "display_name": "RDW-SD",
        "unit": "fL",
        "normal_min": 36.4,
        "normal_max": 46.3,
        "type": "numeric",
    },
    "rdw": {
        "display_name": "RDW",
        "unit": "%",
        "normal_min": 11.5,
        "normal_max": 14.5,
        "type": "numeric",
    },
    "pdw": {
        "display_name": "PDW",
        "unit": "fL",
        "normal_min": 9.8,
        "normal_max": 16.1,
        "type": "numeric",
    },
    "pct": {
        "display_name": "PCT",
        "unit": "%",
        "normal_min": 0.17,
        "normal_max": 0.38,
        "type": "numeric",
    },
    "neutrophil %": {
        "display_name": "Neutrophil %",
        "unit": "%",
        "normal_min": 50,
        "normal_max": 70,
        "type": "numeric",
    },
    "monocyte %": {
        "display_name": "Monocyte %",
        "unit": "%",
        "normal_min": 2,
        "normal_max": 11,
        "type": "numeric",
    },
    "lymphocyte %": {
        "display_name": "Lymphocyte %",
        "unit": "%",
        "normal_min": 18,
        "normal_max": 42,
        "type": "numeric",
    },
    "hematocrit": {
        "display_name": "Hematocrit",
        "unit": "%",
        "normal_min": 35,
        "normal_max": 49,
        "type": "numeric",
    },
    "ph (strip)": {
        "display_name": "pH (Strip)",
        "unit": "-",
        "normal_min": 5,
        "normal_max": 9,
        "type": "numeric",
    },
    "specific gravity (strip)": {
        "display_name": "Specific Gravity (Strip)",
        "unit": "-",
        "normal_min": 1.010,
        "normal_max": 1.030,
        "type": "numeric",
    }
}


# Original Kaggle test names → standardized English application names.
KAGGLE_TEST_NAME_MAP = {
    "glikozile hemoglobin (hba1c)": "Glycosylated Hemoglobin (HbA1c)",
    "i̇nsülin": "Insulin",
    "insülin": "Insulin",
    "serbest t4": "Free T4",
    "trombosit": "Platelet Count",
    "lökosit": "WBC",
    "eritrosit": "RBC",
    "nötrofil%": "Neutrophil %",
    "monosit%": "Monocyte %",
    "lenfosit%": "Lymphocyte %",
    "hematokrit": "Hematocrit",
    "ph (strip)": "pH (Strip)",
    "dansite (strip)": "Specific Gravity (Strip)"
}


def normalize_test_name(test_name: str) -> str:
    """Convert an input/Kaggle test name to our standardized English name."""

    original = test_name.strip()
    key = original.lower()

    if key in KAGGLE_TEST_NAME_MAP:
        return KAGGLE_TEST_NAME_MAP[key]

    return original


def get_test_config(test_name: str):
    """Return the configuration for a supported laboratory test."""

    normalized_name = normalize_test_name(test_name)
    key = normalized_name.strip().lower()

    # Direct lookup.
    if key in REFERENCE_RANGES:
        return normalized_name, REFERENCE_RANGES[key]

    # Aliases for equivalent existing/Kaggle terminology.
    aliases = {
        "platelet count": "platelet count",
        "platelet": "platelet",
        "wbc": "wbc",
        "leukocyte": "leukocyte",
        "rbc": "rbc",
        "erythrocyte / rbc": "erythrocyte",
    }

    if key in aliases:
        alias_key = aliases[key]
        return normalized_name, REFERENCE_RANGES[alias_key]

    raise ValueError(f"Unknown laboratory test: {test_name}")


def classify_lab(test_name: str, value):
    """
    Classify a laboratory result as Normal, Warning, or Critical.

    Numeric tests use their reference range.
    Categorical tests compare their observed value with the expected value.
    """

    normalized_name, reference = get_test_config(test_name)

    # Categorical result
    if reference["type"] == "categorical":
        observed = str(value).strip().lower()
        expected = reference["reference_value"].strip().lower()

        if observed == expected:
            status = "Normal"
        else:
            # A categorical abnormality is conservatively classified as Warning.
            status = "Warning"

        return {
            "test_name": normalized_name,
            "status": status,
            "reference_range": reference["reference_value"],
            "unit": reference["unit"],
        }

    # Numeric result
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"{normalized_name} requires a numeric laboratory value."
        )

    if (
        "critical_low" in reference
        and numeric_value < reference["critical_low"]
    ) or (
        "critical_high" in reference
        and numeric_value > reference["critical_high"]
    ):
        status = "Critical"

    elif (
        numeric_value < reference["normal_min"]
        or numeric_value > reference["normal_max"]
    ):
        status = "Warning"

    else:
        status = "Normal"

    return {
        "test_name": normalized_name,
        "status": status,
        "reference_range": {
            "min": reference["normal_min"],
            "max": reference["normal_max"],
        },
        "unit": reference["unit"],
    }


def get_supported_tests():
    """Return the unified English test catalogue for the frontend."""

    tests = []

    for config in REFERENCE_RANGES.values():
        tests.append({
            "name": config["display_name"],
            "unit": config["unit"],
            "type": config["type"],
            "reference_range": (
                {
                    "min": config["normal_min"],
                    "max": config["normal_max"],
                }
                if config["type"] == "numeric"
                else config["reference_value"]
            ),
        })

    # Remove duplicate display names while preserving order.
    unique_tests = []
    seen = set()

    for test in tests:
        key = test["name"].lower()

        if key not in seen:
            seen.add(key)
            unique_tests.append(test)

    return unique_tests