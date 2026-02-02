import { useState } from "react";
import api from "../services/api";
import ChatBox from "../components/chatbox";
import JobCard from "../components/jobcard";
import { useAuth } from "../context/authcontext";

export default function Chat() {
  const { logout } = useAuth();
  const [results, setResults] = useState([]);
  const [metadata, setMetadata] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (message) => {
    setIsLoading(true);
    try {
      const res = await api.post("/api/chat", { message });
      setResults(res.data.results || []);
      setMetadata(res.data.metadata || {});
    } catch (error) {
      console.error("Chat error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      maxWidth: "1000px",
      width: "100%",
      padding: "40px 20px",
      margin: "0 auto",
      display: "flex",
      flexDirection: "column",
      minHeight: "100vh"
    }}>
      <header style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: "40px"
      }}>
        <div>
          <h2 style={{ margin: 0, fontSize: "1.8rem", fontWeight: "800" }}>Talent Matcher</h2>
          <p style={{ margin: 0, color: "var(--text-muted)", fontSize: "0.9rem" }}>AI-Powered Candidate Discovery</p>
        </div>
        <button
          onClick={logout}
          style={{
            background: "transparent",
            border: "1px solid var(--glass-border)",
            color: "var(--text-muted)",
            padding: "8px 16px",
            fontSize: "0.85rem"
          }}
        >
          Sign Out
        </button>
      </header>

      <main style={{ flex: 1 }}>
        <div style={{ marginBottom: "40px" }}>
          <ChatBox onSend={sendMessage} />
        </div>

        <div style={{ textAlign: "left" }}>
          {(metadata.keywords?.length > 0 || metadata.ai_reason) && (
            <div className="glass" style={{ padding: "24px", marginBottom: "40px", borderLeft: "4px solid var(--primary)" }}>
              {metadata.keywords?.length > 0 && (
                <div style={{ fontSize: "0.9em", color: "var(--text-muted)", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{ fontSize: "1.2rem" }}>🔍</span>
                  <span>
                    <strong>Extracted Intent:</strong> {metadata.keywords.join(", ")}
                  </span>
                </div>
              )}

              {metadata.ai_reason && (
                <div style={{
                  display: "flex",
                  gap: 12,
                  alignItems: "flex-start",
                  fontSize: "1.05rem",
                  lineHeight: "1.6"
                }}>
                  <span style={{
                    fontSize: "1.2rem",
                    background: "rgba(99, 102, 241, 0.1)",
                    padding: "6px",
                    borderRadius: "8px"
                  }}>🤖</span>
                  <div>
                    <strong style={{ color: "var(--primary)", display: "block", marginBottom: 4, fontSize: "0.85rem", textTransform: "uppercase", letterSpacing: "0.05em" }}>AI Recommendation</strong>
                    {metadata.ai_reason}
                  </div>
                </div>
              )}
            </div>
          )}

          <section>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
              <h3 style={{ margin: 0 }}>Matching Candidates</h3>
              {results.length > 0 && (
                <span style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>{results.length} profiles found</span>
              )}
            </div>

            {isLoading ? (
              <div style={{ textAlign: "center", padding: "60px", color: "var(--text-muted)" }}>
                Analysing profiles and calculating matches...
              </div>
            ) : results.length === 0 ? (
              <div className="glass" style={{ padding: "60px", textAlign: "center", color: "var(--text-muted)" }}>
                <div style={{ fontSize: "2rem", marginBottom: "16px" }}>⚡</div>
                <p>Ready to find your next star? Try searching for specific skills or locations.</p>
                <div style={{ display: "flex", gap: 10, justifyContent: "center", marginTop: 20 }}>
                  <code style={{ background: "rgba(255,255,255,0.05)", padding: "4px 8px", borderRadius: 4 }}>"Python Developer"</code>
                  <code style={{ background: "rgba(255,255,255,0.05)", padding: "4px 8px", borderRadius: 4 }}>"Bangalore Backend"</code>
                </div>
              </div>
            ) : (
              <div style={{ display: "grid", gap: 20, gridTemplateColumns: "repeat(auto-fill, minmax(450px, 1fr))" }}>
                {results.map((r) => (
                  <JobCard key={r.user_id} data={r} />
                ))}
              </div>
            )}
          </section>
        </div>
      </main>

      <footer style={{ marginTop: 60, textAlign: "center", color: "var(--text-muted)", fontSize: "0.8rem" }}>
        Powered by Ollama Semantic Search Engine
      </footer>
    </div>
  );
}
