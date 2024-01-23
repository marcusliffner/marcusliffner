<?php 
$unamn = $_SESSION['uname'];
$inloggad = 
'
Välkommen '.$unamn.'<a href="?action=logout"> Log Out</a>
';

$nav = 
'
      <nav>
        <ul>
          <li>Link</li>
          <li>Link</li>
          <li>Link</li>
        </ul>
      </nav>
';

$article = 
'

';

if(isset($_GET["page"])){
switch($_GET["page"]){

case "":
    
$article = '

';

break;

}}