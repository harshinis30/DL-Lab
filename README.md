# Deep Learning - Lab excercise



A hands-on collection of deep learning labs covering core concepts — from building neural networks from scratch to transformers and vision models. Each lab is designed to reinforce theoretical understanding through practical implementation.

---

## 📂 Structure

```
dl-labs/
├── lab01/    # Feed Forward & Back-Propagation (from scratch)
├── lab02/    # ANN for MNIST Classification
├── lab03/    # CNN for MNIST + Comparative Report
├── lab04/    # ResNet-34 for Skin Lesion & Deepfake Detection
├── lab05/    # AutoEncoders — MNIST Compression
├── lab06/    # Anomaly Detection using VAE & GAN (MRI)
├── lab07/    # Tumor Segmentation using UNet
├── lab08/    # Sentiment Classification using RNN & LSTM
├── lab09/    # News Summarization using BART (Transformers)
└── lab10/    # Chest X-Ray Classification using ViT
```

---

## 🗒️ Labs Overview

| Lab | Topic | Dataset |
|-----|-------|---------|
| 01 | Feedforward & Backpropagation from scratch | IRIS (Setosa vs Versicolor) |
| 02 | Fully Connected ANN | MNIST |
| 03 | CNN + ANN vs CNN comparison report | MNIST |
| 04 | ResNet-34 (custom) — Skin lesion & Deepfake detection | ISIC 2019, Custom Deepfake |
| 05 | PCA vs AutoEncoder compression, t-SNE visualization | MNIST |
| 06 | Anomaly detection — VAE & GAN reconstruction | LGG MRI |
| 07 | UNet segmentation — Baseline vs Heatmap-guided | LGG MRI |
| 08 | Sentiment analysis — RNN vs LSTM | SST-2 |
| 09 | Fine-tuned BART for news summarization | ILSUM-1.0 (English) |
| 10 | Vision Transformer (ViT) for chest X-ray classification | Chest X-Ray Dataset |

---

## 🛠️ Setup

```bash
pip install torch torchvision
pip install tensorflow keras
pip install transformers datasets
pip install scikit-learn matplotlib numpy pandas
```

> Most labs are designed to run on **Google Colab / Kaggle** free-tier GPUs.

---



---

*IIITDM Kancheepuram — Deep Learning Course*
