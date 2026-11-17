output "instance_id" {
  value = aws_instance.smrithi_server.id
}

output "public_ip" {
  value = aws_instance.smrithi_server.public_ip
}

output "vpc_id" {
  value = aws_vpc.smrithi_vpc.id
}

output "web_url" {
  value = "http://${aws_instance.smrithi_server.public_ip}"
}
