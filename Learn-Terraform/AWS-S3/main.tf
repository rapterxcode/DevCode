terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
    region = var.aws_region
    profile = "default"
}

#S3 Bucket
resource "aws_s3_bucket" "b" {
    bucket = var.bucket_name
    tags = {
        Name = var.bucket_name
        Environment = "Dev"
    }
}

#S3 Bucket Policy