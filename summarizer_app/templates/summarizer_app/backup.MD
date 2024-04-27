{% extends 'summarizer_app/base.html' %}
{% load static %}
{% block content %}
<!DOCTYPE html>
<html lang="en">


<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Summarization</title>
    <link rel="stylesheet" href="{% static 'styles.css' %}">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
        .sidebar {
            height: 100vh;
            width: 0;
            position: fixed;
            top: 0;
            left: 0;
            background-color: #304356;
            overflow-x: hidden;
            transition: 0.3s;
            padding-top: 30px;
            z-index: 3000;
            color: white;


        }




        /* Styles for the links in the sidebar */
        .sidebar a {
            padding: 10px 15px;
            text-decoration: none;
            font-size: 25px;
            color: #818181;
            display: block;
            /* transition: 0.3s; */
        }




        /* Change color on hover */
        .sidebar a:hover {
            color: #f1f1f1;
        }




        /* Styles for the close button */
        .sidebar .close-btn {
            cursor: pointer;
            font-size: 36px;


        }




        /* Styles to push content when sidebar is open */
        .content {
            /* transition: margin-left 0.5s; */
            padding: 16px;


        }




        /* Styles for the button to open the sidebar */
        #open-btn {
            font-size: 30px;
            cursor: pointer;
            position: fixed;
            z-index: 1;
            top: 100px;
            left: 20px;
        }


        .flex {
            display: flex;
            flex-direction: row;
        }




        .align-center {
            align-items: center;
            margin-inline: 15px;
            justify-content: space-between;
        }


        .user {
            font-size: 20px;
            width: 200px;
            height: 30px;
            overflow: hidden
        }


        .sidebar-content {
            margin-top: 10px;
            padding-left: 8px;
            padding-right: 30px;
            height: 80%;
            overflow-y: scroll;
            scrollbar-color: #304356#304356;
        }


        .history-title {
            font-weight: bold;
            padding-inline: 10px;
        }


        .delete-all-btn {
            /* Styles for the Delete All button */
            margin-left: 60px;
            padding: 10px 15px;
            background-color: #dc3545;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
            position: relative;
            margin-bottom: 0;




        }




        .delete-all-btn:hover {
            /* Hover effect for the Delete All button */
            background-color: #c82333;
        }


        /* Media query for responsive design */
        @media screen and (max-width: 768px) {
            .sidebar {
                width: 0;
            }




            .content {
                margin-left: 0;
            }
        }
    </style>
</head>


<body>
    <div class="content">
        <div id="sidebar" class="sidebar">
            <div class="flex align-center">


                <!-- <div class="user">
                    <p>{{ user.get_full_name }}</p>
                </div> -->
                <div class="close-btn" onclick="toggleSidebar()">&times;</div>
            </div>
            <div class="sidebar-content">
                <p href="#" class="history-title">History</p>
                <div class="history" id="historyLinks">
                    <a>Link1</a>
                </div>
            </div>
            <button onclick='deleteAllLinks()' class="delete-all-btn">Delete All</button>
            <div class="user">
                <p>{{ user.get_full_name }}</p>
            </div>
        </div>
        <div id="open-btn" onclick="toggleSidebar()">&#9776;</div> <!-- Moved the button inside .content -->
        <div class="card floating-box my-4 mx-5">
            <h1 class="mb-4" style="text-align: center;">Text Summarization</h1>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6 border-right pr-4">
                        <h5>Original Text</h5>
                        <label for="word_count_original"><strong>Word Count:</strong> <span
                                id="word_count_original">0</span></label>
                        <textarea id="input_text" name="input_text" class="form-control mb-2" rows="15"
                            oninput="updateWordCount()"></textarea>
                        <label for="algorithm">Choose Algorithm:</label>
                        <select id="algorithm" name="algorithm" class="form-control mb-3" onchange="var algorithmSelect = document.getElementById('algorithm');
                               var summaryLengthSpan = document.getElementById('sentences');
                               if (algorithmSelect.value === 'LSA') {
                                   summaryLengthSpan.style.display = 'inline';
                               } else {
                                   summaryLengthSpan.style.display = 'none';
                               }">
                            <option value="T5">T5 Original</option>
                            <option value="T5_our">T5 Our model</option>
                            <option value="LSA">LSA</option>
                        </select>
                        <span id="summary_length_value">Summary Length: 200</span>
                        <span id="sentences" style="display: none;">Sentences</span>
                        <input type="range" id="summary_length" name="summary_length" class="form-control-range mb-3"
                            min="1" max="1000" value="200" oninput="updateSummaryLengthValue(this.value)">
                        <button type="button" class="btn btn-primary" onclick="
                               var inputText = document.getElementById('input_text').value.trim();
                               if (inputText.length === 0) {
                                   alert('Please enter some data before proceeding.');
                                   return;
                               }
                               if (inputText.length < 30) {
                                   alert('Please enter at least 30 characters');
                                   return;
                               }
                               summarizeText();
                           "> Summarize </button>
                    </div>
                    <div class="col-md-6 pl-4">
                        <h5>Summarized Text</h5>
                        <div class="summary-box">
                            <div class="fixed-bottom-bar">
                                <p><strong>Word Count:</strong> <span id="word_count_summary">0</span> |
                                    <strong>Sentence Count:</strong> <span id="sentence_count_summary">0</span>
                                </p>
                            </div>
                            <p id="summarized_text"></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <!-- <footer class="footer" style="position: fixed; bottom: 0; width: 100%;">
       <p id="current-date-time"></p>
   </footer> -->




    <script src="{% static 'summarizer.js' %}"></script>
    <script>
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


        // function updateDateTime() {
        //     const today = new Date();
        //     const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
        //     const formattedDateTime = today.toLocaleString('en-US', options);
        //     document.getElementById('current-date-time').textContent = formattedDateTime;
        // }




        // setInterval(updateDateTime, 1000);
        // updateDateTime();
    </script>
</body>


</html>
{% endblock %}
