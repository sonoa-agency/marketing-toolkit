#!/usr/bin/env python3
"""
حاسبة معدل التفاعل — Engagement Rate Calculator
تحسب معدل التفاعل لمنشور أو حساب وتقيمه مقابل متوسطات المجال.

Computes engagement rate for a post or account and benchmarks it.

مثال | Example:
    python3 engagement_calculator.py --likes 340 --comments 45 --shares 60 \
        --followers 12000
    python3 engagement_calculator.py --likes 200 --comments 30 --shares 10 \
        --reach 5000 --by reach
"""

import argparse
import sys

# متوسطات معدل التفاعل التقريبية (حسب الحسابات الصغيرة والمتوسطة)
# Rough engagement-rate benchmarks for small/medium accounts
BENCHMARKS = [
    (5.0, "ممتاز 🔥 — أداء أعلى من أغلب الحسابات"),
    (3.0, "جيد جداً ✅ — فوق المتوسط"),
    (1.0, "متوسط ⚖️ — ضمن المعدل الطبيعي"),
    (0.0, "منخفض 📉 — جرّب تغيير نوع المحتوى أو وقت النشر"),
]


def engagement_rate(likes, comments, shares, base):
    """يحسب معدل التفاعل كنسبة مئوية. ER% = (interactions / base) * 100."""
    if base <= 0:
        raise ValueError("عدد المتابعين/الوصول يجب أن يكون أكبر من صفر")
    return (likes + comments + shares) / base * 100


def benchmark(rate):
    """يرجع التقييم المناسب للمعدل."""
    for threshold, label in BENCHMARKS:
        if rate >= threshold:
            return label
    return BENCHMARKS[-1][1]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="حاسبة معدل التفاعل — engagement rate calculator",
    )
    parser.add_argument("--likes", "-l", type=int, default=0, help="عدد الإعجابات")
    parser.add_argument("--comments", "-c", type=int, default=0, help="عدد التعليقات")
    parser.add_argument("--shares", "-s", type=int, default=0, help="عدد المشاركات")
    parser.add_argument("--saves", type=int, default=0, help="عدد مرات الحفظ (إنستجرام)")
    parser.add_argument("--followers", "-f", type=int, help="عدد المتابعين")
    parser.add_argument("--reach", "-r", type=int, help="الوصول (مرات الظهور)")
    parser.add_argument("--by", choices=["followers", "reach"], default="followers",
                        help="طريقة الحساب: بالمتابعين أم بالوصول (افتراضي: followers)")
    args = parser.parse_args(argv)

    base = args.reach if args.by == "reach" else args.followers
    if not base:
        print("خطأ: حدد --followers أو --reach حسب طريقة الحساب", file=sys.stderr)
        return 1

    try:
        rate = engagement_rate(args.likes, args.comments, args.shares + args.saves, base)
    except ValueError as exc:
        print(f"خطأ | Error: {exc}", file=sys.stderr)
        return 1

    total = args.likes + args.comments + args.shares + args.saves
    base_label = "الوصول" if args.by == "reach" else "المتابعين"

    print("\nالنتيجة | Result")
    print("───────────────")
    print(f"إجمالي التفاعلات : {total:,}")
    print(f"أساس الحساب ({base_label}): {base:,}")
    print(f"معدل التفاعل      : {rate:.2f}%")
    print(f"التقييم           : {benchmark(rate)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
