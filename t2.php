<?php


$decode_id="nimda";
$decode_pw="";


for($i=0;$i<20;$i++){
  $decode_id=base64_encode($decode_id);
  $decode_pw=base64_encode($decode_pw);
}

$decode_id=str_replace("1", "!",$decode_id);
$decode_id=str_replace("2", "@",$decode_id);
$decode_id=str_replace("3", "$",$decode_id);
$decode_id=str_replace("4", "^",$decode_id);
$decode_id=str_replace("5", "&",$decode_id);
$decode_id=str_replace("6", "*",$decode_id);
$decode_id=str_replace("7", "(",$decode_id);
$decode_id=str_replace("8", ")",$decode_id);

echo("$decode_id");
//$decode_pw<hr>");

if($decode_id=="admin" && $decode_pw=="nimda"){
  solve(6);
}
?>
