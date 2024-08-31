import React from 'react';
import { FaFacebook, FaTwitter, FaLinkedin } from 'react-icons/fa';
import { Link } from 'react-router-dom';

import "../styles/Footer.css";

function Footer() {
	return (
		<footer>
			<div className="left-section">
				<p>&copy; 2024 Your Company. All rights reserved.</p>
			</div>

			<div className="middle-section">
				<div className="company-section">
					<h3>Company</h3>
					<ul>
						<li>
							<Link to="/partners" className="btn btn-link text-light">
								Partners
							</Link>
						</li>
						<li>
							<Link to="/contact_us" className="btn btn-link text-light">
								Contact Us
							</Link>
						</li>
						<li>
							<Link to="/LegalInformation" className="btn btn-link text-light">
								Legal Information
							</Link>
						</li>
					</ul>
				</div>
				
				<div className="partner-section">
					<h3>Partner Section</h3>
					<ul>
						<li>
							<Link to="/partners" className="btn btn-link text-light">
								Partners
							</Link>
						</li>
						<li>
							<Link to="/contact_us" className="btn btn-link text-light">
								Contact Us
							</Link>
						</li>
						<li>
							<Link to="/LegalInformation" className="btn btn-link text-light">
								Legal Information
							</Link>
						</li>
					</ul>
				</div>
			</div>

			<div className="right-section">
				<div className="socialmedia-section">
					<h3>Connect with Us</h3>
					<a href="https://www.facebook.com" target="_blank" rel="noopener noreferrer" className="btn btn-outline-light mx-2">
						<FaFacebook />
					</a>
					<a href="https://www.twitter.com" target="_blank" rel="noopener noreferrer" className="btn btn-outline-light mx-2">
						<FaTwitter />
					</a>
					<a href="https://www.linkedin.com" target="_blank" rel="noopener noreferrer" className="btn btn-outline-light mx-2">
						<FaLinkedin />
					</a>
				</div>
			</div>
		</footer>
	);
}

export default Footer;
