import { useState } from "react";
import LabInput from "./components/LabInput";
import ResultsDisplay from "./components/ResultsDisplay";
import "./App.css";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeLabs = async (labs) => {
    setLoading(true);
    setError("");
    setResults([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze_labs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ labs }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to analyze laboratory results.");
      }

      setResults(data.results);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the Clinical Lab Analyzer backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <div className="brand-icon">
  <svg
    viewBox="0 0 64 64"
    xmlns="http://www.w3.org/2000/svg"
    aria-label="Clinical laboratory logo"
    role="img"
  >
    <path
      d="M25 8h14"
      stroke="currentColor"
      strokeWidth="4"
      strokeLinecap="round"
    />

    <path
      d="M28 8v19L14 49c-2.5 4.5.7 10 5.9 10h24.2c5.2 0 8.4-5.5 5.9-10L36 27V8"
      fill="none"
      stroke="currentColor"
      strokeWidth="4"
      strokeLinejoin="round"
    />

    <path
      d="M19 43h26"
      stroke="currentColor"
      strokeWidth="4"
      strokeLinecap="round"
    />

    <path
      d="M23 37c3 2 5 2 8 0s5-2 9 0"
      fill="none"
      stroke="currentColor"
      strokeWidth="3"
      strokeLinecap="round"
    />

    <path
      d="M45 17v12M39 23h12"
      stroke="currentColor"
      strokeWidth="3"
      strokeLinecap="round"
    />
  </svg>
</div>

          <div>
            <h1>Clinical Lab Results Analyzer</h1>
            <p>
              AI-assisted interpretation of laboratory results using
              severity classification and explainable AI.
            </p>
          </div>
        </div>
      </header>

      <main className="container">
        <LabInput onAnalyze={analyzeLabs} loading={loading} />

        {error && (
          <div className="error-message">
            <strong>Analysis Error</strong>
            <p>{error}</p>
          </div>
        )}

        <ResultsDisplay results={results} />
      </main>

      <footer>
        <p>
          AI-generated information is for educational purposes and does not
          replace professional medical advice.
        </p>
      </footer>
    </div>
  );
}

export default App;