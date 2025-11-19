---
name: terraform-iac
description: Automate infrastructure with Terraform HCL, modules, state management, workspaces, and AWS provider.
---

# Terraform Infrastructure as Code

Terraform enables declarative infrastructure automation through HCL (HashiCorp Configuration Language). Master configuration syntax, modular design, state management, workspaces, and provider configuration for reproducible infrastructure across cloud platforms.

## Quick Start

**Basic Terraform configuration:**

```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  tags = {
    Name = "web-server"
  }
}

output "instance_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IP of web server"
}
```

**Initialize and apply:**

```bash
terraform init
terraform plan
terraform apply
terraform destroy
```

## Key Concepts

### HCL Syntax
Declarative configuration language for defining infrastructure:

```hcl
# Variables
variable "instance_count" {
  type        = number
  default     = 3
  description = "Number of instances"
}

variable "tags" {
  type = map(string)
  default = {
    Environment = "production"
    Owner       = "devops"
  }
}

# Resources
resource "aws_security_group" "app" {
  name        = "app-sg"
  description = "Application security group"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Data sources (reference existing resources)
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# Outputs
output "security_group_id" {
  value = aws_security_group.app.id
}
```

### Modules
Reusable configuration components:

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true

  tags = {
    Name = var.name
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidr
  availability_zone = var.availability_zone

  tags = {
    Name = "${var.name}-public"
  }
}

# modules/vpc/variables.tf
variable "name" {
  type = string
}

variable "cidr_block" {
  type = string
}

variable "public_subnet_cidr" {
  type = string
}

variable "availability_zone" {
  type = string
}

# modules/vpc/outputs.tf
output "vpc_id" {
  value = aws_vpc.main.id
}

output "subnet_id" {
  value = aws_subnet.public.id
}

# root main.tf
module "vpc" {
  source = "./modules/vpc"

  name                = "app-vpc"
  cidr_block          = "10.0.0.0/16"
  public_subnet_cidr  = "10.0.1.0/24"
  availability_zone   = "us-east-1a"
}
```

### State Management
Terraform stores infrastructure state in terraform.tfstate:

```hcl
# Local state (development)
# terraform.tfstate is created locally

# Remote state (production)
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Workspaces
Manage multiple environments from one configuration:

```bash
terraform workspace new production
terraform workspace select production
terraform apply
terraform workspace select default
```

```hcl
# Use workspace in configuration
locals {
  environment = terraform.workspace
  instance_type = terraform.workspace == "production" ? "t3.large" : "t3.micro"
}

resource "aws_instance" "app" {
  instance_type = local.instance_type

  tags = {
    Environment = local.environment
  }
}
```

## Common Patterns

**AWS VPC with private database:**

```hcl
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
}

resource "aws_security_group" "db" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
}

resource "aws_db_instance" "main" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15.1"
  instance_class       = "db.t3.micro"
  identifier           = "mydb"
  username             = "admin"
  password             = random_password.db.result
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]
  skip_final_snapshot  = false
  final_snapshot_identifier = "mydb-final-snapshot"
}
```

**DRY configuration with locals:**

```hcl
locals {
  common_tags = {
    Project     = "webapp"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  instance_count = {
    dev  = 1
    prod = 3
  }
}

resource "aws_instance" "app" {
  count         = local.instance_count[var.environment]
  instance_type = "t3.micro"

  tags = merge(
    local.common_tags,
    {
      Name = "app-${count.index + 1}"
    }
  )
}
```

**For loops and conditional logic:**

```hcl
variable "subnets" {
  type = list(object({
    name              = string
    cidr_block        = string
    availability_zone = string
  }))
}

resource "aws_subnet" "main" {
  for_each          = { for s in var.subnets : s.name => s }
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr_block
  availability_zone = each.value.availability_zone

  tags = {
    Name = each.key
  }
}

output "subnet_ids" {
  value = { for name, subnet in aws_subnet.main : name => subnet.id }
}
```

## Best Practices

✅ Use version constraints for providers
✅ Store state remotely with encryption and locking
✅ Use modules to organize code
✅ Separate variables, locals, and outputs
✅ Use workspaces for environment separation
✅ Validate with `terraform validate` and `terraform fmt`
✅ Use `terraform plan` before applying
✅ Implement CICD for infrastructure changes
✅ Encrypt sensitive values in state
✅ Use consistent naming conventions
✅ Document modules with README.md
✅ Version control all Terraform code

## Common Pitfalls

❌ Storing terraform.tfstate in version control
❌ Using hardcoded values instead of variables
❌ Not using remote state backend
❌ Applying directly to production without review
❌ Mixing manual changes with IaC (state drift)
❌ Not backing up state files
❌ Ignoring state locking (concurrent applies)
❌ Using latest provider versions without constraints
❌ Storing secrets in code or state

## Resources

- [Terraform Official Documentation](https://www.terraform.io/docs)
- [Terraform Best Practices](https://www.terraform.io/docs/language)
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Learning Path](https://learn.hashicorp.com/collections/terraform/aws-get-started)
- [Module Registry](https://registry.terraform.io/browse/modules)
