from pathlib import Path
import importlib.util
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
PHASE1 = PROJECT / '01-router'
sys.path.insert(0, str(PHASE1))

from factory_router.models import Domain, TaskType
from factory_router.policy import MODEL_IDS

CATALOG = json.loads((ROOT / 'catalog' / 'agent_catalog.json').read_text(encoding='utf-8'))
ROUTE_MAP = json.loads((ROOT / 'catalog' / 'route_agent_map.json').read_text(encoding='utf-8'))

class Phase1ContractTests(unittest.TestCase):
    def test_domains_exist_in_phase1(self):
        valid = {d.value for d in Domain}
        self.assertTrue(set(ROUTE_MAP).issubset(valid), set(ROUTE_MAP) - valid)

    def test_tasks_exist_in_phase1(self):
        valid = {t.value for t in TaskType}
        for domain, task_map in ROUTE_MAP.items():
            unknown = set(task_map) - valid
            self.assertFalse(unknown, (domain, unknown))

    def test_agent_models_match_phase1_model_ids(self):
        valid = set(MODEL_IDS.values())
        for a in CATALOG['agents']:
            self.assertIn(a['model'], valid, a['name'])

    def test_core_router_specialist_targets_exist(self):
        names = {a['name'] for a in CATALOG['agents']}
        for required in {
            'astra_problem_specialist',
            'software_integration_owner',
            'software_astra_debug_specialist',
            'cad_integration_owner',
            'cad_astra_mechanism_specialist',
            'verification_reviewer',
        }:
            self.assertIn(required, names)

if __name__ == '__main__':
    unittest.main(verbosity=2)
