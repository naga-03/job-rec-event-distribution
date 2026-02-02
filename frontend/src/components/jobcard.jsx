export default function JobCard({ data }) {
  return (
    <div style={{
      border: "1px solid #444",
      borderRadius: 10,
      padding: 16,
      backgroundColor: "#1e1e1e",
      boxShadow: "0 4px 6px rgba(0,0,0,0.3)"
    }}>
      <h4 style={{ margin: "0 0 8px 0", color: "#646cff" }}>{data.name}</h4>
      <div style={{ fontWeight: "bold", fontSize: "0.9em", marginBottom: 4 }}>{data.headline}</div>
      <div style={{ fontSize: "0.85em", color: "#ccc" }}>📍 {data.location} | 💼 {data.experience_years} Years EXP</div>

      <div style={{ marginTop: 12, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ fontSize: "0.8em" }}>
          {data.skills?.map(s => (
            <span key={s} style={{
              background: "#333",
              padding: "2px 8px",
              borderRadius: 4,
              marginRight: 4,
              fontSize: "0.9em"
            }}>{s}</span>
          ))}
        </div>
        <div style={{ color: "#4ade80", fontWeight: "bold" }}>Score: {data.match_score}</div>
      </div>
    </div>
  );
}
