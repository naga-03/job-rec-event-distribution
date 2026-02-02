import { createContext, useContext, useState } from "react";
import { login as loginApi } from "../services/auth";
import { clearToken } from "../utils/token";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [userType, setUserType] = useState(() => {
    const savedType = localStorage.getItem("userType");
    console.log("AuthProvider: Initializing userType from localStorage:", savedType);
    return savedType;
  });

  const login = async (username, password) => {
    const role = await loginApi(username, password);
    console.log("AuthProvider: Login successful, role:", role);
    localStorage.setItem("userType", role);
    setUserType(role);
  };

  const logout = () => {
    clearToken();
    localStorage.removeItem("userType");
    setUserType(null);
  };

  return (
    <AuthContext.Provider value={{ userType, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
