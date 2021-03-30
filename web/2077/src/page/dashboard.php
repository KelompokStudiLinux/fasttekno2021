<?php

global $pdo;

if (empty($_SESSION['name'])) {
    echo "<script>window.location.replace('/?page=login.php')</script>";
    die;
}

?>

<div class="container mt-4 text-white text-center">
    <h1 class="mt-5">Welcome, <?php echo $_SESSION['name']; ?></h1>
</div>
