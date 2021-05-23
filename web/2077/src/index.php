<?php
if (empty($_GET['page'])) {
  header('Location: /?page=dashboard.php');
  die;
}

session_start(); ?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2077</title>
  <link async href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
  <link async rel="stylesheet" href="assets/style.css" />
</head>

<body>
  <nav class="navbar navbar-expand-sm navbar-dark bg-dark">
    <div class="container">
      <a class="navbar-brand" href="/">2077</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
        <ul class="navbar-nav mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" href="?page=dashboard.php">Dashboard</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="?page=login.php">Login</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <main class="container my-5">
    <?php include 'page/' . $_GET['page']; ?>
  </main>
</body>

</html>
