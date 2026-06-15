$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
Set-Location $PSScriptRoot
$python = ".\venv\Scripts\python.exe"

function Run-Step($name, $script) {
    Write-Output ("=" * 60)
    Write-Output "STEP: $name  ($(Get-Date -Format 'HH:mm:ss'))"
    Write-Output ("=" * 60)
    & $python $script
    if ($LASTEXITCODE -ne 0) {
        Write-Output "PIPELINE FAILED at step: $name (exit $LASTEXITCODE)"
        exit 1
    }
}

Run-Step "Train LoRA v2"   "scripts/03_train_lora.py"
Run-Step "Merge model"     "scripts/04_merge_model.py"
Run-Step "Run evals (30q)" "scripts/13_run_evals.py"
Run-Step "Score evals"     "scripts/14_score_evals_v3.py"

Write-Output "PIPELINE COMPLETE ($(Get-Date -Format 'HH:mm:ss'))"
