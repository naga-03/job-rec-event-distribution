import { AuthProvider, useAuth } from "./context/authcontext";
import Login from "./pages/Login";
import Chat from "./pages/chat";
import Notifications from "./pages/notifications";

function RoleRouter() {
  const { userType, logout } = useAuth();

  if (!userType) return <Login />;
  if (userType === "recruiter") return <Chat />;
  if (userType === "job_seeker") return <Notifications />;

  // Handle invalid userType by logging out and showing login
  logout();
  return <Login />;
}

export default function App() {
  return (
    <AuthProvider>
      <RoleRouter />
    </AuthProvider>
  );
}
