# عدة التسويق للوكالات (Marketing Toolkit)

أدوات Python صغيرة ومفيدة لفرق التسويق ووكالات الإعلان — تعمل من سطر الأوامر، **بدون أي مكتبات خارجية** (المكتبة القياسية فقط). من تطوير [Sonoa Agency](https://sonoa.online).

## الأدوات

### 1. باني روابط UTM — `utm-builder/`

يولّد روابط تتبع نظيفة للحملات ويحفظ سجلها في CSV.

```bash
python3 utm-builder/utm_builder.py https://sonoa.online/offer \
    --source facebook --medium cpc --campaign eid_2026 --log links.csv
```

- يطبّع المدخلات تلقائياً (حروف صغيرة، `_` بدل المسافات) لتقارير Analytics نظيفة.
- يحافظ على أي معاملات موجودة أصلاً في الرابط.
- `--log` يبني أرشيفاً لكل روابط حملاتك في ملف واحد.

### 2. مولّد تقويم المحتوى — `content-calendar/`

يولّد خطة نشر أسبوعية (CSV يفتح في Excel وGoogle Sheets) بتوزيع متوازن لمحاور المحتوى على المنصات.

```bash
python3 content-calendar/content_calendar.py --weeks 4 \
    --pillars "تعليمي,عرض خاص,قصة عميل,ترفيهي,منتج" \
    --platforms "facebook,instagram,tiktok" --out calendar.csv
```

- يوزع المحاور بالتناوب ويقترح فكرة ووقت نشر لكل منشور.
- أفكار المنشورات والأوقات في قواميس أعلى الملف — عدّلها حسب كل عميل.
- الترميز `utf-8-sig` حتى تظهر العربية صحيحة في Excel.

### 3. حاسبة معدل التفاعل — `engagement-calculator/`

تحسب معدل التفاعل (بالمتابعين أو بالوصول) وتقيّمه مقابل متوسطات المجال.

```bash
python3 engagement-calculator/engagement_calculator.py \
    --likes 340 --comments 45 --shares 60 --followers 12000
```

## المتطلبات

Python 3.8+ فقط — لا `pip install` لأي شيء.

## الرخصة

MIT — استخدمها وعدّلها بحرية.

---

# Marketing Toolkit

Small, dependency-free Python CLI tools for marketing teams and agencies, by [Sonoa Agency](https://sonoa.online).

- **utm-builder/** — generates clean UTM campaign URLs and logs them to CSV
- **content-calendar/** — generates a rotating weekly content calendar (Excel-ready CSV, Arabic-safe)
- **engagement-calculator/** — computes engagement rate (by followers or reach) with benchmarks

Requires only Python 3.8+. Licensed under MIT. Full docs in Arabic above.
