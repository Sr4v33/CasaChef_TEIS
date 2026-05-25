param(
    [string]$LocaleRoot = (Join-Path $PSScriptRoot "..\locale")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Convert-PoLiteral {
    param([string]$Literal)

    $trimmed = $Literal.Trim()
    if (-not $trimmed.StartsWith('"')) {
        return ""
    }

    $content = $trimmed.Substring(1, $trimmed.Length - 2)
    return [regex]::Unescape($content)
}

function Read-PoEntries {
    param([string]$Path)

    $entries = @{}
    $msgid = $null
    $msgstr = $null
    $state = $null

    foreach ($line in Get-Content -LiteralPath $Path -Encoding UTF8) {
        $trimmed = $line.Trim()
        if ($trimmed.Length -eq 0 -or $trimmed.StartsWith("#")) {
            continue
        }

        if ($trimmed.StartsWith("msgid ")) {
            if ($null -ne $msgid -and $null -ne $msgstr) {
                $entries[$msgid] = $msgstr
            }
            $msgid = Convert-PoLiteral $trimmed.Substring(6)
            $msgstr = $null
            $state = "msgid"
            continue
        }

        if ($trimmed.StartsWith("msgstr ")) {
            $msgstr = Convert-PoLiteral $trimmed.Substring(7)
            $state = "msgstr"
            continue
        }

        if ($trimmed.StartsWith('"')) {
            if ($state -eq "msgid") {
                $msgid += Convert-PoLiteral $trimmed
            }
            elseif ($state -eq "msgstr") {
                $msgstr += Convert-PoLiteral $trimmed
            }
        }
    }

    if ($null -ne $msgid -and $null -ne $msgstr) {
        $entries[$msgid] = $msgstr
    }

    return $entries
}

function Write-MoFile {
    param(
        [hashtable]$Entries,
        [string]$OutputPath
    )

    $utf8 = [System.Text.Encoding]::UTF8
    $keys = @($Entries.Keys | Sort-Object)
    $count = $keys.Count

    $idByteArrays = @()
    $strByteArrays = @()
    foreach ($key in $keys) {
        $idByteArrays += ,$utf8.GetBytes([string]$key)
        $strByteArrays += ,$utf8.GetBytes([string]$Entries[$key])
    }

    $headerSize = 28
    $origTableOffset = $headerSize
    $transTableOffset = $origTableOffset + ($count * 8)
    $dataOffset = $transTableOffset + ($count * 8)

    $origOffsets = @()
    $transOffsets = @()
    $cursor = $dataOffset

    foreach ($bytes in $idByteArrays) {
        $origOffsets += $cursor
        $cursor += $bytes.Length + 1
    }
    foreach ($bytes in $strByteArrays) {
        $transOffsets += $cursor
        $cursor += $bytes.Length + 1
    }

    $directory = Split-Path -Parent $OutputPath
    if (-not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Path $directory | Out-Null
    }

    $stream = [System.IO.File]::Open($OutputPath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write)
    try {
        $writer = New-Object System.IO.BinaryWriter($stream, $utf8)

        $writer.Write([uint32]2500072158)
        $writer.Write([uint32]0)
        $writer.Write([uint32]$count)
        $writer.Write([uint32]$origTableOffset)
        $writer.Write([uint32]$transTableOffset)
        $writer.Write([uint32]0)
        $writer.Write([uint32]0)

        for ($index = 0; $index -lt $count; $index++) {
            $writer.Write([uint32]$idByteArrays[$index].Length)
            $writer.Write([uint32]$origOffsets[$index])
        }

        for ($index = 0; $index -lt $count; $index++) {
            $writer.Write([uint32]$strByteArrays[$index].Length)
            $writer.Write([uint32]$transOffsets[$index])
        }

        foreach ($bytes in $idByteArrays) {
            $writer.Write($bytes)
            $writer.Write([byte]0)
        }

        foreach ($bytes in $strByteArrays) {
            $writer.Write($bytes)
            $writer.Write([byte]0)
        }

        $writer.Flush()
    }
    finally {
        $stream.Dispose()
    }
}

$poFiles = Get-ChildItem -LiteralPath $LocaleRoot -Recurse -Filter *.po
foreach ($poFile in $poFiles) {
    $entries = Read-PoEntries -Path $poFile.FullName
    $moPath = [System.IO.Path]::ChangeExtension($poFile.FullName, ".mo")
    Write-MoFile -Entries $entries -OutputPath $moPath
    Write-Host "Compiled $($poFile.FullName) -> $moPath"
}
