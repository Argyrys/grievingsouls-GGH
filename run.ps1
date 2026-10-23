# Veritas Vision - one-shot launcher
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

# Free port 8000 if a previous run is still holding it
$busy = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($busy) {
    $procId = $busy.OwningProcess | Select-Object -First 1
    Write-Host "Stopping old server (PID $procId) on port 8000..."
    Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 600
}

Write-Host ""
Write-Host "  VERITAS VISION - server starting" -ForegroundColor Cyan
Write-Host "  Dashboard : http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "  Mock pages: http://127.0.0.1:8000/mocks/" -ForegroundColor White
Write-Host "  Extension : load unpacked from .\extension in chrome://extensions" -ForegroundColor White
Write-Host "  Stop      : Ctrl+C in this window" -ForegroundColor White
Write-Host ""

py -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
