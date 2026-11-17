variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "key_name" {
  type    = string
  default = "smrithi-key"
}

variable "owner_email" {
  type    = string
  default = "yogyatha12345@gmail.com"
}

variable "environment" {
  type    = string
  default = "dev"
}
