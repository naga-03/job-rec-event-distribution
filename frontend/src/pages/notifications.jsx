import { useEffect, useState } from "react";
import api from "../services/api";
import { useAuth } from "../context/authcontext";

export default function Notifications() {
  const { logout } = useAuth();
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const fetchNotifications = () => {
      api.get("/api/notifications").then((res) => {
        // ✅ Standard API returns { success: true, count: X, data: [...] }
        setNotifications(res.data.data || []);
      });
    };

    fetchNotifications(); // Initial fetch

    const interval = setInterval(fetchNotifications, 5000); // Poll every 5 seconds

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <button onClick={logout}>Logout</button>
      <h2>Notifications</h2>

      {notifications.length === 0 && (
        <p>No notifications yet.</p>
      )}

      {notifications.map((n) => (
        <div
          key={n.notification_id}
          style={{
            border: "1px solid #444",
            borderRadius: 8,
            padding: 15,
            margin: "10px 0",
            backgroundColor: "#1e1e1e",
            textAlign: "left"
          }}
        >
          <div style={{ fontWeight: "bold", marginBottom: 5 }}>New Job Match</div>
          <div>{n.message}</div>
          <small style={{ color: "#888" }}>
            {new Date(n.created_at).toLocaleString()}
          </small>
        </div>
      ))}
    </div>
  );
}
