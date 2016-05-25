% import constants
% import json

% def main():
<body>
    <!-----       <div class="login-button" id="login-button">
            <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">Login/Register</button>
        </div>   ---->


<!-- Uses a transparent header that draws on top of the layout's background -->
<style>
.demo-layout-transparent {
background: url('/static/img/Web19201.png') center / cover;
}
.demo-layout-transparent .mdl-layout__header,
.demo-layout-transparent .mdl-layout__drawer-button {
/* This background is dark, so we set text to white. Use 87% black instead if
your background is light. */
color: white;
}
</style>

<div class="demo-layout-transparent mdl-layout mdl-js-layout">
<header class="mdl-layout__header mdl-layout__header--transparent">
<div class="mdl-layout__header-row">
<!-- Title -->
<span class="mdl-layout-title">BookSearch</span>
<!-- Add spacer, to align navigation to the right -->
<div class="mdl-layout-spacer"></div>
<!-- Navigation -->
<nav class="mdl-navigation">
<a class="mdl-navigation__link" href="">Link</a>
<a class="mdl-navigation__link" href="">Link</a>
<a class="mdl-navigation__link" href="">Link</a>
<a class="mdl-navigation__link" href="">Link</a>
</nav>
</div>
</header>
<div class="mdl-layout__drawer">
<span class="mdl-layout-title">Title</span>
<nav class="mdl-navigation">
<a class="mdl-navigation__link" href="/login">Login</a>
<a class="mdl-navigation__link" href="/about">About Us</a>
<a class="mdl-navigation__link" href="">Link</a>
<a class="mdl-navigation__link" href="">Link</a>
</nav>
</div>
<main class="mdl-layout__content">
</main>
</div>

</body>

% end

<%
    rebase("layout")
%>