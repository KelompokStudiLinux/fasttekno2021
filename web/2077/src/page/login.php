<?php

if ($_POST) {
	$name = trim($_POST['name']);

	$_SESSION['name'] = $name;
	header('Location: ?page=dashboard.php');
	die;
}

?>

<div class="bg-dark col-sm-6 offset-sm-3 my-5 p-5">
	<div class="container">
		<h1 class="text-center mb-3">Login</h1>
		<form method="POST" action="">
			<div class="mb-3">
				<input type="text" class="form-control" name="name" placeholder="Your Name" autofocus required>
			</div>
			<button type="submit" class="btn btn-primary">Submit</button>
		</form>
	</div>
</div>

