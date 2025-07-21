# Istio Microservices POC

This project demonstrates the implementation of a microservices architecture using ASP.NET Core, Docker, Kubernetes, and Istio. It consists of three microservices: Product, Order, and Customer services.

## Prerequisites

- Docker Desktop with Kubernetes enabled
- Istio installed on the Kubernetes cluster
- PowerShell
- .NET 8.0 SDK

## Project Structure

```
├── src/
│   ├── ProductService/
│   ├── OrderService/
│   └── CustomerService/
├── kubernetes/
│   └── base/
│       ├── product-deployment.yaml
│       ├── order-deployment.yaml
│       ├── customer-deployment.yaml
│       ├── gateway.yaml
│       ├── destination-rules.yaml
│       └── kustomization.yaml
├── deploy.ps1
└── docker-compose.yml
```

## Features

1. **Microservices**
   - Product Service: Manages product catalog
   - Order Service: Handles order processing
   - Customer Service: Manages customer information

2. **Istio Features**
   - Service Mesh
   - Traffic Management
   - Load Balancing
   - Circuit Breaking
   - Health Checks
   - Metrics and Monitoring

3. **Kubernetes Features**
   - Deployments with replicas
   - Services
   - Resource management
   - Health probes

## Getting Started

1. **Install Prerequisites**
   ```powershell
   # Install Istio
   istioctl install --set profile=demo -y
   ```

2. **Deploy the Application**
   ```powershell
   # Run the deployment script
   .\deploy.ps1
   ```

3. **Access the Services**
   - API endpoints:
     * Product Service: `http://<gateway-url>/api/product`
     * Order Service: `http://<gateway-url>/api/order`
     * Customer Service: `http://<gateway-url>/api/customer`
   - Swagger UI endpoints:
     * Product Service: `http://<gateway-url>/swagger`
     * Order Service: `http://<gateway-url>/order`
     * Customer Service: `http://<gateway-url>/customer`

## Service Endpoints

### Product Service
- GET `/api/product` - List all products
- GET `/api/product/{id}` - Get product by ID
- POST `/api/product` - Create new product
- PUT `/api/product/{id}` - Update product
- DELETE `/api/product/{id}` - Delete product

### Order Service
- GET `/api/order` - List all orders
- GET `/api/order/{id}` - Get order by ID
- GET `/api/order/customer/{customerId}` - Get orders by customer
- POST `/api/order` - Create new order
- PUT `/api/order/{id}/status` - Update order status
- DELETE `/api/order/{id}` - Delete order

### Customer Service
- GET `/api/customer` - List all customers
- GET `/api/customer/{id}` - Get customer by ID
- POST `/api/customer` - Create new customer
- PUT `/api/customer/{id}` - Update customer
- DELETE `/api/customer/{id}` - Delete customer

## Configuration Details

### Swagger UI Configuration
Each service exposes its Swagger UI at a specific endpoint:
- Product Service: Uses root path `/swagger`
- Order Service: Uses `/order` path
- Customer Service: Uses `/customer` path

The Swagger JSON is served at:
- Product Service: `/swagger/v1/swagger.json`
- Order Service: `/order/swagger/v1/swagger.json`
- Customer Service: `/customer/swagger/v1/swagger.json`

## Troubleshooting

1. **Swagger UI Not Loading**
   ```bash
   # Check pod status
   kubectl get pods -n istio-demo
   
   # Check pod logs
   kubectl logs <pod-name> -n istio-demo
   
   # Check Istio proxy logs
   kubectl logs <pod-name> -c istio-proxy -n istio-demo
   ```

2. **API Endpoints Not Accessible**
   ```bash
   # Verify Gateway IP
   kubectl get svc istio-ingressgateway -n istio-system
   
   # Check Virtual Service
   kubectl get virtualservice -n istio-demo -o yaml
   
   # Verify service endpoints
   kubectl get endpoints -n istio-demo
   ```

3. **Network Issues**
   ```bash
   # Check service details
   kubectl describe svc <service-name> -n istio-demo
   
   # Verify pod networking
   kubectl describe pod <pod-name> -n istio-demo
   ```

## Monitoring and Observability

1. **Access Kiali Dashboard**
   ```bash
   istioctl dashboard kiali
   ```

2. **Access Grafana Dashboard**
   ```bash
   istioctl dashboard grafana
   ```

3. **Access Jaeger Tracing**
   ```bash
   istioctl dashboard jaeger
   ```

## Clean Up

To remove the application and its resources:

```powershell
kubectl delete namespace istio-demo
```

## Note

This is a POC implementation with in-memory data storage. For production use, consider adding:
- Persistent storage
- Authentication and authorization
- Proper error handling and logging
- Environment-specific configurations
- CI/CD pipelines
