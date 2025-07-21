import React, { useState } from 'react';
import { auth } from './firebase';
import { signInWithPhoneNumber, RecaptchaVerifier } from 'firebase/auth';

function Login({ onLogin }) {
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState('phone'); // 'phone' or 'otp'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [confirmationResult, setConfirmationResult] = useState(null);

  const setupRecaptcha = () => {
    if (!window.recaptchaVerifier) {
      window.recaptchaVerifier = new RecaptchaVerifier(
        auth,
        'recaptcha-container',
        {
          size: 'invisible',
          callback: () => {},
        }       
      );
    }
  }; 

  const handleSendOtp = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    setupRecaptcha();
    try {
      const confirmation = await signInWithPhoneNumber(auth, phone, window.recaptchaVerifier);
      setConfirmationResult(confirmation);
      setStep('otp');
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await confirmationResult.confirm(otp);
      onLogin();
    } catch (err) {
      setError('Invalid OTP. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="login-container">
      <h2>Login with Mobile Number</h2>
      {step === 'phone' && (
        <form onSubmit={handleSendOtp} className="login-form">
          <input
            type="tel"
            placeholder="Enter mobile number (e.g. +1234567890)"
            value={phone}
            onChange={e => setPhone(e.target.value)}
            className="input-field"
            disabled={loading}
            required
          />
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Sending OTP...' : 'Send OTP'}
          </button>
        </form>
      )}
      {step === 'otp' && (
        <form onSubmit={handleVerifyOtp} className="login-form">
          <input
            type="text"
            placeholder="Enter OTP"
            value={otp}
            onChange={e => setOtp(e.target.value)}
            className="input-field"
            disabled={loading}
            required
          />
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Verifying...' : 'Verify OTP'}
          </button>
        </form>
      )}
      <div id="recaptcha-container"></div>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
}

export default Login; 