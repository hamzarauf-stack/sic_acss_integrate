import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [courseSchedules, setCourseSchedules] = useState('');
  const [enrollmentsData, setEnrollmentsData] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const clearData = () => {
    setCourseSchedules('');
    setEnrollmentsData('');
    localStorage.removeItem('access_token');

    navigate('/');
  };

  const sendCourseSchedules = async () => {
    const token = localStorage.getItem('access_token');

    try {
      const response = await fetch('http://localhost:8001/api/micro-acss/schedules/send_schedules', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setCourseSchedules(JSON.stringify(data.response, null, 2));
        setError('');
      } else {
        setError(data.response.detail || 'Failed to send course schedules.');
        setCourseSchedules('');
      }
    } catch (error) {
      setError('An error occurred. Please try again.');
      setCourseSchedules('');
    }
  };

  const sendEnrollmentsData = async() => {
    const token = localStorage.getItem('access_token');

    try {
      const response = await fetch('http://localhost:8000/api/micro-sci/enrollments/send_enrollments', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setEnrollmentsData(JSON.stringify(data.response, null, 2));
        setError('');
      } else {
        setError(data.response.detail || 'Failed to send enrollments.');
        setEnrollmentsData('');
      }
    } catch (error) {
      setError('An error occurred. Please try again.');
      setEnrollmentsData('');
    }
  }


  return (
    <div style={styles.container}>
      <h2>Dashboard</h2>
      {error && <p style={styles.error}>{error}</p>}
      <div style={styles.buttons}>
        <button onClick={sendCourseSchedules} style={styles.button}>Send Course Schedules</button>
        <button onClick={sendEnrollmentsData} style={styles.button}>Send Enrollments Data</button>
        <button onClick={clearData} style={styles.button}>Logout</button>
      </div>
      <div style={styles.dataContainer}>
        <div style={styles.systemSection}>
          <h3>Student Information System</h3>
          <textarea value={courseSchedules} readOnly style={styles.textarea}></textarea>
        </div>
        <div style={styles.systemSection}>
          <h3>Academic Scheduling System</h3>
          <textarea value={enrollmentsData} readOnly style={styles.textarea}></textarea>
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    textAlign: 'center',
    padding: '20px',
  },
  buttons: {
    margin: '20px 0',
  },
  error: {
    color: '#ff0000', 
    marginBottom: '15px',
    textAlign: 'center',
  },
  button: {
    margin: '0 10px',
    padding: '10px 20px',
    cursor: 'pointer',
  },
  dataContainer: {
    display: 'flex',
    justifyContent: 'space-around',
    marginTop: '30px',
  },
  systemSection: {
    width: '45%',
  },
  textarea: {
    width: '100%',
    height: '200px',
  },
}

export default Dashboard;
