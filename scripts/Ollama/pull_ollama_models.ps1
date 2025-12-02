# =============================
# pull_ollama_models.ps1
# Pull multiple Ollama models automatically from LLM_List.conf
# =============================

# Path to model list file
$modelListFile = ".\LLM_List.conf"

# Check if file exists
if (-not (Test-Path $modelListFile)) {
    Write-Host "❌ Model list file not found: $modelListFile" -ForegroundColor Red
    exit 1
}

# Read models from file
$modelList = Get-Content $modelListFile | Where-Object { $_.Trim() -ne "" }

foreach ($model in $modelList) {
    Write-Host "Pulling model: $model ..." -ForegroundColor Cyan
    try {
        & ollama pull $model
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Successfully pulled $model" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to pull $model (exit code $LASTEXITCODE)" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Exception pulling $model: $_" -ForegroundColor Red
    }
}

Write-Host "All models attempted." -ForegroundColor Yellow
