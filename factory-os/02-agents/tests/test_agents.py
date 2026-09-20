from pathlib import Path
import json
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / "agents"
CATALOG = json.loads((ROOT / "catalog" / "agent_catalog.json").read_text(encoding="utf-8"))
ROUTE_MAP = json.loads((ROOT / "catalog" / "route_agent_map.json").read_text(encoding="utf-8"))
ALLOWED_MODELS = {"gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol", "gpt-5.6", "gpt-6-astra"}
ALLOWED_EFFORTS = {"low", "medium", "high", "xhigh", "max", "none"}
ALLOWED_SANDBOX = {"read-only", "workspace-write"}

class AgentLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = sorted(AGENT_DIR.glob("*.toml"))
        cls.parsed = [tomllib.loads(p.read_text(encoding="utf-8")) for p in cls.files]
        cls.by_name = {a["name"]: a for a in cls.parsed}

    def test_minimum_library_size(self):
        self.assertGreaterEqual(len(self.files), 24)

    def test_required_fields_and_values(self):
        for a in self.parsed:
            for key in ("name", "description", "developer_instructions", "model", "model_reasoning_effort", "sandbox_mode"):
                self.assertIn(key, a, (a.get("name"), key))
                self.assertTrue(str(a[key]).strip(), (a.get("name"), key))
            self.assertIn(a["model"], ALLOWED_MODELS)
            self.assertIn(a["model_reasoning_effort"], ALLOWED_EFFORTS)
            self.assertIn(a["sandbox_mode"], ALLOWED_SANDBOX)

    def test_names_unique_and_filenames_match(self):
        names = [a["name"] for a in self.parsed]
        self.assertEqual(len(names), len(set(names)))
        for p, a in zip(self.files, self.parsed):
            self.assertEqual(p.stem, a["name"])

    def test_catalog_matches_native_files(self):
        catalog_names = {a["name"] for a in CATALOG["agents"]}
        self.assertEqual(catalog_names, set(self.by_name))
        for c in CATALOG["agents"]:
            n = c["name"]
            self.assertEqual(c["model"], self.by_name[n]["model"])
            self.assertEqual(c["effort"], self.by_name[n]["model_reasoning_effort"])
            self.assertEqual(c["sandbox"], self.by_name[n]["sandbox_mode"])

    def test_astra_is_read_only_and_bounded(self):
        astras = [a for a in self.parsed if a["model"] == "gpt-6-astra"]
        self.assertGreaterEqual(len(astras), 3)
        for a in astras:
            self.assertEqual(a["sandbox_mode"], "read-only", a["name"])
            text = (a["description"] + " " + a["developer_instructions"]).lower()
            self.assertTrue("specialist" in text or "bottleneck" in text)

    def test_integration_owners_are_sol_writers(self):
        for name in ("software_integration_owner", "cad_integration_owner"):
            a = self.by_name[name]
            self.assertIn(a["model"], {"gpt-5.6", "gpt-5.6-sol"})
            self.assertEqual(a["sandbox_mode"], "workspace-write")
            self.assertEqual(a["model_reasoning_effort"], "high")

    def test_explorers_do_not_write(self):
        for name in ("general_explorer", "software_repo_mapper", "cad_geometry_inspector", "research_scout"):
            self.assertEqual(self.by_name[name]["sandbox_mode"], "read-only")

    def test_route_map_only_names_existing_agents(self):
        for domain, task_map in ROUTE_MAP.items():
            for task, names in task_map.items():
                self.assertTrue(names, (domain, task))
                for n in names:
                    self.assertIn(n, self.by_name, (domain, task, n))

    def test_no_danger_full_access(self):
        for a in self.parsed:
            self.assertNotEqual(a["sandbox_mode"], "danger-full-access")

    def test_writers_are_not_luna_or_astra(self):
        for a in self.parsed:
            if a["sandbox_mode"] == "workspace-write":
                self.assertIn(a["model"], {"gpt-5.6-terra", "gpt-5.6-sol", "gpt-5.6"}, a["name"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
