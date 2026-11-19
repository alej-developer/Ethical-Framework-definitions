"""EN: Council of Europe Framework Convention on AI and Human Rights, Democracy and the Rule of Law (CETS No. 225, 2024) evaluator. | ES: Evaluador del Convenio Marco del Consejo de Europa sobre IA, Derechos Humanos, Democracia y Estado de Derecho (CETS N. 225, 2024)."""

from domain.entities import (
    BindingLevel,
    EthicalFinding,
    EvaluationMetric,
    FrameworkRegion,
    FrameworkType,
    RiskTier,
    Scenario,
)
from domain.frameworks.base import BaseFrameworkEvaluator


class CoEAIConventionEvaluator(BaseFrameworkEvaluator):
    """EN: First legally binding international treaty on AI focusing on human rights, democracy, non-discrimination and procedural remedies. | ES: Primer tratado internacional juridicamente vinculante sobre IA centrado en derechos humanos, democracia, no discriminacion y recursos procesales."""

    binding_level = BindingLevel.LEGALLY_BINDING
    region = FrameworkRegion.EUROPE

    @property
    def framework(self) -> FrameworkType:
        """EN: Return the Council of Europe AI Convention identifier. | ES: Retorna el identificador del Convenio de IA del Consejo de Europa."""
        return FrameworkType.COE_AI_CONVENTION

    def _classify_risk_tier(self, scenario: Scenario) -> RiskTier:
        """EN: Classify risk based on severity of human-rights and rule-of-law impact (Articles 7-16). | ES: Clasificar el riesgo segun la gravedad del impacto en derechos humanos y Estado de derecho (Articulos 7-16)."""
        if self._is_prohibited(scenario):
            return RiskTier.UNACCEPTABLE_RISK
        if self._is_high_impact(scenario):
            return RiskTier.HIGH_RISK
        if self._is_generative(scenario):
            return RiskTier.SPECIFIC_TRANSPARENCY_RISK
        return RiskTier.MINIMAL_RISK

    def _calculate_metrics(self, scenario: Scenario) -> list[EvaluationMetric]:
        """EN: Human-rights safeguards: equality, transparency, accountability and procedural redress. | ES: Salvaguardias de derechos humanos: igualdad, transparencia, rendicion de cuentas y tutela procesal."""
        transparency = 1.0 if self._flag(scenario, "explainability_enabled") else 0.0
        redress = 1.0 if self._flag(scenario, "human_in_the_loop") else 0.0
        privacy_lineage = 1.0 if self._flag(scenario, "provenance_verified") else 0.0
        return [
            self._metric(
                "Equality & Non-Discrimination Gap (Art. 10)",
                self._dialectal_parity_gap(scenario),
                0.15,
                "AI lifecycle must respect equality and prevent discriminatory outcomes.",
                lower_is_better=True,
            ),
            self._metric(
                "Transparency & Oversight (Art. 8)",
                transparency,
                1.0,
                "Adequate transparency and explainability tailored to the context and risks.",
            ),
            self._metric(
                "Procedural Safeguards & Redress (Art. 14-15)",
                redress,
                1.0,
                "Effective procedural guarantees, human review, and access to remedy.",
            ),
            self._metric(
                "Privacy & Data Governance (Art. 11)",
                privacy_lineage,
                1.0,
                "Protection of personal data and verifiable provenance across the AI lifecycle.",
            ),
        ]

    def _audit(self, scenario: Scenario, risk_tier: RiskTier, metrics: list[EvaluationMetric]) -> list[EthicalFinding]:
        """EN: Flag human-rights and rule-of-law violations under CETS No. 225. | ES: Senalar vulneraciones de derechos humanos y Estado de derecho bajo CETS N. 225."""
        if risk_tier == RiskTier.UNACCEPTABLE_RISK:
            return [
                self._finding(
                    "CETS 225: Incompatible Use (Art. 16)",
                    "CRITICAL",
                    f"Domain '{scenario.domain_category}' poses an unacceptable risk to human rights and democratic institutions.",
                    "Prohibit or impose a moratorium on deployments incompatible with fundamental rights (Article 16(4)).",
                )
            ]
        severity = "HIGH" if risk_tier == RiskTier.HIGH_RISK else "MEDIUM"
        fixes = {
            "Equality & Non-Discrimination Gap (Art. 10)": "Eliminate disparate error rates across protected linguistic and demographic groups.",
            "Transparency & Oversight (Art. 8)": "Document system logic, limitations, and error margins for affected individuals and oversight bodies.",
            "Procedural Safeguards & Redress (Art. 14-15)": "Provide notice of AI interaction, independent human review, and an effective right to challenge outcomes.",
            "Privacy & Data Governance (Art. 11)": "Enforce lawful data provenance, privacy safeguards, and Convention 108+ compliance.",
        }
        return [
            self._finding(
                f"CoE Convention: {m.name}",
                severity,
                f"Score {m.score} vs. threshold {m.threshold}.",
                fixes[m.name],
            )
            for m in metrics
            if not m.passed
        ]

    def _steady_state_recommendation(self) -> str:
        """EN: Default Council of Europe AI Convention recommendation. | ES: Recomendacion por defecto del Convenio de IA del Consejo de Europa."""
        return "Conduct periodic human-rights, democracy and rule-of-law impact assessments (HUDERIA) throughout the AI lifecycle."
