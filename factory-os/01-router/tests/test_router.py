import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'01-router'))
from factory_router.models import *
from factory_router.router import route_task
class RouterTests(unittest.TestCase):
 def r(self,**kw): return route_task(TaskContract.from_dict(kw))
 def test_chat_sol(self): self.assertEqual(self.r(domain='general',task_type='chat').primary.tier,ModelTier.SOL)
 def test_simple_impl_terra(self): self.assertEqual(self.r(domain='software',task_type='implementation',complexity=2,uncertainty=1).primary.tier,ModelTier.TERRA)
 def test_hard_debug_astra_specialist(self): self.assertIsNotNone(self.r(domain='software',task_type='debug',complexity=5,uncertainty=5,novelty=4,failure_count=2).specialist)
 def test_cad_edit_terra(self): self.assertEqual(self.r(domain='cad_3dp',task_type='cad_edit',complexity=2,uncertainty=1).primary.tier,ModelTier.TERRA)
 def test_hard_mechanism_has_specialist(self): self.assertIsNotNone(self.r(domain='cad_3dp',task_type='mechanism_design',complexity=5,uncertainty=4,novelty=4).specialist)
 def test_overlap_single_writer(self): self.assertEqual(self.r(domain='software',task_type='implementation',write_overlap_risk=5,parallelizability=5).parallelism.write_workers,1)
 def test_strong_verification_reduces_score(self):
  a=self.r(domain='software',task_type='implementation',complexity=3,uncertainty=3,verification_strength=5,deterministic_tools_available=True)
  b=self.r(domain='software',task_type='implementation',complexity=3,uncertainty=3,verification_strength=1,deterministic_tools_available=False)
  self.assertLess(a.score,b.score)
 def test_repeated_failures_escalate(self): self.assertEqual(self.r(domain='software',task_type='implementation',failure_count=4).primary.tier,ModelTier.ASTRA)
 def test_eco_hard_debug_not_below_sol(self): self.assertEqual(self.r(domain='software',task_type='debug',complexity=5,uncertainty=4,budget_mode='eco').primary.tier,ModelTier.SOL)
if __name__=='__main__': unittest.main()
