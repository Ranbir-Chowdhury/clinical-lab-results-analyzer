# Clinical Lab Results Analyzer

An AI-assisted full-stack web application for analyzing laboratory test
results, classifying them by severity, routing them by priority, and
generating clinically relevant explanations and suggested next steps.

Built with **React, FastAPI, MCP, and Google Gemini**.

> **Medical disclaimer:** This application is for educational and
> software-demonstration purposes. AI-generated explanations are not a
> diagnosis and do not replace evaluation by a qualified healthcare
> professional.

## Features

-   23 quantitative laboratory tests.
-   Deterministic reference-range classification: **Normal / Warning /
    Critical**.
-   Severity routing: **Critical → Warning → Normal**.
-   MCP-based agent communication.
-   Google Gemini-generated explanations and recommended next steps.
-   Manual laboratory-result entry.
-   CSV upload using `test_name,value,unit`.
-   Color-coded severity results.
-   Explainable results showing why a result was flagged.
-   Three synthetic CSV datasets under `/test_data`.

## Technology Stack

  Layer                 Technology
  --------------------- ---------------------------------------------------------
  Frontend              React + Vite
  Backend               Python + FastAPI
  Agent communication   MCP
  LLM                   Google Gemini API
  CSV parsing           Papa Parse
  Validation            Pydantic
  API server            Uvicorn
  Dataset               Kaggle -- Laboratory Test Results -- Anonymized Dataset

## Architecture

``` text
React Frontend
  │
  ├── Manual Input
  └── CSV Upload
        │
        ▼
FastAPI /analyze_labs
        │
        ▼
MCP Agent
        │
        ├── Classify
        └── Route by Severity
                │
                ▼
          Google Gemini
                │
                └── Explain + Next Step
                        │
                        ▼
                Results Dashboard
```

## Workflow

The application follows the required:

**Classify → Route → Explain**

### 1. Classify

Each submitted value is compared with its configured reference range.

-   **Normal**: within the configured normal range.
-   **Warning**: outside the normal range but not beyond a configured
    critical threshold.
-   **Critical**: beyond a configured critical threshold.

### 2. Route

Results are ordered:

``` text
Critical
Warning
Normal
```

### 3. Explain

Google Gemini is called to generate a clinically relevant explanation
and recommended next step for each result.

The application deliberately separates deterministic classification from
GenAI explanation: reference-range logic determines severity, while the
LLM provides natural-language explainability.

## MCP

The MCP server exposes the agent tools:

-   `classify_lab_result`
-   `route_by_severity`

The agent communicates with the MCP server before requesting the Gemini
explanation.

## Supported Laboratory Tests

1.  Glucose
2.  Hemoglobin
3.  WBC
4.  Platelet Count
5.  Creatinine
6.  Cholesterol
7.  Ferritin
8.  Glycosylated Hemoglobin (HbA1c)
9.  Total IgE
10. Insulin
11. Free T4
12. Leukocyte
13. RBC
14. RDW-SD
15. RDW
16. PDW
17. PCT
18. Neutrophil %
19. Monocyte %
20. Lymphocyte %
21. Hematocrit
22. pH (Strip)
23. Specific Gravity (Strip)

Reference ranges and classification rules are maintained in
`backend/classifier.py`.

## Kaggle Dataset

The project uses the required Kaggle dataset:

**Laboratory Test Results -- Anonymized Dataset**

Relevant quantitative tests and reference ranges from the dataset were
incorporated into the classifier. Dataset-specific names are
standardized to the application's test names where required, for
example:

``` text
Glikozile Hemoglobin (HbA1c) → Glycosylated Hemoglobin (HbA1c)
Trombosit                    → Platelet Count
Lökosit                      → WBC
Eritrosit                    → RBC
```

## CSV Input

CSV files must contain:

``` csv
test_name,value,unit
```

Example:

``` csv
test_name,value,unit
WBC,35,10^3/uL
Glycosylated Hemoglobin (HbA1c),34,%
Ferritin,28.9,ug/L
```

The React frontend uses **Papa Parse** to read the CSV, validates the
required columns, checks numeric values, and converts the rows into the
same structure used by manual input.

## Synthetic Test Data

Three synthetic datasets are included:

``` text
test_data/
├── synthetic_normal.csv
├── synthetic_warning.csv
└── synthetic_critical.csv
```

They provide repeatable CSV input for demonstrating different severity
scenarios.

## Project Structure

``` text
clinical-lab-analyzer/
├── backend/
│   ├── agent.py
│   ├── classifier.py
│   ├── llm_service.py
│   ├── main.py
│   ├── mcp_server.py
│   ├── models.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LabInput.jsx
│   │   │   ├── ResultsDisplay.jsx
│   │   │   └── SeverityBadge.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── package-lock.json
│
├── test_data/
│   ├── synthetic_normal.csv
│   ├── synthetic_warning.csv
│   └── synthetic_critical.csv
│
├── .gitignore
├── LICENSE
└── README.md
```

## Setup

### Prerequisites

-   Python 3.10+
-   Node.js 18+
-   npm
-   Google Gemini API key

### Backend

From the project root:

``` powershell
cd backend
python -m venv venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `backend/.env`:

``` env
GEMINI_API_KEY=your_gemini_api_key
```

Start the backend:

``` powershell
uvicorn main:app --reload
```

Backend:

``` text
http://127.0.0.1:8000
```

Swagger API documentation:

``` text
http://127.0.0.1:8000/docs
```

### Frontend

Open a second terminal:

``` powershell
cd frontend
npm install
npm run dev
```

Frontend:

``` text
http://localhost:5173
```

## Using the Application

### Manual input

1.  Select a laboratory test.
2.  Enter its numeric value.
3.  The unit is populated automatically.
4.  Add additional tests if required.
5.  Select **Analyze Results**.
6.  Review severity, AI explanation, and recommended next step.

### CSV input

1.  Prepare a CSV containing `test_name,value,unit`.
2.  Select **Upload CSV**.
3.  Choose the CSV file.
4.  Review the imported results.
5.  Select **Analyze Results**.
6.  Review the generated analysis.

## Example Results

### Normal

``` csv
test_name,value,unit
Ferritin,28.9,ug/L
```

Expected classification: **Normal**

### Warning

``` csv
test_name,value,unit
Glucose,185,mg/dL
```

Expected classification: **Warning**

### Critical

``` csv
test_name,value,unit
WBC,35,10^3/uL
```

Expected classification: **Critical**

For multiple submitted results, the interface prioritizes:

``` text
Critical → Warning → Normal
```

## Testing

The supplied synthetic CSV files can be used to exercise the CSV
workflow:

``` text
test_data/synthetic_normal.csv
test_data/synthetic_warning.csv
test_data/synthetic_critical.csv
```

The FastAPI endpoint can also be tested through:

``` text
http://127.0.0.1:8000/docs
```

The MCP tools can be inspected with MCP-compatible tooling.

## Error Handling

The application handles:

-   Invalid laboratory test names.
-   Missing laboratory data.
-   Non-numeric laboratory values.
-   Unsupported classification requests.
-   CSV files with missing required columns.
-   AI service failures.

## Explainable AI

The application does not return only a severity label such as:

``` text
WBC → Critical
```

It presents the observed test and value together with an AI-generated
explanation and recommended next step.

This supports the assignment's Explainable AI requirement by helping
users understand why a result was flagged rather than simply displaying
an abnormality label.

## Clinical Limitations

Reference ranges can vary according to laboratory methodology, patient
characteristics, age, sex, clinical context, and other factors.

The ranges configured in this demonstration should not be treated as
universal clinical standards.

AI-generated information may be incomplete or inappropriate for an
individual patient. This application is therefore a technical and
educational demonstration, not a medical diagnostic system.

## AI Provider

This project uses **Google Gemini** for the explanation stage.

Classification is performed using deterministic reference-range rules,
while Gemini generates the natural-language explanation and suggested
next step.

## Git History

The repository was developed iteratively with meaningful commits
covering:

-   Backend and MCP agent implementation.
-   Gemini AI clinical explanations.
-   React clinical analyzer interface.
-   Kaggle laboratory test support.
-   CSV input support.
-   Synthetic laboratory test datasets.
-   Clinical analyzer interface improvements.

## Assignment Alignment

  Requirement                  Implementation
  ---------------------------- -----------------------------------------------
  FastAPI backend              `backend/main.py`
  `POST /analyze_labs`         Implemented
  Classify → Route → Explain   Implemented
  MCP server                   `backend/mcp_server.py`
  MCP agent                    `backend/agent.py`
  LLM explanations             Google Gemini
  React frontend               `frontend/src/`
  Form input                   `LabInput.jsx`
  CSV input                    Papa Parse + `LabInput.jsx`
  Severity display             `SeverityBadge.jsx` + result cards
  AI explanations              `ResultsDisplay.jsx`
  Suggested next steps         Gemini-generated
  Kaggle dataset               Laboratory Test Results -- Anonymized Dataset
  Synthetic CSV data           `test_data/`

## License

See the repository `LICENSE` file for licensing information.

## Disclaimer

**This software is not a medical diagnostic system.**

It is a technical demonstration of a GenAI-enabled laboratory-result
analysis workflow. Laboratory results and AI-generated explanations
should be reviewed by qualified healthcare professionals before any
clinical decision is made.
