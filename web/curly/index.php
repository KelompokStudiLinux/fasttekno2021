<?php

$url = htmlspecialchars($_GET['url']);
system("curl -sL $url");
