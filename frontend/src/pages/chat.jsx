import { useState } from "react";
import api from "../services/api";
import ChatBox from "../components/chatbox";
import JobCard from "../components/jobcard";
import { useAuth } from "../context/authcontext";

export default function Chat() {
  const { logout } = useAuth();
  const [results, setResults] = useState([]);

  const sendMessage = async (message) => {
    const res = await api.post("/api/chat", { message });
    setResults(res.data.results || []);
  };

  return (
    <div style={{ padding: 20, maxWidth: 800, margin: "0 auto" }}>
      <button onClick={logout} style={{ float: "right" }}>Logout</button>
      <div style={{ clear: "both" }}></div>

      <h2>Recruiter Chat</h2>

      <div style={{ marginBottom: 30 }}>
        <ChatBox onSend={sendMessage} />
      </div>

      <div style={{ textAlign: "left" }}>
        <h3>Matching Candidates</h3>
        {results.length === 0 && (
          <p style={{ color: "#888" }}>Try searching for 'Python' or 'Bangalore' to find matches.</p>
        )}

        <div style={{ display: "grid", gap: 15 }}>
          {results.map((r) => (
            <JobCard key={r.user_id} data={r} />
          ))}
        </div>
      </div>
    </div>
  );
}
