# AWS EC2 Infrastructure with Terraform

This project deploys a complete AWS infrastructure including VPC, subnets, security groups, and an EC2 instance running Nginx using Terraform.

## Architecture

The infrastructure includes:
- **VPC** with DNS support
- **Internet Gateway** for public access
- **Public Subnet** with auto-assign public IP
- **Route Table** with internet access
- **Security Group** allowing SSH (22), HTTP (80), and HTTPS (443)
- **EC2 Instance** running Ubuntu 22.04 LTS with Nginx

## Prerequisites

1. **AWS CLI** configured with appropriate credentials
2. **Terraform** installed (version >= 1.0)
3. **AWS EC2 Key Pair** created in your target region

## Configuration

### Variables

Edit `terraform.tfvars` or modify `variables.tf` defaults:

| Variable | Description | Default |
|----------|-------------|---------|
| `aws_region` | AWS region | `ap-southeast-1` |
| `project_name` | Project name for resource naming | `my-web-app` |
| `vpc_cidr` | CIDR block for VPC | `10.0.0.0/16` |
| `public_subnet_cidr` | CIDR block for public subnet | `10.0.1.0/24` |
| `availability_zone` | Availability zone | `ap-southeast-1a` |
| `instance_type` | EC2 instance type | `t2.micro` |
| `ami_id` | Ubuntu Server AMI ID | `ami-0b8607d2721c94a77` |
| `key_pair_name` | EC2 Key Pair name | `phonerapterx` |

### Key Pair Setup

Ensure you have an EC2 Key Pair named `phonerapterx` (or update the variable) in your AWS region:

```bash
aws ec2 create-key-pair --key-name phonerapterx --query 'KeyMaterial' --output text > phonerapterx.pem
chmod 400 phonerapterx.pem
```

## Usage

### Deploy Infrastructure

1. **Initialize Terraform**
   ```bash
   terraform init
   ```

2. **Plan deployment**
   ```bash
   terraform plan
   ```

3. **Apply configuration**
   ```bash
   terraform apply
   ```

### Access the Web Server

After deployment, access your Nginx server using the output URL:
```bash
terraform output website_url
```

### SSH Access

Connect to your EC2 instance:
```bash
ssh -i phonerapterx.pem ubuntu@$(terraform output -raw instance_public_ip)
```

### Destroy Infrastructure

To clean up all resources:
```bash
terraform destroy
```

## Outputs

| Output | Description |
|--------|-------------|
| `vpc_id` | VPC ID |
| `public_subnet_id` | Public subnet ID |
| `internet_gateway_id` | Internet Gateway ID |
| `security_group_id` | Security Group ID |
| `instance_id` | EC2 instance ID |
| `ami_id` | AMI ID used |
| `instance_public_ip` | Public IP address |
| `instance_public_dns` | Public DNS name |
| `website_url` | Direct URL to website |

## Security Considerations

- Security group allows SSH access from anywhere (0.0.0.0/0)
- Consider restricting SSH access to your IP range
- Update the AMI ID if using different regions
- Regularly update the Ubuntu instance

## Files Structure

```
.
├── main.tf              # Main Terraform configuration
├── variables.tf         # Variable definitions
├── outputs.tf          # Output definitions
├── terraform.tfvars    # Variable values (optional)
├── install_nginx.sh    # Nginx installation script
└── README.md          # This file
```

## Troubleshooting

1. **Key Pair Not Found**: Ensure the key pair exists in the specified region
2. **AMI Not Available**: Update the AMI ID for your target region
3. **Access Denied**: Check AWS credentials and permissions
4. **Instance Not Accessible**: Verify security group rules and route table configuration

## Cost Optimization

- Uses t2.micro instance (eligible for AWS Free Tier)
- Terminate resources when not needed to avoid charges
- Monitor AWS billing dashboard regularly