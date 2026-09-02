import SeverityBadge from "./SeverityBadge";

function ResultsDisplay({ results }) {
  if (!results || results.length === 0) {
    return null;
  }

  return (
    <section className="results-section">
      <div className="section-heading">
        <div>
          <h2>Analysis Results</h2>
          <p>
            Results are prioritized by severity and explained using AI.
          </p>
        </div>
      </div>

      <div className="results-list">
        {results.map((result, index) => (
          <article
            className={`result-card ${result.status.toLowerCase()}`}
            key={`${result.test_name}-${index}`}
          >
            <div className="result-header">
              <div>
                <h3>{result.test_name}</h3>
                <div className="result-value">
                  {result.value} {result.unit}
                </div>
              </div>

              <SeverityBadge status={result.status} />
            </div>

            <div className="result-content">
              <div className="result-block">
                <h4>AI Explanation</h4>
                <p>{result.explanation}</p>
              </div>

              <div className="result-block">
                <h4>Recommended Next Step</h4>
                <p>{result.next_step}</p>
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default ResultsDisplay;