import { useState } from "react";

export default function ChatBox({ onSend }) {
  const [message, setMessage] = useState("");

  const submit = () => {
    if (!message.trim()) return;
    onSend(message);
    setMessage("");
  };

  return (
    <div>
      <input
        placeholder="Search candidates..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={submit}>Send</button>
    </div>
  );
}
