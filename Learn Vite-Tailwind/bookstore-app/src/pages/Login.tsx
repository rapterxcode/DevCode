"use client";

import * as React from "react";

// @icons
import { Wallet } from "iconoir-react";

// @types
interface Web3LoginProps {}

export default function Login({}: Web3LoginProps) {
  const [email, setEmail] = React.useState("");

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handleConnect = () => {
    console.log("Connecting with email:", email);
  };

  const handleGoogleSignIn = () => {
    console.log("Signing in with Google");
  };

  const handleWalletAuth = () => {
    console.log("Wallet authentication");
  };

  return (
    <div className="max-w-lg mx-auto bg-white rounded-lg shadow-lg border border-blue-200">
      <div className="p-8 text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Web3 Login Simplified
        </h2>
        <p className="text-gray-600 max-w-lg mx-auto">
          Enjoy quick and secure access to your accounts on various Web3
          platforms.
        </p>
      </div>
      <div className="p-8 space-y-4">
        <div className="w-full space-y-1.5">
          <label className="text-sm font-semibold text-gray-700">
            Your Email
          </label>
          <input 
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            id="email" 
            type="email" 
            placeholder="name@mail.com" 
            value={email}
            onChange={handleEmailChange}
          />
        </div>
        <button 
          className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors font-medium"
          onClick={handleConnect}
        >
          Connect
        </button>
        <button
          className="w-full border border-gray-300 text-gray-700 py-3 px-4 rounded-lg hover:bg-gray-50 transition-colors font-medium flex items-center justify-center gap-3"
          onClick={handleGoogleSignIn}
        >
          <img
            src="https://v3.material-tailwind.com/icon/google.svg"
            alt="google"
            className="w-5 h-5"
          />
          Sign in with Google
        </button>
        <button
          className="w-full border border-gray-300 text-gray-700 py-3 px-4 rounded-lg hover:bg-gray-50 transition-colors font-medium flex items-center justify-center gap-3"
          onClick={handleWalletAuth}
        >
          <Wallet className="w-5 h-5 stroke-2" /> 
          Wallet Authentication
        </button>
      </div>
      <div className="px-8 pb-8 pt-0">
        <p className="text-sm text-center text-gray-600 max-w-xs mx-auto">
          Upon signing in, you consent to abide by our{" "}
          <a href="#" className="text-blue-600 hover:underline">
            Terms of Service
          </a>{" "}
          &{" "}
          <a href="#" className="text-blue-600 hover:underline">
            Privacy Policy.
          </a>
        </p>
      </div>
    </div>
  );
}