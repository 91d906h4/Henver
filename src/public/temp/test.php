<?php

session_start();

echo $_SERVER['SERVER_NAME'];

$_SESSION["asd"] = 1;

echo($_GET["test"]);

echo($_SESSION["asd"]);

echo("<h1>YEAH!</h1>");

?>
<img src="./download.jpg" />

<a href="/">Back to home page</a>