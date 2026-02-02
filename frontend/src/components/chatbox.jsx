import { useState } from "react";

export default function ChatBox({ onSend }) {
  const [message, setMessage] = useState("");

  const submit = () => {
    if (!message.trim()) return;
    onSend(message);
    setMessage("");
  };

  return (
    <div style={{ display: "flex", gap: 10 }}>
      <input
        placeholder="Search candidates (e.g. 'Python Bangalore')..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && submit()}
        style={{
          flex: 1,
          padding: "12px 16px",
          borderRadius: 8,
          border: "1px solid #444",
          backgroundColor: "#1a1a1a",
          color: "white",
          fontSize: "1rem"
        }}
      />
      <button
        onClick={submit}
        style={{
          padding: "0 24px",
          backgroundColor: "#646cff",
          color: "white",
          fontWeight: "bold"
        }}
      >
        Send
      </button>
    </div>
  );
}
