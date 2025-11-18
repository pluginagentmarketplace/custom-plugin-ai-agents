# DevOps Agent Implementation Guide
## Practical Examples for Claude Code Plugin

---

## 1. Linux & Shell Agent

### Agent Purpose
Provide Linux system administration guidance, command generation, and shell script development assistance.

### Core Skills

#### Skill: `linux-system-info`
**Purpose**: Get system information and diagnostics

**Example Prompts**:
- "Check what processes are using the most CPU"
- "Show me disk usage by directory"
- "List all open network connections"

**Generated Commands**:
```bash
# CPU usage
top -bn1 | head -20

# Disk usage by directory
du -sh /* | sort -hr

# Network connections
ss -tulpn

# System information
lsb_release -a
uname -a
```

#### Skill: `shell-script-generator`
**Purpose**: Generate and optimize bash scripts

**Example Input**:
```
Type: System maintenance
Task: Backup directory to S3 daily
Schedule: Every 24 hours
```

**Generated Script**:
```bash
#!/bin/bash
# Backup script for system maintenance
set -euo pipefail

# Configuration
BACKUP_DIR="/home/user/data"
S3_BUCKET="my-backup-bucket"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/var/log/backup_${TIMESTAMP}.log"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

backup_to_s3() {
    log "Starting backup of $BACKUP_DIR"

    # Create tar archive
    tar czf "/tmp/backup_${TIMESTAMP}.tar.gz" "$BACKUP_DIR" || {
        log "ERROR: Failed to create backup archive"
        exit 1
    }

    # Upload to S3
    aws s3 cp "/tmp/backup_${TIMESTAMP}.tar.gz" \
        "s3://${S3_BUCKET}/backups/" || {
        log "ERROR: Failed to upload to S3"
        exit 1
    }

    # Cleanup
    rm -f "/tmp/backup_${TIMESTAMP}.tar.gz"
    log "Backup completed successfully"
}

# Error handling
trap 'log "ERROR: Script failed on line $LINENO"' ERR

backup_to_s3
```

**Cron Job Setup**:
```bash
# Add to crontab
0 2 * * * /opt/scripts/backup.sh
```

#### Skill: `user-permission-manager`
**Purpose**: Manage users, groups, and permissions

**Example Scenarios**:

1. **Create new user with sudo access**:
```bash
# Create user
useradd -m -s /bin/bash devops-user

# Add to sudoers
usermod -aG sudo devops-user

# Set password (or use SSH key)
passwd devops-user

# Setup SSH key
mkdir -p /home/devops-user/.ssh
chmod 700 /home/devops-user/.ssh
# Add public key to authorized_keys
chmod 600 /home/devops-user/.ssh/authorized_keys
chown -R devops-user:devops-user /home/devops-user/.ssh
```

2. **Setup file permissions for application**:
```bash
# Create app user
useradd -r -s /bin/false appuser

# Create app directory
mkdir -p /opt/myapp
chown appuser:appuser /opt/myapp
chmod 755 /opt/myapp

# Restrict to app user
chmod 750 /opt/myapp/config
chmod 640 /opt/myapp/config/secrets.env
```

---

## 2. Docker Agent

### Agent Purpose
Guide Docker containerization, image optimization, and best practices.

### Core Skills

#### Skill: `dockerfile-generator`
**Purpose**: Generate optimized Dockerfiles with best practices

**Example Input**:
```
Application: Python FastAPI API
Base OS: Ubuntu 22.04
Dependencies: FastAPI, SQLAlchemy, PostgreSQL
Port: 8000
```

**Generated Dockerfile**:
```dockerfile
# Multi-stage build for optimization
FROM python:3.11-slim as builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage - minimal image
FROM python:3.11-slim

# Set non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Security: run as non-root
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Associated Files**:

`.dockerignore`:
```
.git
.gitignore
__pycache__
*.pyc
*.pyo
*.egg-info
dist
build
.env
.pytest_cache
.vscode
.idea
```

`requirements.txt`:
```
fastapi==0.104.0
uvicorn[standard]==0.24.0
sqlalchemy==2.0.0
psycopg2-binary==2.9.9
```

#### Skill: `docker-compose-generator`
**Purpose**: Generate Docker Compose files for multi-container applications

**Example Input**:
```
Services: Web API (Python), PostgreSQL, Redis, Nginx
Environment: Development with hot-reload
```

**Generated docker-compose.yml**:
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:16-alpine
    container_name: myapp_db
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: ${DB_PASSWORD:-changeMe}
      POSTGRES_DB: appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - myapp_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis Cache
  cache:
    image: redis:7-alpine
    container_name: myapp_cache
    ports:
      - "6379:6379"
    networks:
      - myapp_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # FastAPI Application
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: myapp_api
    environment:
      DATABASE_URL: postgresql://appuser:${DB_PASSWORD:-changeMe}@db:5432/appdb
      REDIS_URL: redis://cache:6379
      LOG_LEVEL: ${LOG_LEVEL:-INFO}
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    ports:
      - "8000:8000"
    volumes:
      - .:/app  # Hot reload for development
    networks:
      - myapp_network
    command: uvicorn main:app --host 0.0.0.0 --reload
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: myapp_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    networks:
      - myapp_network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  myapp_network:
    driver: bridge
```

**.env.example**:
```
# Database
DB_PASSWORD=secure_password_here
DB_USER=appuser

# Application
LOG_LEVEL=INFO
DEBUG=false

# External services
API_KEY=
EXTERNAL_SERVICE_URL=
```

#### Skill: `docker-optimization`
**Purpose**: Analyze and optimize Docker images

**Common Optimization Strategies**:

1. **Multi-stage builds** (reduces size 50-80%)
```dockerfile
FROM node:18 as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
CMD ["node", "dist/index.js"]
```

2. **Use alpine base images** (5-10MB vs 100+MB)
```dockerfile
FROM python:3.11-alpine
```

3. **Minimize layers** (combine commands)
```dockerfile
# Bad (many layers)
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git

# Good (one layer)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*
```

4. **Leverage layer caching**
```dockerfile
# Put frequently changing items last
COPY package.json .
RUN npm ci
COPY . .
RUN npm run build
```

---

## 3. Kubernetes Agent

### Agent Purpose
Guide Kubernetes deployment, configuration, and operations.

### Core Skills

#### Skill: `kubernetes-manifest-generator`
**Purpose**: Generate Kubernetes manifests for deployments

**Example Input**:
```
Application: Multi-tier web app
Services: Frontend (React), Backend (Python API), Database (PostgreSQL)
Replicas: 3
Environment: Production
```

**Generated Manifests**:

`namespace.yaml`:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: myapp-prod
  labels:
    environment: production
    managed-by: terraform
```

`configmap.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: myapp-prod
data:
  LOG_LEVEL: "INFO"
  API_BASE_URL: "https://api.example.com"
  DATABASE_POOL_SIZE: "20"
```

`secret.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: myapp-prod
type: Opaque
data:
  database_url: cG9zdGdyZXM6Ly91c2VyOnBhc3NAZGI6NTQzMi9hcHBkYg==  # base64 encoded
  api_key: YWJjZGVmZ2hpamtsbW5vcA==  # base64 encoded
```

`backend-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
  namespace: myapp-prod
  labels:
    app: backend-api
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: backend-api
  template:
    metadata:
      labels:
        app: backend-api
        version: v1
    spec:
      # Security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

      # Service account for RBAC
      serviceAccountName: backend-api-sa

      # Pod anti-affinity for distribution
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - backend-api
              topologyKey: kubernetes.io/hostname

      containers:
      - name: backend-api
        image: myregistry.azurecr.io/backend-api:1.0.0
        imagePullPolicy: Always

        ports:
        - name: http
          containerPort: 8000
          protocol: TCP

        # Environment variables
        env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: LOG_LEVEL
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database_url
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace

        # Resource requests and limits
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        # Health checks
        livenessProbe:
          httpGet:
            path: /health/live
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2

        # Volume mounts
        volumeMounts:
        - name: app-logs
          mountPath: /var/log/app

      # Volumes
      volumes:
      - name: app-logs
        emptyDir: {}

      # Node selector
      nodeSelector:
        workload: general

      # Tolerations for special nodes
      tolerations:
      - key: workload
        operator: Equal
        value: batch
        effect: NoSchedule

      # Restart policy
      restartPolicy: Always
      terminationGracePeriodSeconds: 30

---
apiVersion: v1
kind: Service
metadata:
  name: backend-api
  namespace: myapp-prod
  labels:
    app: backend-api
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: http
    protocol: TCP
    name: http
  selector:
    app: backend-api
  sessionAffinity: None

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-api-hpa
  namespace: myapp-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: backend-api-sa
  namespace: myapp-prod

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: backend-api-role
  namespace: myapp-prod
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list", "watch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: backend-api-rolebinding
  namespace: myapp-prod
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: backend-api-role
subjects:
- kind: ServiceAccount
  name: backend-api-sa
  namespace: myapp-prod
```

#### Skill: `helm-chart-generator`
**Purpose**: Generate Helm charts for reusable deployments

**Generated Chart Structure**:
```
myapp-chart/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   ├── networkpolicy.yaml
│   ├── _helpers.tpl
│   └── NOTES.txt
└── README.md
```

`Chart.yaml`:
```yaml
apiVersion: v2
name: myapp
description: A Helm chart for MyApp Kubernetes deployment
type: application
version: 1.0.0
appVersion: "1.0.0"
home: https://github.com/myorg/myapp
sources:
  - https://github.com/myorg/myapp
maintainers:
  - name: DevOps Team
    email: devops@example.com
keywords:
  - myapp
  - api
  - backend
```

`values.yaml`:
```yaml
# Default values
replicaCount: 3

image:
  repository: myregistry.azurecr.io/myapp
  pullPolicy: Always
  tag: "1.0.0"

imagePullSecrets: []

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

nodeSelector:
  workload: general

affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: app
                operator: In
                values:
                  - "{{ include \"myapp.name\" . }}"
          topologyKey: kubernetes.io/hostname

tolerations: []

securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
```

#### Skill: `kubernetes-troubleshooting`
**Purpose**: Diagnose and fix Kubernetes issues

**Common Scenarios**:

1. **Pod stuck in pending state**:
```bash
# Check pod status
kubectl describe pod <pod-name> -n <namespace>

# Check node capacity
kubectl top nodes

# Check resource requests
kubectl get pods -o json | jq '.items[].spec.containers[].resources'

# Check for taints/tolerations
kubectl describe node <node-name>
```

2. **Pod crashing/restarting**:
```bash
# Check pod logs
kubectl logs <pod-name> -n <namespace>

# Check previous logs (if restarted)
kubectl logs <pod-name> -n <namespace> --previous

# Check pod events
kubectl describe pod <pod-name> -n <namespace>

# Check resource usage
kubectl top pod <pod-name> -n <namespace>
```

3. **Service not accessible**:
```bash
# Check service
kubectl get svc -n <namespace>

# Check endpoints
kubectl get endpoints <service-name> -n <namespace>

# Check selectors
kubectl get pods -l <selector-key>=<selector-value> -n <namespace>

# Test connectivity
kubectl exec <pod-name> -n <namespace> -- curl http://<service>
```

---

## 4. Terraform Agent

### Agent Purpose
Guide Infrastructure as Code development with Terraform.

### Core Skills

#### Skill: `terraform-aws-generator`
**Purpose**: Generate Terraform configurations for AWS resources

**Example Input**: Create VPC with subnets, security groups, and EC2 instance

**Generated main.tf**:
```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "myorg-terraform-state"
    key            = "prod/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "Terraform"
      CreatedAt   = timestamp()
    }
  }
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Public Subnets
resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet-${count.index + 1}"
    Type = "Public"
  }
}

# Private Subnets
resource "aws_subnet" "private" {
  count              = length(var.private_subnet_cidrs)
  vpc_id             = aws_vpc.main.id
  cidr_block         = var.private_subnet_cidrs[count.index]
  availability_zone  = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "${var.project_name}-private-subnet-${count.index + 1}"
    Type = "Private"
  }
}

# Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
  domain = "vpc"

  tags = {
    Name = "${var.project_name}-nat-eip"
  }

  depends_on = [aws_internet_gateway.main]
}

# NAT Gateway
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "${var.project_name}-nat"
  }

  depends_on = [aws_internet_gateway.main]
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block      = "0.0.0.0/0"
    gateway_id      = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-private-rt"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(aws_subnet.private)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

# Security Group
resource "aws_security_group" "app" {
  name        = "${var.project_name}-app-sg"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidrs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-app-sg"
  }
}

# EC2 Instance
resource "aws_instance" "app" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.app.id]
  key_name               = aws_key_pair.deployer.key_name

  root_block_device {
    volume_size           = var.root_volume_size
    volume_type           = "gp3"
    delete_on_termination = true
    encrypted             = true
  }

  tags = {
    Name = "${var.project_name}-app"
  }
}

# Data source for availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Data source for Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

# Key Pair
resource "aws_key_pair" "deployer" {
  key_name   = "${var.project_name}-deployer"
  public_key = var.deployer_public_key
}
```

**Generated variables.tf**:
```hcl
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "project_name" {
  description = "Project name"
  type        = string
  validation {
    condition     = length(var.project_name) > 0 && length(var.project_name) <= 32
    error_message = "Project name must be between 1 and 32 characters."
  }
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "root_volume_size" {
  description = "Root volume size in GB"
  type        = number
  default     = 20
  validation {
    condition     = var.root_volume_size >= 10 && var.root_volume_size <= 100
    error_message = "Root volume size must be between 10 and 100 GB."
  }
}

variable "deployer_public_key" {
  description = "Public SSH key for deployments"
  type        = string
  sensitive   = true
}

variable "allowed_ssh_cidrs" {
  description = "CIDR blocks allowed for SSH access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
```

**Generated outputs.tf**:
```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "app_security_group_id" {
  description = "App security group ID"
  value       = aws_security_group.app.id
}

output "app_instance_id" {
  description = "App instance ID"
  value       = aws_instance.app.id
}

output "app_instance_public_ip" {
  description = "App instance public IP"
  value       = aws_instance.app.public_ip
}

output "nat_gateway_ip" {
  description = "NAT Gateway Elastic IP"
  value       = aws_eip.nat.public_ip
}
```

#### Skill: `terraform-module-developer`
**Purpose**: Create reusable Terraform modules

**Module Structure**:
```
modules/vpc/
├── main.tf
├── variables.tf
├── outputs.tf
├── locals.tf
└── README.md
```

**Module Pattern - Generic VPC**:
```hcl
# modules/vpc/main.tf
resource "aws_vpc" "this" {
  cidr_block = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.tags,
    {
      Name = "${var.name}-vpc"
    }
  )
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnets)
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.public_subnets[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index % length(data.aws_availability_zones.available.names)]

  tags = merge(
    var.tags,
    {
      Name = "${var.name}-public-${count.index + 1}"
      Type = "Public"
    }
  )
}

# ... additional resources
```

---

## 5. CI/CD Agent

### Agent Purpose
Guide CI/CD pipeline design and implementation.

### Core Skills

#### Skill: `github-actions-generator`
**Purpose**: Generate GitHub Actions workflow files

**Example Input**: Build, test, and deploy Python API to Kubernetes

**Generated .github/workflows/deploy.yml**:
```yaml
name: Build, Test & Deploy

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt

    - name: Run linting
      run: |
        flake8 src/
        black --check src/
        isort --check-only src/

    - name: Run unit tests
      run: |
        pytest --cov=src tests/
        coverage report --fail-under=80

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Log in to Container Registry
      if: github.event_name == 'push'
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha

    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: ${{ github.event_name == 'push' }}
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: read

    steps:
    - uses: actions/checkout@v4

    - name: Set up Kube config
      run: |
        mkdir -p $HOME/.kube
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
        chmod 600 $HOME/.kube/config

    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/api-deployment \
          api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          -n production
        kubectl rollout status deployment/api-deployment -n production

    - name: Verify deployment
      run: |
        sleep 10
        kubectl get pods -n production
        kubectl logs -n production -l app=api --tail=50

    - name: Slack notification
      if: always()
      uses: slackapi/slack-github-action@v1
      with:
        payload: |
          {
            "text": "Deployment ${{ job.status }}",
            "blocks": [
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "*Deployment ${{ job.status }}*\nRef: ${{ github.ref }}\nAuthor: ${{ github.actor }}"
                }
              }
            ]
          }
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 6. AWS Agent

### Agent Purpose
Guide AWS infrastructure setup and management.

### Core Skills

#### Skill: `aws-architecture-designer`
**Purpose**: Design AWS architectures for specific use cases

**Example Scenarios**:

1. **High-Availability Web Application**
```
Requirements:
├── Multiple availability zones
├── Auto-scaling
├── Load balancing
├── Database replication
└── CDN for static content

AWS Architecture:
├── Route53 for DNS
├── CloudFront for CDN
├── ALB across AZs
├── Auto Scaling Group
├── RDS Multi-AZ
├── ElastiCache for caching
├── CloudWatch for monitoring
└── S3 for backups
```

2. **Serverless Microservices**
```
Services:
├── API Gateway
├── Lambda functions
├── DynamoDB for data
├── SNS/SQS for messaging
├── Cognito for auth
├── CloudFormation for IaC
└── X-Ray for tracing

Benefits:
├── No server management
├── Auto-scaling
├── Pay per use
└── High availability built-in
```

---

## 7. Monitoring & Observability Agent

### Agent Purpose
Guide monitoring, logging, and alerting setup.

### Core Skills

#### Skill: `prometheus-grafana-setup`
**Purpose**: Configure Prometheus and Grafana

**Generated prometheus.yml**:
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    monitor: 'myapp-monitor'

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__

  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
```

---

## Implementation Checklist for Plugin Development

### Phase 1: Foundation
- [ ] Linux/Shell Agent implementation
- [ ] Git workflow guidance
- [ ] Basic command generation

### Phase 2: Containerization
- [ ] Docker Dockerfile generator
- [ ] Docker Compose generator
- [ ] Image optimization advisor

### Phase 3: Orchestration
- [ ] Kubernetes manifest generator
- [ ] Helm chart generator
- [ ] Deployment troubleshooting

### Phase 4: Infrastructure as Code
- [ ] Terraform configuration generator
- [ ] Module templates and patterns
- [ ] State management guidance

### Phase 5: Cloud Platform
- [ ] AWS architecture designer
- [ ] Resource provisioning
- [ ] Cost optimization

### Phase 6: CI/CD & Automation
- [ ] GitHub Actions workflow generator
- [ ] Pipeline design patterns
- [ ] Deployment strategies

### Phase 7: Monitoring & Security
- [ ] Monitoring setup (Prometheus/Grafana)
- [ ] Security hardening guides
- [ ] Compliance templates

---

**Document Version**: 1.0
**Last Updated**: 2025-11-18
**For**: Claude Code Plugin DevOps Agent Implementation
