param(
    [Parameter(Mandatory = $true)]
    [string]$InputDocx,

    [Parameter(Mandatory = $true)]
    [string]$OutputPdf
)

$word = $null
$document = $null

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $document = $word.Documents.Open($InputDocx)
    $document.Fields.Update() | Out-Null

    foreach ($section in $document.Sections) {
        foreach ($footer in $section.Footers) {
            if ($footer.Exists) {
                $footer.Range.Fields.Update() | Out-Null
            }
        }
    }

    $document.Save()
    $document.ExportAsFixedFormat($OutputPdf, 17)
}
finally {
    if ($null -ne $document) {
        $document.Close($false)
    }
    if ($null -ne $word) {
        $word.Quit()
    }
}
