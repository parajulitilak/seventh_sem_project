function populateFromHistory(topic, inputText, summary) {
    // Populate the input text area
    document.getElementById("input_text").value = inputText;
    var summarizedText = summary;
    document.getElementById("summarized_text").textContent = summarizedText;

}

// Function to fetch user history and populate the sidebar
window.addEventListener('DOMContentLoaded', function () {
    fetchUserHistory();
});


//below is the code for leftnavbar-deleteicon and its functionality individial icon lai delete garne
function fetchUserHistory() {
    fetch('/summarization/summarize/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const historyLinks = document.getElementById('historyLinks');
        historyLinks.innerHTML = ''; // Clear existing history links

        // Iterate over each history item and create a link for it
        data.forEach(historyItem => {
            const historyDiv = document.createElement('div');
            historyDiv.classList.add('history-list');
            historyDiv.style.marginBottom = '10px'; // Add gap between history items
            historyDiv.style.position = 'relative'; // Add position relative to contain absolute positioned delete icon
            historyDiv.style.height="25px";
            historyDiv.style.padding = '4px'; // Increase padding to make the background bigger
            
            // History text
            const historyText = document.createTextNode(historyItem.short_topic);
            historyDiv.appendChild(historyText);

            // Delete icon
            const deleteIcon = document.createElement('i');
            deleteIcon.classList.add('fas', 'fa-trash-alt'); // Font Awesome trash icon classes
            deleteIcon.style.position = 'absolute';
            deleteIcon.style.right = '5px';
            deleteIcon.style.top = '50%';
            deleteIcon.style.transform = 'translateY(-50%)';
            deleteIcon.style.cursor = 'pointer';
            deleteIcon.style.color = 'red'; // Make the icon red
            deleteIcon.style.opacity = '0'; // Initially hide the delete icon
            deleteIcon.addEventListener('click', function (event) {
                event.stopPropagation(); // Prevent click event from bubbling up to historyDiv
                deleteHistoryItem(historyItem); // Delete the history item
                historyLinks.removeChild(historyDiv); // Remove the history item from the DOM
            });
            historyDiv.appendChild(deleteIcon);

            // Hover effect
            historyDiv.addEventListener('mouseenter', function () {
                historyDiv.style.backgroundColor = "rgba(0, 120, 215, 0.3)"; // Adjusted color to resemble ChatGPT's left bar
                deleteIcon.style.opacity = '1'; // Show delete icon on hover
            });
            historyDiv.addEventListener('mouseleave', function () {
                historyDiv.style.backgroundColor = ""; // Reset background color on mouse leave
                deleteIcon.style.opacity = '0'; // Hide delete icon on mouse leave
            });

            historyDiv.addEventListener('click', function () {
                populateFromHistory(historyItem.short_topic, historyItem.input_text, historyItem.summarized_text);
            });
            historyLinks.appendChild(historyDiv);
        });
    })
    .catch(error => console.error('Error fetching user history:', error));
}


//start
// Function to update the history list every 5 seconds
function updateHistoryList() {
    fetchUserHistory();
    setTimeout(updateHistoryList, 500); // Update every 5 seconds
}

// Call the function to update the history list initially and start the update loop
window.addEventListener('DOMContentLoaded', function () {
    fetchUserHistory(); // Fetch user history when the page loads
    updateHistoryList(); // Start the update loop
});
//
// Function to delete history item
function deleteHistoryItem(historyItem) {
    // Display a confirmation dialog
    var confirmation = confirm(`Are you sure you want to delete "${historyItem.short_topic}"?`);
    
    // If user confirms, proceed with deletion
    if (confirmation) {
        // Send a DELETE request to delete the history item
        fetch(`/delete-history/${historyItem.id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCSRFToken(), // Include CSRF token if required
            },
        })
        .then(response => {
            if (response.ok) {
                historyItem.remove(); // Remove the history item from the UI
            } else {
                console.error('Failed to delete history item:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error deleting history item:', error);
        });
    }
}





function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementsByClassName("content")[0];
    if (sidebar.style.width === "250px" || window.innerWidth <= 768) {
        sidebar.style.width = "0";
        content.style.marginLeft = "0";
    } else {
        sidebar.style.width = "250px";
        content.style.marginLeft = "250px";
    }
}

// Close the sidebar when the window is resized to a smaller size
window.addEventListener("resize", function () {
    if (window.innerWidth <= 768) {
        document.getElementById("sidebar").style.width = "0";
        document.getElementsByClassName("content")[0].style.marginLeft = "0";
    }
});

// Close the sidebar initially if the window is small
if (window.innerWidth <= 768) {
    document.getElementById("sidebar").style.width = "0";
    document.getElementsByClassName("content")[0].style.marginLeft = "0";
}

function deleteAllLinks() {
    // Display a confirmation dialog
    var confirmation = confirm("Are you sure you want to delete history?");
    // Check if user clicked "Ok"
    if (confirmation) {
        // If user clicked "Ok", clear the history
        document.getElementById("historyLinks").innerHTML = "";
    }
}

function deleteLink(historyItem) {
    const historyItemId = historyItem.dataset.historyId; // Assuming historyId is stored as a data attribute

    fetch(`/delete-history/${historyItemId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token if required
        },
    })
    .then(response => {
        if (response.ok) {
            historyItem.remove(); // Remove the history item from the UI
        } else {
            console.error('Failed to delete history item:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error deleting history item:', error);
    });
}

// Function to get CSRF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function logout() {
    // Perform logout actions here
    // For example, redirect the user to the logout URL
    window.location.href = '/logout'; // Replace '/logout' with your actual logout URL
}

// Function to fetch CSRF token from cookies
function getCsrfCookie(name) {
    const cookieName = name + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');
    for(let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i].trim();
        if (cookie.indexOf(cookieName) === 0) {
            return cookie.substring(cookieName.length, cookie.length);
        }
    }
    return null;
}


// Function to delete all history of user 
function deleteAllLinks() {
    // Fetch CSRF token from cookies
    const csrftoken = getCookie('csrftoken');
    
    // Send DELETE request with CSRF token included in headers
    fetch('/delete-all-history', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken  // Include CSRF token in headers
        },
        body: JSON.stringify({}) // You can pass any data if required
    })
    .then(response => {
        if (response.ok) {
            // Reload the page or perform any other action upon successful deletion
            window.location.reload();
        } else {
            // Handle error response
            console.error('Failed to delete user history');
        }
    })
    .catch(error => {
        console.error('Error deleting user history:', error);
    });
}




function updateWordCount() {
    const inputText = document.getElementById('input_text').value;
    const wordCount = countWords(inputText);
    document.getElementById('word_count_original').textContent = wordCount;
}

function updateSummaryLengthValue(value) {
    document.getElementById('summary_length_value').textContent = `Summary Length: ${value}`;
}

function countWords(text) {
    const words = text.trim().split(/\s+/);
    return words.length;
}

function countSentences(text) {
    const sentences = text.trim().split(/[.!?]+[\s,]*/);
    return sentences.length;
}


function summarizeText() {
    const inputText = document.getElementById('input_text').value;
    const algorithm = document.getElementById('algorithm').value;
    const summaryLength = document.getElementById('summary_length').value;

    const formData = new FormData();
    formData.append('input_text', inputText);
    formData.append('algorithm', algorithm);
    formData.append('summary_length', summaryLength);

    const url = '/summarization/summarize/';

    fetch(url, {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            updateUI(data);
        })
        .catch(error => {
            console.error('Error generating and updating summary:', error);
        });
}

function updateUI(summaryDetails) {
    const wordCountElement = document.getElementById('word_count_summary');
    const sentenceCountElement = document.getElementById('sentence_count_summary');

    // Initialize Word Count and Sentence Count with 0
    let wordCount = 0;
    let sentenceCount = 0;

    if (wordCountElement && sentenceCountElement) {
        const { generated_summary } = summaryDetails;

        // Update Word Count and Sentence Count when the summary is received
        if (generated_summary) {
            const { word_count, sentence_count } = summaryDetails;
            wordCount = word_count;
            sentenceCount = sentence_count;
        }

        wordCountElement.textContent = wordCount;
        sentenceCountElement.textContent = sentenceCount;

        const summarizedTextElement = document.getElementById('summarized_text');
        if (summarizedTextElement) {
            summarizedTextElement.textContent = generated_summary;
        } else {
            console.error('Error updating UI: summarized_text element not found');
        }
    } else {
        console.error('Error updating UI: word_count_summary or sentence_count_summary element not found');
    }
}

// Function to get CSRF token from cookies
function getCSRFToken() {
    const name = 'csrftoken';  // Name of the CSRF token cookie
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}


// Function to prompt confirmation before deleting account
function deleteAccount() {
    var confirmation = confirm("Are you sure you want to delete your account? This action cannot be undone.");
    if (confirmation) {
        fetch('/delete-account/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/account-deleted/';
            } else {
                console.error('Failed to delete account');
            }
        })
        .catch(error => {
            console.error('Error deleting account:', error);
        });
    }
}




