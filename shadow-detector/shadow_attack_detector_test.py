from shadow_attack_detector import *
import unittest

class Test_ShadowAttackDetector(unittest.TestCase):
    def test_check_sig_state(self):
        self.assertEqual(check_sig_state("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed.pdf"), 0)
        self.assertEqual(check_sig_state("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed-signed.pdf"), 1, "No Signature Found")

    def test_shadow_hide_and_hide_replace_detector(self):
        self.assertEqual(shadow_hide_and_hide_replace_detector("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed-signed.pdf"), 0)
        self.assertEqual(shadow_hide_and_hide_replace_detector("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed-signed-manipulated.pdf"), 1)

    def test_shadow_hide_preventor(self):
        self.assertEqual(shadow_hide_preventor("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed.pdf"), 1)


if __name__ == '__main__':
    unittest.main()