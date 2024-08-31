import React, { useState } from 'react';
import "../styles/ContactUs.css";

function ContactUs() {
	const [name, setName] = useState('');
	const [mobile, setMobile] = useState('');
	const [email, setEmail] = useState('');
	const [message, setMessage] = useState('');

	const handleContact = async (e) => {
		e.preventDefault();
		const response = await fetch('http://localhost:5000/contact_us', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name, mobile, email, message }),
		});
		const data = await response.json();
		console.log(data.message);
	};

	return (
		<form onSubmit={handleContact}>

			<h2>Contact Us</h2>
			<input
				type="text"
				value={name}
				onChange={(e) => setName(e.target.value)}
				placeholder="Your name"
				required
			/>
			<input
				type="tel"
				value={mobile}
				onChange={(e) => setMobile(e.target.value)}
				placeholder="Your mobile number"
				required
			/>
			<input
				type="email"
				value={email}
				onChange={(e) => setEmail(e.target.value)}
				placeholder="Your email"
				required
			/>
			<textarea
				value={message}
				onChange={(e) => setMessage(e.target.value)}
				placeholder="Your message"
				required
			></textarea>
			<button type="submit">Send</button>
		</form>
	);
}

export default ContactUs;
