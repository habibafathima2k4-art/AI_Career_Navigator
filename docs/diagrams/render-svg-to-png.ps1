param(
  [Parameter(Mandatory = $true)]
  [string]$InputSvg,
  [Parameter(Mandatory = $true)]
  [string]$OutputPng
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$resolvedSvg = (Resolve-Path $InputSvg).Path
$outputPath = [System.IO.Path]::GetFullPath($OutputPng)
$outputDir = Split-Path $outputPath -Parent

if (-not (Test-Path $outputDir)) {
  New-Item -ItemType Directory -Path $outputDir | Out-Null
}

$uri = [System.Uri]::new($resolvedSvg)

$form = New-Object System.Windows.Forms.Form
$form.Width = 1800
$form.Height = 1400
$form.StartPosition = "Manual"
$form.Location = New-Object System.Drawing.Point(-2000, -2000)

$web = New-Object System.Windows.Forms.WebBrowser
$web.ScrollBarsEnabled = $false
$web.ScriptErrorsSuppressed = $true
$web.Dock = "Fill"
$form.Controls.Add($web)

$script:done = $false
$script:errorMessage = $null

$handler = [System.Windows.Forms.WebBrowserDocumentCompletedEventHandler]{
  param($sender, $e)
  try {
    if ($null -eq $web.Url -or $e.Url.AbsoluteUri -ne $web.Url.AbsoluteUri) {
      return
    }

    Start-Sleep -Milliseconds 1500

    $bmp = New-Object System.Drawing.Bitmap($web.Width, $web.Height)
    $rect = New-Object System.Drawing.Rectangle(0, 0, $web.Width, $web.Height)
    $web.DrawToBitmap($bmp, $rect)
    $bmp.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
    $script:done = $true
  } catch {
    $script:errorMessage = $_.Exception.Message
  } finally {
    $form.Close()
  }
}

$web.add_DocumentCompleted($handler)
$web.Navigate($uri.AbsoluteUri)
[void]$form.ShowDialog()

if ($script:errorMessage) {
  throw $script:errorMessage
}

if (-not (Test-Path $outputPath)) {
  throw "PNG output was not created."
}

Write-Output $outputPath
