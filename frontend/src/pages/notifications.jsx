import { useEffect, useState } from "react";
import api from "../services/api";
import { useAuth } from "../context/authcontext";

export default function Notifications() {
  const { logout } = useAuth();
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const fetchNotifications = () => {
      api.get("/api/notifications").then((res) => {
        setNotifications(res.data.data || []);
      });
    };

    fetchNotifications();
    const interval = setInterval(fetchNotifications, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{
      maxWidth: "800px",
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
          <h2 style={{ margin: 0, fontSize: "1.8rem", fontWeight: "800" }}>Your Notifications</h2>
          <p style={{ margin: 0, color: "var(--text-muted)", fontSize: "0.9rem" }}>Stay updated on your carrier opportunities</p>
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
        {notifications.length === 0 ? (
          <div className="glass" style={{ padding: "60px", textAlign: "center", color: "var(--text-muted)" }}>
            <div style={{ fontSize: "2rem", marginBottom: "16px" }}>📭</div>
            <p>You're all caught up! Matches will appear here once recruiters search for your skills.</p>
          </div>
        ) : (
          <div style={{ display: "grid", gap: 16 }}>
            {notifications.map((n) => (
              <div
                key={n.notification_id}
                className="glass"
                style={{
                  padding: "20px",
                  textAlign: "left",
                  borderLeft: n.read ? "1px solid var(--glass-border)" : "4px solid var(--primary)",
                  animation: "fadeIn 0.3s ease-out"
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
                  <div style={{ fontWeight: "bold", fontSize: "1.1rem" }}>
                    ✨ New Job Match Found
                  </div>
                  <small style={{ color: "var(--text-muted)", fontSize: "0.75rem" }}>
                    {new Date(n.created_at).toLocaleDateString()}
                  </small>
                </div>

                <div style={{ color: "var(--text-muted)", fontSize: "0.95rem", lineHeight: "1.6" }}>
                  {n.message}
                </div>

                <div style={{ marginTop: 16, fontSize: "0.8rem", display: "flex", gap: 8, alignItems: "center" }}>
                  <span style={{
                    background: "rgba(99, 102, 241, 0.1)",
                    color: "var(--primary)",
                    padding: "4px 10px",
                    borderRadius: "6px",
                    fontWeight: "600"
                  }}>
                    ACTION REQUIRED
                  </span>
                  <span style={{ color: "var(--text-muted)" }}>•</span>
                  <span style={{ color: "var(--text-muted)" }}>Recruiter is reviewing your profile</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      <footer style={{ marginTop: 60, textAlign: "center", color: "var(--text-muted)", fontSize: "0.8rem" }}>
        © 2026 Talent Matcher Engine v2.0
      </footer>
    </div>
  );
}
