param(
    [string]$Target,
    [string]$DestDir
)

$ws = New-Object -ComObject WScript.Shell

$name = [System.IO.Path]::GetFileNameWithoutExtension($Target) + ".lnk"
$link = Join-Path $DestDir $name

$sc = $ws.CreateShortcut($link)
$sc.TargetPath = $Target
$sc.WorkingDirectory = Split-Path $Target
$sc.IconLocation = $Target
$sc.Save()
