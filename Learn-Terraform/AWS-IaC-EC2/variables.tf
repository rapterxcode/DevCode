variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "my-web-app"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "Availability zone"
  type        = string
  default     = "ap-southeast-1a"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for Ubuntu Server"
  type        = string
  default     = "ami-0b8607d2721c94a77" # Ubuntu Server 22.04 LTS in ap-southeast-1
}

variable "key_pair_name" {
  description = "Name of the EC2 Key Pair"
  type        = string
  default     = "phonerapterx"
}