from pydantic import BaseModel
from typing import List, Dict, Any

class BCOTemplate(BaseModel):
    template_id: str
    name: str
    description: str
    target_scope: str
    pattern_logic: str # Description of what this pattern looks for
    default_ontology_states: List[str]
    metadata: Dict[str, Any]

class TemplateMarketplace:
    def __init__(self):
        self.templates = {
            "startup_seed": BCOTemplate(
                template_id="startup_seed",
                name="High-Growth Startup Rhythm",
                description="Optimized for rapid iteration and high implementation velocity.",
                target_scope="organization",
                pattern_logic="Looks for high implementation/coordination ratio with short research cycles.",
                default_ontology_states=["implementation", "coordination", "deep_focus"],
                metadata={"category": "rhythm", "industry": "tech"}
            ),
            "oss_maintainer": BCOTemplate(
                template_id="oss_maintainer",
                name="Open Source Maintainer Dynamics",
                description="Models the specific review and coordination patterns of OSS projects.",
                target_scope="team",
                pattern_logic="Prioritizes review and coordination states across geographically distributed members.",
                default_ontology_states=["review", "coordination", "planning"],
                metadata={"category": "collaboration", "type": "remote-first"}
            ),
            "enterprise_platform": BCOTemplate(
                template_id="enterprise_platform",
                name="Enterprise Platform Stability",
                description="Focuses on debugging, review, and rigorous documentation patterns.",
                target_scope="team",
                pattern_logic="Flags low review-to-implementation ratios as coordination risks.",
                default_ontology_states=["debugging", "review", "planning"],
                metadata={"category": "governance", "tier": "enterprise"}
            )
        }

    def list_templates(self) -> List[BCOTemplate]:
        return list(self.templates.values())

    def get_template(self, template_id: str) -> BCOTemplate:
        return self.templates.get(template_id)
