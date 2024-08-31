import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/LabourPage.css';


import agentsignup from '../images/agent_img/img_agentlogin03.jpg'
import agentlogin from '../images/agent_img/img_agentlogin01.jpg'

import cbsignup from '../images/cb_img/img_cbsignup.jpg'
import cblogin from '../images/cb_img/img_cblogin01.jpg'

import laboursignup from '../images/labour_imgs/img_signup01.jpg'
import labourlogin from '../images/labour_imgs/img_userlogin01.jpg'


function LabourPage() {
	return (
		
		<div className="labour-page-container">


		<br></br>
		<br></br>
		
			<div className="row-block">
				<div className="nav-block agent-block">
					<img src={agentsignup} alt="agentsignup" /> {/* Use the imported image */}
					<div className="nav-block-content">
						<h2>Agent Sign Up</h2>
						<p>Create an account as an agent.</p>
						<Link to="/AgentSignup">Sign Up</Link>
					</div>
				</div>
				<div className="nav-block agent-block">
					<img src={agentlogin} alt="agentlogin" /> {/* Use the imported image */}
					{/* <img src="https://upload.wikimedia.org/wikipedia/commons/8/8c/Google.jpg" alt="Google Background" /> */}
					<div className="nav-block-content">
						<h2>Agent Login</h2>
						<p>Already an agent? Log in here.</p>
						<Link to="/AgentLogin">Login</Link>
					</div>
				</div>
			</div>

			<div className="row-block">
				<div className="nav-block commission-block">
					<img src={cbsignup} alt="cbsignup" /> {/* Use the imported image */}
					{/* <img src="https://upload.wikimedia.org/wikipedia/commons/8/8c/Google.jpg" alt="Google Background" /> */}
					<div className="nav-block-content">
						<h2>Commission-Based Sign Up</h2>
						<p>Sign up for commission-based work.</p>
						<Link to="/CommissionSignup">Sign Up</Link>
					</div>
				</div>
				<div className="nav-block commission-block">
					<img src={cblogin} alt="cblogin" /> {/* Use the imported image */}
					<div className="nav-block-content">
						<h2>Commission-Based Login</h2>
						<p>Log in for commission-based work.</p>
						<Link to="/CommissionLogin">Login</Link>
					</div>
				</div>
			</div>


			<div className="row-block">
				<div className="nav-block labour-block">
				<img src={laboursignup} alt="laboursignup" /> {/* Use the imported image */}
					<div className="nav-block-content">
						<h2>Labour Sign Up</h2>
						<p>Create an account to access exclusive features.</p>
						<Link to="/LabourSignup">Sign Up</Link>
					</div>
				</div>
				<div className="nav-block labour-block">
					<img src={labourlogin} alt="labourlogin" /> {/* Use the imported image */}
					<div className="nav-block-content">
						<h2>Labour Login</h2>
						<p>Already have an account? Log in to continue.</p>
						<Link to="/LabourLogin">Login</Link>
					</div>
				</div>
			</div>

			<div className="back-home">
				<p>Back to home page</p>
				<Link to="/">Back to Homepage</Link>
			</div>
		</div>
	);
}

export default LabourPage;
