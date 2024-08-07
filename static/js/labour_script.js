let currentOrderId = null;

function openModal(orderId) {
    currentOrderId = orderId;
    document.getElementById('otpModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('otpModal').style.display = 'none';
}

async function validateOTP() {
    const otp = document.getElementById('otpInput').value;
    const response = await fetch('/validate_otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ order_id: currentOrderId, otp: otp }),
    });

    const result = await response.json();

    if (result.success) {
        document.getElementById(`startButton_${currentOrderId}`).style.display = 'none';
        document.getElementById(`endButton_${currentOrderId}`).style.display = 'inline';
        closeModal();
        alert('Work started successfully!');
    } else {
        alert('Invalid OTP. Please try again.');
    }
}

async function endWork(orderId) {
    const response = await fetch('/end_work', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ order_id: orderId }),
    });

    const result = await response.json();

    if (result.success) {
        document.getElementById(`endButton_${orderId}`).disabled = true;
        alert('Work ended successfully!');
    } else {
        alert('Error ending work. Please try again.');
    }
}
