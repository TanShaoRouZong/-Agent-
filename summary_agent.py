"""
Summary Agent — 决策报告生成
汇总所有Agent的分析结果，生成最终可交付决策报告
"""

import json
import anthropic


class SummaryAgent:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.name = "SummaryAgent"
        self.model = "claude-sonnet-4-20250514"

    def log(self, msg: str):
        print(f"  [{self.name}] {msg}")

    def run(self, parsed_info: dict, risk_result: dict) -> dict:
        self.log("整合各Agent结果，生成决策报告...")

        prompt = f"""基于以下合同解析结果和风险评估，生成一份简洁的最终决策报告。

【解析结果】
{json.dumps(parsed_info, ensure_ascii=False, indent=2)}

【风险评估】
{json.dumps(risk_result, ensure_ascii=False, indent=2)}

请按以下JSON格式返回，不要包含其他文字：
{{
  "executive_summary": "3句话的执行摘要",
  "sign_recommendation": "建议签署/建议修改后签署/建议不签署",
  "key_negotiation_points": ["最重要的3个谈判要点"],
  "immediate_actions": ["立即需要做的事项"],
  "estimated_legal_risk_exposure": "预估法律风险敞口金额",
  "review_completed_at": "当前时间戳占位符"
}}"""

        self.log("生成执行摘要与决策建议...")
        start = __import__('time').time()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )

        elapsed = __import__('time').time() - start
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        self.log(f"API响应完成 | 耗时: {elapsed:.2f}s | Token消耗: {tokens_used:,}")

        raw = response.content[0].text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            result = json.loads(raw)
            rec = result.get("sign_recommendation", "N/A")
            self.log(f"✅ 报告生成完成 | 签署建议: {rec}")
            print(f"\n  {'='*50}")
            print(f"  📊 执行摘要: {result.get('executive_summary', '')}")
            print(f"  🖊️  建议: {rec}")
            print(f"  💰 风险敞口: {result.get('estimated_legal_risk_exposure', 'N/A')}")
            print(f"  {'='*50}")
            return result
        except json.JSONDecodeError:
            self.log("⚠️ JSON解析失败，返回原始文本")
            return {"raw": raw}
