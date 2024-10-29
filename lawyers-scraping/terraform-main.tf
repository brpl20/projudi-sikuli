provider "aws" {
  region = "us-west-2"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# Use data source to reference existing security group
data "aws_security_group" "scraper_sg" {
  name = "oabGroup"
}

# Use data source to reference existing IAM role
data "aws_iam_role" "scraper_role" {
  name = "scraper_role"
}

# Use data source to reference existing IAM instance profile
data "aws_iam_instance_profile" "scraper_profile" {
  name = "scraper_profile"
}

# Keep the policy attachment, but reference the existing role
resource "aws_iam_role_policy_attachment" "s3_access" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
  role       = data.aws_iam_role.scraper_role.name
}

resource "aws_instance" "scraper" {
  count                = 255
  ami                  = data.aws_ami.ubuntu.id
  instance_type        = "t3.large"
  key_name             = "oabgetter"
  iam_instance_profile = data.aws_iam_instance_profile.scraper_profile.name

  vpc_security_group_ids = " "

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo add-apt-repository -y ppa:mozillateam/ppa
              sudo apt-get update
              sudo apt install -y python3 python3-pip python3.11-venv firefox-esr unzip awscli

              # Create .env file
              cat << EOT > "/home/ubuntu/.env"
              AWS_ACCESS_KEY_ID=${var.aws_access_key_id}
              AWS_SECRET_ACCESS_KEY=${var.aws_secret_access_key}
              S3_BUCKET=${var.s3_bucket}
              EOT

              # Calculate instance number (1 to 255)
              INSTANCE_NUM=$((${count.index} + 1))

              # Download scraper.py from S3
              aws s3 cp s3://""

              # Set up Python environment and run the script
              cd /home/ubuntu
              python3 -m venv scraper_env
              source scraper_env/bin/activate
              pip3 install --upgrade pip
              pip3 install selenium requests boto3 python-dotenv

              # Run the scraper
              python3 scraper.py $INSTANCE_NUM

              # Signal completion
              aws s3 cp ""
              EOF

  tags = {
    Name = "Scraper-Instance-$${count.index + 1}"
  }
}

variable "aws_access_key_id" {
  description = "AWS Access Key ID"
  type        = string
}

variable "aws_secret_access_key" {
  description = "AWS Secret Access Key"
  type        = string
}

variable "s3_bucket" {
  description = "S3 bucket for storing scraped data and completion signals"
  type        = string
  default     = "oabapi"
}

output "scraper_instances" {
  value       = aws_instance.scraper[*].public_ip
  description = "The public IPs of the scraper instances"
}

output "security_group_id" {
  value       = data.aws_security_group.scraper_sg.id
  description = "The ID of the security group used for the scraper"
}