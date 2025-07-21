# 🔥 Firestore Test Application

A simple React application to test Firebase Firestore database operations. This app provides a clean interface to perform basic CRUD (Create, Read, Update, Delete) operations on Firestore.

## Features

- ✅ **Add Items**: Create new items with text content
- ✅ **View Items**: Display all items from Firestore with timestamps
- ✅ **Edit Items**: Update existing items inline
- ✅ **Delete Items**: Remove items from the database
- ✅ **Real-time Updates**: See changes immediately after operations
- ✅ **Modern UI**: Beautiful, responsive design with smooth animations
- ✅ **Loading States**: Visual feedback during database operations

## Prerequisites

- Node.js (version 14 or higher)
- npm or yarn
- Firebase project with Firestore enabled

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Firebase Configuration

1. **Create a Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Add project" and follow the setup wizard
   - Enable Firestore Database in your project

2. **Get Your Firebase Config**:
   - In Firebase Console, go to Project Settings (gear icon)
   - Scroll down to "Your apps" section
   - Click "Add app" and choose "Web"
   - Register your app and copy the configuration object

3. **Update Firebase Config**:
   - Open `src/firebase.js`
   - Replace the placeholder values with your actual Firebase configuration:

```javascript
const firebaseConfig = {
  apiKey: "your-actual-api-key",
  authDomain: "your-project-id.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project-id.appspot.com",
  messagingSenderId: "your-messaging-sender-id",
  appId: "your-app-id"
};
```

### 3. Firestore Security Rules

Make sure your Firestore security rules allow read/write access. For testing purposes, you can use these rules (⚠️ **NOT for production**):

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

**Important**: These rules allow anyone to read and write to your database. For production, implement proper authentication and authorization.

### 4. Start the Application

```bash
npm start
```

The application will open at `http://localhost:3000`

## Usage

1. **Adding Items**: Type text in the input field and click "Add Item"
2. **Viewing Items**: All items are automatically loaded and displayed
3. **Editing Items**: Click the "Edit" button on any item, modify the text, and click "Save"
4. **Deleting Items**: Click the "Delete" button on any item to remove it

## Project Structure

```
src/
├── App.js          # Main React component with CRUD operations
├── App.css         # Styles for the application
├── firebase.js     # Firebase configuration and initialization
├── index.js        # React app entry point
└── index.css       # Global styles
```

## Firebase Firestore Operations Used

- `addDoc()` - Create new documents
- `getDocs()` - Read documents from a collection
- `updateDoc()` - Update existing documents
- `deleteDoc()` - Delete documents
- `collection()` - Reference to a collection
- `doc()` - Reference to a specific document

## Troubleshooting

### Common Issues

1. **"Firebase: Error (auth/unauthorized)"**
   - Check your Firebase configuration in `src/firebase.js`
   - Verify your Firestore security rules

2. **"Firebase: Error (permission-denied)"**
   - Update your Firestore security rules to allow read/write access
   - Make sure Firestore is enabled in your Firebase project

3. **"Module not found" errors**
   - Run `npm install` to install dependencies
   - Make sure you're in the correct directory

### Getting Help

- Check the [Firebase Documentation](https://firebase.google.com/docs)
- Review the [Firestore Documentation](https://firebase.google.com/docs/firestore)
- Check the browser console for detailed error messages

## Next Steps

Once you're comfortable with the basic operations, you can enhance this application by:

- Adding user authentication
- Implementing real-time listeners with `onSnapshot()`
- Adding data validation
- Implementing pagination for large datasets
- Adding search and filtering capabilities
- Implementing offline support

## License

This project is open source and available under the [MIT License](LICENSE). 