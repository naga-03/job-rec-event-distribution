import api from "./api";
import { setToken } from "../utils/token";

export async function login(username, password) {
  const res = await api.post("/auth/login", {
    username,
    password,
  });

  const token = res.data.access_token;
  setToken(token);

  const payload = JSON.parse(atob(token.split(".")[1]));
  return payload.user_type;
}
