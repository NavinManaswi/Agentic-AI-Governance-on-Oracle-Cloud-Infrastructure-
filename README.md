# 🤖 Agentic AI Governance on Oracle Cloud Infrastructure (OCI)

## Zero-Trust Governance for Autonomous AI Agents on OCI Generative AI

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()
[![OCI](https://img.shields.io/badge/OCI-Certified-red.svg)]()
[![Generative AI](https://img.shields.io/badge/Generative%20AI-Ready-blue.svg)]()
[![OWASP Agentic](https://img.shields.io/badge/OWASP%20Agentic-Aligned-green.svg)]()
[![CSA ATF](https://img.shields.io/badge/CSA%20ATF-Compatible-purple.svg)]()

---

## 📋 Table of Contents

- [About This Project](#-about-this-project)
- [Why This Matters](#-why-this-matters)
- [OCI Agentic AI Stack](#-oci-agentic-ai-stack)
- [Architecture](#-architecture)
- [OCI Services Used](#-oci-services-used)
- [Quick Start](#-quick-start)
- [What's Inside](#-whats-inside)
- [Key Artifacts](#-key-artifacts)
- [Deployment](#-deployment)
- [License](#-license)

---

## 🎯 About This Project

This project implements a **complete governance and security framework** for AI agents built on **OCI Generative AI** — Oracle's fully managed enterprise AI platform.

**What it does:**

| Capability | Description |
|------------|-------------|
| 🔐 **Zero-Trust Identity** | OCI IAM policies with deny-by-default for agent identities |
| 📋 **Policy-as-Code** | IAM policies + Zero Trust Packet Routing (ZPR) for service communication |
| 🛡️ **Runtime Guardrails** | AI Guardrails for Content Moderation (CM), Prompt Injection (PI), and PII protection |
| 🌐 **Network Security** | VCN + Private Endpoints + Zero Trust Packet Routing |
| 📊 **Continuous Monitoring** | OCI Logging + OCI Monitoring + OpenTelemetry |
| 🚨 **Incident Response** | Agentic-specific incident runbook with kill-switch capabilities |
| 📁 **Audit Evidence** | OCI Logging with 10-year retention + audit trails |

---

## 🚨 Why This Matters

OCI's Enterprise AI governance in OCI Generative AI combines infrastructure, identity, network security, and runtime controls to help keep AI systems secure.

### OCI's Agentic Governance Services

| Service | Purpose | Key Feature |
|---------|---------|-------------|
| **OCI Generative AI Agents** | Fully managed service for creating intelligent virtual agents | RAG capabilities, LLM integration |
| **AI Guardrails** | Configurable safety and compliance controls | CM, PI, PII protection |
| **OCI IAM** | Identity and access management | Deny-by-default policies |
| **Zero Trust Packet Routing (ZPR)** | Identity-based service communication | Secure inter-service communication |
| **OCI Logging** | Centralized log collection | 10-year retention for compliance |
| **OCI Monitoring** | Key metric monitoring | Availability, performance |
| **OpenTelemetry** | Distributed tracing | End-to-end observability |

---

## 🏗️ OCI Agentic AI Stack
┌─────────────────────────────────────────────────────────────────────────────┐
│ OCI AGENTIC AI GOVERNANCE STACK │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ IDENTITY & ACCESS LAYER │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ OCI IAM │ │ Deny-by- │ │ Zero Trust Packet │ │ │
│ │ │ Policies │ │ Default │ │ Routing (ZPR) │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ RUNTIME & GOVERNANCE LAYER │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ OCI │ │ AI │ │ Generative AI │ │ │
│ │ │ Generative │ │ Guardrails │ │ Agents │ │ │
│ │ │ AI │ │ (CM, PI, │ │ (RAG + LLM) │ │ │
│ │ │ │ │ PII) │ │ │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ NETWORK SECURITY LAYER │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ VCN │ │ Private │ │ Network Security │ │ │
│ │ │ (Virtual │ │ Endpoints │ │ Groups │ │ │
│ │ │ Cloud │ │ │ │ │ │ │
│ │ │ Network) │ │ │ │ │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ OBSERVABILITY & AUDIT LAYER │ │
│ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │
│ │ │ OCI Logging │ │ OCI │ │ OpenTelemetry │ │ │
│ │ │ (Audit │ │ Monitoring │ │ (Tracing) │ │ │
│ │ │ Trail) │ │ (Metrics) │ │ │ │ │
│ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘


---

## 🔧 OCI Services Used

| Service | Purpose | Key Feature |
|---------|---------|-------------|
| **OCI Generative AI Agents** | Agent runtime and RAG capabilities | Fully managed, LLM-powered agents |
| **AI Guardrails** | Runtime safety and compliance | CM, PI, PII protection |
| **OCI IAM** | Identity and access management | Deny-by-default policies |
| **Zero Trust Packet Routing (ZPR)** | Secure service communication | Identity-based routing |
| **OCI VCN** | Virtual Cloud Network | Network isolation |
| **OCI Logging** | Audit and operational logs | 10-year retention |
| **OCI Monitoring** | Metrics and alerting | Availability, performance |
| **OCI Functions** | Serverless PDP | Policy evaluation |

---

## 🚀 Quick Start

| Step | Action | Command |
|------|--------|---------|
| **1** | Clone the repository | `git clone https://github.com/yourusername/agentic-ai-governance-oci.git` |
| **2** | Navigate to the project | `cd agentic-ai-governance-oci` |
| **3** | Configure Terraform | `cp terraform/terraform.tfvars.example terraform/terraform.tfvars` |
| **4** | Deploy infrastructure | `./scripts/deploy.sh` |
| **5** | Test governance | `python scripts/test-governance.py` |

---

## 📂 What's Inside

| Folder | Description |
|--------|-------------|
| **terraform/** | Terraform infrastructure-as-code for all OCI resources |
| **src/policy-engine/** | OCI Function PDP for policy evaluation |
| **src/remediator/** | Kill-switch and remediation |
| **policies/iam/** | OCI IAM policies for agents |
| **policies/guardrails/** | AI Guardrails configuration |
| **policies/zpr/** | Zero Trust Packet Routing policies |
| **audit-framework/** | CSA ATF and OWASP Agentic Top 10 mapping |
| **scripts/** | Deployment and testing scripts |

---

## 🏆 Key Artifacts

### 1. OCI IAM Policies
Zero-trust identity for AI agents with deny-by-default policies.

### 2. AI Guardrails Configuration
Runtime safety controls: Content Moderation (CM), Prompt Injection (PI), PII Protection.

### 3. Zero Trust Packet Routing (ZPR)
Identity-based network security for service-to-service communication.

### 4. OCI Function PDP
Policy Decision Point for agent authorization with IAM + Guardrails + ZPR integration.

---

## 🚀 Deployment

### Prerequisites

- OCI CLI installed and configured
- Terraform installed
- Python 3.11+ installed

### One-Click Deployment

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-ai-governance-oci.git
cd agentic-ai-governance-oci

# Make the deployment script executable
chmod +x scripts/deploy.sh

# Run the deployment
./scripts/deploy.sh

## Manual Deployment

# Initialize Terraform
cd terraform
terraform init
terraform apply

# Deploy OCI Function
fn deploy --app agentic-governance

# Configure IAM policies
oci iam policy create --name agent-governance-policy ...

# Configure AI Guardrails
# (via OCI Console or API)
📝 License
This project is licensed under the MIT License.

⭐ Star This Repository
If you find this project helpful, please star this repository and share it with your network!
