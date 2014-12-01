<?php
include_once('header.php');
echo $_SESSION["username"];
echo "<br />";
#$command1 = "sudo docker ps | awk '{print $12}'";
$command1 = "sudo docker ps";
$command2 = "sudo docker ps -a";
$output1 = [];
$output2 = [];
#exec("sudo ls",$output);
#print_r($output);
#echo "<br />";
exec($command1, $output1);
for($i = 1; $i < sizeof($output1);$i++)
{
$pos=strpos($output1[$i],"0.0.0.0");
$x=substr($output1[$i],$pos+8);
$pos=strpos($x,"->");
$x=substr($x,0,$pos);
echo ' <h3> You app is running at : <a href="' . 'http://54.173.121.252:'. $x . '"> '  . ' http://54.173.121.252:'. $x . ' </a><br /> </h3>';
}
for($i = 1; $i < sizeof($output2);$i++)
{
$pos=strpos($output2[$i],"0.0.0.0");
$x=substr($output2[$i],$pos+8);
$pos=strpos($x,"->");
$x=substr($x,0,$pos);
echo ' <h3> You app is running at : <a href="' . 'http://54.173.121.252:'. $x . '"> '  . ' http://54.173.121.252:'. $x . ' </a><br /> </h3>';
}
#echo " Here   <br />";
echo '<a href="deploy.php">Deploy</a><br />';
?>

