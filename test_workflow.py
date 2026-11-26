import unittest
from workflow import run

class WorkflowTests(unittest.TestCase):
    def test_complete(self):
        self.assertEqual(run({"objective":"Demo","acceptance":"Test passes","owner":"Reviewer"})["status"], "structurally_valid")
    def test_repair_needs_review(self):
        result = run({"objective":"Demo"})
        self.assertEqual(result["status"], "review_required")
        self.assertEqual(result["trace"][2]["changed"], ["acceptance","owner"])
    def test_invalid_types(self):
        self.assertEqual(run({"objective":4})["status"], "review_required")
    def test_input_unchanged(self):
        data = {"objective":"Demo"}
        run(data)
        self.assertEqual(data, {"objective":"Demo"})
    def test_existing_draft(self):
        self.assertEqual(run({"objective":"DRAFT: confirm","acceptance":"x","owner":"y"})["status"], "review_required")

if __name__ == "__main__":
    unittest.main()
