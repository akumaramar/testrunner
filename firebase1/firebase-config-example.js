// Example Firebase configuration
// Copy this file to src/firebase.js and replace the values with your actual Firebase project configuration

import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
    apiKey: "AIzaSyBCIFDfQ9a3419O7k41c32B_JyLi3Ti2jY",
    authDomain: "publicmatrimoni.firebaseapp.com",
    projectId: "publicmatrimoni",
    storageBucket: "publicmatrimoni.appspot.com",
    messagingSenderId: "207954337407",
    appId: "1:207954337407:web:0105f0e18a6840361f294a",
    measurementId: "G-QVJ8TRM4GZ"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore
export const db = getFirestore(app);

export default app; 