import { useState } from "react";

export default function ChatBox({ onSend }) {
  const [message, setMessage] = useState("");

  const submit = () => {
    if (!message.trim()) return;
    onSend(message);
    setMessage("");
  };

  return (
    <div className="glass" style={{ display: "flex", gap: 12, padding: 8 }}>
      <input
        placeholder="How can I help you find talent today?..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && submit()}
        style={{
          flex: 1,
          padding: "14px 20px",
          borderRadius: 12,
          border: "1px solid rgba(255,255,255,0.05)",
          color: "white",
          fontSize: "0.95rem",
        }}
      />
      <button
        onClick={submit}
        style={{
          borderRadius: 12,
          display: "flex",
          alignItems: "center",
          gap: 8,
          padding: "0 28px"
        }}
      >
        <span>Search</span>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
        </svg>
      </button>
    </div>
  );
}
