import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

// Your Firebase configuration
// Replace these values with your actual Firebase project configuration
const firebaseConfig = {
  apiKey: "AIzaSyBCIFDfQ9a3419O7k41c32B_JyLi3Ti2jY",
  authDomain: "publicmatrimoni.firebaseapp.com",
  projectId: "publicmatrimoni", // <-- THIS MUST BE YOUR REAL PROJECT ID
  storageBucket: "publicmatrimoni.appspot.com",
  messagingSenderId: "207954337407",
  appId: "1:207954337407:web:0105f0e18a6840361f294a",
  measurementId: "G-QVJ8TRM4GZ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore
export const db = getFirestore(app);
export const auth = getAuth(app);

export default app; 