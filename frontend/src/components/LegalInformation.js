import React from 'react';
import "../styles/LegalInformation.css";




import industryHelperImg from '../images/labour_img/img_industryhelper01.jpg'
import cleanerImg from '../images/labour_img/img_cleaner03.jpg'; 

function LegalInformation() {

	return (

                <div className="company-info">
                <br></br>
                <br></br>
                <br></br>

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
                                <img src={industryHelperImg} alt="Industry Helper" className="about-img" />
                                <div className="about-content">
                                <h1>How it Works?</h1>
                        <p> Create an Account: Sign up for a free account on our user-friendly platform.
                                Post Your Task: Describe your specific needs, including location, timeline, and preferred budget.
                                Receive Bids: Qualified professionals will submit bids for your task, providing details about their experience, rates, and availability.
                                Choose Your Provider: Review bids, compare profiles, and select the best candidate for your job.
                                Complete Your Task: Communicate directly with your chosen provider, track progress, and provide feedback upon completion.
                        </p>

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
                        </div>

                        <p>
                Company Name and Registration Details
                Company Name: [DigiLabour Solutions]
                Registration Number: [Your Company Registration Number]
                Incorporation Date: [31-12-2024]
                Registered Address: [JP Nagar, Bangalore]
                Nature of Business
                Briefly describe your company's primary activities. For example: "We provide a digital platform that connects skilled laborers with individuals and businesses seeking their services."
                Terms of Service and Privacy Policy
                Link to your Terms of Service: "Please review our [Terms of Service] for detailed information about your rights and obligations when using our platform."
                Link to your Privacy Policy: "Our [Privacy Policy] outlines how we collect, use, and protect your personal information."
                Governing Law
                Specify the jurisdiction that governs your business and the terms of service. For example: "These terms and conditions are governed by and construed in accordance with the laws of [Jurisdiction]."
                Dispute Resolution
                Outline the dispute resolution process, such as arbitration or mediation. For example: "Any dispute arising out of or in connection with these terms and conditions shall be resolved through [Dispute Resolution Method]."
                Intellectual Property
                State that your company owns or licenses the intellectual property related to your platform. For example: "All intellectual property rights in the platform, including but not limited to trademarks, copyrights, and patents, are owned by [Your Company Name]."
                Disclaimer
                Include a disclaimer to limit your liability. For example: "We make no warranties or representations as to the accuracy or completeness of the information provided on our platform."
                Note: It's highly recommended to consult with a legal professional to ensure that your legal content is accurate, comprehensive, and compliant with applicable laws and regulations.

                Additional Considerations:

                Accessibility Statement: If your website is intended to be accessible to individuals with disabilities, consider adding an accessibility statement.
                Data Protection Compliance: If you process personal data of individuals in the European Union or other regions with strict data protection laws (like GDPR or CCPA), ensure your privacy policy and practices comply with these regulations.
                By including this legal information on your "About Us" page, you're providing transparency and protecting your company from potential legal issues.
        </p>
        </div>

 

	);
}

export default LegalInformation;
