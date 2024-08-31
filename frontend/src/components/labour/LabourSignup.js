import React, { useState } from 'react';

function LabourSignup() {
	const [name, setName] = useState('');
	const [professional, setProfessional] = useState('');
	const [mobilenumber, setMobileNumber] = useState('');
	const [alternativemobilenumber, setAlternativeMobileNumber] = useState('');
	const [mailid, setMailID] = useState('');
	const [address, setAddress] = useState('');
	const [city, setCity] = useState('');
	const [pincode, setPincode] = useState('');
	const [state, setState] = useState('');
	const [proof, setProof] = useState(null);
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');

	const handleFileChange = (e) => {
		setProof(e.target.files[0]);
	};

	const handleSignup = async (e) => {
		e.preventDefault();
		const formData = new FormData();
		formData.append('name', name);
		formData.append('professional', professional);
		formData.append('mobile_number', mobilenumber);
		formData.append('alt_mobile_number', alternativemobilenumber);
		formData.append('email', mailid);
		formData.append('address', address);
		formData.append('city', city);
		formData.append('state', state);
		formData.append('pincode', pincode);
		formData.append('username', username);
		formData.append('password', password);
		formData.append('address_proof', proof);

		try {
			const response = await fetch('http://localhost:5000/LabourSignup', {
				method: 'POST',
				body: formData,
			});
			const data = await response.json();
			if (response.ok) {
				alert('Signup Successful');
			} else {
				alert('Signup Failed: ' + data.message);
			}
		} catch (error) {
			console.error('Error:', error);
		}
	};

	return (
		<form onSubmit={handleSignup}>
			<h2>Signup</h2>
			<input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
			<input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="professional" required />
			<input type="text" value={mobilenumber} onChange={(e) => setMobileNumber(e.target.value)} placeholder="Mobile Number" required />
			<input type="text" value={alternativemobilenumber} onChange={(e) => setAlternativeMobileNumber(e.target.value)} placeholder="Alternative Mobile Number" required />
			<input type="email" value={mailid} onChange={(e) => setMailID(e.target.value)} placeholder="Email" required />
			<input type="text" value={address} onChange={(e) => setAddress(e.target.value)} placeholder="Address" required />
			<input type="text" value={city} onChange={(e) => setCity(e.target.value)} placeholder="City" required />
			<input type="text" value={state} onChange={(e) => setState(e.target.value)} placeholder="State" required />
			<input type="text" value={pincode} onChange={(e) => setPincode(e.target.value)} placeholder="Pincode" required />
			<input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
			<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
			<input type="file" onChange={handleFileChange} required />
			<button type="submit">Signup</button>
		</form>
	);
}

export default LabourSignup;
