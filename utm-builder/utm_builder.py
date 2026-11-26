#!/usr/bin/env python3
"""
باني روابط UTM — UTM Link Builder
يولّد روابط تتبع للحملات التسويقية ويحفظها في ملف CSV.

Generates UTM-tagged campaign URLs and optionally appends them to a CSV log.

أمثلة | Examples:
    python3 utm_builder.py https://sonoa.online/offer \
        --source facebook --medium cpc --campaign eid_2026

    python3 utm_builder.py https://sonoa.online --source instagram \
        --medium story --campaign ramadan --content video_v2 --log links.csv
"""

import argparse
import csv
import sys
from datetime import datetime
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

# المصادر الشائعة للحملات — تظهر كاقتراحات في رسالة المساعدة فقط
COMMON_SOURCES = ["facebook", "instagram", "tiktok", "google", "whatsapp", "snapchat", "youtube"]


def build_utm_url(url, source, medium, campaign, term=None, content=None):
    """يبني الرابط النهائي مع معاملات UTM. Returns the URL with UTM params appended."""
    parsed = urlparse(url.strip())
    if not parsed.scheme:
        raise ValueError("الرابط يجب أن يبدأ بـ https:// أو http:// — URL must include a scheme")
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"بروتوكول غير مدعوم: {parsed.scheme}")

    # نحتفظ بأي معاملات موجودة مسبقاً في الرابط
    query = dict(parse_qsl(parsed.query))
    query.update({
        "utm_source": source,
        "utm_medium": medium,
        "utm_campaign": campaign,
    })
    if term:
        query["utm_term"] = term
    if content:
        query["utm_content"] = content

    return urlunparse(parsed._replace(query=urlencode(query)))


def append_to_log(path, row):
    """يضيف سطراً لملف CSV (وينشئ الملف مع الترويسة لو غير موجود)."""
    fieldnames = ["created_at", "url", "source", "medium", "campaign", "term", "content", "final_url"]
    file_exists = False
    try:
        with open(path, "r", encoding="utf-8"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="باني روابط UTM للحملات التسويقية — UTM campaign link builder",
        epilog=f"مصادر شائعة | common sources: {', '.join(COMMON_SOURCES)}",
    )
    parser.add_argument("url", help="رابط الصفحة — the landing page URL (https://...)")
    parser.add_argument("--source", "-s", required=True, help="مصدر الزيارة: facebook, instagram, ...")
    parser.add_argument("--medium", "-m", required=True, help="الوسيلة: cpc, story, post, email, ...")
    parser.add_argument("--campaign", "-c", required=True, help="اسم الحملة: ramadan_2026, launch, ...")
    parser.add_argument("--term", "-t", help="الكلمة المفتاحية (للإعلانات المدفوعة)")
    parser.add_argument("--content", help="تمييز النسخ: video_v2, blue_banner, ...")
    parser.add_argument("--log", "-l", metavar="CSV", help="احفظ النتيجة في ملف CSV")
    args = parser.parse_args(argv)

    # تنظيف وتطبيع المدخلات: حروف صغيرة وشرطات سفلية بدل المسافات
    def clean(value):
        return value.strip().lower().replace(" ", "_") if value else value

    source, medium, campaign = clean(args.source), clean(args.medium), clean(args.campaign)
    term, content = clean(args.term), clean(args.content)

    try:
        final_url = build_utm_url(args.url, source, medium, campaign, term, content)
    except ValueError as exc:
        print(f"خطأ | Error: {exc}", file=sys.stderr)
        return 1

    print("\nالرابط النهائي | Final URL:\n")
    print(final_url)
    print()

    if args.log:
        row = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "url": args.url, "source": source, "medium": medium,
            "campaign": campaign, "term": term or "", "content": content or "",
            "final_url": final_url,
        }
        append_to_log(args.log, row)
        print(f"تم الحفظ في | Saved to {args.log}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
