<?php
$file_path = "../www/" . $_GET['file']; // Path to the file you want to display

// Check if the file exists
if (isset($file_path)) {
    // Read the content of the file
    $file_content = include($file_path);

    // Output the content of the file as is
    echo $file_content;
} else {
    echo "File not found";
}
?>
