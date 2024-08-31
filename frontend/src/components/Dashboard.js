import React, { useEffect, useState } from 'react';

function Dashboard() {
	const [users, setUsers] = useState([]);

	useEffect(() => {
		fetch('http://localhost:5000/api/dashboard')
			.then(response => response.json())
			.then(data => setUsers(data))
			.catch(error => console.error('Error:', error));
	}, []);

	return (
		<div>
			<h2>Dashboard</h2>
			<ul>
				{users.map((user, index) => (
					<li key={index}>{user.username}</li>
				))}
			</ul>
		</div>
	);
}

export default Dashboard;
