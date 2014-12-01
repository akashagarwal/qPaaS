
 <?php
 include_once('header.php');

echo $_SESSION["username"];
?>
<form action="deploy-submit.php" method="GET">
 <label for="appname">AppName</label> <input type="text" name="appname"><br>
 App <select name="app-type">
 <option value="php">PHP</option>
 <option value="python">Python</option>
 </select>
 <br>
 Framework <select name="framework">
 <option value="flask">Flask</option>
 <option value="django">Django</option>
 <option value="apache2">Apache2</option>
 </select>
 <br>
 TarFile <input type="file" name="tarfile"><br>
 Dependecies <input type="file" name="dependencyfile"><br>
 <input type="submit" value="Deploy">
 <form>
