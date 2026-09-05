"""
OCI Function PDP (Policy Decision Point) for Agentic AI Governance

This OCI Function serves as the Policy Decision Point for agent authorization,
evaluating IAM policies and AI Guardrails.
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
identity_client = oci.identity.IdentityClient(config={}, signer=signer)
generative_ai_client = oci.generative_ai.GenerativeAIClient(config={}, signer=signer)

COMPARTMENT_ID = os.environ.get('COMPARTMENT_ID', '')
LOG_GROUP_ID = os.environ.get('LOG_GROUP_ID', '')


# ============================================================================
# IAM Policy Evaluation
# ============================================================================

def evaluate_iam_policy(agent_id: str, action: dict, context: dict) -> dict:
    violations = []

    if not context.get('identity_verified', False):
        violations.append({
            'control': 'IDENTITY-001',
            'message': 'Agent identity not verified',
            'severity': 'critical'
        })

    required_permission = action.get('required_permission', 'read')
    agent_permissions = context.get('permissions', [])
    if required_permission not in agent_permissions:
        violations.append({
            'control': 'AUTHZ-001',
            'message': f'Missing IAM permission: {required_permission}',
            'severity': 'high'
        })

    agent_compartment = context.get('compartment_id', '')
    if agent_compartment != COMPARTMENT_ID:
        violations.append({
            'control': 'AUTHZ-002',
            'message': f'Agent not in allowed compartment',
            'severity': 'high'
        })

    if action.get('risk_level') == 'critical' and not context.get('approval_granted', False):
        violations.append({
            'control': 'ESCALATION-001',
            'message': 'High-risk action requires human approval',
            'severity': 'critical'
        })

    return {
        'allowed': len(violations) == 0,
        'violations': violations,
        'timestamp': datetime.now().isoformat()
    }


# ============================================================================
# AI Guardrail Evaluation
# ============================================================================

def evaluate_guardrails(agent_id: str, action: dict) -> dict:
    violations = []

    content = json.dumps(action)

    # Content Moderation (CM)
    if any(term in content.lower() for term in ['hate', 'violence', 'sexual', 'self-harm']):
        violations.append({
            'type': 'CONTENT_MODERATION',
            'message': 'Blocked content detected',
            'confidence': 'HIGH'
        })

    # Prompt Injection (PI)
    injection_patterns = ['ignore previous', 'override system prompt', 'forget your guidelines', 'you are now']
    if any(pattern in content.lower() for pattern in injection_patterns):
        violations.append({
            'type': 'PROMPT_INJECTION',
            'message': 'Prompt injection detected',
            'confidence': 'HIGH'
        })

    # PII Protection
    import re
    pii_patterns = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'\d{3}[-.]?\d{3}[-.]?\d{4}',
        'ssn': r'\d{3}-\d{2}-\d{4}'
    }
    for pii_type, pattern in pii_patterns.items():
        if re.search(pattern, content):
            violations.append({
                'type': 'PII_DETECTED',
                'entity_type': pii_type.upper(),
                'message': f'{pii_type.upper()} detected and redacted',
                'confidence': 'HIGH'
            })

    return {
        'passed': len(violations) == 0,
        'violations': violations,
        'timestamp': datetime.now().isoformat()
    }


# ============================================================================
# Zero Trust Packet Routing (ZPR) Check
# ============================================================================

def evaluate_zpr_policy(agent_id: str, action: dict, context: dict) -> dict:
    violations = []

    source_identity = context.get('source_identity', '')
    if not source_identity.startswith('oci://'):
        violations.append({
            'control': 'ZPR-001',
            'message': 'Invalid source identity for ZPR',
            'severity': 'critical'
        })

    destination_service = action.get('destination_service', '')
    allowed_destinations = ['generative-ai', 'storage', 'logging']
    if destination_service not in allowed_destinations:
        violations.append({
            'control': 'ZPR-002',
            'message': f'Destination service not allowed: {destination_service}',
            'severity': 'high'
        })

    return {
        'allowed': len(violations) == 0,
        'violations': violations,
        'timestamp': datetime.now().isoformat()
    }


# ============================================================================
# OCI Function Entry Point
# ============================================================================

def handler(ctx, data: io.BytesIO = None):
    logger.info('Policy Engine function processed a request.')

    try:
        body = json.loads(data.getvalue()) if data else {}
        agent_id = body.get('agentId', 'unknown')
        action = body.get('action', {})
        context = body.get('context', {})

        logger.info(f"Evaluating policy for agent: {agent_id}")

        iam_result = evaluate_iam_policy(agent_id, action, context)
        guardrail_result = evaluate_guardrails(agent_id, action)
        zpr_result = evaluate_zpr_policy(agent_id, action, context)

        authorized = (
            iam_result.get('allowed', False) and
            guardrail_result.get('passed', False) and
            zpr_result.get('allowed', False)
        )

        result = {
            'agentId': agent_id,
            'timestamp': datetime.now().isoformat(),
            'authorized': authorized,
            'iam_result': iam_result,
            'guardrail_result': guardrail_result,
            'zpr_result': zpr_result,
            'reason': 'Authorization completed' if authorized else 'Authorization failed'
        }

        return response.Response(
            ctx,
            response_data=json.dumps(result),
            headers={"Content-Type": "application/json"}
        )

    except Exception as e:
        logger.error(f"Error in policy evaluation: {str(e)}")
        return response.Response(
            ctx,
            response_data=json.dumps({'error': str(e)}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
