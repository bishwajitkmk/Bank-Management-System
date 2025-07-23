import { useAuth } from "../context/AuthContext";
import Header from "../components/common/Header";
import {
  CreditCard,
  TrendingUp,
  DollarSign,
  Activity,
  ArrowUpRight,
  ArrowDownRight,
} from "lucide-react";

const Dashboard = () => {
  const { user } = useAuth();

  // Mock data - in real app this would come from API
  const stats = [
    {
      name: "Total Balance",
      value: "$12,345.67",
      change: "+12.5%",
      changeType: "positive",
      icon: DollarSign,
    },
    {
      name: "Active Accounts",
      value: "3",
      change: "+1",
      changeType: "positive",
      icon: CreditCard,
    },
    {
      name: "Monthly Transactions",
      value: "47",
      change: "-5.2%",
      changeType: "negative",
      icon: Activity,
    },
    {
      name: "Investment Growth",
      value: "+$2,340",
      change: "+8.1%",
      changeType: "positive",
      icon: TrendingUp,
    },
  ];

  const recentTransactions = [
    {
      id: 1,
      type: "deposit",
      amount: 500,
      description: "Salary deposit",
      date: "2024-01-15",
      time: "09:30 AM",
    },
    {
      id: 2,
      type: "withdrawal",
      amount: -120,
      description: "ATM withdrawal",
      date: "2024-01-14",
      time: "02:15 PM",
    },
    {
      id: 3,
      type: "transfer",
      amount: -75,
      description: "Transfer to John Doe",
      date: "2024-01-13",
      time: "11:45 AM",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.username}!
          </h1>
          <p className="mt-2 text-gray-600">
            Here's what's happening with your accounts today.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat) => {
            const Icon = stat.icon;
            return (
              <div
                key={stat.name}
                className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">
                      {stat.name}
                    </p>
                    <p className="text-2xl font-bold text-gray-900 mt-1">
                      {stat.value}
                    </p>
                  </div>
                  <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
                    <Icon className="h-6 w-6 text-blue-600" />
                  </div>
                </div>
                <div className="flex items-center mt-4">
                  {stat.changeType === "positive" ? (
                    <ArrowUpRight className="h-4 w-4 text-green-500" />
                  ) : (
                    <ArrowDownRight className="h-4 w-4 text-red-500" />
                  )}
                  <span
                    className={`ml-1 text-sm font-medium ${
                      stat.changeType === "positive"
                        ? "text-green-600"
                        : "text-red-600"
                    }`}
                  >
                    {stat.change}
                  </span>
                  <span className="ml-2 text-sm text-gray-500">
                    from last month
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Recent Transactions */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">
              Recent Transactions
            </h2>
          </div>
          <div className="divide-y divide-gray-200">
            {recentTransactions.map((transaction) => (
              <div
                key={transaction.id}
                className="px-6 py-4 flex items-center justify-between"
              >
                <div className="flex items-center">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center ${
                      transaction.type === "deposit"
                        ? "bg-green-100"
                        : transaction.type === "withdrawal"
                        ? "bg-red-100"
                        : "bg-blue-100"
                    }`}
                  >
                    {transaction.type === "deposit" ? (
                      <ArrowUpRight className="h-5 w-5 text-green-600" />
                    ) : transaction.type === "withdrawal" ? (
                      <ArrowDownRight className="h-5 w-5 text-red-600" />
                    ) : (
                      <Activity className="h-5 w-5 text-blue-600" />
                    )}
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-900">
                      {transaction.description}
                    </p>
                    <p className="text-sm text-gray-500">
                      {transaction.date} at {transaction.time}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p
                    className={`text-sm font-medium ${
                      transaction.amount > 0 ? "text-green-600" : "text-red-600"
                    }`}
                  >
                    {transaction.amount > 0 ? "+" : ""}$
                    {Math.abs(transaction.amount).toFixed(2)}
                  </p>
                </div>
              </div>
            ))}
          </div>
          <div className="px-6 py-4 border-t border-gray-200">
            <button className="text-sm font-medium text-blue-600 hover:text-blue-500 transition-colors duration-200">
              View all transactions →
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
