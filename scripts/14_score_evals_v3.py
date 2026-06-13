"""
Semantic eval scorer (v3) - no model, no network, instant.

Replaces v2's exact-keyword matcher with:
  1. Porter stemming   -> empiricism~empirical, discusses~discussion, reveals~reveal
  2. Synonym/concept map (Agile-specific) -> value~valuable, wip~work in progress
  3. Gapped phrase match -> "lightweight framework" matches "lightweight Agile framework"

Usage:
  python scripts/14_score_evals_v3.py [path/to/eval_results.json]
If no path is given, scores the most recent evals/eval_results_*.json.
Prints the v3 (semantic) score next to the v2 (exact) score so the grader
effect is isolated from the model. Also reports the ids 1-10 subset when the
file has all 30 questions, for apples-to-apples comparison with older runs.
"""
import sys
import io
import json
import re
from pathlib import Path
from datetime import datetime

# Avoid Windows cp1252 crashes on any stray non-ascii.
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PHRASE_GAP = 3  # max intervening tokens allowed inside a multi-word keyword


# --------------------------------------------------------------------------
# Vendored Porter stemmer (Martin Porter's algorithm, compact pure-Python).
# --------------------------------------------------------------------------
class PorterStemmer:
    def __init__(self):
        self.b = ""
        self.k = 0
        self.j = 0

    def cons(self, i):
        if self.b[i] in "aeiou":
            return False
        if self.b[i] == "y":
            return True if i == 0 else not self.cons(i - 1)
        return True

    def m(self):
        n, i = 0, 0
        while True:
            if i > self.j:
                return n
            if not self.cons(i):
                break
            i += 1
        i += 1
        while True:
            while True:
                if i > self.j:
                    return n
                if self.cons(i):
                    break
                i += 1
            i += 1
            n += 1
            while True:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i += 1
            i += 1

    def vowelinstem(self):
        return any(not self.cons(i) for i in range(self.j + 1))

    def doublec(self, j):
        if j < 1 or self.b[j] != self.b[j - 1]:
            return False
        return self.cons(j)

    def cvc(self, i):
        if i < 2 or not self.cons(i) or self.cons(i - 1) or not self.cons(i - 2):
            return False
        return self.b[i] not in "wxy"

    def ends(self, s):
        length = len(s)
        if length > self.k + 1:
            return False
        if self.b[self.k - length + 1:self.k + 1] != s:
            return False
        self.j = self.k - length
        return True

    def setto(self, s):
        self.b = self.b[:self.j + 1] + s + self.b[self.j + len(s) + 1:]
        self.k = self.j + len(s)

    def r(self, s):
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        if self.b[self.k] == "s":
            if self.ends("sses"):
                self.k -= 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != "s":
                self.k -= 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k -= 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j
            if self.ends("at"):
                self.setto("ate")
            elif self.ends("bl"):
                self.setto("ble")
            elif self.ends("iz"):
                self.setto("ize")
            elif self.doublec(self.k):
                self.k -= 1
                if self.b[self.k] in "lsz":
                    self.k += 1
            elif self.m() == 1 and self.cvc(self.k):
                self.setto("e")

    def step1c(self):
        if self.ends("y") and self.vowelinstem():
            self.b = self.b[:self.k] + "i" + self.b[self.k + 1:]

    def step2(self):
        if self.k < 1:
            return
        ch = self.b[self.k - 1]
        pairs = {
            "a": [("ational", "ate"), ("tional", "tion")],
            "c": [("enci", "ence"), ("anci", "ance")],
            "e": [("izer", "ize")],
            "l": [("bli", "ble"), ("alli", "al"), ("entli", "ent"),
                  ("eli", "e"), ("ousli", "ous")],
            "o": [("ization", "ize"), ("ation", "ate"), ("ator", "ate")],
            "s": [("alism", "al"), ("iveness", "ive"), ("fulness", "ful"),
                  ("ousness", "ous")],
            "t": [("aliti", "al"), ("iviti", "ive"), ("biliti", "ble")],
            "g": [("logi", "log")],
        }
        for suf, rep in pairs.get(ch, []):
            if self.ends(suf):
                self.r(rep)
                return

    def step3(self):
        ch = self.b[self.k]
        pairs = {
            "e": [("icate", "ic"), ("ative", ""), ("alize", "al")],
            "i": [("iciti", "ic")],
            "l": [("ical", "ic"), ("ful", "")],
            "s": [("ness", "")],
        }
        for suf, rep in pairs.get(ch, []):
            if self.ends(suf):
                self.r(rep)
                return

    def step4(self):
        ch = self.b[self.k - 1]
        suffixes = {
            "a": ["al"], "c": ["ance", "ence"], "e": ["er"], "i": ["ic"],
            "l": ["able", "ible"], "n": ["ant", "ement", "ment", "ent"],
            "o": ["ion", "ou"], "s": ["ism"], "t": ["ate", "iti"],
            "u": ["ous"], "v": ["ive"], "z": ["ize"],
        }
        for suf in suffixes.get(ch, []):
            if self.ends(suf):
                if suf == "ion" and not (self.j >= 0 and self.b[self.j] in "st"):
                    return
                if self.m() > 1:
                    self.k = self.j
                return

    def step5(self):
        self.j = self.k
        if self.b[self.k] == "e":
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k - 1)):
                self.k -= 1
        if self.b[self.k] == "l" and self.doublec(self.k) and self.m() > 1:
            self.k -= 1

    def stem(self, w):
        w = w.lower()
        if len(w) <= 2:
            return w
        try:
            self.b, self.k, self.j = w, len(w) - 1, len(w) - 1
            self.step1ab()
            self.step1c()
            self.step2()
            self.step3()
            self.step4()
            self.step5()
            return self.b[:self.k + 1]
        except Exception:
            return w


_PS = PorterStemmer()


def stem_tokens(text):
    return [_PS.stem(t) for t in re.findall(r"[a-z0-9]+", text.lower())]


# --------------------------------------------------------------------------
# Agile synonym / concept map. Keys are the eval keywords; values are alternate
# surface forms that mean the same thing. Stemming already covers plurals and
# simple inflections, so this only lists genuine concept variants.
# --------------------------------------------------------------------------
SYNONYMS = {
    "lightweight framework": ["lightweight agile framework"],
    "empiricism": ["empirical", "empirical process control"],
    "iterative": ["incremental", "iteration", "increment"],
    "value": ["valuable", "benefit", "worth"],
    "15 minutes": ["15-minute", "fifteen minutes", "15 minute", "timeboxed to 15"],
    "inspect progress": ["inspect", "inspection"],
    "plan": ["planning", "next 24 hours", "actionable plan"],
    "work in progress": ["wip"],
    "multitasking": ["context switching", "multi-tasking"],
    "bottleneck": ["constraint", "pile up", "piling up"],
    "standard": ["quality measure", "quality criteria", "criteria", "quality standard"],
    "transparent": ["transparency", "shared understanding", "visible"],
    "complete": ["done", "finished", "releasable"],
    "no action": ["without action", "no action item", "nothing of value",
                  "no improvement", "no concrete", "produces nothing"],
    "improvement": ["improve", "actionable improvement"],
    "continuous": ["continual", "ongoing", "every sprint"],
    "simultaneous": ["at the same time", "all at once", "privately then reveal"],
    "discussion": ["discuss", "explain", "reasoning"],
    "reveal": ["show their cards", "show cards", "turn over"],
    "scope": ["scope change", "total scope", "added work"],
    "visible": ["shows", "makes visible", "reveals"],
    "percentage": ["ratio", "percent", "proportion"],
    "smallest": ["minimal", "simplest", "minimum", "least"],
    "red": ["failing test", "write a failing"],
    "green": ["passing test", "make it pass", "minimal code"],
    "build": ["compilation", "compile"],
    "daily": ["multiple times a day", "every day", "several times a day", "frequently"],
    "psychological safety": ["safe", "safety", "without fear", "blame-free"],
    "best job": ["did the best", "best they could", "best job they could"],
    "scaled agile framework": ["safe framework", "safe is"],
    "agile release train": ["release train", "art"],
    "representative": ["ambassador", "one member from each", "delegate"],
    "definition of done": ["dod", "done criteria"],
    "work in progress (wip)": ["wip"],
}


def phrase_in(needle_stems, hay_stems):
    """Ordered subsequence match allowing up to PHRASE_GAP gaps between tokens."""
    if not needle_stems:
        return False
    if len(needle_stems) == 1:
        return needle_stems[0] in hay_stems
    pos = -1
    for tok in needle_stems:
        found = -1
        for i in range(pos + 1, len(hay_stems)):
            if hay_stems[i] == tok:
                if pos >= 0 and i - pos - 1 > PHRASE_GAP:
                    break
                found = i
                break
        if found == -1:
            return False
        pos = found
    return True


def keyword_found(keyword, answer_stems):
    candidates = [keyword] + SYNONYMS.get(keyword.lower(), [])
    for cand in candidates:
        if phrase_in(stem_tokens(cand), answer_stems):
            return True
    return False


# --------------------------------------------------------------------------
def exact_found(keyword, answer_lower):
    return re.search(r"\b" + re.escape(keyword.lower()) + r"\b", answer_lower) is not None


DIFF_MULT = {"easy": 1.0, "medium": 1.5, "hard": 2.0}


def score_file(path):
    results = json.load(open(path, encoding="utf-8"))

    sem_total = sem_max = ex_total = ex_max = 0.0
    sem_by_id = {}
    cat_scores = {}

    print("=" * 64)
    print(f"Scoring (v3 semantic): {Path(path).name}")
    print("=" * 64)

    for r in results:
        ans = r["mini_me_answer"]
        ans_stems = stem_tokens(ans)
        ans_lower = ans.lower()
        kws = r["expected_keywords"]
        mult = DIFF_MULT[r["difficulty"]]

        if len(ans.strip()) < 20:
            sem_hits, ex_hits = [], []
        else:
            sem_hits = [k for k in kws if keyword_found(k, ans_stems)]
            ex_hits = [k for k in kws if exact_found(k, ans_lower)]

        sem_total += len(sem_hits) * mult
        sem_max += len(kws) * mult
        ex_total += len(ex_hits) * mult
        ex_max += len(kws) * mult
        sem_by_id[r["id"]] = (len(sem_hits) * mult, len(kws) * mult)

        cat = r["category"]
        c = cat_scores.setdefault(cat, [0.0, 0.0])
        c[0] += len(sem_hits) * mult
        c[1] += len(kws) * mult

        pct = len(sem_hits) / len(kws) * 100 if kws else 0
        tag = "PASS" if pct >= 70 else "PART" if pct >= 40 else "FAIL"
        delta = len(sem_hits) - len(ex_hits)
        flag = f"  (+{delta} vs exact)" if delta else ""
        print(f"[{tag}] Q{r['id']:<2} {pct:3.0f}%  "
              f"sem {len(sem_hits)}/{len(kws)}  exact {len(ex_hits)}/{len(kws)}{flag}")
        missing = [k for k in kws if k not in sem_hits]
        if missing:
            print(f"        still missing: {', '.join(missing)}")

    sem_pct = sem_total / sem_max * 100 if sem_max else 0
    ex_pct = ex_total / ex_max * 100 if ex_max else 0

    print("-" * 64)
    print(f"SEMANTIC (v3): {sem_total:.1f}/{sem_max:.1f} = {sem_pct:.1f}%")
    print(f"EXACT    (v2): {ex_total:.1f}/{ex_max:.1f} = {ex_pct:.1f}%")
    print(f"Grader lift:   +{sem_pct - ex_pct:.1f} points (same answers)")

    if all(i in sem_by_id for i in range(1, 11)):
        s = sum(sem_by_id[i][0] for i in range(1, 11))
        m = sum(sem_by_id[i][1] for i in range(1, 11))
        print(f"\nOriginal ids 1-10 subset (semantic): {s:.1f}/{m:.1f} = {s / m * 100:.1f}%")

    print("\nCATEGORY BREAKDOWN (semantic):")
    for cat, (sc, mx) in sorted(cat_scores.items()):
        print(f"  {cat:<22} {sc / mx * 100:5.1f}%")

    report = {
        "timestamp": datetime.now().isoformat(),
        "eval_file": str(path),
        "grader": "v3-semantic (porter stem + synonyms + gapped phrase)",
        "semantic_percentage": sem_pct,
        "exact_percentage": ex_pct,
        "category_scores": {k: v[0] / v[1] * 100 for k, v in cat_scores.items()},
    }
    out = f"evals/score_report_v3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    json.dump(report, open(out, "w", encoding="utf-8"), indent=2)
    print(f"\nSaved: {out}")
    return sem_pct


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        files = sorted(Path("evals").glob("eval_results_*.json"))
        if not files:
            print("No eval results found.")
            sys.exit(1)
        path = str(files[-1])
    score_file(path)


if __name__ == "__main__":
    main()
