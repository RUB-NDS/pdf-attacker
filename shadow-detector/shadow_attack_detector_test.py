from shadow_attack_detector import *
import unittest

class Test_ShadowAttackDetector(unittest.TestCase):
    def test_check_sig_state(self):
        self.assertEqual(check_sig_state("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed.pdf"), 0)
        self.assertEqual(check_sig_state("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed-signed.pdf"), 1, "No Signature Found")

    def test_shadow_hide_and_hide_replace_detector(self):
        self.assertEqual(shadow_hide_and_hide_replace_detector("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed-signed.pdf"), 0)
        self.assertEqual(shadow_hide_and_hide_replace_detector("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed-signed-manipulated_v1.pdf"), 1)
        self.assertEqual(shadow_hide_and_hide_replace_detector("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed-signed-manipulated_v2.pdf"), 1)

    def test_shadow_hide_preventor(self):
        self.assertEqual(shadow_hide_preventor("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed.pdf"), 1)

class Test_ShadowAttackDetectorIntegration(unittest.TestCase):
    """
    These are very basics tests. Only validating if the file has either
    - no warning (equals 0) or
    - any warnings (greater 0)
    """

    def test_start_preventor_detector_with_honest(self):
        self.assertEqual(start_preventor_detector("./shadow-demo-exploits/hide-and-replace/honest.pdf"), 0)
        self.assertEqual(start_preventor_detector("./shadow-demo-exploits/replace/font/honest.pdf"), 0)
        self.assertEqual(start_preventor_detector("./shadow-demo-exploits/replace/forms/honest.pdf"), 0)

    def test_start_preventor_detector_with_manipulated_hide_form(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/form/hide-from-shadowed-signed-manipulated.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/form/hide-from-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/form/hide-from-shadowed.pdf"), 0)

    def test_start_preventor_detector_with_manipulated_hide_form_and_text(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/form_and_form/shadowed_form_over_form-signed-manipulated_v1.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/form_and_form/shadowed_form_over_form-signed-manipulated_v2.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/form_and_form/shadowed_form_over_form-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/form_and_form/shadowed_form_over_form.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/form_and_text/form_over_text-signed-manipulated.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/form_and_text/form_over_text-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/form_and_text/form_over_text.pdf"), 0)

    def test_start_preventor_detector_with_manipulated_hide_xref_image(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed-signed-manipulated_v1.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed-signed-manipulated_v2.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/xref_image/hide-from-shadowed.pdf"), 0)

    def test_start_preventor_detector_with_manipulated_hide_and_replace(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide-and-replace/hide-and-replace-shadowed-signed-manipulated.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide-and-replace/hide-and-replace-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide-and-replace/hide-and-replace-shadowed.pdf"), 0)

    def test_start_preventor_detector_with_manipulated_replace_font(self):
        self.assertEquals(start_preventor_detector("./shadow-demo-exploits/replace/font/replace-font-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/replace/font/replace-font-shadowed-signed-manipulated.pdf"), 0)

    def test_start_preventor_detector_with_manipulated_replace_form(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/replace/forms/replace-form-shadowed-signed-manipulated.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/replace/forms/replace-form-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/replace/forms/replace-form-shadowed.pdf"), 0)

if __name__ == '__main__':
    unittest.main()