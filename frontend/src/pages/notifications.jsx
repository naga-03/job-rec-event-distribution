import { useEffect, useState } from "react";
import api from "../services/api";
import { useAuth } from "../context/authcontext";

export default function Notifications() {
  const { logout } = useAuth();
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const fetchNotifications = () => {
      api.get("/api/notifications").then((res) => {
        setNotifications(res.data);
      });
    };

    fetchNotifications(); // Initial fetch

    const interval = setInterval(fetchNotifications, 5000); // Poll every 5 seconds

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  return (
    <div>
      <button onClick={logout}>Logout</button>
      <h2>Notifications</h2>

      {notifications.length === 0 && (
        <p>No notifications yet.</p>
      )}

      {notifications.map((n) => (
        <div key={n.notification_id}>{n.message}</div>
      ))}
    </div>
  );
}
