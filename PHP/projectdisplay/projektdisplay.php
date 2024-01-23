<?php

function get_website_data($url)
 {   
    // Use the PHP file_get_contents() function to download the HTML of the website
    $html = file_get_contents($url);

    // Use a regular expression to extract the title and description from the HTML
    preg_match("/<title>(.+?)<\/title>/i", $html, $title_matches);
    preg_match("/<meta name=\"description\" content=\"(.+?)\"/i", $html, $description_matches);
    preg_match("/<img[^>]+src\s*=\s*[\"\']?([^\"\' >]+)[\"\']?[^>]*>/i", $html, $img_matches);


    //Sets null data as empty 
    if(!isset($title_matches[1]))
      { $title_matches[1] = ''; }
    if(!isset($description_matches[1]))
      { $description_matches[1] = ''; }     
    if(!isset($img_matches[1]))
      { $img_matches[1] = ''; }
    else
    {
      // Return the website data as an array
    
     // Check if the src attribute is a local file path or a URL
    if (preg_match("/https|www/", $img_matches[1])) 
      {
        return array
        (
          'title' => $title_matches[1],
          'description' => $description_matches[1],
          'img' => $img_matches[1]
        ); 
      } 
      else if($img_matches[1][0]=="/")  {        
       return array
       (
         'title' => $title_matches[1],
         'description' => $description_matches[1],
         'img' => $url.$img_matches[1]
       ); 
     }
      else {
             // The src attribute is a URL, so we can display the image directly
            return array
            (
              'title' => $title_matches[1],
              'description' => $description_matches[1],
              'img' => $url.'/'.$img_matches[1]
            ); 
          }
  
      }   
  }

function writeprojekt() 

    {
      // Set up an array of website URLs to loop through
      $websites = file('file.txt');
      $websites = array_map('rtrim', $websites);

       // Loop through the array of websites
      foreach ($websites as $url) 

          {
          // Use the URL to retrieve the title and description of the website
          $website_data = get_website_data($url);
            if ($website_data['img'] == '')
              {
              echo "<a href=".$url."  class='website-preview'>";
                echo "<h3>" . $website_data['title'] . "</h3>";
                echo "<p>" . substr($website_data['description'],0,250) . "</p>";
                echo "<div class='website-previewnoimg'></div>";
               /* echo $url; */
              echo "</a>";
              }
              else
              {
            // Display the preview image and website data on the page
            echo "<a href=".$url."  class='website-preview'>";
              echo "<img src='". $website_data['img'] . "' alt='Website preview image' >";
              echo "<h3>" . $website_data['title'] . "</h3>";
              echo "<p>" . substr($website_data['description'],0,250) . "</p>";
             /* echo $url; */
            echo "</a>";
            }
          }
    }

?> 