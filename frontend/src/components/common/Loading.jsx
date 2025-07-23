import { Loader2 } from "lucide-react";

const Loading = ({ size = "default", text = "Loading..." }) => {
  const sizeClasses = {
    small: "w-4 h-4",
    default: "w-8 h-8",
    large: "w-12 h-12",
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="flex flex-col items-center space-y-4">
        <Loader2
          className={`${sizeClasses[size]} animate-spin text-blue-600`}
        />
        {text && <p className="text-gray-600 font-medium">{text}</p>}
      </div>
    </div>
  );
};

export default Loading;
