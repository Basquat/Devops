terraform {
  # Configuration for the remote backend
  backend "remote" {
    # The name of your Terraform Cloud organization.
    organization = "basquat-devops"  # Change to your organization
    
    # The name of the Terraform Cloud workspace to store Terraform state files in.
    workspaces {
      name = "devops-postgresql"  # Change to your workspace name
    }
  }
}

# Configure the Aiven provider
provider "aiven" {
  # The API token can be specified via the 'AVN_API_TOKEN' environment variable
}

# Create a PostgreSQL service
resource "aiven_postgresql" "defaultdb" {
  project      = var.aiven_project
  cloud_name   = "google-europe-west1"  # Change to your preferred cloud/region
  plan         = "startup-4"  # Adjust plan as needed
  service_name = "devops-joaodan-b63e"  # Must match the hostname from the original README
  
  # PostgreSQL specific settings
  pg {
    user_config = {
      # Default PostgreSQL settings
      pg_tune = true
    }
  }
  
  # Ensure the service is running
  maintenance_window {
    day   = "sun"
    hour  = 10
  }
  
  # Enable termination protection to prevent accidental deletion
  termination_protection = true
}

# Create a database within the PostgreSQL service
resource "aiven_postgresql_database" "defaultdb" {
  project      = var.aiven_project
  service_name = aiven_postgresql.defaultdb.service_name
  database_name = "defaultdb"
}

# Create a service user (avnadmin is typically the default user)
resource "aiven_postgresql_user" "avnadmin" {
  project      = var.aiven_project
  service_name = aiven_postgresql.defaultdb.service_name
  user_name    = "avnadmin"
  
  # Grant all privileges on the defaultdb database
  pg_privileges {
    database = "defaultdb"
    privileges = [
      "CREATE",
      "CONNECT",
      "TEMPORARY",
      "SELECT",
      "INSERT",
      "UPDATE",
      "DELETE",
      "TRUNCATE",
      "REFERENCES",
      "TRIGGER"
    ]
  }
}

# Output the connection details for the application
# We'll parse the service_uri to get individual components
output "db_host" {
  description = "The hostname of the PostgreSQL service"
  # Assuming service_uri format: postgres://user:password@host:port/database
  value       = split(":", split("@", aiven_postgresql.defaultdb.service_uri)[1])[0]
}

output "db_port" {
  description = "The port of the PostgreSQL service"
  # Extract port from service_uri: postgres://user:password@host:port/database
  value       = split("/", split(":", split("@", aiven_postgresql.defaultdb.service_uri)[1])[1])[0]
}

output "db_name" {
  description = "The database name"
  value       = aiven_postgresql_database.defaultdb.database_name
}

output "db_user" {
  description = "The database user"
  value       = split(":", split("@", aiven_postgresql.defaultdb.service_uri)[0])[0]
}

# Note: The password is sensitive and won't be output directly
# It can be retrieved from the service URI or via Aiven CLI/API
# To get the password, you would need to parse:
# password = split(":", split("@", aiven_postgresql.defaultdb.service_uri)[0])[1]
