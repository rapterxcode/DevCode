output "instance_public_ip" {
  value = aws_instance.web.public_ip
  description = "Public IP of the EC2 instance"
}

output "instance_private_ip" {
  value = aws_instance.web.private_ip
  description = "Private IP of the EC2 instance"
}

output "instance_id" {
  value = aws_instance.web.id
  description = "ID of the EC2 instance"
}

output "instance_public_dns" {
  value = aws_instance.web.public_dns
  description = "Public DNS of the EC2 instance"
}

output "instance_private_dns" {
  value = aws_instance.web.private_dns
  description = "Private DNS of the EC2 instance"
}

output "instance_security_group_id" {
  value = aws_security_group.web.id
  description = "Security group ID of the EC2 instance"
}

output "instance_security_group_name" {
  value = aws_security_group.web.name
  description = "Security group name of the EC2 instance"
}

output "instance_security_group_description" {
  value = aws_security_group.web.description
  description = "Security group description of the EC2 instance"
}

output "instance_security_group_vpc_id" {
  value = aws_security_group.web.vpc_id
  description = "Security group VPC ID of the EC2 instance"
}

output "instance_security_group_ingress" {
  value = aws_security_group.web.ingress
  description = "Security group ingress of the EC2 instance"
}

output "instance_security_group_egress" {
  value = aws_security_group.web.egress
  description = "Security group egress of the EC2 instance"
}

output "instance_security_group_tags" {
  value = aws_security_group.web.tags
  description = "Security group tags of the EC2 instance"
}

output "instance_security_group_vpc_id" {
  value = aws_security_group.web.vpc_id
  description = "Security group VPC ID of the EC2 instance"
}

