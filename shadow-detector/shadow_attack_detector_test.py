from shadow_attack_detector import check_sig_state, start_preventor_detector, preventor, shadow_hide_and_hide_replace_detector, shadow_hide_form_detector, shadow_replace_font_detector, shadow_replace_form_detector
import unittest

class Test_ShadowAttackDetector(unittest.TestCase):
    def test_check_sig_state(self):
        self.assertEqual(check_sig_state("./shadow-demo-exploits/hide/variant-1_hide-via-referenced-object/1_original-document.pdf"), 0)
        self.assertEqual(check_sig_state("./shadow-demo-exploits/hide/variant-1_hide-via-referenced-object/3_original-document-shadowed-signed.pdf"), 1, "No Signature Found")

    def test_shadow_hide_variant_1(self):
        self.assertEqual(preventor("./shadow-demo-exploits/hide/variant-1_hide-via-referenced-object/2_original-document-shadowed.pdf"), 1)
        self.assertEqual(preventor("./shadow-demo-exploits/hide/variant-1_hide-via-referenced-object/3_original-document-shadowed-signed.pdf"), 1)
        self.assertEqual(preventor("./shadow-demo-exploits/hide/variant-1_hide-via-referenced-object/4_original-document-shadowed-signed-manipulated_v1.pdf"), 1)
        self.assertEqual(shadow_hide_and_hide_replace_detector("./shadow-demo-exploits/hide/variant-1_hide-via-referenced-object/4_original-document-shadowed-signed-manipulated_v2.pdf"), 1)

    def test_shadow_hide_variant_2(self):
        self.assertEqual(preventor("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-form-via-form/2_original-document-shadowed.pdf"), 2)
        self.assertEqual(preventor("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-form-via-form/3_original-document-shadowed-signed.pdf"), 2)
        self.assertEqual(shadow_hide_form_detector("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-form-via-form/4_original-document-shadowed-signed-manipulated.pdf"), 2)

    def test_shadow_hide_variant_2_form(self):
        self.assertEqual(preventor("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-form-via-form/2_original-document-shadowed.pdf"), 2)
        self.assertEqual(preventor("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-form-via-form/3_original-document-shadowed-signed.pdf"), 2)
        self.assertEqual(shadow_hide_form_detector("shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-form-via-form/4_original-document-shadowed-signed-manipulated.pdf"), 0)
        self.assertEqual(shadow_hide_and_hide_replace_detector("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-form-via-form/4_original-document-shadowed-signed-manipulated.pdf"), 0)

    def test_shadow_hide_variant_2_text(self):
        self.assertEqual(preventor("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-text-via-form/2_original-document-shadowed.pdf"), 2)
        self.assertEqual(preventor("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-text-via-form/3_original-document-shadowed-signed.pdf"), 2)
        self.assertEqual(shadow_hide_form_detector("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-text-via-form/4_original-document-shadowed-signed-manipulated.pdf"), 2)

    def test_replace_variant_1(self):
        self.assertEqual(preventor("./shadow-demo-exploits/replace/variant-1_replace-via-overlay/2_original-document-shadowed.pdf"), 1)
        self.assertEqual(preventor("./shadow-demo-exploits/replace/variant-1_replace-via-overlay/3_original-document-shadowed-signed.pdf"), 1)
        self.assertEqual(shadow_replace_form_detector("./shadow-demo-exploits/replace/variant-1_replace-via-overlay/4_original-document-shadowed-signed-manipulated.pdf"), 1)

    def test_replace_variant_2(self):
        self.assertEquals(shadow_replace_font_detector("./shadow-demo-exploits/replace/variant-2_replace-via-overwrite/4_original-document-shadowed-signed-manipulated.pdf"), 1)

    def test_shadow_hide_and_replace_variant_1(self):
        self.assertEqual(preventor("./shadow-demo-exploits/hide-and-replace/variant-1_change_object_references/2_original-document-shadowed.pdf"), 13)
        self.assertEqual(preventor("./shadow-demo-exploits/hide-and-replace/variant-1_change_object_references/3_original-document-shadowed-signed.pdf"), 15)
        self.assertEqual(shadow_hide_and_hide_replace_detector("./shadow-demo-exploits/hide-and-replace/variant-1_change_object_references/4_original-document-shadowed-signed-manipulated.pdf"), 14)

class Test_ShadowAttackDetectorIntegration(unittest.TestCase):
    """
    These are very basics tests. Only validating if the file has either
    - no warning (equals 0) or
    - any warnings (greater 0)
    """

    def test_start_preventor_detector_with_honest(self):
        self.assertEqual(start_preventor_detector("./shadow-demo-exploits/hide/variant-1_hide-via-referenced-object/1_original-document.pdf"), 0)
        self.assertEqual(start_preventor_detector("./shadow-demo-exploits/hide-and-replace/variant-1_change_object_references/1_original-document.pdf"), 0)
        self.assertEqual(start_preventor_detector("./shadow-demo-exploits/replace/variant-2_replace-via-overwrite/1_original-document.pdf"), 0)
        self.assertEqual(start_preventor_detector("./shadow-demo-exploits/replace/variant-1_replace-via-overlay/1_original-document.pdf"), 0)

    def test_start_preventor_detector_with_hide_variant_1(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/variant-1_hide-via-referenced-object/4_original-document-shadowed-signed-manipulated_v1.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/variant-1_hide-via-referenced-object/4_original-document-shadowed-signed-manipulated_v2.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/variant-1_hide-via-referenced-object/3_original-document-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/variant-1_hide-via-referenced-object/2_original-document-shadowed.pdf"), 0)

    def test_start_preventor_detector_with_hide_variant_2_form(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-form-via-form/4_original-document-shadowed-signed-manipulated.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-form-via-form/3_original-document-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-form-via-form/2_original-document-shadowed.pdf"), 0)

    def test_start_preventor_detector_with_hide_variant_2_text(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-text-via-form/2_original-document-shadowed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-text-via-form/3_original-document-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide/variant-2_hide-via-referenced-object/hide-text-via-form/4_original-document-shadowed-signed-manipulated.pdf"), 0)

    def test_start_preventor_detector_with_replace_variant_1(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/replace/variant-1_replace-via-overlay/2_original-document-shadowed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/replace/variant-1_replace-via-overlay/3_original-document-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/replace/variant-1_replace-via-overlay/4_original-document-shadowed-signed-manipulated.pdf"), 0)

    def test_start_preventor_detector_with_replace_variant_2(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/replace/variant-2_replace-via-overwrite/2_original-document-shadowed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/replace/variant-2_replace-via-overwrite/3_original-document-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/replace/variant-2_replace-via-overwrite/4_original-document-shadowed-signed-manipulated.pdf"), 0)

    def test_start_preventor_detector_with_hide_and_replace_variant_1(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide-and-replace/variant-1_change_object_references/2_original-document-shadowed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide-and-replace/variant-1_change_object_references/3_original-document-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide-and-replace/variant-1_change_object_references/4_original-document-shadowed-signed-manipulated.pdf"), 0)

    def test_start_preventor_detector_with_hide_and_replace_variant_2(self):
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide-and-replace/variant-2_change_objects_usage/2_original-document-shadowed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide-and-replace/variant-2_change_objects_usage/3_original-document-shadowed-signed.pdf"), 0)
        self.assertGreater(start_preventor_detector("./shadow-demo-exploits/hide-and-replace/variant-2_change_objects_usage/4_original-document-shadowed-signed-manipulated.pdf"), 0)

if __name__ == '__main__':
    unittest.main()