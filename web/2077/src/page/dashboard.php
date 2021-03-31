<?php

global $pdo;

if (empty($_SESSION['name'])) {
    header('Location: ?page=login.php');
    die;
}

?>

<div class="container mt-4 text-white text-center">
    <h1 class="mt-5">Welcome, <?php echo $_SESSION['name']; ?></h1>
</div>
