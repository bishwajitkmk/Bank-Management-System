import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import Header from "../components/common/Header";
import {
  Plus,
  Filter,
  Download,
  ArrowUpRight,
  ArrowDownRight,
  ArrowLeftRight,
  Calendar,
  DollarSign,
  Search,
} from "lucide-react";
import { transactionService } from "../services/transactionService";
import { accountService } from "../services/accountService";
import toast from "react-hot-toast";

const Transactions = () => {
  const { user } = useAuth();
  const [transactions, setTransactions] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [filters, setFilters] = useState({
    accountId: "",
    type: "",
    startDate: "",
    endDate: "",
    search: "",
  });
  const [createForm, setCreateForm] = useState({
    type: "deposit",
    accountId: "",
    amount: "",
    description: "",
    toAccountId: "",
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      const [transactionsRes, accountsRes] = await Promise.all([
        transactionService.getTransactions(),
        accountService.getAccounts(),
      ]);

      setTransactions(transactionsRes.transactions || []);
      setAccounts(accountsRes.accounts || []);

      // Set default account for create form
      if (accountsRes.accounts && accountsRes.accounts.length > 0) {
        setCreateForm((prev) => ({
          ...prev,
          accountId: accountsRes.accounts[0].id,
        }));
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      toast.error("Failed to load transactions");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateTransaction = async (e) => {
    e.preventDefault();

    if (!createForm.accountId || !createForm.amount) {
      toast.error("Please fill in all required fields");
      return;
    }

    try {
      let response;

      if (createForm.type === "transfer") {
        if (!createForm.toAccountId) {
          toast.error("Please select destination account");
          return;
        }
        response = await accountService.transfer(
          createForm.accountId,
          createForm.toAccountId,
          parseFloat(createForm.amount),
          createForm.description
        );
      } else if (createForm.type === "deposit") {
        response = await accountService.deposit(
          createForm.accountId,
          parseFloat(createForm.amount),
          createForm.description
        );
      } else if (createForm.type === "withdraw") {
        response = await accountService.withdraw(
          createForm.accountId,
          parseFloat(createForm.amount),
          createForm.description
        );
      }

      if (response.message) {
        toast.success("Transaction completed successfully!");
        setShowCreateModal(false);
        setCreateForm({
          type: "deposit",
          accountId: accounts.length > 0 ? accounts[0].id : "",
          amount: "",
          description: "",
          toAccountId: "",
        });
        fetchData(); // Refresh the transactions list
      } else {
        toast.error(response.error || "Transaction failed");
      }
    } catch (error) {
      console.error("Error creating transaction:", error);
      toast.error("Failed to create transaction");
    }
  };

  const getTransactionIcon = (type) => {
    switch (type) {
      case "deposit":
        return <ArrowUpRight className="h-5 w-5 text-green-600" />;
      case "withdrawal":
        return <ArrowDownRight className="h-5 w-5 text-red-600" />;
      case "transfer":
        return <ArrowLeftRight className="h-5 w-5 text-blue-600" />;
      default:
        return <DollarSign className="h-5 w-5 text-gray-600" />;
    }
  };

  const getTransactionColor = (type) => {
    switch (type) {
      case "deposit":
        return "bg-green-100 text-green-800";
      case "withdrawal":
        return "bg-red-100 text-red-800";
      case "transfer":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const formatAmount = (amount, currency = "USD") => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: currency,
    }).format(Math.abs(amount));
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getAccountNumber = (accountId) => {
    const account = accounts.find((acc) => acc.id === accountId);
    return account ? account.account_number : "Unknown";
  };

  const filteredTransactions = transactions.filter((transaction) => {
    if (
      filters.accountId &&
      transaction.account_id !== parseInt(filters.accountId)
    )
      return false;
    if (filters.type && transaction.transaction_type !== filters.type)
      return false;
    if (
      filters.search &&
      !transaction.description
        .toLowerCase()
        .includes(filters.search.toLowerCase())
    )
      return false;
    if (
      filters.startDate &&
      new Date(transaction.created_at) < new Date(filters.startDate)
    )
      return false;
    if (
      filters.endDate &&
      new Date(transaction.created_at) > new Date(filters.endDate)
    )
      return false;
    return true;
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Transactions</h1>
            <p className="mt-2 text-gray-600">
              View and manage your transaction history
            </p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 transition-colors duration-200"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Transaction
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Account
              </label>
              <select
                value={filters.accountId}
                onChange={(e) =>
                  setFilters({ ...filters, accountId: e.target.value })
                }
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Accounts</option>
                {accounts.map((account) => (
                  <option key={account.id} value={account.id}>
                    {account.account_type.charAt(0).toUpperCase() +
                      account.account_type.slice(1)}{" "}
                    - {account.account_number}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Type
              </label>
              <select
                value={filters.type}
                onChange={(e) =>
                  setFilters({ ...filters, type: e.target.value })
                }
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Types</option>
                <option value="deposit">Deposit</option>
                <option value="withdrawal">Withdrawal</option>
                <option value="transfer">Transfer</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Start Date
              </label>
              <input
                type="date"
                value={filters.startDate}
                onChange={(e) =>
                  setFilters({ ...filters, startDate: e.target.value })
                }
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                End Date
              </label>
              <input
                type="date"
                value={filters.endDate}
                onChange={(e) =>
                  setFilters({ ...filters, endDate: e.target.value })
                }
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search descriptions..."
                  value={filters.search}
                  onChange={(e) =>
                    setFilters({ ...filters, search: e.target.value })
                  }
                  className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Transactions List */}
        {filteredTransactions.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
            <DollarSign className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No transactions found
            </h3>
            <p className="text-gray-600 mb-6">
              {transactions.length === 0
                ? "You haven't made any transactions yet."
                : "No transactions match your current filters."}
            </p>
            {transactions.length === 0 && (
              <button
                onClick={() => setShowCreateModal(true)}
                className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 transition-colors duration-200"
              >
                <Plus className="h-4 w-4 mr-2" />
                Make Your First Transaction
              </button>
            )}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex justify-between items-center">
                <h2 className="text-lg font-medium text-gray-900">
                  Transaction History ({filteredTransactions.length})
                </h2>
                <button className="flex items-center text-sm font-medium text-blue-600 hover:text-blue-500 transition-colors duration-200">
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </button>
              </div>
            </div>
            <div className="divide-y divide-gray-200">
              {filteredTransactions.map((transaction) => (
                <div
                  key={transaction.id}
                  className="px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors duration-200"
                >
                  <div className="flex items-center">
                    <div
                      className={`w-10 h-10 rounded-full flex items-center justify-center ${getTransactionColor(
                        transaction.transaction_type
                      )}`}
                    >
                      {getTransactionIcon(transaction.transaction_type)}
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-900">
                        {transaction.description ||
                          `${
                            transaction.transaction_type
                              .charAt(0)
                              .toUpperCase() +
                            transaction.transaction_type.slice(1)
                          }`}
                      </p>
                      <p className="text-sm text-gray-500">
                        Account: {getAccountNumber(transaction.account_id)} •{" "}
                        {formatDate(transaction.created_at)}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p
                      className={`text-sm font-medium ${
                        transaction.amount > 0
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      {transaction.amount > 0 ? "+" : ""}
                      {formatAmount(transaction.amount)}
                    </p>
                    <span
                      className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getTransactionColor(
                        transaction.transaction_type
                      )}`}
                    >
                      {transaction.transaction_type}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Create Transaction Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  New Transaction
                </h3>
                <form onSubmit={handleCreateTransaction} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Transaction Type
                    </label>
                    <select
                      value={createForm.type}
                      onChange={(e) =>
                        setCreateForm({ ...createForm, type: e.target.value })
                      }
                      className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="deposit">Deposit</option>
                      <option value="withdraw">Withdrawal</option>
                      <option value="transfer">Transfer</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Account
                    </label>
                    <select
                      value={createForm.accountId}
                      onChange={(e) =>
                        setCreateForm({
                          ...createForm,
                          accountId: e.target.value,
                        })
                      }
                      className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">Select Account</option>
                      {accounts.map((account) => (
                        <option key={account.id} value={account.id}>
                          {account.account_type.charAt(0).toUpperCase() +
                            account.account_type.slice(1)}{" "}
                          - {account.account_number}
                        </option>
                      ))}
                    </select>
                  </div>

                  {createForm.type === "transfer" && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        To Account
                      </label>
                      <select
                        value={createForm.toAccountId}
                        onChange={(e) =>
                          setCreateForm({
                            ...createForm,
                            toAccountId: e.target.value,
                          })
                        }
                        className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="">Select Destination Account</option>
                        {accounts
                          .filter(
                            (account) =>
                              account.id !== parseInt(createForm.accountId)
                          )
                          .map((account) => (
                            <option key={account.id} value={account.id}>
                              {account.account_type.charAt(0).toUpperCase() +
                                account.account_type.slice(1)}{" "}
                              - {account.account_number}
                            </option>
                          ))}
                      </select>
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Amount
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      min="0.01"
                      value={createForm.amount}
                      onChange={(e) =>
                        setCreateForm({ ...createForm, amount: e.target.value })
                      }
                      className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="0.00"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Description (Optional)
                    </label>
                    <input
                      type="text"
                      value={createForm.description}
                      onChange={(e) =>
                        setCreateForm({
                          ...createForm,
                          description: e.target.value,
                        })
                      }
                      className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Transaction description"
                    />
                  </div>

                  <div className="flex space-x-3 pt-4">
                    <button
                      type="button"
                      onClick={() => setShowCreateModal(false)}
                      className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 transition-colors duration-200"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 transition-colors duration-200"
                    >
                      Create Transaction
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Transactions;
