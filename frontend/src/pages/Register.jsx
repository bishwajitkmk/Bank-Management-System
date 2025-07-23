import { Link } from "react-router-dom";
import { Building2 } from "lucide-react";

const Register = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="flex justify-center">
            <Building2 className="h-12 w-12 text-blue-600" />
          </div>
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            Register for SecureBank
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Registration form coming soon...
          </p>
        </div>

        <div className="bg-white py-8 px-6 shadow-xl rounded-lg border border-gray-200 text-center">
          <p className="text-gray-600 mb-4">
            Registration functionality will be implemented soon.
          </p>
          <Link
            to="/login"
            className="font-medium text-blue-600 hover:text-blue-500 transition-colors duration-200"
          >
            Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Register;
