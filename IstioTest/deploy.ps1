# Function to check command execution
function Test-CommandExecution {
    param (
        [string]$ErrorMessage
    )
    if (-not $?) {
        Write-Host "Error: $ErrorMessage" -ForegroundColor Red
        exit 1
    }
}

# Function to wait for pods
function Wait-ForPods {
    param (
        [int]$timeoutSeconds = 300
    )
    $startTime = Get-Date
    while ($true) {
        $pods = kubectl get pods -n istio-demo -o jsonpath='{.items[*].status.phase}'
        if (-not $pods) {
            Write-Host "No pods found yet..." -ForegroundColor Yellow
        }
        elseif ($pods -match "Pending|ContainerCreating") {
            Write-Host "Pods still initializing..." -ForegroundColor Yellow
        }
        elseif ($pods -match "Failed|Unknown") {
            Write-Host "Some pods failed to start:" -ForegroundColor Red
            kubectl get pods -n istio-demo
            return $false
        }
        elseif ($pods -match "^(Running\s+)*Running$") {
            Write-Host "All pods are running!" -ForegroundColor Green
            return $true
        }

        $elapsed = (Get-Date) - $startTime
        if ($elapsed.TotalSeconds -gt $timeoutSeconds) {
            Write-Host "Timeout waiting for pods" -ForegroundColor Red
            return $false
        }
        Start-Sleep -Seconds 5
    }
}

try {
    # Check kubectl
    Write-Host "Checking kubectl connection..." -ForegroundColor Green
    kubectl version --client
    Test-CommandExecution "kubectl not found or not configured"

    # Check if Istio is installed
    Write-Host "`nChecking Istio installation..." -ForegroundColor Green
    $istioNamespace = kubectl get namespace istio-system --ignore-not-found
    if (-not $istioNamespace) {
        Write-Host "Installing Istio..." -ForegroundColor Yellow
        istioctl install --set profile=demo -y
        Test-CommandExecution "Failed to install Istio"
        Start-Sleep -Seconds 30
    }

    # Clean up existing deployment
    Write-Host "`nCleaning up existing deployment..." -ForegroundColor Yellow
    kubectl delete namespace istio-demo --ignore-not-found
    Start-Sleep -Seconds 10

    # Create namespace
    Write-Host "`nCreating namespace..." -ForegroundColor Green
    kubectl create namespace istio-demo
    Test-CommandExecution "Failed to create namespace"

    # Enable Istio injection
    Write-Host "Enabling Istio injection..." -ForegroundColor Green
    kubectl label namespace istio-demo istio-injection=enabled --overwrite
    Test-CommandExecution "Failed to enable Istio injection"

    # Build Docker images
    Write-Host "`nBuilding Docker images..." -ForegroundColor Green
    docker build -t product-service:latest ./src/ProductService
    Test-CommandExecution "Failed to build product-service image"
    
    docker build -t order-service:latest ./src/OrderService
    Test-CommandExecution "Failed to build order-service image"
    
    docker build -t customer-service:latest ./src/CustomerService
    Test-CommandExecution "Failed to build customer-service image"

    # Apply Kubernetes configurations
    Write-Host "`nApplying Kubernetes configurations..." -ForegroundColor Green
    kubectl apply -k ./kubernetes/base -n istio-demo
    Test-CommandExecution "Failed to apply Kubernetes configurations"

    # Wait for pods
    Write-Host "`nWaiting for pods to start..." -ForegroundColor Yellow
    $podsReady = Wait-ForPods
    if (-not $podsReady) {
        throw "Failed to start pods"
    }

    # Display deployment status
    Write-Host "`nDeployment Status:" -ForegroundColor Cyan
    Write-Host "----------------------------------------"
    Write-Host "Pods:"
    kubectl get pods -n istio-demo
    Write-Host "`nServices:"
    kubectl get services -n istio-demo
    Write-Host "`nVirtualServices:"
    kubectl get virtualservices -n istio-demo
    Write-Host "----------------------------------------"

    # Get Gateway URL
    Write-Host "`nGetting Gateway URL..." -ForegroundColor Yellow
    $INGRESS_HOST = kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
    if (-not $INGRESS_HOST) {
        Write-Host "Using localhost for Gateway URL" -ForegroundColor Yellow
        $INGRESS_HOST = "localhost"
    }

    $GATEWAY_URL = "${INGRESS_HOST}:80"

    # Display endpoints
    Write-Host "`nEndpoints:" -ForegroundColor Green
    Write-Host "Gateway URL: http://${GATEWAY_URL}"
    Write-Host "`nAPI Endpoints:"
    Write-Host "Products: http://${GATEWAY_URL}/api/product"
    Write-Host "Orders: http://${GATEWAY_URL}/api/order"
    Write-Host "Customers: http://${GATEWAY_URL}/api/customer"
    
    Write-Host "`nSwagger UI:"
    Write-Host "Products: http://${GATEWAY_URL}/swagger"
    Write-Host "Orders: http://${GATEWAY_URL}/order"
    Write-Host "Customers: http://${GATEWAY_URL}/customer"

    # Display troubleshooting commands
    Write-Host "`nTroubleshooting Commands:" -ForegroundColor Magenta
    Write-Host "View pod logs: kubectl logs <pod-name> -n istio-demo"
    Write-Host "Check pod details: kubectl describe pod <pod-name> -n istio-demo"
    Write-Host "View Istio proxy logs: kubectl logs <pod-name> -c istio-proxy -n istio-demo"
    Write-Host "List all resources: kubectl get all -n istio-demo"
    Write-Host "Access Kiali: istioctl dashboard kiali"
}
catch {
    Write-Host "`nDeployment failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "`nDiagnostic information:" -ForegroundColor Yellow
    Write-Host "Pods status:"
    kubectl get pods -n istio-demo
    Write-Host "`nEvents:"
    kubectl get events -n istio-demo --sort-by='.lastTimestamp'
    exit 1
}
