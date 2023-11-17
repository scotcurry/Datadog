$currentDate = Get-Date -Format "yyyy/MM/dd HH:mm"
$majorVersion = $currentDate.Substring(3, 1)
$minorVersion = $currentDate.Substring(5, 2)
If ($minorVersion.Substring(0,1) -eq "0") {
    $minorVersion = $minorVersion.Substring(1, 1)
}
$dayVersion = $currentDate.Substring(8,2)

$buildVersionHours = [Int]$currentDate.Substring(11, 2)
$hourMinutes = $buildVersionHours * 60
$minutes = [Int]$currentDate.Substring(14, 2)
$buildVersionValue = $hourMinutes + $minutes
$buildVersionString = $buildVersionValue.ToString()

$version = $majorVersion + "." + $minorVersion + $dayVersion + "." + $buildVersionString
return $version