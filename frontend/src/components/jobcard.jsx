export default function JobCard({ data }) {
  return (
    <div className="glass" style={{
      padding: "20px",
      transition: "transform 0.2s ease, box-shadow 0.2s ease",
      cursor: "default"
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
        <div>
          <h4 style={{
            margin: 0,
            fontSize: "1.2rem",
            background: "linear-gradient(90deg, #fff, #94a3b8)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent"
          }}>
            {data.name}
          </h4>
          <div style={{ color: "var(--primary)", fontWeight: "600", fontSize: "0.9rem", marginTop: 2 }}>
            {data.headline}
          </div>
        </div>
        <div style={{
          background: "rgba(16, 185, 129, 0.1)",
          color: "var(--accent)",
          padding: "4px 12px",
          borderRadius: "20px",
          fontSize: "0.75rem",
          fontWeight: "700",
          border: "1px solid rgba(16, 185, 129, 0.2)"
        }}>
          MATCHED
        </div>
      </div>

      <div style={{ fontSize: "0.85em", color: "var(--text-muted)", display: "flex", gap: 15 }}>
        <span>📍 {data.location}</span>
        <span>💼 {data.experience_years} Years Experience</span>
      </div>

      <div style={{ marginTop: 20 }}>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {data.skills?.map(s => (
            <span key={s} style={{
              background: "rgba(255,255,255,0.03)",
              border: "1px solid rgba(255,255,255,0.08)",
              padding: "4px 12px",
              borderRadius: "8px",
              fontSize: "0.8rem",
              color: "#cbd5e1"
            }}>{s}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
