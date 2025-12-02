# =============================
# pull_ollama_models.ps1
# Pull multiple Ollama models automatically
# =============================

# List of Ollama models to pull
$modelList = @(
    "deepseek-coder:6.7b",
    "qwen2-coder:7b",
    "codegemma:7b",
    "codellama:7b",
    "codellama:13b"
)

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
