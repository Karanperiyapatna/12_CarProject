import React from "react";
import "../styles/AboutUs.css";

import { useLocation } from 'react-router-dom';

import industryHelperImg from '../images/labour_img/img_industryhelper01.jpg'
import cleanerImg from '../images/labour_img/img_cleaner03.jpg'; 
import babycaretaker from '../images/labour_img/img_babytc01.jpg';
import painterImg from '../images/labour_img/img_electirician02.jpg';

// import cleaner from '../images/labour_img/img_cleaner03.jpg';
// import acRepair from '../src/images/labour_img/img_electrician01.jpg';
// import painter from '../src/images/labour_img/img_electirician02.jpg';
import gardening from '../images/labour_img/img_gardner02.jpg';
// import industryHelper from '../src/images/labour_img/img_industryhelper01.jpg';
// import officeCleaner from '../src/images/labour_img/img_clener04.jpg';
import constructionHelper from '../images/labour_img/img_constructionhelper03.jpg';


function AboutUs() {
	const location = useLocation();
  
	// Scroll to the section based on the hash in the URL
	React.useEffect(() => {
	  const hash = location.hash;
	  if (hash) {
		const element = document.querySelector(hash);
		if (element) {
		  element.scrollIntoView({ behavior: 'smooth' });
		}
	  }
	}, [location]);
  
	return (
		<div className="company-info">
			<br></br>
			<br></br>
			<br></br>
	
			<div className="intro-content">
					<img src={industryHelperImg} alt="Industry Helper" />
					<div className="text-content">
						<h1>Introduction to Company</h1>
						<h2>DigiLabour Solution is a cutting-edge digital platform designed to revolutionize the
							way you connect with skilled professionals. Our mission is to make it easy and efficient
							for individuals and businesses to find and hire reliable labor
							for a wide range of tasks.
						</h2>
					</div>
			</div>


			<div className="mission-section">
				<h1>Mission</h1>
				<p>
				To revolutionize the labor market by connecting individuals with the skills they need to 
				complete tasks efficiently and conveniently, empowering both service providers and consumers
				through a reliable and user-friendly digital platform.
				</p>
			</div>

			<div className="vision-section">
				<h1>Vision of the Company</h1>
				<p>
					Our vision is to become the leading e-labor platform, fostering a
					collaborative and efficient workforce. To become the global leader in on-demand labor
					solutions, offering a seamless and innovative platform that benefits individuals, 
					businesses, and communities worldwide by fostering economic growth, efficiency, and 
					accessibility.
				</p>
			</div>

			<div className="workingprocess-section">
				<h1>How it Works?</h1>
				<p> Create an Account: Sign up for a free account on our user-friendly platform.
					Post Your Task: Describe your specific needs, including location, timeline, and preferred budget.
					Receive Bids: Qualified professionals will submit bids for your task, providing details about their experience, rates, and availability.
					Choose Your Provider: Review bids, compare profiles, and select the best candidate for your job.
					Complete Your Task: Communicate directly with your chosen provider, track progress, and provide feedback upon completion.
				</p>
			</div>

			<div className="legal-section">
			</div>


			<div className="about-us-container">
				<h1>In Details</h1>

				{/* Industry Helper Section */}
				<div id="baby-takecare" className="about-section">
					<img src={babycaretaker} alt="Industry Helper" className="about-img" />
					<div className="about-content">
					<h2>Baby Take Care and Helper</h2>
					<p>Our dedicated Baby Care and Helpers are trained to provide nurturing and attentive care for your little ones. They are skilled in all aspects of infant and toddler care, from feeding and diapering to playtime and soothing. Our team is committed to creating a safe and comfortable environment for your child.</p>

					<p>Whether you need full-time childcare, part-time assistance, or occasional help, our Baby Care and Helpers are available to meet your family's needs. We prioritize your child's well-being and ensure that they receive the highest quality care.</p>

					<p>Our services include:
					<ul>
						<li>Infant care</li>
						<li>Toddler care</li>
						<li>Feeding and diapering</li>
						<li>Playtime activities</li>
						<li>Soothing and comforting</li>
						<li>Light housekeeping tasks related to child care</li>
						<li>Transportation to and from activities (if applicable)</li>
					</ul>
					</p>
						
					<p>We understand the importance of finding the right caregiver for your child, and we are committed to matching you with a compassionate and experienced professional. Contact us today to learn more about our Baby Care and Helper services.</p>
					</div>
				</div>

				{/* Industry Helper Section */}
				<div id="industry-helper" className="about-section">
					<img src={industryHelperImg} alt="Industry Helper" className="about-img" />
					<div className="about-content">
					<h2>Industry Helper</h2>
					<p>
						Our Industry Helpers are skilled in a variety of industrial tasks, ranging from machinery operation to
						basic maintenance. They are trained to handle the rigors of industrial environments, ensuring safety and
						efficiency in every job they undertake.
					</p>
					<p>
						Whether you need help with heavy lifting, assembly line support, or general labor, our Industry Helpers
						are ready to assist with their expertise and dedication. We prioritize the safety and well-being of both
						our workers and your operations.
					</p>
					</div>
				</div>


				{/* Cleaner Section */}
				<div id="cleaner" className="about-section">
					<img src={cleanerImg} alt="Cleaner" className="about-img" />
					<div className="about-content">
					<h2>Cleaner</h2>
					<p>
						Our Cleaners are experts in maintaining spotless environments, whether it’s in residential, commercial, or
						industrial settings. They are trained in the latest eco-friendly cleaning methods and use safe, effective
						cleaning products to ensure your space is not only clean but also environmentally responsible.
					</p>
					<p>
						From deep cleaning to regular maintenance, our Cleaners handle every task with care and precision. We
						understand the importance of a clean space in promoting health and productivity, and our Cleaners are
						dedicated to delivering the highest standards of cleanliness.
					</p>
					</div>
				</div>

				{/* Painter Section */}
				<div id="painter" className="about-section">
					<img src={painterImg} alt="painter" className="about-img" />
					<div className="about-content">
					<h2>Painter</h2>
					<p>
						Our Painters are skilled professionals who bring color and life to any space,
						whether it’s residential, commercial, or industrial. They are trained in the latest 
						techniques and use high-quality, eco-friendly paints to ensure your project is not 
						only visually stunning but also safe for the environment.
					</p>
					<p>
						From intricate detail work to broad strokes, our Painters handle every job with 
						precision and care. We understand the impact of a well-painted space on mood and
						atmosphere, and our Painters are committed to delivering a flawless finish that
						meets the highest standards of craftsmanship.
					</p>
					</div>
				</div>

				
				{/* Construction Helper Section */}
				<div id="constructionhelper" className="about-section">
					<img src={constructionHelper} alt="constructionhelper" className="about-img" />
					<div className="about-content">
					<h2>Construction Helpers</h2>
					<p>
						Our Construction Helpers are essential team members who support a wide range of
						building and renovation projects, whether it’s residential, commercial, or industrial.
						They are trained in the latest construction techniques and safety protocols,
						ensuring that every task is performed efficiently and safely.
					</p>
					<p>
						From assisting with heavy lifting to handling tools and materials, our Construction
						Helpers are reliable and hardworking. We understand the importance of every role 
						in a successful construction project, and our Helpers are committed to contributing
						to the quality and progress of your build with dedication and skill.
					</p>
					</div>
				</div>

				{/* Gardening Helper Section */}
				<div id="gardening" className="about-section">
					<img src={gardening} alt="gardening" className="about-img" />
					<div className="about-content">
					<h2>Gardener</h2>
					<p>
						Our Gardeners are experts in creating and maintaining beautiful, thriving outdoor
						spaces, whether it’s a residential garden, commercial landscape, or public park.
						They are skilled in the latest horticultural techniques and use eco-friendly 
						practices to ensure your garden is not only lush and vibrant but also sustainable.
					</p>
					<p>
					    From planting and pruning to regular maintenance, our Gardeners handle every task with 
					    care and precision. We understand the importance of a well-kept garden in enhancing the
					    beauty and serenity of your surroundings, and our Gardeners are dedicated to delivering
					    the highest standards of gardening excellence.
					</p>
					</div>
				</div>


			</div>
		</div>
	);
};

export default AboutUs;


// EXTRA CODE *****************************************************************************************

{/* <div className="advantage-section">
				<h3>Why Choose DigiLabour Solution?</h3>
				<div className="advantages">
					<div className="advantage-item">
						<p>
						Convenience and Efficiency: Our platform streamlines the hiring process, saving you time and effort.
						Quality and Reliability: We carefully vet our service providers to ensure they meet our high standards of quality and professionalism.
						Flexibility and Customization: Tailor your service to your specific needs, whether it's a one-time task or ongoing project.
						Safety and Security: We prioritize your safety and security by providing a secure platform for transactions and communication.
						Competitive Pricing: Our competitive pricing structure makes it affordable to hire skilled professionals for your needs.
						</p>
					</div>
					<div className="advantage-item">
						<h4>User Account</h4>
						<p>
							It is one of the significant features to integrate into your
							beauty and salon service booking app. Urban Company-like top
							handymen booking app development must and should have this feature
							to provide better control to users on their KYC and other personal
							information added in the application.
						</p>
					</div>
					<div className="advantage-item">
						<h4>My Bookings</h4>
						<p>
							On-demand home services apps like Urban Company, with the
							integration of the “My Bookings” feature, will allows users to
							view their bookings history and ensure better visibility into
							their orders 24*7.
						</p>
					</div>
					<div className="advantage-item">
						<h4>Set Date and Time</h4>
						<p>
							Here is another important feature that helps users to schedule
							their appointments at their convenience before they proceed to
							checkout. It optimizes user experiences as well as adds value to
							its functionalities.
						</p>
					</div>
					<div className="advantage-item">
						<h4>Secure Online Payments</h4>
						<p>
							Urban Company like an Indian popular at-home services app should
							offer flexible online and offline (cash On Delivery) payment
							facilities to the users. It will enhance users enhance and improve
							app experiences.
						</p>
					</div>
					<div className="advantage-item">
						<h4>Live Location Tracking</h4>
						<p>
							On-demand delivery app development without a live location
							tracking feature is worthless. Marketplace applications or best
							multipurpose apps like Urban Company must be integrated with
							in-app Google maps and GPS tracking functionalities. It allows
							users to track the locations of beauticians or handymen in
							real-time like how we track the rider status on food delivery
							apps.
						</p>
					</div>
					<div className="advantage-item">
						<h4>In-app Chat or Call</h4>
						<p>
							Integration of virtual chat or audio call facilities in Urban
							Company like on-demand delivery service apps will help vendors to
							contact customers and vice versa.
						</p>
					</div>
					<div className="advantage-item">
						<h4>Reviews and Ratings</h4>
						<p>
							This user-friendly feature allows users to give feedback on
							specific services provided by professionals. On the other side,
							adding reviews and rating features in the on-demand haircut
							services app will increase the application’s reliability as it
							allows new users to analyze the service quality.
						</p>
					</div>
					<div className="advantage-item">
						<h4>Deals and Discounts</h4>
						<p>
							Every e-commerce app, marketplace app, or Urban Company like
							on-demand service delivery apps are giving price relaxation to
							customers by offering discounts and coupons to the users. Adding
							this feature will grab the attention and improve conversions.
						</p>
					</div>
					<div className="advantage-item">
						<h4>Push Notifications</h4>
						<p>
							This feature plays a vital role in notifying users about deals,
							discounts, bookings, and payments.
						</p>
					</div>
					<div className="advantage-item">
						<h4>Features For Service providers or Handymen</h4>
						<p>
							Here are a few must-have features to add to Urban Company like an
							in-home hair spa service delivery app in the vendor panel.
						</p>
						<ul>
							<li>Easy Login and registration</li>
							<li>Profile Management</li>
							<li>Order Management</li>
							<li>In-app chat with customer</li>
							<li>Checking slot availability</li>
							<li>Feedback View</li>
							<li>Upload service details</li>
							<li>Upload deals and discounts</li>
							<li>Payment Status Tracking</li>
							<li>Push Notifications</li>
						</ul>
					</div>
					<div className="advantage-item">
						<h4>Features For Admin Panel Development:</h4>
						<ul>
							<li>Dashboard view</li>
							<li>Location-based service updates</li>
							<li>User and vendor profile management</li>
							<li>Services Management</li>
							<li>Reports and sales analytics</li>
							<li>Optimizing service cost and management</li>
							<li>Feedback management</li>
							<li>Push notifications management</li>
						</ul>
					</div>
					<div className="advantage-item">
						<h4>Technology Used</h4>
						<ul>
							<li>
								Java and Kotlin for on-demand home and salon app development on
								the Android operating system
							</li>
							<li>Swift and Objective C for iPhone app development</li>
							<li>Database: MongoDB</li>
							<li>Storage: AWS and Google Cloud</li>
							<li>Online Payment Gateways: PayPal and Stripe</li>
							<li>Push notification feature: Twilio communication APIs</li>
							<li>Reports and Sales Analytics: BigData and Machine Learning</li>
						</ul>
					</div>
					<div className="service-section">
						Home Services: Cleaning, gardening, handyman services, and more.
						Professional Services: Tutoring, graphic design, programming, and other specialized skills.
						Event Services: Catering, bartending, party planning, and event staffing.
						Moving Services: Packing, loading, and unloading assistance.
						And more!
					</div>
				</div>
				
				
*/}