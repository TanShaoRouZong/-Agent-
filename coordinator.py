"""
Coordinator Agent — 调度中枢
负责任务拆分、子Agent调度、结果汇总
"""

import time
from agents.parser_agent import ParserAgent
from agents.risk_agent import RiskAgent
from agents.summary_agent import SummaryAgent


class CoordinatorAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.name = "CoordinatorAgent"

    def log(self, msg: str):
        print(f"[{self.name}] {msg}")

    def run(self, contract_text: str) -> dict:
        self.log("🚀 启动多Agent协作流程...")
        self.log("任务拆分: Parser → Risk → Summary")
        print()

        # Step 1: Parser Agent
        self.log("📋 Step 1/3 — 调度 ParserAgent (结构化信息提取)")
        parser = ParserAgent(self.api_key)
        parsed = parser.run(contract_text)
        print()
        time.sleep(0.3)

        # Step 2: Risk Agent
        self.log("⚠️  Step 2/3 — 调度 RiskAgent (链式推理风险评估)")
        risk = RiskAgent(self.api_key)
        risk_result = risk.run(contract_text, parsed)
        print()
        time.sleep(0.3)

        # Step 3: Summary Agent
        self.log("📝 Step 3/3 — 调度 SummaryAgent (生成最终决策报告)")
        summary = SummaryAgent(self.api_key)
        report = summary.run(parsed, risk_result)
        print()

        self.log("✅ 所有子Agent完成，汇总结果")

        return {
            "parsed_info": parsed,
            "risk_assessment": risk_result,
            "final_report": report
        }
