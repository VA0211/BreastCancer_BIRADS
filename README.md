# Breast Cancer Classification using Mammography

**Dataset: VinDr-Mammo**
- Physionet: https://physionet.org/content/vindr-mammo/1.0.0/

BI-RADS assessment categories (from 1 to 5) and breast density levels (A, B, C, or D) are provided. Regarding abnormal regions, the list of finding categories included in this study are mass, calcification, asymmetries, architectural distortion, and other associated features, namely suspicious lymph node, skin thickening, skin retraction, and nipple retraction. The four abnormal categories - mass, calcification, asymmetries, and architectural distortion - are also assessed BI-RADS. The findings of BI-RADS 2, i.e., benign, were not marked. Only findings of either BI-RADS 3, 4, or 5, which require follow-up examination, were annotated by bounding boxes.

---

**Environment** - Create virtual environment then install required packages:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
