# DAT301m_Group9 - Breast Cancer Classification using Mammography

1. **Dataset: CBIS-DDSM (Curated Breast Imaging Subset of DDSM)**
- The Cancer Imaging Archive (TCIA): https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22516629
  + [How to Download Data from the TCIA Data Portal](https://www.youtube.com/watch?v=NO48XtdHTic&t=3s)
- Kaggle: https://www.kaggle.com/datasets/awsaf49/cbis-ddsm-breast-cancer-image-dataset
---
## About CSV files
* **dicom_info:**<br>
There are 10237 row with 10237 correspond img<br>
There are no duplicate img and they are all in the jpeg folder<br>
There are 1566 unique patient id

* **mass and cal**<br>
There are 892 unique id in mass<br>
There are 753 unique id in cal<br>
But there are 79 same ids in cal as in mass. However their information (img, pathology,...) is all different<br>
**Mass and Calc is different**

---
## Preprocessing
- Artefacts removal:
  + [x] Text remove
  + [ ] White border/line remove &rarr; Different for every img &rarr; How?
- [x] Gamma correction
- [x] Apply CLAHE 

**&rarr; There are 8 img not qualified enough to use after preprocess**

## Augmentation
- [x] Use 3 augmentation:
  + flipping horizontally
  + flipping both horizontally and vertically
  + flipping vertically

**Each apply on original img &rarr; 3 new img** 

---
2. **Dataset: VinDr-Mammo**
- Physionet: https://physionet.org/content/vindr-mammo/1.0.0/

BI-RADS assessment categories (from 1 to 5) and breast density levels (A, B, C, or D) are provided. Regarding abnormal regions, the list of finding categories included in this study are mass, calcification, asymmetries, architectural distortion, and other associated features, namely suspicious lymph node, skin thickening, skin retraction, and nipple retraction. The four abnormal categories - mass, calcification, asymmetries, and architectural distortion - are also assessed BI-RADS. The findings of BI-RADS 2, i.e., benign, were not marked. Only findings of either BI-RADS 3, 4, or 5, which require follow-up examination, were annotated by bounding boxes.

## Preprocessing
- Resize to 224

