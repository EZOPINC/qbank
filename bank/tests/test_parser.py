from django.test import SimpleTestCase
from bank.extraction.base import Page
from bank.parser import extract_tags, parse_pages, split_options
from bank.normalize import content_hash, detect_language

SAMPLE = """Indian National Movement 133
1. In 1906 Muslim League was founded at [MPPCS (Pre) 1992
Uttarakhand UDA/LDA (Pre) 2007]
(A) Lahore (B) Delhi
(C) Calcutta (D) Dhaka
2. Who was the first President of the
Muslim League? [UPPCS (Pre) 1997]
(A) Agha Khan (B) Hamid Khan
(C) Hasan Khan (D) M.A. Jinnah
Answer Sheet
1. (D) 2. (A)
13. Formation of Muslim League
(1906)
1. Next chapter question
(A) a (B) b (C) c (D) d
"""


class ParserTests(SimpleTestCase):
    def test_split_options_inline(self):
        self.assertEqual(split_options("(A) Lahore (B) Delhi"), [("A", "Lahore"), ("B", "Delhi")])
        self.assertEqual(split_options("not an option"), [])

    def test_extract_tags(self):
        text, tags = extract_tags("Stem [UPPCS (Pre) 1993, 1991] end")
        self.assertNotIn("[", text)
        self.assertEqual([t["year"] for t in tags], [1993, 1991])

    def test_parse_sample_block(self):
        qs = parse_pages([Page(1, SAMPLE, None, "digital")])
        self.assertEqual([q["number"] for q in qs], [1, 2, 1])      # chapter heading skipped
        self.assertEqual(qs[0]["answer"], "D")
        self.assertEqual(qs[0]["options"]["D"], "Dhaka")
        self.assertEqual(len(qs[0]["tags"]), 2)
        self.assertEqual(qs[1]["text"], "Who was the first President of the Muslim League?")
        self.assertIsNone(qs[2]["answer"])                           # never invented
        self.assertIn("missing_answer", qs[2]["flags"])

    def test_statements_not_split_as_questions(self):
        txt = "2. Consider:\n1. First statement\n2. Second statement\n(A) 1 (B) 2 (C) 3 (D) 4\n"
        qs = parse_pages([Page(1, txt, None, "digital")])
        self.assertEqual(len(qs), 1)

    def test_language_and_hash(self):
        self.assertEqual(detect_language("ভারতের রাজধানী কোথায়?"), "bn")
        self.assertEqual(detect_language("भारत की राजधानी"), "hi")
        self.assertEqual(content_hash("Q ", "a", "b", "c", "d"), content_hash("q", "A", "B", "C", "D"))
