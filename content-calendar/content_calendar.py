#!/usr/bin/env python3
"""
مولّد تقويم المحتوى — Content Calendar Generator
يولّد خطة محتوى أسبوعية (CSV) للسوشيال ميديا بناءً على محاور المحتوى.

Generates a weekly social-media content calendar as CSV, rotating your
content pillars across platforms and days.

مثال | Example:
    python3 content_calendar.py --weeks 4 --start 2026-01-05 \
        --pillars "تعليمي,عرض خاص,قصة عميل,ترفيهي,منتج" \
        --platforms "facebook,instagram,tiktok" --out calendar.csv
"""

import argparse
import csv
import sys
from datetime import date, timedelta

# أفكار منشورات جاهزة لكل محور — عدّلها حسب نشاطك
# Per-pillar post ideas; edit to fit the business
PILLAR_IDEAS = {
    "تعليمي": ["نصيحة سريعة", "خطأ شائع وتصحيحه", "سؤال وجواب"],
    "عرض خاص": ["عرض لفترة محدودة", "كود خصم", "باقة الأسبوع"],
    "قصة عميل": ["رأي عميل بالصورة", "قبل/بعد", "قصة نجاح قصيرة"],
    "ترفيهي": ["مسابقة تفاعلية", "استطلاع رأي", "ميم من شغل المجال"],
    "منتج": ["ميزة منتج واحدة", "طريقة الاستخدام", "مقارنة بسيطة"],
    "خلف الكواليس": ["يوم من شغلنا", "تعرف على الفريق", "مرحلة من التصنيع"],
}

# أوقات نشر مقترحة لكل منصة (بتوقيت القاهرة) — قابلة للتعديل
PLATFORM_TIMES = {
    "facebook": "13:00",
    "instagram": "20:00",
    "tiktok": "19:00",
    "twitter": "12:00",
    "x": "12:00",
    "linkedin": "09:00",
    "whatsapp": "18:00",
}

# الأيام المقترحة للنشر (0=الإثنين … 6=الأحد) — ننشر يوم ونراحة يوم
POSTING_WEEKDAYS = [0, 2, 4, 6]  # الإثنين، الأربعاء، الجمعة، الأحد


def idea_for(pillar, week_index):
    """يختار فكرة منشور للمحور ويدور بين الأفكار أسبوعاً بعد أسبوع."""
    ideas = PILLAR_IDEAS.get(pillar, ["منشور عام"])
    return ideas[week_index % len(ideas)]


def generate_calendar(start, weeks, pillars, platforms):
    """يبني صفوف التقويم. Returns a list of dict rows ready for CSV."""
    rows = []
    for week in range(weeks):
        for i, weekday in enumerate(POSTING_WEEKDAYS):
            day = start + timedelta(weeks=week, days=(weekday - start.weekday()) % 7)
            pillar = pillars[(week * len(POSTING_WEEKDAYS) + i) % len(pillars)]
            platform = platforms[(week + i) % len(platforms)]
            rows.append({
                "التاريخ": day.isoformat(),
                "اليوم": ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"][day.weekday()],
                "المنصة": platform,
                "المحور": pillar,
                "الفكرة": idea_for(pillar, week),
                "وقت النشر": PLATFORM_TIMES.get(platform, "18:00"),
                "الحالة": "مخطط",
            })
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="مولّد تقويم محتوى للسوشيال ميديا — social content calendar generator",
    )
    parser.add_argument("--weeks", "-w", type=int, default=4, help="عدد الأسابيع (افتراضي: 4)")
    parser.add_argument("--start", "-s", default=None,
                        help="تاريخ البداية YYYY-MM-DD (افتراضي: أقرب إثنين قادم)")
    parser.add_argument("--pillars", "-p", default="تعليمي,عرض خاص,قصة عميل,ترفيهي,منتج",
                        help="محاور المحتوى مفصولة بفواصل")
    parser.add_argument("--platforms", default="facebook,instagram",
                        help="المنصات مفصولة بفواصل")
    parser.add_argument("--out", "-o", default="content_calendar.csv", help="ملف الإخراج CSV")
    args = parser.parse_args(argv)

    if args.start:
        try:
            start = date.fromisoformat(args.start)
        except ValueError:
            print("خطأ: صيغة التاريخ يجب أن تكون YYYY-MM-DD", file=sys.stderr)
            return 1
    else:
        today = date.today()
        start = today + timedelta(days=(7 - today.weekday()) % 7 or 7)

    pillars = [p.strip() for p in args.pillars.split(",") if p.strip()]
    platforms = [p.strip().lower() for p in args.platforms.split(",") if p.strip()]
    if not pillars or not platforms:
        print("خطأ: أدخل محوراً واحداً ومنصة واحدة على الأقل", file=sys.stderr)
        return 1

    rows = generate_calendar(start, args.weeks, pillars, platforms)

    fieldnames = ["التاريخ", "اليوم", "المنصة", "المحور", "الفكرة", "وقت النشر", "الحالة"]
    # utf-8-sig حتى يفتح Excel العربية بشكل صحيح
    with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"تم إنشاء {len(rows)} منشوراً مجدولاً في | Generated {len(rows)} posts → {args.out}")
    print(f"من {rows[0]['التاريخ']} إلى {rows[-1]['التاريخ']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
