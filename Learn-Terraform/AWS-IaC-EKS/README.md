# 🚀 AWS EKS Infrastructure with Terraform

This project provisions an Amazon Elastic Kubernetes Service (EKS) cluster with managed node groups using Terraform Infrastructure as Code (IaC).

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Accessing the Cluster](#-accessing-the-cluster)
- [Cleanup](#-cleanup)
- [Troubleshooting](#-troubleshooting)

## 🏗️ Architecture Overview

The infrastructure includes:

- **EKS Cluster**: Managed Kubernetes control plane
- **Node Group**: Single worker node (min: 1, max: 1, desired: 1)
- **VPC**: Custom VPC with public subnets across 2 AZs
- **IAM Roles**: Proper permissions for EKS cluster and worker nodes
- **Security**: SSH access to worker nodes via key pair

```
┌─────────────────────────────────────────────────────────┐
│                    AWS Region                           │
│  ┌─────────────────────────────────────────────────────┐│
│  │                   VPC (10.0.0.0/16)                ││
│  │  ┌─────────────────────┐  ┌─────────────────────┐   ││
│  │  │  Public Subnet 1    │  │  Public Subnet 2    │   ││
│  │  │   (10.0.1.0/24)     │  │   (10.0.2.0/24)     │   ││
│  │  │                     │  │                     │   ││
│  │  │  ┌─────────────────┐│  │                     │   ││
│  │  │  │  EKS Worker     ││  │                     │   ││
│  │  │  │  Nodes          ││  │                     │   ││
│  │  │  └─────────────────┘│  │                     │   ││
│  │  └─────────────────────┘  └─────────────────────┘   ││
│  └─────────────────────────────────────────────────────┘│
│                                                         │
│  ┌─────────────────────────────────────────────────────┐│
│  │              EKS Control Plane                      ││
│  │            (Managed by AWS)                         ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

## 📦 Prerequisites

- **AWS CLI** configured with appropriate credentials
- **Terraform** >= 1.0
- **kubectl** for cluster management
- **AWS Key Pair** for SSH access to worker nodes

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AWS-IaC-EKS
   ```

2. **Initialize Terraform**
   ```bash
   terraform init
   ```

3. **Review the plan**
   ```bash
   terraform plan
   ```

4. **Deploy the infrastructure**
   ```bash
   terraform apply
   ```

5. **Configure kubectl**
   ```bash
   aws eks update-kubeconfig --region ap-southeast-1 --name my-eks-cluster
   ```

## ⚙️ Configuration

### Variables

Modify `variables.tf` or create a `terraform.tfvars` file:

```hcl
# terraform.tfvars
aws_region = "ap-southeast-1"
project_name = "my-eks-cluster"
cluster_name = "my-eks-cluster"
kubernetes_version = "1.27"
node_instance_type = "t3.medium"
key_pair_name = "your-key-pair-name"
```

### Key Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `aws_region` | AWS region for deployment | `ap-southeast-1` |
| `project_name` | Project name for resource naming | `my-eks-cluster` |
| `cluster_name` | EKS cluster name | `my-eks-cluster` |
| `kubernetes_version` | Kubernetes version | `1.27` |
| `node_instance_type` | Worker node instance type | `t3.medium` |
| `key_pair_name` | EC2 key pair for SSH access | `phonerapterx` |

## 🚀 Deployment

### Step-by-Step Deployment

1. **Validate configuration**
   ```bash
   terraform validate
   ```

2. **Plan the deployment**
   ```bash
   terraform plan -out=tfplan
   ```

3. **Apply the configuration**
   ```bash
   terraform apply tfplan
   ```

4. **Verify deployment**
   ```bash
   # Check cluster status
   aws eks describe-cluster --name my-eks-cluster --region ap-southeast-1
   
   # Check node group status
   aws eks describe-nodegroup --cluster-name my-eks-cluster --nodegroup-name my-eks-cluster-node-group --region ap-southeast-1
   ```

## 🔧 Accessing the Cluster

### Configure kubectl

```bash
# Update kubeconfig
aws eks update-kubeconfig --region ap-southeast-1 --name my-eks-cluster

# Verify connection
kubectl get nodes
kubectl get pods -A
```

### SSH to Worker Nodes

```bash
# Get worker node public IP
kubectl get nodes -o wide

# SSH to worker node
ssh -i ~/.ssh/your-key-pair.pem ec2-user@<node-public-ip>
```

## 📊 Outputs

After successful deployment, you'll get:

- `cluster_endpoint`: EKS cluster API endpoint
- `cluster_name`: EKS cluster name
- `cluster_certificate_authority_data`: Certificate for cluster authentication
- `node_group_arn`: ARN of the EKS node group
- `node_group_status`: Status of the node group

## 🧹 Cleanup

To destroy the infrastructure:

```bash
terraform destroy
```

**⚠️ Warning**: This will permanently delete all resources created by this Terraform configuration.

## 🔍 Troubleshooting

### Common Issues

1. **Insufficient permissions**
   - Ensure your AWS credentials have EKS, EC2, and IAM permissions
   - Check AWS CLI configuration: `aws configure list`

2. **Node group fails to create**
   - Verify the key pair exists in the specified region
   - Check subnet availability zones

3. **kubectl connection issues**
   - Update kubeconfig: `aws eks update-kubeconfig --region <region> --name <cluster-name>`
   - Verify AWS CLI credentials

### Useful Commands

```bash
# Check EKS cluster status
aws eks describe-cluster --name my-eks-cluster

# List node groups
aws eks list-nodegroups --cluster-name my-eks-cluster

# Check Terraform state
terraform show

# Debug kubectl configuration
kubectl config view
```

## 📝 Notes

- **Node Group Scaling**: Currently configured for exactly 1 node (min=1, max=1)
- **Instance Type**: Default is `t3.medium` - suitable for development/testing
- **Network**: Uses public subnets - consider private subnets for production
- **Security**: SSH access enabled via key pair - restrict source IPs in production

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is licensed under the MIT License.