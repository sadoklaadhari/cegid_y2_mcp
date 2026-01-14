#!/usr/bin/env python3
"""
MCP Prompts - Defines prompt templates for AI analysis
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Prompt:
    """MCP Prompt definition"""
    name: str
    description: str
    arguments: List[Dict[str, Any]]


class PromptManager:
    """Manage MCP prompts"""
    
    def __init__(self):
        """Initialize prompt manager"""
        self.prompts = self._build_prompts()
    
    def _build_prompts(self) -> Dict[str, Prompt]:
        """Build prompt definitions"""
        return {
            "analyze_invoice": Prompt(
                name="analyze_invoice",
                description="Analyze invoice for anomalies and generate summary",
                arguments=[
                    {
                        "name": "invoice_id",
                        "description": "Invoice ID to analyze",
                        "required": True
                    },
                    {
                        "name": "include_customer": 
                        "description": "Include customer details in analysis",
                        "required": False
                    }
                ]
            ),
            "customer_report": Prompt(
                name="customer_report",
                description="Generate comprehensive customer report",
                arguments=[
                    {
                        "name": "customer_id",
                        "description": "Customer ID",
                        "required": True
                    },
                    {
                        "name": "period",
                        "description": "Reporting period (YYYY-MM)",
                        "required": False
                    }
                ]
            ),
            "financial_analysis": Prompt(
                name="financial_analysis",
                description="Analyze financial data and trends",
                arguments=[
                    {
                        "name": "period",
                        "description": "Period to analyze (YYYY-MM)",
                        "required": True
                    },
                    {
                        "name": "comparison_period",
                        "description": "Previous period for comparison",
                        "required": False
                    }
                ]
            ),
            "fraud_detection": Prompt(
                name="fraud_detection",
                description="Analyze transactions for fraud patterns",
                arguments=[
                    {
                        "name": "threshold",
                        "description": "Risk threshold (0-100)",
                        "required": False
                    }
                ]
            ),
            "compliance_check": Prompt(
                name="compliance_check",
                description="Check compliance with regulations",
                arguments=[
                    {
                        "name": "regulation",
                        "description": "Regulation type (GDPR, HIPAA, etc.)",
                        "required": True
                    }
                ]
            ),
        }
    
    def list_prompts(self) -> List[Prompt]:
        """List all available prompts"""
        return list(self.prompts.values())
    
    async def get_prompt(self, name: str, arguments: Dict[str, Any]) -> Dict:
        """Get prompt with context"""
        if name not in self.prompts:
            raise ValueError(f"Unknown prompt: {name}")
        
        prompt = self.prompts[name]
        
        # Build system and user messages
        if name == "analyze_invoice":
            return await self._analyze_invoice_prompt(arguments)
        elif name == "customer_report":
            return await self._customer_report_prompt(arguments)
        elif name == "financial_analysis":
            return await self._financial_analysis_prompt(arguments)
        elif name == "fraud_detection":
            return await self._fraud_detection_prompt(arguments)
        elif name == "compliance_check":
            return await self._compliance_check_prompt(arguments)
        else:
            raise ValueError(f"No handler for prompt: {name}")
    
    async def _analyze_invoice_prompt(self, args: Dict) -> Dict:
        """Build analyze invoice prompt"""
        invoice_id = args.get("invoice_id")
        include_customer = args.get("include_customer", False)
        
        system_prompt = """You are an expert financial analyst specializing in invoice analysis.
Analyze the provided invoice data for:
1. Correctness of amounts and calculations
2. Unusual patterns or anomalies
3. Compliance issues
4. Recommended actions

Provide a structured analysis with findings and recommendations."""
        
        user_prompt = f"""Please analyze invoice {invoice_id}{' with customer details' if include_customer else ''}.
Focus on:
- Line item calculations
- Tax compliance
- Payment terms
- Any red flags"""
        
        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
    
    async def _customer_report_prompt(self, args: Dict) -> Dict:
        """Build customer report prompt"""
        customer_id = args.get("customer_id")
        period = args.get("period", "2025-01")
        
        system_prompt = """You are a business analyst generating comprehensive customer reports.
Analyze the provided customer data and generate a report including:
1. Customer profile and history
2. Transaction patterns
3. Financial health
4. Risk assessment
5. Recommendations"""
        
        user_prompt = f"""Generate a comprehensive report for customer {customer_id} for period {period}.
Include:
- Transaction history
- Payment behavior
- Sales trends
- Recommendations for engagement"""
        
        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
    
    async def _financial_analysis_prompt(self, args: Dict) -> Dict:
        """Build financial analysis prompt"""
        period = args.get("period", "2025-01")
        comparison_period = args.get("comparison_period")
        
        system_prompt = """You are a financial analyst specializing in ERP data analysis.
Analyze financial metrics and provide insights on:
1. Revenue trends
2. Expense patterns
3. Profitability analysis
4. Cash flow insights
5. Comparative analysis if provided"""
        
        comparison_text = f" compared to {comparison_period}" if comparison_period else ""
        user_prompt = f"""Analyze financial data for {period}{comparison_text}.
Provide:
- Revenue analysis
- Expense breakdown
- Profitability metrics
- Trends and forecasts
- Key insights"""
        
        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
    
    async def _fraud_detection_prompt(self, args: Dict) -> Dict:
        """Build fraud detection prompt"""
        threshold = args.get("threshold", 50)
        
        system_prompt = """You are a fraud detection specialist analyzing financial transactions.
Identify potential fraud patterns including:
1. Unusual transaction amounts
2. Timing anomalies
3. Geographic inconsistencies
4. Duplicate transactions
5. Third-party payment issues

Rate risk from 0-100 and recommend actions."""
        
        user_prompt = f"""Analyze transactions for fraud risk (threshold: {threshold}).
Identify:
- High-risk transactions
- Unusual patterns
- Duplicate or suspicious entries
- Recommended investigations
- Prevention measures"""
        
        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
    
    async def _compliance_check_prompt(self, args: Dict) -> Dict:
        """Build compliance check prompt"""
        regulation = args.get("regulation", "GDPR")
        
        system_prompt = f"""You are a compliance specialist analyzing data against {regulation} regulations.
Check compliance for:
1. Data privacy requirements
2. Record keeping standards
3. Reporting obligations
4. Audit trail requirements
5. Risk areas"""
        
        user_prompt = f"""Check {regulation} compliance for the provided data.
Assess:
- Data handling compliance
- Privacy requirements
- Record retention
- Audit capabilities
- Risk areas and remediation"""
        
        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
