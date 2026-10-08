Set-Location $PSScriptRoot
python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Package installation failed." -ForegroundColor Red
    Read-Host "Press Enter to close"
    exit 1
}
python app.py
Read-Host "Press Enter to close"
