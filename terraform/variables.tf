# ============================================================================
# Variables: Agentic AI Governance on OCI
# ============================================================================

variable "tenancy_ocid" {
  description = "OCI Tenancy OCID"
  type        = string
}

variable "region" {
  description = "OCI Region"
  type        = string
  default     = "us-phoenix-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "object_storage_namespace" {
  description = "OCI Object Storage namespace"
  type        = string
}

variable "function_image" {
  description = "OCI Function image for policy engine"
  type        = string
  default     = "iad.ocir.io/your-namespace/agent-policy-engine:latest"
}

variable "notification_email" {
  description = "Email address for alerts and notifications"
  type        = string
}
