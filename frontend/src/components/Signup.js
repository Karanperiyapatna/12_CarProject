import React, { useState } from 'react';

function Signup() {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');

	const handleSignup = async (e) => {
		e.preventDefault();
		const response = await fetch('/signup', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ username, password }),
		});
		const data = await response.json();
		console.log(data.message);
	};

	return (
		<form onSubmit={handleSignup}>
			<h2>Signup</h2>
			<input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
			<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
			<button type="submit">Signup</button>
		</form>
	);
}

export default Signup;
