import { baseAxios, authApi, createEndpoint } from "../config/axios";

const AUTH_BASE = "auth";

const authAPI = {
  register: (data: {
    first_name: string;
    last_name: string;
    username: string;
    email: string;
    password: string;
    password2: string;
  }) => {
    return baseAxios.post(createEndpoint(`${AUTH_BASE}/register/`), data);
  },

  login: (data: { username: string; password: string }) => {
    return baseAxios.post(createEndpoint(`${AUTH_BASE}/login/`), data);
  },

  logout: (refreshToken: string) => {
    return authApi.post(createEndpoint(`${AUTH_BASE}/logout/`), {
      refresh: refreshToken,
    });
  },

  getProfile: () => {
    return authApi.get(createEndpoint(`${AUTH_BASE}/profile/`));
  },

  updateProfile: (data: {
    first_name?: string;
    last_name?: string;
    email?: string;
  }) => {
    return authApi.patch(createEndpoint(`${AUTH_BASE}/profile/`), data);
  },

  changePassword: (data: {
    old_password: string;
    new_password: string;
    new_password2: string;
  }) => {
    return authApi.put(createEndpoint(`${AUTH_BASE}/password/change/`), data);
  },

  resetPassword: (email: string) => {
    return baseAxios.post(createEndpoint(`${AUTH_BASE}/password/reset/`), {
      email,
    });
  },

  refreshToken: (refreshToken: string) => {
    return baseAxios.post(createEndpoint(`${AUTH_BASE}/token/refresh/`), {
      refresh: refreshToken,
    });
  },
};

export default authAPI;
