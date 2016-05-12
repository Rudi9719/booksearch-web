<!DOCTYPE html>
<html>
      <head>
        <!-- Styles -->
         % include('views/partials/scripts')
         % include('views/partials/styles')
         <link rel="apple-touch-icon" sizes="57x57" href="/static/icons/apple-icon-57x57.png">
         <link rel="apple-touch-icon" sizes="60x60" href="/static/icons/apple-icon-60x60.png">
         <link rel="apple-touch-icon" sizes="72x72" href="/static/icons/apple-icon-72x72.png">
         <link rel="apple-touch-icon" sizes="76x76" href="/static/icons/apple-icon-76x76.png">
         <link rel="apple-touch-icon" sizes="114x114" href="/static/icons/apple-icon-114x114.png">
         <link rel="apple-touch-icon" sizes="120x120" href="/static/icons/apple-icon-120x120.png">
         <link rel="apple-touch-icon" sizes="144x144" href="/static/icons/apple-icon-144x144.png">
         <link rel="apple-touch-icon" sizes="152x152" href="/static/icons/apple-icon-152x152.png">
         <link rel="apple-touch-icon" sizes="180x180" href="/static/icons/apple-icon-180x180.png">
         <link rel="icon" type="image/png" sizes="192x192"  href="/static/icons/android-icon-192x192.png">
         <link rel="icon" type="image/png" sizes="32x32" href="/static/icons/favicon-32x32.png">
         <link rel="icon" type="image/png" sizes="96x96" href="/static/icons/favicon-96x96.png">
         <link rel="icon" type="image/png" sizes="16x16" href="/static/icons/favicon-16x16.png">


        <link rel="stylesheet" href="/static/css/material.min.css">

            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

         <link rel='stylesheet prefetch' href='http://fonts.googleapis.com/css?family=Roboto:400,100,300,500,700,900|RobotoDraft:400,100,300,500,700,900'>


                <title>{{ "{0} | BookSearch".format(title) if defined("title") else "BookSearch" }}</title>
    </head>

% main()

</html>