import json
import re
from pathlib import Path
from datetime import datetime

print("="*60)
print("📊 Scoring Mini Me Evaluation Results (v2 - Improved)")
print("="*60)

# Find the latest eval results file
eval_files = sorted(Path("evals").glob("eval_results_*.json"))
if not eval_files:
    print("❌ No evaluation results found! Run scripts/13_run_evals.py first.")
    exit(1)

latest_file = eval_files[-1]
print(f"\n📁 Scoring: {latest_file.name}")

# Load results with validation
try:
    with open(latest_file, "r", encoding="utf-8") as f:
        results = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON in results file: {e}")
    exit(1)

# Validate structure
required_fields = ["id", "question", "expected_keywords", "mini_me_answer", "difficulty"]
for result in results:
    for field in required_fields:
        if field not in result:
            print(f"❌ Missing required field '{field}' in question {result.get('id', 'unknown')}")
            exit(1)

print(f"✓ Loaded {len(results)} results")

# Improved keyword matching with word boundaries
def keyword_match(answer, keywords):
    """Match keywords with word boundaries to avoid false positives"""
    answer_lower = answer.lower()
    found = []
    missing = []
    
    for keyword in keywords:
        # Use word boundary regex to avoid "plan" matching "plantation"
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, answer_lower):
            found.append(keyword)
        else:
            missing.append(keyword)
    
    return found, missing

# Score each answer
print("\n🔍 Scoring answers...\n")
total_score = 0
max_score = 0
category_scores = {}

for result in results:
    question = result["question"]
    answer = result["mini_me_answer"]
    expected_keywords = result["expected_keywords"]
    category = result["category"]
    difficulty = result["difficulty"]
    
    # Check minimum answer length
    if len(answer.strip()) < 20:
        print(f"⚠️  Q{result['id']}: Answer too short ({len(answer)} chars)")
        keyword_score = 0
        found_keywords = []
        missing_keywords = expected_keywords
    else:
        # Improved keyword matching
        found_keywords, missing_keywords = keyword_match(answer, expected_keywords)
        keyword_score = len(found_keywords)
    
    max_possible = len(expected_keywords)
    
    # Difficulty multiplier (harder questions worth more)
    difficulty_multiplier = {
        "easy": 1.0,
        "medium": 1.5,
        "hard": 2.0
    }
    
    weighted_score = keyword_score * difficulty_multiplier[difficulty]
    weighted_max = max_possible * difficulty_multiplier[difficulty]
    
    total_score += weighted_score
    max_score += weighted_max
    
    # Track category scores
    if category not in category_scores:
        category_scores[category] = {"score": 0, "max": 0, "count": 0}
    category_scores[category]["score"] += weighted_score
    category_scores[category]["max"] += weighted_max
    category_scores[category]["count"] += 1
    
    # Print result
    percentage = (keyword_score / max_possible * 100) if max_possible > 0 else 0
    status = "✅" if percentage >= 70 else "⚠️" if percentage >= 40 else "❌"
    
    print(f"{status} Q{result['id']}: {question[:50]}...")
    print(f"   Score: {keyword_score}/{max_possible} keywords ({percentage:.0f}%)")
    if found_keywords:
        print(f"   ✓ Found: {', '.join(found_keywords)}")
    if missing_keywords:
        print(f"   ✗ Missing: {', '.join(missing_keywords)}")
    print()

# Calculate overall score
overall_percentage = (total_score / max_score * 100) if max_score > 0 else 0

print("="*60)
print("📊 OVERALL RESULTS")
print("="*60)
print(f"\n🎯 Total Score: {total_score:.1f} / {max_score:.1f} ({overall_percentage:.1f}%)")

# Grade
if overall_percentage >= 90:
    grade = "A+ (Excellent!)"
elif overall_percentage >= 80:
    grade = "A (Great!)"
elif overall_percentage >= 70:
    grade = "B (Good)"
elif overall_percentage >= 60:
    grade = "C (Needs improvement)"
else:
    grade = "D (Poor - needs more training or better RAG)"

print(f"📝 Grade: {grade}")

print("\n📂 CATEGORY BREAKDOWN:")
for category, scores in sorted(category_scores.items()):
    cat_percentage = (scores["score"] / scores["max"] * 100) if scores["max"] > 0 else 0
    print(f"  • {category}: {cat_percentage:.1f}% ({scores['count']} questions)")

print("\n" + "="*60)
print("💡 Recommendations:")
if overall_percentage < 70:
    print("  • Add more relevant documents to the knowledge base")
    print("  • Improve chunking strategy (try smaller chunks)")
    print("  • Increase top_k in the search function")
elif overall_percentage < 85:
    print("  • Good job! Focus on the categories with lower scores")
    print("  • Consider adding more specific examples to the knowledge base")
else:
    print("  • Excellent performance! Mini Me is ready for production")
print("="*60)

# Save score report
report = {
    "timestamp": datetime.now().isoformat(),
    "eval_file": str(latest_file),
    "total_score": total_score,
    "max_score": max_score,
    "percentage": overall_percentage,
    "grade": grade,
    "category_scores": category_scores,
    "improvements": "v2 - Added word boundary matching, length validation, better error handling"
}

report_file = f"evals/score_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(report_file, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print(f"\n📄 Score report saved to: {report_file}")