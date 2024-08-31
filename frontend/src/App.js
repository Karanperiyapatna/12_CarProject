import { BrowserRouter as Router, Route, Routes, useLocation, Navigate, useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './styles/main.css';

import Header from './components/Header';
import Footer from './components/Footer';
import Signup from './components/Signup';
import Login from './components/Login';

import Userpage from './components/Userpage';
import UserLogin from './components/user/UserLogin';
import UserSignup from './components/user/UserSignup';
import UserDashboard from './components/user/UserDashboard';

import LabourPage from './components/LabourPage';
import LabourLogin from './components/labour/LabourLogin';
import LabourSignup from './components/labour/LabourSignup';
import LabourDashboard from './components/labour/LabourDashboard';

import AgentLogin from './components/agent/AgentLogin';
import AgentSignup from './components/agent/AgentSignup';

import CbLogin from './components/cb/CbLogin';
import CbSignup from './components/cb/CbSignup';

import AboutUs from './components/AboutUs';
import ContactUs from './components/ContactUs';

import LegalInformation from './components/LegalInformation';
import Chatbot from './components/Chatbot';


import babycaretaker from '../src/images/labour_img/img_babytc01.jpg';
import cleaner from '../src/images/labour_img/img_cleaner03.jpg';
import acRepair from '../src/images/labour_img/img_electrician01.jpg';
import painter from '../src/images/labour_img/img_electirician02.jpg';
import gardening from '../src/images/labour_img/img_gardner02.jpg';
import industryHelper from '../src/images/labour_img/img_industryhelper01.jpg';
import officeCleaner from '../src/images/labour_img/img_clener04.jpg';
import constructionHelper from '../src/images/labour_img/img_constructionhelper03.jpg';


function HomePageContent() {
	const location = useLocation();
	const navigate = useNavigate();  // Hook for navigation

	const [bookingType, setBookingType] = useState(null);
	const [state, setState] = useState('');
	const [city, setCity] = useState('');
	const [date, setDate] = useState('');
	const [professionalType, setProfessionalType] = useState('');
	const [labours, setLabours] = useState([]);
	const [states, setStates] = useState([]);
	const [cities, setCities] = useState([]);
	const [professionals, setProfessionals] = useState([]);
	const [feedbacks, setFeedbacks] = useState([]);
	const [showPopup, setShowPopup] = useState(false); // for find worker
	const [searchTerm, setSearchTerm] = useState(''); 

	useEffect(() => {
		const fetchLocationData = async () => {
			try {
				const response = await fetch('http://127.0.0.1:5000/get_location_data');
				if (response.ok) {
					const data = await response.json();
					setStates(data.states);
					setCities(data.cities);
					setProfessionals(data.professionals);
				} else {
					console.error('Failed to fetch location data');
				}
			} catch (error) {
				console.error('Error:', error);
			}
		};

		fetchLocationData();
	}, []);

	const handleBookingType = (type) => {
		setBookingType((prevType) => (prevType === type ? null : type));
		setLabours([]);
	};

	const handleSearch = async () => {
		try {
			const response = await fetch('http://localhost:5000/search_labours', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ state, city, date, professionalType }),
			});
	
			if (response.ok) {
				const data = await response.json();
				setLabours(data.labours);
				setShowPopup(true); // Show the popup after the search
			} else {
				alert('Failed to fetch labours!');
			}
		} catch (error) {
			console.error('Error:', error);
		}
	};

	const handleKeywordSearch = () => {
		// Logic to handle keyword search and redirect to the block
		if (searchTerm.toLowerCase() === 'findworker') {
			// Redirect to the find worker section
			navigate('/findworker');
		} else if (searchTerm.toLowerCase() === 'industry-helper') {
			// Redirect to the industry helper section
			navigate('/industry-helper');
		} else {
			alert('Keyword not found!');
		}
	};

	useEffect(() => {
		const fetchFeedbacks = async () => {
							try {
									const response = await fetch('http://127.0.0.1:5000/get_feedbacks');
									if (response.ok) {
											const data = await response.json();
											setFeedbacks(data.feedbacks);
									} else {
											console.error('Failed to fetch feedbacks');
									}
							} catch (error) {
									console.error('Error:', error);
							}
					};

					fetchFeedbacks();
			}, []);

	if (location.pathname === '/') {
		return (
			<div className="home-page-content">
				<br></br>
				<br></br>
				<br></br>
				<br></br>
				<br></br>
				<br></br>
				<div className="welcome-container">
					<div className="welcome-left">
						<h1>Hello User,</h1>
						<h1> Welcome to DigiLabour Solution!!!</h1>
						<p>Explore our services and find the best labors for your needs.</p>
					</div>
					<div className="welcome-right">
						<h2>Work..!</h2>
					</div>
				</div>

				{/* Search input and button 
				<div className="search-container">
					<input 
						type="text" 
						placeholder="Enter keyword (e.g., findworker, industry-helper)" 
						value={searchTerm}
						onChange={(e) => setSearchTerm(e.target.value)} 
					/>
					<button onClick={handleKeywordSearch}>Search</button>
				</div>

				*/}


				{/* Image Carousel row 1*/}
				<div className="carousel-container">
					<div className="carousel">

						<div className="carousel-item">
							<img src={babycaretaker} alt="babycaretaker" />
							<p>Baby Caretaker</p>
							<div className="extra-content">
								<p>Experienced in various taking care the babies</p>
								<button onClick={() => navigate('/about_us#babycaretaker')}>Learn More</button>
							</div>
						</div>
						<div className="carousel-item">
							<img src={cleaner} alt="cleaner" />
							<p>Domestic Cleaner</p>
							<div className="extra-content">
								<p>Specializes in residential and commercial cleaning.</p>
								<button onClick={() => navigate('/about_us#cleaner')}>Learn More</button>
							</div>
						</div>
						<div className="carousel-item">
							<img src={painter} alt="painter" />
							<p>Painter</p>
							<div className="extra-content">
								<p>Trained in eco-friendly Painter and Finish with effective quality</p>
								<button onClick={() => navigate('/about_us#painter')}>Learn More</button>
							</div>
						</div>

					</div>
				</div>  


				<div className="container-findworker">
					<div className="image-container">
						<img src={babycaretaker} alt="Worker Image" />
					</div>
					<div className="content-container">
						<h1>Find a Worker</h1>
						<div className="booking-buttons">
							<button onClick={() => handleBookingType('spot')}>Spot Booking</button>
							<button onClick={() => handleBookingType('advance')}>Advance Booking</button>
						</div>
						
						{bookingType && (
							<div className="form-section">
								<h2>{bookingType === 'spot' ? 'Spot Booking' : 'Advance Booking'} Details</h2>
								<form onSubmit={(e) => { e.preventDefault(); handleSearch(); }} className="search-form">
									<div>
										<label>State:</label>
										<select value={state} onChange={(e) => setState(e.target.value)} required>
											<option value="">Select State</option>
											{states.map((state, index) => (
												<option key={index} value={state}>{state}</option>
											))}
										</select>
									</div>
									<div>
										<label>City:</label>
										<select value={city} onChange={(e) => setCity(e.target.value)} required>
											<option value="">Select City</option>
											{cities.map((city, index) => (
												<option key={index} value={city}>{city}</option>
											))}
										</select>
									</div>
									<div>
										<label>Date:</label>
										<input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
									</div>
									<div>
										<label>Professional Type:</label>
										<select value={professionalType} onChange={(e) => setProfessionalType(e.target.value)} required>
											<option value="">Select Professional</option>
											{professionals.map((professional, index) => (
												<option key={index} value={professional}>{professional}</option>
											))}
										</select>
									</div>
									<button type="submit">Search</button>
								</form>
							</div>
						)}

						{showPopup && (
							<>
								<div className="popup-overlay" onClick={() => setShowPopup(false)}></div>
								<div className="labour-popup">
									<button className="close-button" onClick={() => setShowPopup(false)}>×</button>
									<h3>Available Labours:</h3>
									{labours.length > 0 ? (
										<table>
											<thead>
												<tr>
													<th>Name</th>
													<th>Professional</th>
													<th>Price per Day</th>
												</tr>
											</thead>
											<tbody>
												{labours.map((labour, index) => (
													<tr key={index}>
														<td>{labour.labour_name}</td>
														<td>{labour.professional}</td>
														<td>{labour.price_per_day}</td>
													</tr>
												))}
											</tbody>
										</table>
									) : (
										<p>No labour found for the selected date.</p>
									)}
								</div>
							</>
						)}

					</div>
				</div>

				{/* Image Carousel row 3 */}
				<div className="carousel-container">
					<div className="carousel">
						<div className="carousel-item">
							<img src={industryHelper} alt="industryHelper" />
							<p>Industry Helper</p>
							<div className="extra-content">
								<p>Experienced in various industrial tasks.</p>
								<button onClick={() => navigate('/about_us#industryHelper')}>Learn More</button>
							</div>
						</div>
						<div className="carousel-item">
							<img src={officeCleaner} alt="officeCleaner" />
							<p>Office Cleaner</p>
							<div className="extra-content">
								<p>Specializes in residential and commercial cleaning.</p>
								<button onClick={() => navigate('/about_us#officeCleaner')}>Learn More</button>
							</div>
						</div>
						
						<div className="carousel-item">
							<img src={constructionHelper} alt="constructionHelper" />
							<p>Construction Helper</p>
							<div className="extra-content">
								<p>Trained in eco-friendly cleaning methods.</p>
								<button onClick={() => navigate('/about_us#constructionHelper')}>Learn More</button>
							</div>
						</div>
					</div>
				</div>  


				{/* Image Carousel row 2*/}
				<div className="carousel-container-2">
					<div className="carousel">
						<div className="carousel-item">
							<img src={acRepair} alt="acRepair" />
							<p>AC Reapir</p>
							<div className="extra-content">
								<p>Trained in eco-friendly AC repair and cleaning methods.</p>
								<button onClick={() => navigate('/about_us#acRepair')}>Learn More</button>
							</div>
						</div>
						<div className="carousel-item">
							<img src={painter} alt="painter" />
							<p>Painter</p>
							<div className="extra-content">
								<p>Trained in eco-friendly Painter and Finish with effective quality</p>
								<button onClick={() => navigate('/about_us#painter')}>Learn More</button>
							</div>
						</div>
						<div className="carousel-item">
							<img src={gardening} alt="gardening" />
							<p>Gardening</p>
							<div className="extra-content">
								<p>Trained in eco-friendly Gardner who grow the plant and maintain the plants </p>
								<button onClick={() => navigate('/about_us#gardening')}>Learn More</button>
							</div>
						</div>
					</div>
				</div>



				{/* Customer Feedback Carousel */}
				<div className="feedback-carousel">
						<h2>Recent Customer Feedback</h2>
						<div className="carousel-feedback">
								{feedbacks.map((feedback, index) => (
										<div key={index} className="carousel-item">
												<h3>{feedback.name}</h3>
												<p>Rating: {feedback.rating}/10</p>
												<p>{feedback.feedback}</p>
										</div>
								))}
						</div>
				</div>


				{/* Customer Feedback Carousel */}
				<div className="feedback-carousel">
						<h2>Customer Feedback</h2>
						<div className="carousel">
								{feedbacks.map((feedback, index) => (
										<div key={index} className="carousel-item">
												<h3>{feedback.name}</h3>
												<p>Rating: {feedback.rating}/10</p>
												<p>{feedback.feedback}</p>
										</div>
								))}
						</div>
				</div>


			</div>
		);
	}
	return null;
}

function App() {
	const isLoggedIn = () => {
		return !!sessionStorage.getItem('isLoggedIn'); // Returns true if 'isLoggedIn' exists in sessionStorage
	};

	return (
		<Router>
			<div>
				<Header />
				<HomePageContent />
				<Routes>

					{/* <Route path="/" element={<h2>Home Content</h2>} /> */}
					<Route path="/signup" element={<Signup />} />
					<Route path="/login" element={<Login />} />
					<Route path="/about_us" element={<AboutUs />} />
					<Route path="/contact_us" element={<ContactUs />} />
					<Route path="/LabourPage" element={<LabourPage />} />
					<Route path="/LegalInformation" element={<LegalInformation />} />
					<Route path="/LabourLogin" element={<LabourLogin />} />
					<Route path="/LabourSignup" element={<LabourSignup />} />
					<Route path="/LabourDashboard" element={<LabourDashboard />} />
					<Route path="/userpage" element={<Userpage />} />
					<Route path="/UserLogin" element={<UserLogin />} />
					<Route path="/UserSignup" element={<UserSignup />} />
					<Route
						path="/UserDashboard"
						element={isLoggedIn() ? <UserDashboard /> : <Navigate to="/UserLogin" />}
					/>
					<Route path="/AgentLogin" element={<AgentLogin />} />
					<Route path="/AgentSignup" element={<AgentSignup />} />
					<Route path="/CbLogin" element={<CbLogin />} />
					<Route path="/CbSignup" element={<CbSignup />} />
				</Routes>
				<Footer />
				<Chatbot /> 
			</div>
		</Router>
	);
}

export default App;
