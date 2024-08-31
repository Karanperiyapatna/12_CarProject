import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LabourLogin() {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const navigate = useNavigate();

	const handleLogin = async (e) => {
		e.preventDefault();
		try {
		const response = await fetch('http://localhost:5000/LabourLogin', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ username, password }),
			credentials: 'include',
		});
		const data = await response.json();
		console.log('Response Data:', data);  
		// console.log(data.message);
		if (response.ok) {
			console.log('Login successful:', data);
			sessionStorage.setItem('isLoggedIn', 'true');
			sessionStorage.setItem('labourId', data.labour_id);
			sessionStorage.setItem('labourName', data.name);
			navigate('/LabourDashboard', { state: { name: data.name, labourId: data.labour_id } });
		} else {
			console.error('Login failed:', data.message);
			alert('Login failed: ' + data.message);
		}
	}
	catch (error) {
		console.error('Error:', error);
		alert('An error occurred during login.');
	}
};
	
	return (
		<form onSubmit={handleLogin}>
			<h2>Labour Login</h2>
			<input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
			<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
			<button type="submit">Login</button>
		</form>
	);
}

export default LabourLogin;
