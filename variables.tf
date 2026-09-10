variable "aiven_project" {
  description = "The Aiven project where resources will be created"
  type        = string
  
  # Default value - should be overridden via TF_VAR_aiven_project or terraform.tfvars
  default     = "basquat-devops"
}

# Optional: Define other variables if needed
variable "aiven_api_token" {
  description = "The Aiven API token"
  type        = string
  
  # For security, this should be provided via environment variable AVN_API_TOKEN
  # or via Terraform Cloud variables
  sensitive   = true
}
