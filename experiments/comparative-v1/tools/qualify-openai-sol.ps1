param(
    [string]$Model = "gpt-5.6-sol",
    [ValidateSet("none","low","medium","high","xhigh","max")]
    [string]$ReasoningEffort = "high",
    [string]$OutputPath = ".\openai-sol-qualification.json"
)

$ErrorActionPreference = "Stop"

$started = [System.Diagnostics.Stopwatch]::StartNew()
$timestamp = [DateTimeOffset]::UtcNow.ToString("o")
$endpoint = "https://api.openai.com/v1/responses"
$probe = "Return exactly: DV_STRONG_PATH_PROBE_OK"

$result = [ordered]@{
    schema_version = "comparative-v1-openai-qualification-v1"
    probe_classification = "QUALIFICATION_PROBE_ONLY"
    not_a_comparative_task_run = $true
    holdout_accessed = $false
    timestamp_utc = $timestamp
    provider = "OpenAI"
    candidate_id = "DV-B4-STRONG-OPENAI-SOL"
    endpoint = $endpoint
    requested_model = $Model
    requested_reasoning_effort = $ReasoningEffort
    prompt_sha256 = $null
    http_status = $null
    status = "INCONCLUSIVE"
    qualification_status = "INCONCLUSIVE"
    response_id = "UNMEASURED"
    observed_model = "UNMEASURED"
    response_status = "UNMEASURED"
    normalized_response = "UNMEASURED"
    exact_match = $false
    service_tier = "UNMEASURED"
    input_tokens = "UNMEASURED"
    cached_input_tokens = "UNMEASURED"
    output_tokens = "UNMEASURED"
    reasoning_tokens = "UNMEASURED"
    total_tokens = "UNMEASURED"
    request_identifier = "UNMEASURED"
    latency_ms = $null
    application_retry_count = 0
    provider_retry_metadata = "UNMEASURED"
    secret_persisted = $false
    blocker = $null
}

try {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($probe)
        $result.prompt_sha256 = ([System.BitConverter]::ToString($sha.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }

    if ([string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) {
        $result.status = "BLOCKED"
        $result.qualification_status = "S0_CREDENTIAL_BLOCKED"
        $result.blocker = "OPENAI_API_KEY missing"
        return
    }

    $body = @{
        model = $Model
        input = $probe
        reasoning = @{ effort = $ReasoningEffort }
        max_output_tokens = 64
        service_tier = "default"
    } | ConvertTo-Json -Depth 10 -Compress

    $headers = @{
        Authorization = "Bearer $($env:OPENAI_API_KEY)"
        "Content-Type" = "application/json"
    }

    try {
        $response = Invoke-WebRequest -Method Post -Uri $endpoint -Headers $headers -Body $body -TimeoutSec 60 -SkipHttpErrorCheck
    }
    catch {
        $result.status = "BLOCKED"
        $result.qualification_status = "S0_TRANSPORT_BLOCKED"
        $result.blocker = "TRANSPORT_FAILURE: $($_.Exception.GetType().Name): $($_.Exception.Message)"
        return
    }

    $result.http_status = [int]$response.StatusCode
    foreach ($headerName in @("x-request-id", "request-id")) {
        $value = $response.Headers[$headerName]
        if ($value) {
            $result.request_identifier = [string]$value
            break
        }
    }

    $raw = [string]$response.Content
    try {
        $decoded = $raw | ConvertFrom-Json -Depth 100
    }
    catch {
        $result.status = "FAIL"
        $result.qualification_status = "S0_FAIL"
        $result.blocker = "INVALID_JSON_RESPONSE"
        return
    }

    if ($result.http_status -lt 200 -or $result.http_status -ge 300) {
        $result.status = "BLOCKED"
        $result.qualification_status = if ($result.http_status -in @(401,403,429)) { "S0_CREDENTIAL_OR_QUOTA_BLOCKED" } else { "S0_PROVIDER_BLOCKED" }
        if ($decoded.error) {
            $etype = if ($decoded.error.type) { [string]$decoded.error.type } else { "unknown" }
            $ecode = if ($decoded.error.code) { [string]$decoded.error.code } else { "unknown" }
            $result.blocker = "HTTP_$($result.http_status):${etype}:${ecode}"
        }
        else {
            $result.blocker = "HTTP_$($result.http_status)"
        }
        return
    }

    if ($decoded.id) { $result.response_id = [string]$decoded.id }
    if ($decoded.model) { $result.observed_model = [string]$decoded.model }
    if ($decoded.status) { $result.response_status = [string]$decoded.status }
    if ($decoded.service_tier) { $result.service_tier = [string]$decoded.service_tier }

    $textParts = @()
    foreach ($item in @($decoded.output)) {
        foreach ($content in @($item.content)) {
            if ($content.type -eq "output_text" -and $null -ne $content.text) {
                $textParts += [string]$content.text
            }
        }
    }
    $normalized = ($textParts -join "").Trim()
    $result.normalized_response = $normalized
    $result.exact_match = ($normalized -eq "DV_STRONG_PATH_PROBE_OK")

    if ($decoded.usage) {
        if ($null -ne $decoded.usage.input_tokens) { $result.input_tokens = [int64]$decoded.usage.input_tokens }
        if ($null -ne $decoded.usage.output_tokens) { $result.output_tokens = [int64]$decoded.usage.output_tokens }
        if ($null -ne $decoded.usage.total_tokens) { $result.total_tokens = [int64]$decoded.usage.total_tokens }
        if ($decoded.usage.input_tokens_details -and $null -ne $decoded.usage.input_tokens_details.cached_tokens) {
            $result.cached_input_tokens = [int64]$decoded.usage.input_tokens_details.cached_tokens
        }
        if ($decoded.usage.output_tokens_details -and $null -ne $decoded.usage.output_tokens_details.reasoning_tokens) {
            $result.reasoning_tokens = [int64]$decoded.usage.output_tokens_details.reasoning_tokens
        }
    }

    $identityOk = ($result.observed_model -eq $Model)
    $usageOk = ($result.input_tokens -is [System.ValueType]) -and ($result.output_tokens -is [System.ValueType]) -and ($result.total_tokens -is [System.ValueType])
    $responseOk = ($result.response_status -eq "completed") -and $result.exact_match

    if ($identityOk -and $usageOk -and $responseOk) {
        $result.status = "PASS"
        $result.qualification_status = "S0_READY"
    }
    elseif ($identityOk -and $responseOk) {
        $result.status = "PASS"
        $result.qualification_status = "S0_READY_TELEMETRY_LIMITED"
        $result.blocker = "USAGE_TELEMETRY_INCOMPLETE"
    }
    else {
        $result.status = "FAIL"
        $result.qualification_status = "S0_FAIL"
        $result.blocker = "IDENTITY_OR_RESPONSE_CONTRACT_FAILED"
    }
}
finally {
    $started.Stop()
    $result.latency_ms = [math]::Round($started.Elapsed.TotalMilliseconds, 3)
    $json = $result | ConvertTo-Json -Depth 20
    $json | Set-Content -LiteralPath $OutputPath -Encoding utf8
    $json
}
