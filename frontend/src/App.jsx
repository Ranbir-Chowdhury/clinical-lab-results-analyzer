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
          <div className="brand-icon">+</div>

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