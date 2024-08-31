import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const navigate = useNavigate();

	const handleLogin = async (e) => {
		e.preventDefault();
	
		try {
			const response = await fetch('http://localhost:5000/UserLogin', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ username, password }),
				credentials: 'include',
			});
			const data = await response.json();
	
			console.log('Response Data:', data);  // Log the response data
	
			if (response.ok) {
				console.log('Login successful:', data);
				sessionStorage.setItem('isLoggedIn', 'true');
				sessionStorage.setItem('userId', data.user_id);
				sessionStorage.setItem('userName', data.name);
				navigate('/UserDashboard', { state: { name: data.name, userId: data.user_id } });
			} else {
				console.error('Login failed:', data.message);
				alert('Login failed: ' + data.message);
			}
		} catch (error) {
			console.error('Error:', error);
			alert('An error occurred during login.');
		}
	};
	return (
		<form onSubmit={handleLogin}>
			<br></br>

			
			<h2>Login</h2>
			<input
				type="text"
				value={username}
				onChange={(e) => setUsername(e.target.value)}
				placeholder="Username"
				required
			/>
			<input
				type="password"
				value={password}
				onChange={(e) => setPassword(e.target.value)}
				placeholder="Password"
				required
			/>
			<button type="submit">Login</button>
		</form>
	);
}

export default Login;
