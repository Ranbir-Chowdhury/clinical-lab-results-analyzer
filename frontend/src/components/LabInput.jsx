import { useState } from "react";
import Papa from "papaparse";

const TEST_OPTIONS = [
  { name: "Glucose", unit: "mg/dL" },
  { name: "Hemoglobin", unit: "g/dL" },
  { name: "WBC", unit: "10^3/uL" },
  { name: "Platelet Count", unit: "10^3/uL" },
  { name: "Creatinine", unit: "mg/dL" },
  { name: "Cholesterol", unit: "mg/dL" },
  { name: "Ferritin", unit: "ug/L" },
  { name: "Glycosylated Hemoglobin (HbA1c)", unit: "%" },
  { name: "Total IgE", unit: "KU/L" },
  { name: "Insulin", unit: "mU/L" },
  { name: "Free T4", unit: "ng/dL" },
  { name: "Leukocyte", unit: "10^3/uL"},
  { name: "RBC", unit: "10^6/uL" },
  { name: "RDW-SD", unit: "fL" },
  { name: "RDW", unit: "%" },
  { name: "PDW", unit: "fL" },
  { name: "PCT", unit: "%" },
  { name: "Neutrophil %", unit: "%" },
  { name: "Monocyte %", unit: "%" },
  { name: "Lymphocyte %", unit: "%" },
  { name: "Hematocrit", unit: "%" },
  { name: "pH (Strip)", unit: "-" },
  { name: "Specific Gravity (Strip)", unit: "-" }
];

function LabInput({ onAnalyze, loading }) {
  const [labs, setLabs] = useState([
    {
      test_name: "",
      value: "",
      unit: "",
    },
  ]);

  const addLab = () => {
    setLabs([
      ...labs,
      {
        test_name: "",
        value: "",
        unit: "",
      },
    ]);
  };

  const removeLab = (index) => {
    if (labs.length === 1) return;

    setLabs(labs.filter((_, i) => i !== index));
  };

  const updateLab = (index, field, value) => {
    const updatedLabs = [...labs];

    if (field === "test_name") {
      const selectedTest = TEST_OPTIONS.find(
        (test) => test.name === value
      );

      updatedLabs[index] = {
        ...updatedLabs[index],
        test_name: value,
        unit: selectedTest ? selectedTest.unit : "",
      };
    } else {
      updatedLabs[index][field] = value;
    }

    setLabs(updatedLabs);
  };

  const handleCsvUpload = (event) => {
  const file = event.target.files[0];

  if (!file) {
    return;
  }

  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,

    complete: (results) => {
      if (results.errors.length > 0) {
        alert("Unable to read the CSV file. Please check its format.");
        return;
      }

      const requiredColumns = ["test_name", "value", "unit"];
      const headers = results.meta.fields || [];

      const missingColumns = requiredColumns.filter(
        (column) => !headers.includes(column)
      );

      if (missingColumns.length > 0) {
        alert(
          `CSV is missing required columns: ${missingColumns.join(", ")}`
        );
        return;
      }

      const parsedLabs = results.data
        .map((row) => ({
          test_name: row.test_name?.trim(),
          value: row.value?.trim(),
          unit: row.unit?.trim(),
        }))
        .filter(
          (lab) =>
            lab.test_name &&
            lab.value !== "" &&
            lab.unit
        );

      if (parsedLabs.length === 0) {
        alert("No valid laboratory results were found in the CSV.");
        return;
      }

      const invalidRows = parsedLabs.filter(
        (lab) => Number.isNaN(Number(lab.value))
      );

      if (invalidRows.length > 0) {
        alert("CSV contains laboratory values that are not numeric.");
        return;
      }

      setLabs(
        parsedLabs.map((lab) => ({
          test_name: lab.test_name,
          value: Number(lab.value),
          unit: lab.unit,
        }))
      );
    },

    error: () => {
      alert("Unable to read the CSV file.");
    },
  });

  event.target.value = "";
};

  const handleSubmit = (event) => {
    event.preventDefault();

    const validLabs = labs
      .filter(
        (lab) =>
          lab.test_name &&
          lab.value !== "" &&
          lab.unit
      )
      .map((lab) => ({
        test_name: lab.test_name,
        value: Number(lab.value),
        unit: lab.unit,
      }));

    if (validLabs.length === 0) {
      alert("Please enter at least one laboratory result.");
      return;
    }

    onAnalyze(validLabs);
  };

  return (
    <form className="lab-input" onSubmit={handleSubmit}>
      <div className="section-heading">
        <div>
          <h2>Enter Laboratory Results</h2>
          <p>
            Add one or more laboratory test results for AI-powered analysis.
          </p>
        </div>
      </div>

      {labs.map((lab, index) => (
        <div className="lab-row" key={index}>
          <div className="field">
            <label>Test Name</label>

            <select
              value={lab.test_name}
              onChange={(e) =>
                updateLab(index, "test_name", e.target.value)
              }
            >
              <option value="">Select a test</option>

              {TEST_OPTIONS.map((test) => (
                <option key={test.name} value={test.name}>
                  {test.name}
                </option>
              ))}
            </select>
          </div>

          <div className="field">
            <label>Value</label>

            <input
              type="number"
              step="any"
              placeholder="Enter value"
              value={lab.value}
              onChange={(e) =>
                updateLab(index, "value", e.target.value)
              }
            />
          </div>

          <div className="field">
            <label>Unit</label>

            <input
              type="text"
              value={lab.unit}
              readOnly
              placeholder="Unit"
            />
          </div>

          <button
            type="button"
            className="remove-button"
            onClick={() => removeLab(index)}
            disabled={labs.length === 1}
          >
            Remove
          </button>
        </div>
      ))}
      
      <div className="csv-upload">
        <label htmlFor="csv-file">
          Upload CSV
        </label>

        <input
          id="csv-file"
          type="file"
          accept=".csv,text/csv"
          onChange={handleCsvUpload}
        />

        <p>
          CSV columns: test_name, value, unit
        </p>
      </div>

      <div className="input-actions">
        <button
          type="button"
          className="secondary-button"
          onClick={addLab}
        >
          + Add Test
        </button>

        <button
          type="submit"
          className="primary-button"
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Results"}
        </button>
      </div>
    </form>
  );
}

export default LabInput;