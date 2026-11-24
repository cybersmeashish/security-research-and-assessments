import sys,unittest,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from time_model import interval_decision,study
class TimeTests(unittest.TestCase):
 def test_verified_interior_allowed(self):self.assertEqual(interval_decision(300,60,0,600,True),"allow")
 def test_expiry_boundary_denied(self):self.assertNotEqual(interval_decision(599,1,0,600,True),"allow")
 def test_before_issue_boundary_denied(self):self.assertNotEqual(interval_decision(10,15,0,600,True),"allow")
 def test_unverified_clock_not_current(self):self.assertEqual(interval_decision(300,0,0,600,False),"unverified_clock")
 def test_invalid_values_rejected(self):
  for x in [math.nan,True]:
   with self.assertRaises(ValueError):interval_decision(x,0,0,600,True)
 def test_sound_bound_has_no_unsafe_allow_on_grid(self):
  rows=[x for x in study() if x["radius"]==60];self.assertFalse(any(x["interval_unsafe_allow"] for x in rows));self.assertTrue(any(x["interval_false_deny"] for x in rows))
