function displayOptions() {
    var optionsDiv = document.getElementById('chatbotOptions');
    if (optionsDiv.style.display === 'none' || optionsDiv.style.display === '') {
        optionsDiv.style.display = 'block';
    } else {
        optionsDiv.style.display = 'none';
    }
}

function sendOption(option) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/chatbot_option', true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            document.getElementById('chatbotOutput').textContent = response.message;
        }
    };
    xhr.send(JSON.stringify({ option: option }));
}
