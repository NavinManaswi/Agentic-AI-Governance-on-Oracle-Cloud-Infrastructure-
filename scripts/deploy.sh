#!/bin/bash
# One-click deployment script for Agentic AI Governance on OCI

set -e

echo "🤖 Agentic AI Governance on Oracle Cloud Infrastructure (OCI)"
echo "================================================================"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."
command -v oci >/dev/null 2>&1 || { echo "❌ OCI CLI not found. Please install it."; exit 1; }
command -v terraform >/dev/null 2>&1 || { echo "❌ Terraform not found. Please install it."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 not found. Please install it."; exit 1; }
echo "✅ Prerequisites satisfied."
echo ""

# Check OCI login
echo "🔐 Checking OCI configuration..."
oci iam region list >/dev/null 2>&1 || { echo "❌ OCI CLI not configured. Please run 'oci setup config'."; exit 1; }
echo "✅ OCI configured."
echo ""

# Get user input
read -p "Enter OCI Tenancy OCID: " TENANCY_OCID
read -p "Enter OCI Region (default: us-phoenix-1): " REGION
REGION=${REGION:-us-phoenix-1}
read -p "Enter Object Storage Namespace: " NAMESPACE
read -p "Enter email for notifications: " EMAIL

# Deploy Terraform infrastructure
echo "🚀 Deploying Terraform infrastructure..."
cd terraform

cat > terraform.tfvars << EOF
tenancy_ocid           = "$TENANCY_OCID"
region                 = "$REGION"
environment            = "dev"
object_storage_namespace = "$NAMESPACE"
function_image         = "iad.ocir.io/your-namespace/agent-policy-engine:latest"
notification_email     = "$EMAIL"
EOF

terraform init
terraform plan
terraform apply -auto-approve

cd ..
echo "✅ Infrastructure deployment complete."
echo ""

# Get function endpoint
FUNCTION_ENDPOINT=$(terraform output -raw function_endpoint)
echo "📤 Policy Engine Endpoint: $FUNCTION_ENDPOINT"
echo ""

echo "🎉 Deployment complete!"
echo ""
echo "🔍 OCI Logging available at:"
echo "   https://cloud.oracle.com/logging"
echo ""
echo "📊 OCI Monitoring available at:"
echo "   https://cloud.oracle.com/monitoring"
echo ""
echo "📧 Email notifications configured for: $EMAIL"
echo ""
echo "✅ Your Agentic AI Governance framework is now operational!"
