<?php 
//Create a conection with database
$con = mysqli_connect("localhost", "root", "", "test");

//Set Variebles for the input
$fname = $_POST['fname'];
$lname = $_POST['lname'];
$pno = $_POST['pno'];
$phoneno = $_POST['phoneno'];

//Create a MySQL command to INSERT data into data table
$sql = "INSERT INTO registration(fname, lname,pno,phoneno) VALUES ('$fname', '$lname','$pno','$phoneno')";

//Now Insert data into database
//Check if data is inserted or not
if (!mysqli_query($con, $sql)) {
	echo "Data has not saved";
} else{
	echo "Data is saved successfully";
}


?>