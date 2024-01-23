<html>
   <head>
      <meta charset="UTF-8">
      <meta name="description" content="Studerande portfölj">
      <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1, user-scalable=no">
      <title>website preview</title>
      <link rel="stylesheet" href="style.css">
   </head>
   <body>
<?php
    //innehåller html koden och innehåll som ska visas.

session_start ();
$_SESSION['state']=session_id();      
  
//Kollar om använderaren är inloggad
   if (isset ($_SESSION['msatg'])){
      include("main.php");

      echo '
      <header>
        <a href="" class="logo"></a>
        '.$inloggad.'
        <nav> 
        <h1>Website preview</h1> 
        </nav>
      </header> 
      <aside>
          '.$nav.'
      </aside> 
      <article>
      ';
      /* include functions */ 
      include 'projektdisplay.php';

      /* Prints projekt function */
      writeprojekt();

      echo '
      </article>
      <footer>
      
      </footer>
      ';
      echo $article;//information som visas om personen är inloggad 
      } 
//end if session
//om använderen inte är inloggad,visa inloggnings sida
    else echo '<h2><p>You can <a href="?action=login">Log In</a> with Microsoft</p></h2>';

    //API anslutning, styr vad som händer om en användare kommer ifrån MS inloggings sida, auth användare
    include ("auth.php");
?>


</body>
</html>   