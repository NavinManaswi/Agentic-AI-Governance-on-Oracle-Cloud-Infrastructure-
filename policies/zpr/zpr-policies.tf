# ============================================================================
# Zero Trust Packet Routing (ZPR) Policies
# Enforces secure, identity-based communication between services
# ============================================================================

resource "oci_network_firewall_policy" "agent_zpr_policy" {
  compartment_id = oci_identity_compartment.agent_governance.id
  display_name   = "agent-zpr-policy-${var.environment}"
  description    = "Zero Trust Packet Routing for agentic AI"

  security_rules {
    name        = "allow-agent-to-generative-ai"
    description = "Allow agents to communicate with Generative AI endpoints"
    action      = "ALLOW"
    source_type = "IDENTITY"
    source      = "oci://${var.tenancy_ocid}/agent/*"
    destination_type = "IDENTITY"
    destination = "oci://${var.tenancy_ocid}/generative-ai/*"
    protocol    = "TCP"
  }

  security_rules {
    name        = "allow-agent-to-storage"
    description = "Allow agents to access Object Storage"
    action      = "ALLOW"
    source_type = "IDENTITY"
    source      = "oci://${var.tenancy_ocid}/agent/*"
    destination_type = "IDENTITY"
    destination = "oci://${var.tenancy_ocid}/storage/*"
    protocol    = "TCP"
  }

  security_rules {
    name        = "deny-agent-to-internal"
    description = "Deny agents from accessing internal services"
    action      = "DENY"
    source_type = "IDENTITY"
    source      = "oci://${var.tenancy_ocid}/agent/*"
    destination_type = "IDENTITY"
    destination = "oci://${var.tenancy_ocid}/internal/*"
    protocol    = "TCP"
  }
}
