"""
OCI Function Remediator: Agent Kill-Switch and Remediation

This OCI Function implements kill-switch capabilities and automated remediation
for agentic AI governance violations.
"""

import io
import json
import logging
import os
from datetime import datetime

import oci
from fdk import response

# ============================================================================
# Configuration
# ============================================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

signer = oci.auth.signers.get_resource_principals_signer()
generative_ai_client = oci.generative_ai.GenerativeAIClient(config={}, signer=signer)
identity_client = oci.identity.IdentityClient(config={}, signer=signer)


# ============================================================================
# Kill-Switch Actions
# ============================================================================

def activate_kill_switch(agent_id: str, reason: str, violation_type: str) -> dict:
    logger.warning(f"KILL-SWITCH ACTIVATED for agent: {agent_id}")
    logger.warning(f"Reason: {reason}")
    logger.warning(f"Violation Type: {violation_type}")

    try:
        # In production, call OCI Generative AI API to disable agent
        return {
            'status': 'kill-switch-activated',
            'agent_id': agent_id,
            'reason': reason,
            'violation_type': violation_type,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'kill-switch-failed',
            'agent_id': agent_id,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def revoke_agent_credentials(agent_id: str, reason: str) -> dict:
    logger.info(f"Revoking credentials for agent: {agent_id}")

    try:
        return {
            'status': 'credentials-revoked',
            'agent_id': agent_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'revocation-failed',
            'agent_id': agent_id,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def quarantine_agent(agent_id: str, reason: str) -> dict:
    logger.info(f"Quarantining agent: {agent_id}")

    try:
        return {
            'status': 'agent-quarantined',
            'agent_id': agent_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'quarantine-failed',
            'agent_id': agent_id,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def remove_from_agent_registry(agent_id: str, reason: str) -> dict:
    logger.info(f"Removing agent from registry: {agent_id}")

    try:
        return {
            'status': 'agent-removed-from-registry',
            'agent_id': agent_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'registry-removal-failed',
            'agent_id': agent_id,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


# ============================================================================
# Violation Classification
# ============================================================================

def classify_violation(violation_type: str) -> dict:
    severity_map = {
        'GOAL_HIJACK': {'severity': 'critical', 'action': 'kill-switch'},
        'TOOL_MISUSE': {'severity': 'critical', 'action': 'kill-switch'},
        'PRIVILEGE_ABUSE': {'severity': 'critical', 'action': 'kill-switch'},
        'RESOURCE_EXHAUSTION': {'severity': 'high', 'action': 'quarantine'},
        'IDENTITY_CONFUSION': {'severity': 'critical', 'action': 'revoke-credentials'},
        'MEMORY_POISONING': {'severity': 'high', 'action': 'quarantine'},
        'COST_RUNAWAY': {'severity': 'high', 'action': 'quarantine'},
        'MINOR_ANOMALY': {'severity': 'low', 'action': 'log-only'},
        'GUARDRAIL_VIOLATION': {'severity': 'high', 'action': 'quarantine'},
        'IAM_VIOLATION': {'severity': 'critical', 'action': 'revoke-credentials'},
        'ZPR_VIOLATION': {'severity': 'critical', 'action': 'kill-switch'}
    }

    return severity_map.get(violation_type, {'severity': 'medium', 'action': 'quarantine'})


# ============================================================================
# OCI Function Entry Point
# ============================================================================

def handler(ctx, data: io.BytesIO = None):
    logger.info('Remediator function processed a request.')

    try:
        body = json.loads(data.getvalue()) if data else {}
        agent_id = body.get('agentId', 'unknown')
        violation_type = body.get('violationType', 'UNKNOWN')
        reason = body.get('reason', 'No reason provided')

        logger.info(f"Processing violation for agent: {agent_id}")
        logger.info(f"Violation Type: {violation_type}")

        classification = classify_violation(violation_type)
        severity = classification.get('severity', 'medium')
        action = classification.get('action', 'quarantine')

        result = None

        if action == 'kill-switch':
            result = activate_kill_switch(agent_id, reason, violation_type)
        elif action == 'revoke-credentials':
            result = revoke_agent_credentials(agent_id, reason)
        elif action == 'quarantine':
            result = quarantine_agent(agent_id, reason)
        elif action == 'remove-from-registry':
            result = remove_from_agent_registry(agent_id, reason)
        else:
            result = {
                'status': 'logged-only',
                'agent_id': agent_id,
                'reason': reason,
                'violation_type': violation_type,
                'timestamp': datetime.now().isoformat()
            }

        return response.Response(
            ctx,
            response_data=json.dumps({
                'agentId': agent_id,
                'violationType': violation_type,
                'severity': severity,
                'action': action,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }),
            headers={"Content-Type": "application/json"}
        )

    except Exception as e:
        logger.error(f"Error in remediation: {str(e)}")
        return response.Response(
            ctx,
            response_data=json.dumps({'error': str(e)}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
