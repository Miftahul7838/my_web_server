<?php
$file_path = "../www/" . $_GET['file']; // Path to the file you want to display

// Check if the file exists
if (file_exists($file_path)) {
    // Read the content of the file
    $file_content = file_get_contents($file_path);

    // Output the content of the file as is
    echo $file_content;
} else {
    echo "File not found";
}
?>
