import { apiService } from "./api";

const accountService = {
  // Get all accounts for the current user
  getAccounts: async () => {
    const response = await apiService.get("/accounts");
    return response.data;
  },

  // Get a specific account by ID
  getAccount: async (accountId) => {
    const response = await apiService.get(`/accounts/${accountId}`);
    return response.data;
  },

  // Create a new account
  createAccount: async (accountType, currency = "USD") => {
    const response = await apiService.post("/accounts", {
      account_type: accountType,
      currency: currency,
    });
    return response.data;
  },

  // Update account details
  updateAccount: async (accountId, accountData) => {
    const response = await apiService.put(
      `/accounts/${accountId}`,
      accountData
    );
    return response.data;
  },

  // Delete an account
  deleteAccount: async (accountId) => {
    const response = await apiService.delete(`/accounts/${accountId}`);
    return response.data;
  },

  // Get account balance
  getBalance: async (accountId) => {
    const response = await apiService.get(`/accounts/${accountId}/balance`);
    return response.data;
  },

  // Deposit money into account
  deposit: async (accountId, amount, description = "") => {
    const response = await apiService.post(`/accounts/${accountId}/deposit`, {
      amount: amount,
      description: description,
    });
    return response.data;
  },

  // Withdraw money from account
  withdraw: async (accountId, amount, description = "") => {
    const response = await apiService.post(`/accounts/${accountId}/withdraw`, {
      amount: amount,
      description: description,
    });
    return response.data;
  },

  // Transfer money between accounts
  transfer: async (fromAccountId, toAccountId, amount, description = "") => {
    const response = await apiService.post("/transactions/transfer", {
      from_account_id: fromAccountId,
      to_account_id: toAccountId,
      amount: amount,
      description: description,
    });
    return response.data;
  },

  // Get account transactions
  getTransactions: async (accountId, page = 1, limit = 10) => {
    const response = await apiService.get(
      `/accounts/${accountId}/transactions`,
      {
        params: { page, limit },
      }
    );
    return response.data;
  },
};

export { accountService };
