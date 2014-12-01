<?php

session_start();
if (isset($_SESSION['username'])) {
	echo '<a href="logout.php">Logout</a><br />';
}
else {
	if ($_SERVER['REQUEST_URI'] != 'login.php') {
		header('location: login.php');
	}
}
