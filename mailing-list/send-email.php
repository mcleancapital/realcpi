<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Retrieve form data
    $firstName = htmlspecialchars($_POST["first_name"]);
    $lastName = htmlspecialchars($_POST["last_name"]);
    $email = htmlspecialchars($_POST["email"]);

    // Email details
    $to = "ianmclean@mcleancapital.ca"; // Replace with your Gmail address
    $subject = "New Mailing List Signup";
    $message = "You have a new mailing list signup:\n\n";
    $message .= "First Name: $firstName\n";
    $message .= "Last Name: $lastName\n";
    $message .= "Email: $email\n";

    $headers = "From: no-reply@yourdomain.com\r\n"; // Replace with your domain
    $headers .= "Reply-To: $email\r\n";

    // Send email
    if (mail($to, $subject, $message, $headers)) {
        echo "<h1>Thank you for signing up!</h1>";
        echo "<p>We appreciate your interest and will keep you updated with the latest insights.</p>";
    } else {
        echo "<h1>Something went wrong.</h1>";
        echo "<p>Please try again later or contact us directly.</p>";
    }
} else {
    echo "<h1>Invalid Request</h1>";
    echo "<p>This form can only be submitted via POST method.</p>";
}
?>
