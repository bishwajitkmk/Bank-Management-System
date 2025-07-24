import { apiService } from "./api";

export const authService = {
  // Register a new user
  register: async (username, email, password) => {
    const response = await apiService.post("/auth/register", {
      username,
      email,
      password,
    });
    return response.data;
  },

  // Login user
  login: async (username, password) => {
    const response = await apiService.post("/auth/login", {
      username,
      password,
    });
    return response.data;
  },

  // Get user profile
  getProfile: async () => {
    const response = await apiService.get("/auth/profile");
    return response.data.user;
  },

  // Change password
  changePassword: async (oldPassword, newPassword) => {
    const response = await apiService.post("/auth/change-password", {
      old_password: oldPassword,
      new_password: newPassword,
    });
    return response.data;
  },

  // Reset password
  resetPassword: async (username, email) => {
    const response = await apiService.post("/auth/reset-password", {
      username,
      email,
    });
    return response.data;
  },

  // Logout (client-side only)
  logout: async () => {
    try {
      await apiService.post("/auth/logout");
    } catch (error) {
      // Even if logout fails, we still want to clear local storage
      console.warn("Logout API call failed:", error);
    }
    // Clear local storage regardless of API response
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  },

  // Refresh token
  refreshToken: async () => {
    const response = await apiService.post("/auth/refresh");
    return response.data;
  },
};
