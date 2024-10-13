import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function Login() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/micro-sci/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('access_token', data.access_token);
        navigate('/dashboard');
      } else {
        setError(data.detail || 'Login failed. Please try again.');
      }
    } catch (error) {
      setError('An error occurred. Please try again.');
    }
  };

  return (
    <div style={styles.overlay}>
      <div style={styles.container}>
        <h2 style={styles.title}>Login</h2>
        {error && <p style={styles.error}>{error}</p>}
        <div>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={styles.input}
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.input}
          />
        </div>
        <button onClick={handleLogin} style={styles.button}>Sign In</button>
      </div>
    </div>
  )
}

const styles = {
  overlay: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#f0f2f5', 
  },
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '40px',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#ffffff', 
    width: '300px',
    minWidth: '300px',
  },
  title: {
    marginBottom: '20px',
    color: '#333333',
  },
  error: {
    color: '#ff0000', 
    marginBottom: '15px',
    textAlign: 'center',
  },
  input: {
    padding: '10px',
    margin: '10px 0',
    width: '100%', 
    border: '1px solid #cccccc',
    borderRadius: '4px',
    fontSize: '16px',
  },
  button: {
    padding: '10px 20px',
    marginTop: '20px',
    width: '100%', 
    backgroundColor: '#4CAF50',
    color: '#ffffff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px',
  },
}

export default Login;
