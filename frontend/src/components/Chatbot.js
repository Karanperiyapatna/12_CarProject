import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/Chatbot.css';

const Chatbot = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [selectedOption, setSelectedOption] = useState(null);

    const toggleChatbot = () => {
        setIsOpen(!isOpen);
        if (isOpen) {
            setSelectedOption(null); // Clear selected option when closing
        }
    };

    const handleOptionClick = (option) => {
        setSelectedOption(option);
    };

    return (
        <div className="chatbot-container">
            {!isOpen && (
                <button className="chatbot-icon" onClick={toggleChatbot}>
                    <i className="material-icons">chat</i>
                </button>
            )}
            {isOpen && (
                <div className="chatbot-content">
                    <div className="chatbot-header">
                        <button className="chatbot-close" onClick={toggleChatbot}>×</button>
                    </div>
                    <div className="chatbot-body">
                        {!selectedOption ? (
                            <div className="chatbot-options">
                                <button onClick={() => handleOptionClick('customer')}>Customer Support</button>
                                <button onClick={() => handleOptionClick('marketing')}>Marketing</button>
                            </div>
                        ) : (
                            <div className="chatbot-response">
                                {selectedOption === 'customer' ? (
                                    <div>
                                        <h3>Customer Support</h3>
                                        <p>Email: customer_support@digilaboursolutions.com</p>
                                        <p>Phone: +91-8080808080</p>
                                        <p>How can we assist you with our customer services?</p>
                                        <p><Link to="/contact_us">Click here</Link> for more enquiry</p>
                                    </div>
                                ) : (
                                    <div>
                                        <h3>Marketing</h3>
                                        <p>Email: marketing@digilaboursolutions.com</p>
                                        <p>Phone: +91-90909090</p>
                                        <p>How can we help you with our marketing services?</p>
                                        <p><Link to="/contact_us">Click here</Link> for more enquiry</p>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Chatbot;
