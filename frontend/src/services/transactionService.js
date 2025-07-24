import { apiService } from "./api";

const transactionService = {
  // Get all transactions for the current user
  getTransactions: async (page = 1, limit = 10) => {
    const response = await apiService.get("/transactions", {
      params: { page, limit },
    });
    return response.data;
  },

  // Get a specific transaction by ID
  getTransaction: async (transactionId) => {
    const response = await apiService.get(`/transactions/${transactionId}`);
    return response.data;
  },

  // Create a new transaction
  createTransaction: async (transactionData) => {
    const response = await apiService.post("/transactions", transactionData);
    return response.data;
  },

  // Get transactions for a specific account
  getAccountTransactions: async (accountId, page = 1, limit = 10) => {
    const response = await apiService.get(
      `/accounts/${accountId}/transactions`,
      {
        params: { page, limit },
      }
    );
    return response.data;
  },

  // Get transaction statistics
  getTransactionStats: async (startDate = null, endDate = null) => {
    const params = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;

    const response = await apiService.get("/transactions/stats", { params });
    return response.data;
  },

  // Export transactions
  exportTransactions: async (format = "csv", filters = {}) => {
    const response = await apiService.get("/transactions/export", {
      params: { format, ...filters },
      responseType: "blob",
    });
    return response.data;
  },
};

export { transactionService };
