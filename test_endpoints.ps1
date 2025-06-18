# PowerShell script to test Foodgram API endpoints

# User credentials
$email = "test@example.com"
$password = "testpass123"

# Get JWT token
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/token/login/" -Method Post -ContentType "application/json" -Body (@{email=$email; password=$password} | ConvertTo-Json) -ErrorAction SilentlyContinue

if ($null -eq $response.auth_token) {
    Write-Host "Не удалось получить токен. Проверьте email и пароль."
    exit 1
}

$token = $response.auth_token
$headers = @{ Authorization = "Token $token" }

function Test-Endpoint {
    param(
        [string]$Method,
        [string]$Url,
        [string]$Body = $null
    )
    try {
        if ($Method -eq "GET") {
            $result = Invoke-WebRequest -Uri $Url -Headers $headers -Method Get -UseBasicParsing -ErrorAction Stop
        } elseif ($Method -eq "POST") {
            $result = Invoke-WebRequest -Uri $Url -Headers $headers -Method Post -Body $Body -ContentType "application/json" -UseBasicParsing -ErrorAction Stop
        } elseif ($Method -eq "DELETE") {
            $result = Invoke-WebRequest -Uri $Url -Headers $headers -Method Delete -UseBasicParsing -ErrorAction Stop
        }
        Write-Host "$Method $Url -> $($result.StatusCode)"
    } catch {
        if ($_.Exception.Response) {
            $code = $_.Exception.Response.StatusCode.value__
            Write-Host "$Method $Url -> $code (error)"
        } else {
            Write-Host "$Method $Url -> ERROR: $($_.Exception.Message)"
        }
    }
}

# Test all endpoints
Test-Endpoint GET    "http://localhost:8000/api/users/"
Test-Endpoint POST   "http://localhost:8000/api/auth/jwt/create/" (@{email=$email; password=$password} | ConvertTo-Json)
Test-Endpoint GET    "http://localhost:8000/api/users/"
Test-Endpoint GET    "http://localhost:8000/api/users/me/"
Test-Endpoint GET    "http://localhost:8000/api/users/1/"
Test-Endpoint POST   "http://localhost:8000/api/users/2/subscribe/"
Test-Endpoint DELETE "http://localhost:8000/api/users/2/subscribe/"
Test-Endpoint GET    "http://localhost:8000/api/users/subscriptions/"
Test-Endpoint GET    "http://localhost:8000/api/tags/"
Test-Endpoint GET    "http://localhost:8000/api/ingredients/"
Test-Endpoint GET    "http://localhost:8000/api/ingredients/1"
Test-Endpoint GET    "http://localhost:8000/api/recipes/"
Test-Endpoint GET    "http://localhost:8000/api/recipes/1/"
Test-Endpoint GET    "http://localhost:8000/api/recipes/2/"
Test-Endpoint DELETE "http://localhost:8000/api/recipes/1/"
Test-Endpoint POST   "http://localhost:8000/api/recipes/2/favorite/"
Test-Endpoint DELETE "http://localhost:8000/api/recipes/1/favorite/"
Test-Endpoint POST   "http://localhost:8000/api/recipes/2/shopping_cart/"
Test-Endpoint DELETE "http://localhost:8000/api/recipes/1/shopping_cart/"
Test-Endpoint GET    "http://localhost:8000/api/recipes/download_shopping_cart/" 