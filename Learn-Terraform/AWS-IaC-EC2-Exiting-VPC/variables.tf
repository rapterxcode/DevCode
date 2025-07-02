variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "my-web-app-2025"
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
  default     = "vpc-09c31502cfa78bad0" #ph-vpc
}

variable "ami_id" {
  description = "AMI ID for Ubuntu Server"
  type        = string
  default     = "ami-0b8607d2721c94a77" # Ubuntu Server 22.04 LTS (HVM),EBS General Purpose (SSD) Volume Type. Support available from Canonical  in ap-southeast-1
 // default     = "ami-0a3ece531caa5d49d" # Amazon Linux 2023 AMI 2023.7.20250623.1 x86_64 HVM kernel-6.1 in ap-southeast-1
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_pair_name" {
  description = "Key pair name"
  type        = string
  default     = "phonerapterx"
}

variable "subnet_id" {
  description = "Subnet ID"
  type        = string
  default     = "subnet-049f8c5ce6d2b4bb7" #ph-subnet-private1-ap-southeast-1a
}



variable "instance_name" {
  description = "Instance name"
  type        = string
  default     = "web-server"
}