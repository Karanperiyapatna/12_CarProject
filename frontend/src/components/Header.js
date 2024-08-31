import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Header.css'; 
import logo from '../components/logo.jpg'; // Importing the logo image

function Header() {
	return (
		<header>
			<div className="header-container">
				<div className="logo">
					{/* Adding the local logo image */}
					<img 
						src={logo} 
						alt="Company Logo" 
						style={{ height: '50px', width: 'auto' }} // Adjust the size as needed
					/>
				</div>
				<div className="company-name">
					<h1>Digital Labour Solution</h1>
				</div>
				<nav>
					<ul>
						<li><Link to="/">Home</Link></li>
						<li><Link to="/userpage">User Page</Link></li>
						<li><Link to="/LabourPage">Labour Page</Link></li>
						<li><Link to="/about_us">About Us</Link></li>
						<li><Link to="/contact_us">Contact Us</Link></li>
					</ul>
				</nav>
			</div>
		</header>
	);
}

export default Header;
