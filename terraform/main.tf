# ============================================================================
# Terraform Configuration: Agentic AI Governance on OCI
# ============================================================================

terraform {
  required_version = ">= 1.0"
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 6.0"
    }
  }
}

provider "oci" {
  region = var.region
}

# ============================================================================
# Compartment
# ============================================================================

resource "oci_identity_compartment" "agent_governance" {
  compartment_id = var.tenancy_ocid
  description    = "Compartment for Agentic AI Governance"
  name           = "agentic-governance-${var.environment}"
}

# ============================================================================
# VCN & Networking
# ============================================================================

resource "oci_core_vcn" "agent_vcn" {
  compartment_id = oci_identity_compartment.agent_governance.id
  cidr_blocks    = ["10.0.0.0/16"]
  display_name   = "agent-vcn-${var.environment}"
}

resource "oci_core_subnet" "agent_subnet" {
  compartment_id = oci_identity_compartment.agent_governance.id
  vcn_id         = oci_core_vcn.agent_vcn.id
  cidr_block     = "10.0.1.0/24"
  display_name   = "agent-subnet-${var.environment}"
  route_table_id = oci_core_route_table.agent_route_table.id
  security_list_ids = [oci_core_security_list.agent_security_list.id]
}

resource "oci_core_route_table" "agent_route_table" {
  compartment_id = oci_identity_compartment.agent_governance.id
  vcn_id         = oci_core_vcn.agent_vcn.id
  display_name   = "agent-route-table-${var.environment}"
}

resource "oci_core_security_list" "agent_security_list" {
  compartment_id = oci_identity_compartment.agent_governance.id
  vcn_id         = oci_core_vcn.agent_vcn.id
  display_name   = "agent-security-list-${var.environment}"

  ingress_security_rules {
    protocol    = "6"
    source      = "10.0.0.0/16"
    source_type = "CIDR_BLOCK"
    tcp_options {
      destination_port_range {
        min = 443
        max = 443
      }
    }
  }

  egress_security_rules {
    protocol    = "6"
    destination = "0.0.0.0/0"
    tcp_options {
      destination_port_range {
        min = 443
        max = 443
      }
    }
  }
}

# ============================================================================
# Object Storage (for logs and artifacts)
# ============================================================================

resource "oci_objectstorage_bucket" "agent_logs" {
  compartment_id = oci_identity_compartment.agent_governance.id
  namespace      = var.object_storage_namespace
  name           = "agent-logs-${var.environment}"
  storage_tier   = "Standard"
}

resource "oci_objectstorage_bucket" "agent_artifacts" {
  compartment_id = oci_identity_compartment.agent_governance.id
  namespace      = var.object_storage_namespace
  name           = "agent-artifacts-${var.environment}"
  storage_tier   = "Standard"
}

# ============================================================================
# OCI Logging
# ============================================================================

resource "oci_logging_log_group" "agent_log_group" {
  compartment_id = oci_identity_compartment.agent_governance.id
  display_name   = "agent-log-group-${var.environment}"
}

resource "oci_logging_log" "agent_audit_log" {
  display_name = "agent-audit-log-${var.environment}"
  log_group_id = oci_logging_log_group.agent_log_group.id
  log_type     = "CUSTOM"
  retention_duration = 3650
}

# ============================================================================
# OCI Functions (PDP)
# ============================================================================

resource "oci_functions_application" "agent_governance_app" {
  compartment_id = oci_identity_compartment.agent_governance.id
  display_name   = "agent-governance-app-${var.environment}"
  subnet_ids     = [oci_core_subnet.agent_subnet.id]
}

resource "oci_functions_function" "policy_engine" {
  application_id = oci_functions_application.agent_governance_app.id
  display_name   = "agent-policy-engine-${var.environment}"
  image          = var.function_image
  memory_in_mbs  = 1024
  timeout_in_seconds = 300

  source_details {
    source_type = "INLINE"
    inline_source_base64_encoded = base64encode(file("${path.module}/../src/policy-engine/func.py"))
  }
}

# ============================================================================
# IAM Policies for Agents
# ============================================================================

resource "oci_identity_policy" "agent_governance_policy" {
  compartment_id = var.tenancy_ocid
  name           = "agent-governance-policy-${var.environment}"
  description    = "Policy for agentic AI governance"

  statements = [
    "allow any-user to use generative-ai-family in tenancy",
    "allow any-user to use generative-ai-endpoint in tenancy",
    "allow any-user to read objectstorage-buckets in compartment ${oci_identity_compartment.agent_governance.id}",
    "allow any-user to use logging-family in compartment ${oci_identity_compartment.agent_governance.id}",
    "deny any-user to use network-family in tenancy where request.principal.type != 'agent'"
  ]
}

# ============================================================================
# Outputs
# ============================================================================

output "function_endpoint" {
  value = oci_functions_function.policy_engine.invoke_endpoint
}

output "log_group_id" {
  value = oci_logging_log_group.agent_log_group.id
}

output "compartment_id" {
  value = oci_identity_compartment.agent_governance.id
}
