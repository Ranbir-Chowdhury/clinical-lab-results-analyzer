function SeverityBadge({ status }) {
  const statusClass = status.toLowerCase();

  return (
    <span className={`severity-badge ${statusClass}`}>
      {status}
    </span>
  );
}

export default SeverityBadge;