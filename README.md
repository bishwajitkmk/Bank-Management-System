# 🏦 SecureBank - Professional Bank Management System

A modern, full-stack bank management system built with **Python Flask** backend and **React** frontend, featuring a professional UI/UX design with Tailwind CSS.

## ✨ Features

### 🔐 Authentication & Security

- **JWT-based authentication** with access and refresh tokens
- **Secure password hashing** using Werkzeug
- **Protected routes** with role-based access control
- **Input validation** and sanitization
- **CORS support** for cross-origin requests

### 💳 Account Management

- **Multi-account support** per user
- **Account types**: Savings, Checking, Business
- **Unique account numbers** with auto-generation
- **Real-time balance tracking**
- **Account status management**

### 💰 Transaction Operations

- **Deposit** and **Withdrawal** functionality
- **Inter-account transfers**
- **Transaction history** with detailed records
- **Reference number generation** for tracking
- **Transaction status management**

### 👨‍💼 Admin Panel

- **User management** and monitoring
- **Transaction oversight**
- **System reports** and analytics
- **Account administration**

### 🎨 Modern UI/UX

- **Responsive design** for all devices
- **Professional dashboard** with statistics
- **Real-time notifications** with toast messages
- **Dark mode support** (planned)
- **Accessibility compliant**

## 🏗️ Architecture

```
bank-management-system/
├── backend/                 # Python Flask API
│   ├── app/
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities & validators
│   ├── requirements.txt
│   └── run.py
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── context/       # React context
│   │   └── utils/         # Utilities
│   └── package.json
└── docs/                  # Documentation
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm** or **yarn**

### Backend Setup

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask server:**

   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**

   ```bash
   npm install
   ```

3. **Start the development server:**

   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

## 📋 API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/change-password` - Change password
- `POST /api/auth/reset-password` - Reset password
- `GET /api/auth/profile` - Get user profile
- `POST /api/auth/logout` - User logout

### Accounts (Coming Soon)

- `GET /api/accounts` - Get user accounts
- `POST /api/accounts` - Create new account
- `GET /api/accounts/{id}` - Get account details
- `PUT /api/accounts/{id}` - Update account

### Transactions (Coming Soon)

- `GET /api/transactions` - Get transaction history
- `POST /api/transactions/deposit` - Make deposit
- `POST /api/transactions/withdraw` - Make withdrawal
- `POST /api/transactions/transfer` - Transfer funds

### Admin (Coming Soon)

- `GET /api/admin/users` - Get all users
- `GET /api/admin/transactions` - Get all transactions
- `GET /api/admin/reports` - Generate reports

## 🎯 Current Status

### ✅ Completed

- [x] **Backend API Structure** - Flask app with proper architecture
- [x] **Database Models** - User, Account, Transaction models
- [x] **Authentication System** - JWT-based auth with validation
- [x] **Frontend Structure** - React app with routing
- [x] **Authentication Context** - Global state management
- [x] **Login Page** - Professional login interface
- [x] **Dashboard** - Basic dashboard with mock data
- [x] **Header Component** - Navigation and user menu
- [x] **API Service Layer** - Axios configuration with interceptors

### 🚧 In Progress

- [ ] **Account Management** - Create, view, manage accounts
- [ ] **Transaction Operations** - Deposit, withdraw, transfer
- [ ] **Admin Panel** - User management and monitoring
- [ ] **Registration Page** - User registration form
- [ ] **Real-time Updates** - Live balance and transaction updates

### 📋 Planned Features

- [ ] **Advanced Analytics** - Charts and reporting
- [ ] **Export Functionality** - PDF statements, CSV reports
- [ ] **Notifications** - Email and SMS alerts
- [ ] **Mobile App** - React Native version
- [ ] **Multi-language Support** - Internationalization
- [ ] **Dark Mode** - Theme switching
- [ ] **Advanced Security** - 2FA, biometric authentication

## 🛠️ Technology Stack

### Backend

- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing
- **Werkzeug** - Security utilities
- **SQLite** - Database (can be upgraded to PostgreSQL/MySQL)

### Frontend

- **React 18** - UI library
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **React Hot Toast** - Notifications
- **Lucide React** - Icons
- **Tailwind CSS** - Styling framework
- **Vite** - Build tool

## 🔧 Development

### Code Style

- **Backend**: Follow PEP 8 Python style guide
- **Frontend**: ESLint configuration included
- **Components**: Functional components with hooks
- **State Management**: React Context API

### Testing

- **Backend**: Unit tests with pytest (planned)
- **Frontend**: Component tests with React Testing Library (planned)
- **E2E**: Cypress tests (planned)

## 📦 Deployment

### Backend Deployment

```bash
# Production setup
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Frontend Deployment

```bash
# Build for production
npm run build

# Serve static files
npm run preview
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Contact the development team
- Check the documentation in the `docs/` folder

---

**Built with ❤️ for modern banking solutions**
