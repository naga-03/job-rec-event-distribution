import api from "./api";
import { setToken } from "../utils/token";

export async function login(username, password) {
  console.log("auth service: sending login request for", username);
  const res = await api.post("/api/auth/login", {
    username,
    password,
  });
  console.log("auth service: login response received", res.status);

  const token = res.data.access_token;
  setToken(token);

  const payload = JSON.parse(atob(token.split(".")[1]));
  return payload.user_type;
}
