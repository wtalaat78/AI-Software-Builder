param(
    [ValidateSet("Global","Workspace")]
    [string]$Scope = "Global",
    [string]$WorkspacePath = ""
)
$ErrorActionPreference = "Stop"
$PackageRoot = Split-Path -Parent $PSScriptRoot
if ($Scope -eq "Workspace") {
    if ([string]::IsNullOrWhiteSpace($WorkspacePath)) { throw "WorkspacePath is required for Workspace scope." }
    $Base = (Resolve-Path -LiteralPath $WorkspacePath).Path
    $AgentsRoot = Join-Path $Base ".agents"
} else {
    $Base = Join-Path $HOME ".gemini\config"
    $AgentsRoot = $Base
}
$SkillSource = Join-Path $PackageRoot "skill\ai-software-company"
$AgentSource = Join-Path $PackageRoot "agents"
$RuleSource = Join-Path $PackageRoot "rules"
$SkillTarget = Join-Path $AgentsRoot "skills\ai-software-company"
$AgentTarget = Join-Path $AgentsRoot "agents"
$RuleTarget = Join-Path $AgentsRoot "rules"
$BackupRoot = Join-Path $PackageRoot ("backups\" + (Get-Date -Format "yyyyMMdd-HHmmss"))
New-Item -ItemType Directory -Force -Path $SkillTarget,$AgentTarget,$RuleTarget | Out-Null

function Copy-WithBackup([string]$Source,[string]$Target) {
    if (Test-Path -LiteralPath $Target) {
        $relative = $Target.Replace($AgentsRoot, "").TrimStart("\")
        $backup = Join-Path $BackupRoot $relative
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $backup) | Out-Null
        Copy-Item -LiteralPath $Target -Destination $backup -Force
    }
    Copy-Item -LiteralPath $Source -Destination $Target -Force
}
# Skill directory files (preserve references and nested assets)
Get-ChildItem -LiteralPath $SkillSource -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($SkillSource.Length).TrimStart("\")
    $target = Join-Path $SkillTarget $rel
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
    Copy-WithBackup $_.FullName $target
}
# Agents and rules are flat because Antigravity scans these folders one level deep.
Get-ChildItem -LiteralPath $AgentSource -File -Filter "*.md" | ForEach-Object {
    Copy-WithBackup $_.FullName (Join-Path $AgentTarget $_.Name)
}
Get-ChildItem -LiteralPath $RuleSource -File -Filter "*.md" | ForEach-Object {
    Copy-WithBackup $_.FullName (Join-Path $RuleTarget $_.Name)
}
Write-Host "Installed AI Software Company customization files." -ForegroundColor Green
Write-Host "Scope: $Scope"
Write-Host "Customization root: $AgentsRoot"
Write-Host "Skill: $SkillTarget"
Write-Host "Agents: $AgentTarget"
Write-Host "Rules: $RuleTarget"
if (Test-Path $BackupRoot) { Write-Host "Backups: $BackupRoot" }
Write-Host "Next: run Verify-AntigravityCompany.ps1 with the same scope."
