work related to removing xss vulnerabilities
Begun 10-12-2022
https://www.sanskrit-lexicon.uni-koeln.de/scans/PWGScan/disp1/index.php?key=%22%3E%3E%3Cimg%20src=x%20onerror=confirm(%22xss%22)%3E

payload : ">><img src=x onerror=confirm("xss")>

%22%3E%3E%3Cimg%20src=x%20onerror=confirm(%22xss%22)%3E

function init_inputs_key() {
 // word = citation.
 $ans = "";
 if (isset($_GET['word'])) {
  $x = $_GET['word'];
 }else if (isset($_GET['citation'])) {
  $x = $_GET['citation'];
 }else if (isset($_GET['key'])) {
  $x = $_GET['key'];
 }else {
  $x = "";
 }
 $invalid_characters = array("$", "%", "#", "<", ">", "=", "(", ")");
 $ans = str_replace($invalid_characters, "", $x);
 return $ans;
}

$x = init_inputs_key();
