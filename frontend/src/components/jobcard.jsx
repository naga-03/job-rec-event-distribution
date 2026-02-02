export default function JobCard({ data }) {
  return (
    <div style={{ border: "1px solid #ccc", margin: 8, padding: 8 }}>
      <h4>{data.name}</h4>
      <p>{data.headline}</p>
      <p>Location: {data.location}</p>
      <p>Experience: {data.experience_years}</p>
      <p>Match Score: {data.match_score}</p>
    </div>
  );
}
