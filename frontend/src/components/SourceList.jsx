export default function SourceList({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <ul>
      {sources.map((s, i) => (
        <li key={i}>
          <strong>{s.file}</strong>
          <p>{s.snippet}</p>
        </li>
      ))}
    </ul>
  );
}
