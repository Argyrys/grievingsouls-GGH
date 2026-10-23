import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import lexical  # noqa: E402


class LexicalBlockTests(unittest.TestCase):
    """URLs that must be auto-blocked without rendering or Gemini."""

    def test_leetspeak_paypal(self):
        v = lexical.check_url("https://paypa1.com/")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "block")
        self.assertTrue(v.is_phishing)
        self.assertEqual(v.tier, "lexical")
        self.assertEqual(v.brand_impersonated, "PayPal")
        self.assertGreaterEqual(v.confidence_score, 0.75)

    def test_leetspeak_netflix(self):
        v = lexical.check_url("https://netfl1x.com/")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "block")
        self.assertEqual(v.brand_impersonated, "Netflix")

    def test_brand_in_wrong_domain(self):
        v = lexical.check_url("https://microsoft-login.com/")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "block")
        self.assertEqual(v.brand_impersonated, "Microsoft")

    def test_forged_multi_label_host(self):
        v = lexical.check_url("https://microsoft-secure.login-verify.xyz/")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "block")
        self.assertEqual(v.brand_impersonated, "Microsoft")

    def test_fuzzy_typo_google(self):
        v = lexical.check_url("https://gogle.com/")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "block")
        self.assertEqual(v.brand_impersonated, "Google")

    def test_at_decoy_trick(self):
        v = lexical.check_url("https://paypal.com@evil.example/")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "block")

    def test_public_ip_with_brand_path(self):
        v = lexical.check_url("http://45.33.32.156/paypal/login")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "block")

    def test_swiggy_lookalike(self):
        v = lexical.check_url("https://swiggy-account-verify.top/")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "block")


class LexicalAllowTests(unittest.TestCase):
    """Registered brand domains are allowed instantly."""

    def test_github_allow(self):
        v = lexical.check_url("https://github.com/")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "allow")
        self.assertFalse(v.is_phishing)
        self.assertEqual(v.tier, "lexical")
        self.assertEqual(v.brand_impersonated, "GitHub")

    def test_paypal_allow(self):
        v = lexical.check_url("https://paypal.com/login")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "allow")
        self.assertEqual(v.brand_impersonated, "PayPal")

    def test_microsoft_subdomain_allow(self):
        v = lexical.check_url("https://login.microsoftonline.com/common/oauth2")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "allow")

    def test_suffix_spoof_is_not_trusted(self):
        v = lexical.check_url("https://paypal.com.secure-host.xyz/")
        self.assertIsNotNone(v)
        self.assertEqual(v.recommended_action, "block")


class LexicalEscalateTests(unittest.TestCase):
    """Ambiguous URLs return None -> multimodal pipeline decides."""

    def test_localhost_always_escalates(self):
        self.assertIsNone(lexical.check_url("http://127.0.0.1:8000/mocks/ms-login-canvas.html"))
        self.assertIsNone(lexical.check_url("http://localhost:8000/mocks/chase-mfa.html"))

    def test_private_ip_escalates(self):
        self.assertIsNone(lexical.check_url("http://192.168.1.10/"))

    def test_ordinary_site_escalates(self):
        self.assertIsNone(lexical.check_url("https://example.org/articles/hello"))

    def test_low_signal_lookalike_escalates(self):
        # Weak TLD-only signal without a brand token stays under threshold.
        self.assertIsNone(lexical.check_url("https://myblognotes.xyz/"))


class LeetHelperTests(unittest.TestCase):
    def test_lev1(self):
        self.assertTrue(lexical._lev_within_1("gogle", "google"))
        self.assertTrue(lexical._lev_within_1("paypal", "paypal"))
        self.assertTrue(lexical._lev_within_1("paypai", "paypal"))
        self.assertFalse(lexical._lev_within_1("chase", "paypal"))
        self.assertFalse(lexical._lev_within_1("chat", "chase"))

    def test_leet_variants(self):
        self.assertIn("paypal", lexical._leet_variants("paypa1"))
        self.assertIn("netflix", lexical._leet_variants("netfl1x"))


if __name__ == "__main__":
    unittest.main()
