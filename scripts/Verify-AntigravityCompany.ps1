param(
    [ValidateSet("Global","Workspace")]
    [string]$Scope = "Global",
    [string]$WorkspacePath = ""
)
$ErrorActionPreference = "Stop"
if ($Scope -eq "Workspace") {
    if ([string]::IsNullOrWhiteSpace($WorkspacePath)) { throw "WorkspacePath is required for Workspace scope." }
    $Base = (Resolve-Path -LiteralPath $WorkspacePath).Path
    $Root = Join-Path $Base ".agents"
} else {
    $Root = Join-Path $HOME ".gemini\config"
}
$Skill = Join-Path $Root "skills\ai-software-company\SKILL.md"
$SkillWorkflows = Join-Path $Root "skills\ai-software-company\workflows"
$SkillTemplates = Join-Path $Root "skills\ai-software-company\templates"
$Agents = Join-Path $Root "agents"
$Rules = Join-Path $Root "rules"

if (-not (Test-Path $Skill)) { throw "Master skill missing: $Skill" }
if (-not (Test-Path $SkillWorkflows)) { Write-Warning "Workflows missing in skill directory: $SkillWorkflows" }
if (-not (Test-Path $SkillTemplates)) { Write-Warning "Templates missing in skill directory: $SkillTemplates" }

$agentFiles = @(Get-ChildItem -LiteralPath $Agents -Filter "*.md" -File -ErrorAction SilentlyContinue)
$ruleFiles = @(Get-ChildItem -LiteralPath $Rules -Filter "*.md" -File -ErrorAction SilentlyContinue)
$expected = 31
if ($agentFiles.Count -ne $expected) {
    Write-Warning "Expected $expected agent files in this package; found $($agentFiles.Count) in target. Existing custom agents may be present."
}
$names = @()
$errors = 0
foreach ($f in $agentFiles) {
    $text = Get-Content -LiteralPath $f.FullName -Raw
    if ($text -notmatch '(?ms)\A---\s*\r?\n.+?\r?\n---\s*(\r?\n|\Z)') {
        Write-Warning "Unclosed or malformed YAML frontmatter delimiter: $($f.Name)"
        $errors++
    }
    if ($text -notmatch '(?m)^name:\s*[a-z0-9-]+') {
        Write-Warning "Missing or invalid agent name: $($f.Name)"
        $errors++
    }
    $names += $f.BaseName
}

if ($errors -eq 0) {
    Write-Host "Frontmatter check: All $($agentFiles.Count) agent files passed strict YAML frontmatter validation." -ForegroundColor Green
} else {
    Write-Error "Frontmatter check failed with $errors issues."
}

Write-Host "Master skill: OK"
Write-Host "Agent markdown files found: $($agentFiles.Count)"
Write-Host "Rule markdown files found: $($ruleFiles.Count)"
Write-Host "Agent files:"
$names | Sort-Object | ForEach-Object { Write-Host " - $_" }
Write-Host "Verification completed. Confirm loaded entries in Antigravity Customizations or /agents and /skills." -ForegroundColor Green
