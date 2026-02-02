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
    <div>
      <button onClick={logout}>Logout</button>
      <h2>Recruiter Chat</h2>

      <ChatBox onSend={sendMessage} />

      {results.length === 0 && (
        <p>No matching candidates found.</p>
      )}

      {results.map((r) => (
        <JobCard key={r.user_id} data={r} />
      ))}
    </div>
  );
}
