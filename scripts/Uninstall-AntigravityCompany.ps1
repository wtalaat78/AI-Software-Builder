param(
    [ValidateSet("Global","Workspace")]
    [string]$Scope = "Global",
    [string]$WorkspacePath = "",
    [switch]$Confirm
)
$ErrorActionPreference = "Stop"
if (-not $Confirm) { throw "This removes only the named company skill, 32 company agent files, and 4 company rule files. Re-run with -Confirm after reviewing paths." }
if ($Scope -eq "Workspace") {
    if ([string]::IsNullOrWhiteSpace($WorkspacePath)) { throw "WorkspacePath is required for Workspace scope." }
    $Base = (Resolve-Path -LiteralPath $WorkspacePath).Path
    $Root = Join-Path $Base ".agents"
} else { $Root = Join-Path $HOME ".gemini\config" }
$skill = Join-Path $Root "skills\ai-software-company"
$agents = Join-Path $Root "agents"
$rules = Join-Path $Root "rules"
if (Test-Path $skill) { Remove-Item -LiteralPath $skill -Recurse -Force }
$companyAgentNames = @(
"cto-team-leader","business-analyst","product-manager","solution-architect","ui-ux-designer",
"frontend-developer","backend-developer","mobile-developer","database-engineer","qa-testing-engineer",
"devsecops-security-engineer","code-reviewer","technical-writer","desktop-application-developer",
"api-integration-specialist","cybersecurity-specialist","performance-engineer","cloud-infrastructure-engineer",
"ai-ml-engineer","release-manager","social-media-product-marketing","presentation-sales-enablement",
"skills-research-discovery","humanization-editorial","market-research-competitor-intelligence",
"brand-identity-logo-designer","finops-cost-pricing-strategist","software-license-compliance-specialist",
"reverse-engineering-feature-analyst","reverse-engineering-code-specialist","ui-unslop-specialist",
"work-log-archiver"
)
foreach ($n in $companyAgentNames) {
    $p = Join-Path $agents "$n.md"
    if (Test-Path $p) { Remove-Item -LiteralPath $p -Force }
}
$companyRules = @("company-safety.md","engineering-quality.md","project-memory.md","bilingual-product-quality.md")
foreach ($n in $companyRules) {
    $p = Join-Path $rules $n
    if (Test-Path $p) { Remove-Item -LiteralPath $p -Force }
}
Write-Host "Removed the AI Software Company customizations. Other agents/rules were left untouched." -ForegroundColor Yellow
