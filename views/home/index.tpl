% import constants
% import json

% def main():
<body>
        <div id="background">
            <img class="stretch" src="/static/img/Web19201.png"/>
        </div>
            <img id="suny" src="/static/img/Sunypolyseal.png" />
            <img class="logo" src="/static/img/SUNY.png" />
                <p id="title">BookSearch</p>

<!-------------------------Login Button-------------------------->


        <div class="login-button" id="login-button">
            <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">Login/Register</button>
        </div>


<!---------------------Sliding Menu Bar-------------------------->
        <div class="menu">

                    <!-- Menu icon -->
        <div class="icon-close">
            <img src="/static/img/close.png">
        </div>

                    <!-- Menu -->
            <ul>
                <li><a href="/about">About</a></li>
                <li><a href="/discover">Discover</a></li>
                <li><a href="/help">Help</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
        </div>

        <div class="icon-menu">
            <i class="fa fa-bars"></i>
                    Menu
        </div>
<!--------------------------------------------------------------->

</body>

% end

<%
    rebase("layout")
%>