<?php
#include_once('connection.php');

$username = $_POST['user_id'];
$password = $_POST['password'];

#$query = "SELECT user_id FROM user_info  WHERE user_id = '$username' and  password = '$password'";
#$result = mysqli_query($conn, $query);

#if (mysqli_num_rows($result) > 0) {
	session_start();
	$_SESSION['username'] = $username;
#}

echo "Sex:";
header('location: ./index.php');
