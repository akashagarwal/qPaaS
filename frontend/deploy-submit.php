<?php

$framework=$_GET['framework'];
$output=[];
$success;
if ( $framework === "flask" ) {
	
	exec("sudo bash /home/ubuntu/PaaSApp/PaasServerApp/Flask.sh",$output,$success);
	echo "<h2> The deployment is successful </h3> <br/>";
	echo "<h3> Complete log </h3> <br/>";
	print_r($output);
	print $success;
}
else if ( $framework === "django" ) {
	exec("sudo bash /home/ubuntu/PaaSApp/PaasServerApp/Django.sh",$output,$success);
	echo "<h2> The deployment is successful </h3> <br/>";
	echo "<h3> Complete log </h3> <br/>";
	print_r($output);
	print $success;
}
else if ( $framework === "apache2" ) {
	exec("sudo bash /home/ubuntu/PaaSApp/PaasServerApp/Php.sh",$output,$success);
	echo "<h2> The deployment is successful </h3> <br/>";
	echo "<h3> Complete log </h3> <br/>";
	print_r($output);
	print $success;
}

?>
