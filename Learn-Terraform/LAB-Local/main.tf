terraform {
  required_version = ">= 1.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

provider "local" {
}

resource "local_file" "test-local" {
    content  = var.content
    filename = "${path.module}/${var.filename}"
  
}