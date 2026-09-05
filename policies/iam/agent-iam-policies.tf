# ============================================================================
# OCI IAM Policies for AI Agents
# Zero-trust identity with deny-by-default
# ============================================================================

resource "oci_identity_policy" "agent_core_policy" {
  compartment_id = var.tenancy_ocid
  name           = "agent-core-policy-${var.environment}"
  description    = "Core IAM policy for AI agents"

  statements = [
    "deny any-user to manage all-resources in tenancy where request.principal.type = 'agent'",
    "allow any-user to use generative-ai-family in tenancy where request.principal.type = 'agent'",
    "allow any-user to use generative-ai-endpoint in tenancy where request.principal.id = '${oci_generative_ai_endpoint.agent_endpoint.id}'",
    "allow any-user to read objectstorage-buckets in compartment ${oci_identity_compartment.agent_governance.id} where request.principal.type = 'agent'",
    "allow any-user to use logging-family in compartment ${oci_identity_compartment.agent_governance.id} where request.principal.type = 'agent'",
    "deny any-user to use network-family in tenancy where request.principal.type = 'agent' and request.network.source != '${oci_core_subnet.agent_subnet.id}'"
  ]
}

resource "oci_identity_policy" "agent_guardrail_policy" {
  compartment_id = oci_identity_compartment.agent_governance.id
  name           = "agent-guardrail-policy-${var.environment}"
  description    = "Guardrail enforcement policy for AI agents"

  statements = [
    "allow any-user to use generative-ai-family in tenancy where request.principal.type = 'agent' and request.guardrails.enabled = true"
  ]
}
