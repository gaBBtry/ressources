"""Tests du site. Lancer depuis la racine du dépôt : python3 -m unittest"""
import json
import re
import sys
import types
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PARCOURS = RACINE / "python-lycee"
PAGE = (PARCOURS / "index.html").read_text(encoding="utf-8")


def constante_js(nom):
    """Valeur JSON d'une ligne « const NOM = ...; » de la page."""
    m = re.search(r"^const " + nom + r" = (.*);$", PAGE, re.M)
    return json.loads(m.group(1))


DATA = constante_js("DATA")


def harnais():
    ns = {}
    exec(constante_js("HARNESS"), ns)
    return ns["executer"]


class LivretPDF(unittest.TestCase):
    def test_le_livret_existe_et_la_page_y_renvoie(self):
        self.assertTrue((PARCOURS / "livret-python-terminale.pdf").is_file())
        self.assertIn('href="livret-python-terminale.pdf"', PAGE)


class PolicesLocales(unittest.TestCase):
    def test_aucune_page_ne_contacte_google_fonts(self):
        for page in RACINE.rglob("*.html"):
            self.assertNotIn("fonts.googleapis.com", page.read_text(encoding="utf-8"), page)
            self.assertNotIn("fonts.gstatic.com", page.read_text(encoding="utf-8"), page)

    def test_les_fichiers_de_police_existent(self):
        css = (PARCOURS / "fonts" / "fonts.css").read_text(encoding="utf-8")
        urls = re.findall(r"url\(([^)]+)\)", css)
        self.assertTrue(urls)
        for u in urls:
            self.assertTrue((PARCOURS / "fonts" / u).is_file(), u)
        self.assertIn('href="fonts/fonts.css"', PAGE)

    def test_la_licence_des_polices_est_fournie(self):
        self.assertIn("SIL OPEN FONT LICENSE", (PARCOURS / "fonts" / "OFL.txt").read_text(encoding="utf-8"))


class MentionsLegales(unittest.TestCase):
    def test_la_page_existe_et_est_liee(self):
        texte = (RACINE / "mentions-legales.html").read_text(encoding="utf-8")
        self.assertIn("Hébergeur", texte)
        self.assertIn("GitHub", texte)
        self.assertIn('href="/mentions-legales.html"', PAGE)


class Clavier(unittest.TestCase):
    def test_chaque_aide_clavier_indique_comment_sortir_de_l_editeur(self):
        aides = re.findall(r'<span class="hint-k">(.*?)</span>', PAGE)
        self.assertEqual(len(aides), 3)
        for aide in aides:
            self.assertIn("<kbd>Échap</kbd>", aide)


class Execution(unittest.TestCase):
    def test_aucun_code_de_depart_ne_tourne_sans_fin(self):
        executer = harnais()
        for m in DATA:
            for e in m["exercices"]:
                if "np" in e["depart"]:
                    continue  # numpy n'est pas installé pour les tests
                with self.subTest(e["id"]):
                    r = json.loads(executer(e["depart"], e["test"], 1.0))
                    self.assertNotEqual(r["type"], "Delai")
                    self.assertFalse(r["ok"])

    def test_input_pose_la_question_dans_la_fenetre_et_garde_la_reponse_dans_la_sortie(self):
        questions = []
        faux_js = types.ModuleType("js")
        faux_js.prompt = lambda q: questions.append(q) or "42"
        sys.modules["js"] = faux_js
        try:
            r = json.loads(harnais()('x = input("Ton âge ? ")\nprint("âge", x)'))
        finally:
            del sys.modules["js"]
        self.assertEqual(questions, ["Ton âge ? "])
        self.assertEqual(r["sortie"], "Ton âge ? 42\nâge 42\n")


class Page(unittest.TestCase):
    def test_pas_de_code_mort_de_paquets(self):
        self.assertNotIn("MANIFEST", PAGE)

    def test_balises_de_partage(self):
        for prop in ("og:title", "og:description", "og:type", "og:url", "og:locale"):
            self.assertIn('<meta property="' + prop + '"', PAGE)

    def test_la_licence_est_indiquee(self):
        self.assertIn("CC BY-NC-SA 4.0", (RACINE / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
