import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import '../../styles/LabourPage.css';

const LabourDashboard = () => {
    const location = useLocation();
    const { name = 'Unknown User', labourId = 'Unknown ID' } = location.state || {};
    const [requests, setRequests] = useState([]);
    const [otp, setOtp] = useState(''); 
    const [currentBookingId, setCurrentBookingId] = useState(null);
    const [bookedDetails, setBookedDetails] = useState([]);
    const [showEndPopup, setShowEndPopup] = useState(false); // State to show/hide end work popup

    // Function to fetch pending requests
    const fetchRequests = useCallback(async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/get_requests?labour_id=${labourId}`);
            if (response.data && Array.isArray(response.data.requests)) {
                setRequests(response.data.requests);
            } else {
                console.error('Unexpected data format for requests:', response.data);
                setRequests([]);
            }
        } catch (error) {
            console.error('Error fetching requests:', error);
        }
    }, [labourId]);

    // Function to fetch booked details
    const fetchBookedDetails = useCallback(async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/get_booked_details?labour_id=${labourId}`);
            if (response.data && Array.isArray(response.data.bookedDetails)) {
                setBookedDetails(response.data.bookedDetails);
            } else {
                console.error('Unexpected data format for booked details:', response.data);
                setBookedDetails([]);
            }
        } catch (error) {
            console.error('Error fetching booked details:', error);
        }
    }, [labourId]);

    useEffect(() => {
        fetchRequests();
        fetchBookedDetails();
    }, [location.state, labourId, fetchRequests, fetchBookedDetails]);

    const handleResponse = async (userId, response) => {
        try {
            const res = await axios.post('http://127.0.0.1:5000/respond_request', {
                labour_id: labourId,
                user_id: userId,
                response: response
            });

            if (res.status === 200) {
                alert(`Request ${response}ed successfully`);
                setRequests(requests.filter(request => request.user_id !== userId));
                fetchBookedDetails(); 
            }
        } catch (error) {
            console.error(`Error ${response}ing request:`, error);
            alert(`Failed to ${response} request`);
        }
    };

    const handleStart = (bookingId) => {
        setCurrentBookingId(bookingId); 
        const otpValue = prompt('Enter OTP to start work:'); 
        if (otpValue) {
            validateOtp(bookingId, otpValue);
        }
    };

    const validateOtp = async (bookingId, otpValue) => {
        try {
            const res = await axios.post('http://127.0.0.1:5000/validate_otp', {
                order_id: bookingId,
                otp: otpValue
            });

            if (res.status === 200 && res.data.success) {
                alert('OTP validated successfully!');
                setBookedDetails(bookedDetails.map(detail =>
                    detail.order_id === bookingId ? { ...detail, status: 'Started' } : detail
                ));
            } else {
                alert('Invalid OTP. Please try again.');
            }
        } catch (error) {
            console.error('Error validating OTP:', error);
            alert('Failed to validate OTP');
        }
    };

    const handleEndWork = () => {
        setShowEndPopup(true); // Show the end work confirmation popup
    };

    const submitPayment = async () => {
        try {
            const res = await axios.post('http://127.0.0.1:5000/end_work', {
                order_id: currentBookingId
            });

            if (res.status === 200) {
                alert('Work ended successfully and payment submitted!');
                setBookedDetails(bookedDetails.map(detail =>
                    detail.order_id === currentBookingId ? { ...detail, status: 'Ended' } : detail
                ));
                setShowEndPopup(false); // Close the popup
            } else {
                alert('Failed to end work or submit payment.');
            }
        } catch (error) {
            console.error('Error ending work or submitting payment:', error);
            alert('Failed to end work or submit payment.');
        }
    };

    return (
        <div>
            <h1>Welcome, {name}!</h1>
            <p>Your Labour ID: {labourId}</p>

            <h2>Notifications</h2>
            {requests.length > 0 ? (
                requests.map(request => (
                    <div key={request.user_id} className="notification">
                        <p>Request from User ID: {request.user_id}</p>
                        <button onClick={() => handleResponse(request.user_id, 'accept')}>Accept</button>
                        <button onClick={() => handleResponse(request.user_id, 'reject')}>Reject</button>
                    </div>
                ))
            ) : (
                <p>No new requests.</p>
            )}

            <h2>Booked Details</h2>
            {bookedDetails.length > 0 ? (
                <table className="booked-details-table">
                    <thead>
                        <tr>
                            <th>Booking ID</th>
                            <th>User ID</th>
                            <th>Status</th>
                            <th>Start Date</th>
                            <th>End Date</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {bookedDetails.map(detail => (
                            <tr key={detail.order_id}>
                                <td>{detail.order_id}</td>
                                <td>{detail.user_id}</td>
                                <td>{detail.status}</td>
                                <td>{detail.start_date}</td>
                                <td>{detail.end_date}</td>
                                <td>
                                    {detail.status === 'Started' ? (
                                        <button className="end-button" onClick={handleEndWork}>End</button>
                                    ) : (
                                        <button className="start-button" onClick={() => handleStart(detail.order_id)}>Start</button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No booked details available.</p>
            )}

            {showEndPopup && (
                <div className="end-popup">
                    <h2>Confirm End of Work</h2>
                    <p>Order ID: {currentBookingId}</p>
                    <button onClick={submitPayment}>Submit Payment</button>
                    <button onClick={() => setShowEndPopup(false)}>Cancel</button>
                </div>
            )}
        </div>
    );
};

export default LabourDashboard;



// import React, { useState, useEffect } from 'react';
// import { useLocation } from 'react-router-dom';
// import axios from 'axios';

// function LabourDashboard() {
//     const location = useLocation();
//     const { name, labourId } = location.state || { name: 'Unknown User', labourId: 'Unknown ID' };

//     const [requests, setRequests] = useState([]);

//     useEffect(() => {
//         console.log('Location state:', location.state);
//     }, [location]);

//     return (
//         <div>
//             <h1>Welcome, {name}!</h1>
//             <p>Your Labour ID: {labourId}</p>
//         </div>
//     );
// }

// export default LabourDashboard;
