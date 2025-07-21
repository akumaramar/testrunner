import React, { useState, useEffect } from 'react';
import { 
  collection, 
  addDoc, 
  getDocs, 
  deleteDoc, 
  doc, 
  updateDoc 
} from 'firebase/firestore';
import { db } from './firebase';
import './App.css';
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';
import Login from './Login';

function App() {
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editText, setEditText] = useState('');
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState(null);

  // Fetch all items from Firestore
  const fetchItems = async () => {
    setLoading(true);
    try {
      const querySnapshot = await getDocs(collection(db, 'items'));
      const itemsList = querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      setItems(itemsList);
    } catch (error) {
      console.error('Error fetching items: ', error);
      alert('Error fetching items: ' + error.message);
    }
    setLoading(false);
  };

  // Add new item to Firestore
  const addItem = async (e) => {
    e.preventDefault();
    if (!newItem.trim()) return;

    setLoading(true);
    try {
      await addDoc(collection(db, 'items'), {
        text: newItem,
        timestamp: new Date()
      });
      setNewItem('');
      fetchItems();
    } catch (error) {
      console.error('Error adding item: ', error);
      alert('Error adding item: ' + error.message);
    }
    setLoading(false);
  };

  // Delete item from Firestore
  const deleteItem = async (id) => {
    setLoading(true);
    try {
      await deleteDoc(doc(db, 'items', id));
      fetchItems();
    } catch (error) {
      console.error('Error deleting item: ', error);
      alert('Error deleting item: ' + error.message);
    }
    setLoading(false);
  };

  // Start editing an item
  const startEdit = (item) => {
    setEditingId(item.id);
    setEditText(item.text);
  };

  // Save edited item
  const saveEdit = async (id) => {
    if (!editText.trim()) return;

    setLoading(true);
    try {
      await updateDoc(doc(db, 'items', id), {
        text: editText,
        timestamp: new Date()
      });
      setEditingId(null);
      setEditText('');
      fetchItems();
    } catch (error) {
      console.error('Error updating item: ', error);
      alert('Error updating item: ' + error.message);
    }
    setLoading(false);
  };

  // Cancel editing
  const cancelEdit = () => {
    setEditingId(null);
    setEditText('');
  };

  // Listen for auth state changes
  useEffect(() => {
    const auth = getAuth();
    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      setUser(firebaseUser);
    });
    return () => unsubscribe();
  }, []);

  // Load items on component mount
  useEffect(() => {
    fetchItems();
  }, []);

  if (!user) {
    return <Login onLogin={() => {}} />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔥 Firestore Test App</h1>
        <p>Test your Firestore database with this simple CRUD application</p>
        <button className="btn btn-secondary" style={{float: 'right'}} onClick={() => signOut(getAuth())}>Sign Out</button>
      </header>

      <main className="App-main">
        {/* Add Item Form */}
        <div className="add-item-section">
          <h2>Add New Item</h2>
          <form onSubmit={addItem} className="add-form">
            <input
              type="text"
              value={newItem}
              onChange={(e) => setNewItem(e.target.value)}
              placeholder="Enter item text..."
              className="input-field"
              disabled={loading}
            />
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Adding...' : 'Add Item'}
            </button>
          </form>
        </div>

        {/* Items List */}
        <div className="items-section">
          <h2>Items ({items.length})</h2>
          {loading && <div className="loading">Loading...</div>}
          
          <div className="items-list">
            {items.map((item) => (
              <div key={item.id} className="item-card">
                {editingId === item.id ? (
                  // Edit mode
                  <div className="edit-mode">
                    <input
                      type="text"
                      value={editText}
                      onChange={(e) => setEditText(e.target.value)}
                      className="input-field"
                      autoFocus
                    />
                    <div className="edit-buttons">
                      <button 
                        onClick={() => saveEdit(item.id)} 
                        className="btn btn-success"
                        disabled={loading}
                      >
                        Save
                      </button>
                      <button 
                        onClick={cancelEdit} 
                        className="btn btn-secondary"
                        disabled={loading}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  // View mode
                  <div className="item-content">
                    <p className="item-text">{item.text}</p>
                    <p className="item-timestamp">
                      {item.timestamp?.toDate?.()?.toLocaleString() || 'No timestamp'}
                    </p>
                    <div className="item-actions">
                      <button 
                        onClick={() => startEdit(item)} 
                        className="btn btn-edit"
                        disabled={loading}
                      >
                        Edit
                      </button>
                      <button 
                        onClick={() => deleteItem(item.id)} 
                        className="btn btn-delete"
                        disabled={loading}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          {items.length === 0 && !loading && (
            <div className="empty-state">
              <p>No items yet. Add your first item above!</p>
            </div>
          )}
        </div>
      </main>

      <footer className="App-footer">
        <p>Firebase Firestore Test Application</p>
      </footer>
    </div>
  );
}

export default App; 