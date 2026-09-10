# Flask Application with PostgreSQL Connection on Aiven

This is a simple Flask application configured to connect to a PostgreSQL database hosted on Aiven Cloud, deployed using Terraform.

## Architecture

- Application: Flask web application (app.py)
- Database: PostgreSQL hosted on Aiven Cloud
- Infrastructure: Terraform for provisioning Aiven resources
- CI/CD: GitHub Actions workflow for Terraform execution

## Prerequisites

1. Terraform installed (v1.0+)
2. Aiven account with API token
3. GitHub repository with secrets configured (for automated deployment)

## Manual Deployment

### 1. Configure Aiven Provider

Create a terraform.tfvars file or set environment variables:

Option 1: terraform.tfvars
```
aiven_project = "your-aiven-project-name"
```

Option 2: Environment variables
```
export TF_VAR_aiven_project="your-aiven-project-name"
export AVN_API_TOKEN="your-aiven-api-token"
```

### 2. Initialize and Apply Terraform

```
terraform init
terraform apply
```

### 3. Get Connection Details

After applying, Terraform will output the database connection details. Configure your application with these environment variables:

```
export DB_HOST="your-host-from-output"
export DB_PORT="27506"
export DB_NAME="defaultdb"
export DB_USER="avnadmin"
export DB_PASSWORD="your-password-from-aiven"
export DB_SSLMODE="require"
```

### 4. Run the Application

```
pip install -r requirements.txt
python app.py
```

## Environment Variables

The application expects the following environment variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DB_HOST | Database hostname | Yes | - |
| DB_PORT | Database port | No | 27506 |
| DB_NAME | Database name | Yes | - |
| DB_USER | Database username | Yes | - |
| DB_PASSWORD | Database password | Yes | - |
| DB_SSLMODE | SSL mode | No | require |

## GitHub Actions Deployment

The repository includes a GitHub Actions workflow (.github/workflows/terraform.yml) that automatically:

1. Runs terraform init, fmt, and plan on pull requests
2. Runs terraform apply on pushes to the main branch

### Required GitHub Secrets

For the workflow to function, configure these secrets in your repository:

- TF_API_TOKEN: Terraform Cloud API token
- AVN_API_TOKEN: Aiven API token (for the provider)
- TF_VAR_aiven_project: Your Aiven project name

## Application Endpoints

- GET /: Returns basic information about the database configuration
- GET /db-test: Tests the database connection and returns PostgreSQL version

## Security Notes

- Never commit sensitive information like passwords or API tokens
- The .gitignore file should exclude terraform.tfvars and similar files
- Database credentials are managed via Aiven and should be rotated periodically
