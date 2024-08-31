import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Userpage.css'; 
import usersignup from '../images/user_img/img_signup01.jpg';  // Import the local image
import userlogin from '../images/user_img/img_userlogin01.jpg'

function Userpage() {
    return (
        <div>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            
            <nav>
                <ul>
                    <li>
                        <div className="nav-block signup-block">
                            <img src={usersignup} alt="usersignup" /> {/* Use the imported image */}
                            <div className="nav-block-content">
                                <h2>Sign Up</h2>
                                <p>Create an account to access exclusive features.</p>
                                <Link to="/UserSignup">Sign Up</Link>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div className="nav-block login-block">
                            <img src={userlogin} alt="userlogin" /> {/* Use the imported image */}
                            <div className="nav-block-content">
                                <h2>Login</h2>
                                <p>Already have an account? Log in to continue.</p>
                                <Link to="/UserLogin">Login</Link>
                            </div>
                        </div>
                    </li>
                </ul>
            </nav>
        </div>
    );
}

export default Userpage;
