"""Run from this folder: python -m unittest -v test_birthday_gen.py"""
import os
from pathlib import Path
import subprocess
import sys
import unittest

import birthday_gen as app

SCRIPT = Path(__file__).with_name("birthday_gen.py")


def run_cli(*args, input_text=""):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--no-delay", "--no-color", *args],
        input=input_text, text=True, encoding="utf-8", capture_output=True,
        timeout=10, env=env,
    )


class BirthdayTests(unittest.TestCase):
    def test_named_run(self):
        result = run_cli("--name", "نور")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("نور", result.stdout)
        self.assertIn("[3/3]", result.stdout)
        self.assertNotIn("\033[", result.stdout)

    def test_blank_cli_name(self):
        result = run_cli("--name", "   ")
        self.assertEqual(result.returncode, 2)
        self.assertIn("فاضي", result.stderr)

    def test_interactive_reroll(self):
        result = run_cli(input_text="نور\n1\n0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("BIRTHDAY WORKFLOW"), 2)

    def test_change_name(self):
        result = run_cli(input_text="نور\n2\nعلي\n0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("تجهيز الاسم: علي", result.stdout)

    def test_empty_name_and_invalid_choice(self):
        result = run_cli(input_text="\nنور\nwrong\n2\n\n0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("الاسم فاضي", result.stdout)
        self.assertIn("اختيار مش معروف", result.stdout)
        self.assertIn("الاسم الحالي زي ما هو", result.stdout)

    def test_eof_at_all_prompts(self):
        for text in ("", "نور\n", "نور\n2\n"):
            with self.subTest(input=text):
                result = run_cli(input_text=text)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_arabic_digits(self):
        result = run_cli(input_text="نور\n١\n٢\nعلي\n٠\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("BIRTHDAY WORKFLOW"), 3)

    def test_dynamic_messages(self):
        previous = None
        messages = set()
        for _ in range(200):
            message = app.generate_message("نور", previous)
            self.assertIn("نور", message)
            self.assertNotEqual(message, previous)
            messages.add(message)
            previous = message
        self.assertGreater(len(messages), 1)

    def test_dynamic_confetti(self):
        previous = None
        for _ in range(200):
            confetti = app.generate_confetti(previous)
            self.assertNotEqual(confetti, previous)
            self.assertEqual(len(confetti.split()), 12)
            previous = confetti


if __name__ == "__main__":
    unittest.main()
