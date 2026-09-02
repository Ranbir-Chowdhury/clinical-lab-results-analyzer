import { useState } from "react";

const TEST_UNITS = {
  Glucose: "mg/dL",
  Hemoglobin: "g/dL",
  WBC: "10^3/uL",
  "Platelet Count": "10^3/uL",
  Creatinine: "mg/dL",
  Cholesterol: "mg/dL",
};

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

  updatedLabs[index][field] = value;

  if (field === "test_name") {
    updatedLabs[index].unit = TEST_UNITS[value] || "";
  }

  setLabs(updatedLabs);
};

  const handleSubmit = (event) => {
    event.preventDefault();

    const validLabs = labs
      .filter(
        (lab) =>
          lab.test_name.trim() &&
          lab.value !== "" &&
          lab.unit.trim()
      )
      .map((lab) => ({
        test_name: lab.test_name.trim(),
        value: Number(lab.value),
        unit: lab.unit.trim(),
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
    <option value="Glucose">Glucose</option>
    <option value="Hemoglobin">Hemoglobin</option>
    <option value="WBC">WBC</option>
    <option value="Platelet Count">Platelet Count</option>
    <option value="Creatinine">Creatinine</option>
    <option value="Cholesterol">Cholesterol</option>
  </select>
</div>

          <div className="field">
            <label>Value</label>
            <input
              type="number"
              step="any"
              placeholder="e.g. 180"
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
              placeholder="e.g. mg/dL"
              value={lab.unit}
              onChange={(e) =>
                updateLab(index, "unit", e.target.value)
              }
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