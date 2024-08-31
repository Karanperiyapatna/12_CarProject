import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../../styles/UserDashboard.css';

function UserDashboard() {
    const location = useLocation();
    const { name, userId } = location.state || { name: 'Unknown User', userId: 'Unknown ID' };
    const navigate = useNavigate();

    const [bookingType, setBookingType] = useState(null);
    const [state, setState] = useState('');
    const [city, setCity] = useState('');
    const [date, setDate] = useState('');
    const [professionalType, setProfessionalType] = useState('');
    const [labours, setLabours] = useState([]);
    const [states, setStates] = useState([]);
    const [cities, setCities] = useState([]);
    const [professionals, setProfessionals] = useState([]);
    const [bookings, setBookings] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);

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

    useEffect(() => {
        const fetchBookings = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/get_user_bookings?user_id=${userId}`);
                console.log('Bookings response:', response.data);
                setBookings(response.data.bookings);
            } catch (error) {
                console.error('Error fetching bookings:', error);
            }
        };

        fetchBookings();
    }, [userId]);

    const renderStatus = (status) => {
        if (status === 7) return 'Accepted';
        if (status === 8) return 'Rejected';
        return 'Pending';
    };

    const handleLogout = async () => {
        try {
            const response = await fetch('http://localhost:5000/logout', {
                method: 'POST',
                credentials: 'include',
            });

            if (response.ok) {
                alert('Logout successful!');
                navigate('/UserLogin');
            } else {
                alert('Logout failed!');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleBookingType = (type) => {
        setBookingType(type);
        setLabours([]);
    };

    const handleSearch = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/search_labours', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ state, city, date, professionalType }),
            });

            if (response.ok) {
                const data = await response.json();
                setLabours(data.labours.map(labour => ({ ...labour, status: 'Idle' })));
                setIsModalOpen(true);  // Open the modal when labours are fetched
            } else {
                alert('Failed to fetch labours!');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleSendRequest = async (labourIndex) => {
        const labour = labours[labourIndex];

        if (!labour.labour_id) {
            console.error('Labour ID is undefined!');
            return;
        }

        // Update status to "Pending"
        const updatedLabours = [...labours];
        updatedLabours[labourIndex].status = 'Pending';
        setLabours(updatedLabours);
        localStorage.setItem('selectedLabours', JSON.stringify(updatedLabours));

        try {
            const response = await axios.post('http://127.0.0.1:5000/send_request', {
                user_id: userId,
                username: name,
                labour: labour,
                request_date: new Date().toISOString()
            });

            if (response.status === 200) {
                // Assume backend returns the updated status (7 for Accepted, 8 for Rejected)
                const updatedStatus = response.data.status === 7 ? 'Approved' : 'Rejected';
                updatedLabours[labourIndex].status = updatedStatus;
                setLabours(updatedLabours);
                setIsModalOpen(false); // Close the modal after sending the request
                alert(`Request ${updatedStatus.toLowerCase()} successfully`);
            }
        } catch (error) {
            console.error('Error sending request:', error);
            alert('Failed to send request');
        }
    };

    const BookedDetails = ({ bookings, renderStatus }) => {
        const [isVisible, setIsVisible] = useState(false);

        const toggleVisibility = () => {
            setIsVisible(prevState => !prevState);
        };

        return (
            <div>
                <button className="toggle-button" onClick={toggleVisibility}>
                    {isVisible ? 'Hide Your Booked Details' : 'Show Your Booked Details'}
                </button>
                {isVisible && (
                    <table>
                        <thead>
                            <h3>Booked info with Labour Deatils</h3>
                            <tr>
                                <th>Order ID</th>
                                <th>Labour ID</th>
                                <th>Labour Name</th>
                                <th>Working Date</th>
                                <th>Status</th>
                                <th>OTP</th>
                                <th>Price</th>
                            </tr>
                        </thead>
                        <tbody>
                            {bookings.length > 0 ? (
                                bookings.map(booking => (
                                    <tr key={booking.labour_id}>
                                        <td>{booking.order_id}</td>
                                        <td>{booking.labour_id}</td>
                                        <td>{booking.labour_name}</td>
                                        <td>{new Date(booking.request_date).toLocaleString()}</td>
                                        <td>{renderStatus(booking.status)}</td>
                                        <td>{booking.otp}</td>
                                        <td>{booking.price}</td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="3">No bookings found.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                )}
            </div>
        );
    };

    return (
        <div className="user-dashboard-container">
            <div className="welcome-section">
                <h1>Welcome, {name}!</h1>
                <p>Your User ID: {userId}</p>
                <button className="logout-button" onClick={handleLogout}>Logout</button>
            </div>

            <BookedDetails bookings={bookings} renderStatus={renderStatus} />

            <div className="buttons-section">
                <button className="spot-button" onClick={() => handleBookingType('spot')}>Spot Booking</button>
                <button className="advance-button" onClick={() => handleBookingType('advance')}>Advance Booking</button>
                <button className="advance-button" onClick={() => handleBookingType('longterm')}>Long Term Booking</button>
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
                                <option value="">Select Professional Type</option>
                                {professionals.map((professional, index) => (
                                    <option key={index} value={professional}>{professional}</option>
                                ))}
                            </select>
                        </div>
                        <button type="submit">Search</button>
                    </form>
                </div>
            )}

            {/* Modal Popup for Available Labours */}
            {isModalOpen && labours.length > 0 && (
                <div className="modal">
                     <div class="modal-content">
                        <h2>Available Labours</h2>
						<button class="close">&times;</button>
                        <div className="labours-header">
                            <span>Labour ID</span>
                            <span>Status</span>
                            <span>Action</span>
                        </div>
                        <ul>
                            {labours.map((labour, index) => (
                                <li key={labour.labour_id}>
                                    <span>{labour.labour_id}</span>
                                    <span>{labour.status}</span>
                                    <button
                                        disabled={labour.status === 'Pending'}
                                        onClick={() => handleSendRequest(index)}
                                    >
                                        Send Request
                                    </button>
                                </li>
                            ))}
                        </ul>
                        <button onClick={() => setIsModalOpen(false)}>Close</button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default UserDashboard;
