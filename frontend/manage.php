<?php
session_start();
?>



<?php
// Echo session variables that were set on previous page
echo "user is " . $_SESSION["user"] . ".<br>";
?>
