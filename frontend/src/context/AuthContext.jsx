import { createContext, useContext, useState, useEffect } from "react";
import { authService } from "../services/authService";

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem("access_token"));
  const [refreshToken, setRefreshToken] = useState(
    localStorage.getItem("refresh_token")
  );

  useEffect(() => {
    const initializeAuth = async () => {
      if (token) {
        try {
          const userData = await authService.getProfile();
          setUser(userData);
        } catch (error) {
          console.error("Failed to get user profile:", error);
          logout();
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await authService.login(username, password);
      const { access_token, refresh_token, user: userData } = response;

      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);

      setToken(access_token);
      setRefreshToken(refresh_token);
      setUser(userData);

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || "Login failed",
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authService.register(userData);
      return { success: true, data: response };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || "Registration failed",
      };
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setToken(null);
    setRefreshToken(null);
    setUser(null);
  };

  const changePassword = async (oldPassword, newPassword) => {
    try {
      await authService.changePassword(oldPassword, newPassword);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || "Password change failed",
      };
    }
  };

  const resetPassword = async (username, email) => {
    try {
      await authService.resetPassword(username, email);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || "Password reset failed",
      };
    }
  };

  const value = {
    user,
    loading,
    token,
    login,
    register,
    logout,
    changePassword,
    resetPassword,
    isAuthenticated: !!user,
    isAdmin: user?.is_admin || false,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
