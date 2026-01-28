# Auto AI Gold Trader – نظام تداول الذهب الآلي بالذكاء الاصطناعي

نظام ذكي لتحليل وتوقع سعر الذهب (XAU/USD) باستخدام مؤشرات فنية + نماذج LSTM و Random Forest + واجهة Streamlit.

## هيكل المشروع (Project Structure)




ai_gold_trader/
├── app.py                  # الواجهة الرئيسية (Streamlit dashboard)
├── data_fetch.py           # جلب بيانات سعر الذهب من Yahoo Finance
├── analysis.py             # حساب المؤشرات الفنية (EMA, RSI, MACD, Volatility, ...)
├── quant_features.py       # إضافة ميزات كمية للنماذج
├── ml_model.py             # تدريب وتحميل نماذج LSTM + RandomForest
├── decision_engine.py      # اتخاذ قرار BUY / SELL / HOLD
├── alerts.py               # إرسال تنبيهات إلى Discord
├── requirements.txt
├── README.md
└── utils/
├── model_utils.py      # حفظ وتحميل النماذج
├── backtester.py       # اختبار رجعي (Sharpe ratio, drawdown, ...)
└── visualization.py    # رسم الشارتات والإشارات
## كيف يعمل النظام (How It Works)

1. `data_fetch.py` → يجلب بيانات الذهب الحية/التاريخية ويخزنها محليًا (cache).
2. `analysis.py` → يحسب EMA20/50، RSI14، Volatility، Momentum، Unusual moves.
3. `quant_features.py` → يمكن توسيعه لميزات إضافية (مثل MACD، Bollinger...).
4. `ml_model.py` → يدرب/يحمل LSTM لتوقع السعر + RandomForest للتصنيف.
5. `decision_engine.py` → يجمع الإشارات → يقرر BUY/SELL/HOLD مع الثقة.
6. `alerts.py` → يرسل تنبيه Discord عند إشارة قوية.
7. `app.py` → يعرض: السعر الحالي، التوقع، القرار، SL/TP، شارت ملون.
8. `utils/` → أدوات مساعدة (حفظ نماذج، backtesting، visualization).

## المميزات الرئيسية (Features)

- تحديثات حية لسعر الذهب عبر Yahoo Finance
- نمذجة تنبؤية بـ LSTM (توقع السعر) + Random Forest (اتجاه)
- تنبيهات Discord تلقائية
- حساب Stop Loss و Take Profit ديناميكي
- نظام ثقة (Confidence scoring)
- داشبورد تفاعلي ملون مع إشارات التداول
- إمكانية Backtesting (Sharpe، Max Drawdown)
- دعم متعدد الإطارات الزمنية (قابل للتوسع)

## المتطلبات (Requirements)

انظر `requirements.txt`

## طريقة التشغيل (Usage)

```bash
# 1. استنسخ المستودع (أو أنشئ المجلد يدويًا)
git clone <your-repo-url>
cd ai_gold_trader

# 2. ثبت المكتبات
pip install -r requirements.txt

# 3. شغل التطبيق
streamlit run app.py
