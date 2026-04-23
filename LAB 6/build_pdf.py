"""
Build lab6_report.pdf using ReportLab Platypus.
Run from the LAB 6 directory:
    python build_pdf.py
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import (
    Color, HexColor, white, black, lightgrey
)
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, ListFlowable, ListItem, KeepTogether,
    CondPageBreak
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import Preformatted

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE   = r"c:\Users\Larika\Desktop\Sem 6\DL LAB\LAB 6"
IMG    = os.path.join(BASE, "images")
OUT    = os.path.join(BASE, "lab6_report.pdf")

# ── Colour palette ────────────────────────────────────────────────────────────
DARKBLUE  = HexColor("#003366")
STEELBLUE = HexColor("#4682B4")
LIGHTGRAY = HexColor("#F5F5F5")
CODEBG    = HexColor("#F0F0F0")
TOMATO    = HexColor("#FF6347")
GOLD      = HexColor("#FFD700")
NOTEBG    = HexColor("#EBF5FB")
NOTEBRD   = STEELBLUE
KEYBG     = HexColor("#FEFAE0")
KEYBRD    = DARKBLUE

# ── Document ──────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT,
    pagesize=A4,
    leftMargin=2.4*cm, rightMargin=2.4*cm,
    topMargin=2.4*cm,  bottomMargin=2.4*cm,
    title="Lab 06 – Anomaly Detection using VAE and GAN",
    author="CS23B1028 R K Larika & CS23B1050 S Harshini",
)

W = A4[0] - 4.8*cm   # usable width

# ── Styles ────────────────────────────────────────────────────────────────────
ss = getSampleStyleSheet()

def S(name, **kw):
    base = ss[name]
    return ParagraphStyle(name+"_custom", parent=base, **kw)

TitleS    = S("Title",   fontSize=22, textColor=DARKBLUE,
              spaceAfter=6, fontName="Helvetica-Bold", alignment=TA_CENTER)
SubTitleS = S("Normal",  fontSize=14, textColor=STEELBLUE,
              spaceAfter=4, fontName="Helvetica-Bold", alignment=TA_CENTER)
MetaS     = S("Normal",  fontSize=11, textColor=black,
              spaceAfter=3, alignment=TA_CENTER)
H1S       = S("Heading1",fontSize=14, textColor=DARKBLUE,
              fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4)
H2S       = S("Heading2",fontSize=12, textColor=STEELBLUE,
              fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=3)
H3S       = S("Heading3",fontSize=11, textColor=DARKBLUE,
              fontName="Helvetica-BoldOblique", spaceBefore=6, spaceAfter=2)
BodyS     = S("Normal",  fontSize=10, leading=14, spaceAfter=4,
              alignment=TA_JUSTIFY)
BulletS   = S("Normal",  fontSize=10, leading=14, spaceAfter=2,
              leftIndent=14, bulletIndent=4)
CaptionS  = S("Normal",  fontSize=9, textColor=HexColor("#444444"),
              fontName="Helvetica-Oblique", alignment=TA_CENTER,
              spaceAfter=6, spaceBefore=2)
CodeS     = ParagraphStyle("Code", fontName="Courier", fontSize=8,
              leading=11, backColor=CODEBG, leftIndent=8, rightIndent=4,
              spaceAfter=6, spaceBefore=4, borderColor=STEELBLUE,
              borderWidth=0.5, borderPadding=5)
NoteS     = S("Normal",  fontSize=9.5, leading=13, backColor=NOTEBG,
              leftIndent=8, rightIndent=8, spaceAfter=6, spaceBefore=4,
              borderColor=NOTEBRD, borderWidth=1, borderPadding=6,
              textColor=HexColor("#1a5276"))
KeyS      = S("Normal",  fontSize=9.5, leading=13, backColor=KEYBG,
              leftIndent=8, rightIndent=8, spaceAfter=6, spaceBefore=4,
              borderColor=KEYBRD, borderWidth=1, borderPadding=6,
              textColor=HexColor("#1a2744"), fontName="Helvetica-Bold")

# ── Helper builders ───────────────────────────────────────────────────────────

def rule(color=STEELBLUE, thickness=1):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=4, spaceBefore=4)

def h1(text):
    return [rule(DARKBLUE, 1.5), Paragraph(text, H1S), rule(STEELBLUE, 0.5)]

def h2(text):
    return [Paragraph(text, H2S)]

def h3(text):
    return [Paragraph(text, H3S)]

def body(text):
    return Paragraph(text, BodyS)

def note(text):
    return Paragraph(f"<b>Note:</b> {text}", NoteS)

def key(text):
    return Paragraph(f"<b>Key Takeaway:</b> {text}", KeyS)

def bullet_list(items):
    li = [ListItem(Paragraph(item, BulletS), bulletColor=STEELBLUE,
                   bulletType='bullet', leftIndent=18)
          for item in items]
    return ListFlowable(li, bulletType='bullet', start='•',
                        leftIndent=14, spaceAfter=4)

def numbered_list(items):
    li = [ListItem(Paragraph(item, BulletS), bulletColor=DARKBLUE,
                   leftIndent=22)
          for item in items]
    return ListFlowable(li, bulletType='1', start=1,
                        leftIndent=14, spaceAfter=4)

def code_block(lines, caption=None):
    text = "\n".join(lines)
    elems = [Preformatted(text, CodeS)]
    if caption:
        elems.append(Paragraph(f"<i>Listing: {caption}</i>", CaptionS))
    return elems

def img_block(fname, caption, max_w=None, max_h=None):
    path = os.path.join(IMG, fname)
    if not os.path.exists(path):
        return [Paragraph(f"[Image not found: {fname}]", CaptionS)]
    from PIL import Image as PILImage
    with PILImage.open(path) as pil:
        pw, ph = pil.size
    ratio = ph / pw
    w = min(max_w or W, W)
    h = w * ratio
    if max_h and h > max_h:
        h = max_h
        w = h / ratio
    return [
        Spacer(1, 4),
        Image(path, width=w, height=h, hAlign="CENTER",
              kind='proportional'),
        Paragraph(caption, CaptionS),
        Spacer(1, 4),
    ]

def two_imgs(fname1, fname2, cap1, cap2, cap_full):
    path1 = os.path.join(IMG, fname1)
    path2 = os.path.join(IMG, fname2)
    from PIL import Image as PILImage
    col_w = (W - 0.5*cm) / 2

    def make_img(path, cw):
        with PILImage.open(path) as p:
            pw, ph = p.size
        ratio = ph / pw
        h = cw * ratio
        return Image(path, width=cw, height=h, hAlign="CENTER",
                     kind='proportional')

    i1 = make_img(path1, col_w)
    i2 = make_img(path2, col_w)
    p1 = Paragraph(cap1, CaptionS)
    p2 = Paragraph(cap2, CaptionS)
    tbl = Table([[i1, i2], [p1, p2]],
                colWidths=[col_w, col_w])
    tbl.setStyle(TableStyle([
        ('ALIGN',    (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',   (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0),(-1,-1), 2),
        ('BOTTOMPADDING',(0,0),(-1,-1), 2),
    ]))
    return [tbl, Paragraph(cap_full, CaptionS), Spacer(1, 6)]

def data_table(header, rows, col_widths=None):
    data = [header] + rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',  (0,0),(-1,0), DARKBLUE),
        ('TEXTCOLOR',   (0,0),(-1,0), white),
        ('FONTNAME',    (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',    (0,0),(-1,-1), 9),
        ('ALIGN',       (0,0),(-1,-1), 'LEFT'),
        ('VALIGN',      (0,0),(-1,-1), 'MIDDLE'),
        ('GRID',        (0,0),(-1,-1), 0.4, HexColor("#BBBBBB")),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [white, LIGHTGRAY]),
        ('LEFTPADDING', (0,0),(-1,-1), 6),
        ('RIGHTPADDING',(0,0),(-1,-1), 6),
        ('TOPPADDING',  (0,0),(-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
        ('LINEBELOW',   (0,0),(-1,0), 1, STEELBLUE),
    ]))
    return [t, Spacer(1, 8)]

# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── TITLE PAGE ────────────────────────────────────────────────────────────────
story += [
    Spacer(1, 1*cm),
    rule(DARKBLUE, 2),
    Spacer(1, 0.5*cm),
    Paragraph("Anomaly Detection using", TitleS),
    Paragraph("Variational Autoencoder (VAE)", TitleS),
    Paragraph("and Generative Adversarial Network (GAN)", TitleS),
    Spacer(1, 0.3*cm),
    rule(STEELBLUE, 1),
    Spacer(1, 0.5*cm),
    Paragraph("Lab Report — Lab 06", SubTitleS),
    Paragraph("Deep Learning Laboratory", SubTitleS),
    Spacer(1, 1*cm),
]
meta = [
    ["Students :", "CS23B1028  R K Larika"],
    ["",           "CS23B1050  S Harshini"],
    ["Dataset :",  "LGG MRI Segmentation (Kaggle — mateuszbuda)"],
    ["Platform :", "Kaggle GPU (NVIDIA T4)"],
    ["Framework:", "PyTorch 2.x"],
]
from reportlab.lib.utils import simpleSplit
from datetime import date
meta.append(["Date :", date.today().strftime("%d %B %Y")])
mt = Table(meta, colWidths=[3.5*cm, W - 3.5*cm])
mt.setStyle(TableStyle([
    ('FONTNAME',    (0,0),(0,-1), 'Helvetica-Bold'),
    ('FONTSIZE',    (0,0),(-1,-1), 10),
    ('ALIGN',       (0,0),(0,-1), 'RIGHT'),
    ('ALIGN',       (1,0),(1,-1), 'LEFT'),
    ('TOPPADDING',  (0,0),(-1,-1), 3),
    ('BOTTOMPADDING',(0,0),(-1,-1), 3),
    ('TEXTCOLOR',   (0,0),(0,-1), DARKBLUE),
]))
story += [mt, Spacer(1, 1*cm), rule(DARKBLUE, 2), PageBreak()]

# ── SECTION 1: Introduction ───────────────────────────────────────────────────
story += h1("1.  Introduction and Objective")
story += [
    body("Anomaly detection in medical imaging is a high-stakes problem where the goal is to "
         "identify pathological regions (e.g. brain tumours) <i>without</i> pixel-level "
         "annotations during training.  A powerful unsupervised strategy trains a generative "
         "model exclusively on <b>normal</b> (healthy) scans and exploits the model's inability "
         "to faithfully reconstruct <b>abnormal</b> (tumour-containing) anatomy as an anomaly "
         "signal."),
    Spacer(1, 4),
    body("This lab explores and compares two state-of-the-art generative architectures:"),
]
story += [numbered_list([
    "<b>Variational Autoencoder (VAE)</b> — a probabilistic encoder-decoder that learns a "
    "smooth, Gaussian-regularised latent space.",
    "<b>Encoder-Decoder Generator (GAN)</b> — a U-Net style generator adversarially trained "
    "with a PatchGAN discriminator.",
])]
story += [
    body("Both models are trained <b>only on normal MRI slices</b>.  At inference, an abnormal "
         "slice is poorly reconstructed; the pixel-wise absolute difference between the original "
         "and its reconstruction produces a Region-of-Interest (ROI) mask that localises the tumour."),
    Spacer(1, 8),
]

# ── SECTION 2: Dataset ────────────────────────────────────────────────────────
story += h1("2.  Dataset and Preprocessing")
story += h2("2.1  Dataset Description")
story += [
    body("The experiment uses the <b>LGG MRI Segmentation</b> dataset "
         "(mateuszbuda/lgg-mri-segmentation) on Kaggle.  It contains brain MRI slices from "
         "Low-Grade Glioma (LGG) patients with corresponding binary tumour masks."),
    Spacer(1, 4),
]
story += data_table(
    ["Split", "Count", "Label Criterion"],
    [
        ["Total MRI slices",       "3,929",   "—"],
        ["Normal slices",          "2,556",   "Mask has no white pixels"],
        ["Abnormal slices",        "1,373",   "Mask has ≥ 1 white pixel"],
        ["Training (normal only)", "2,173",   "85% of normal set"],
        ["Validation (normal)",    "383",     "15% of normal set"],
        ["Test (abnormal)",        "1,373",   "All abnormal slices"],
    ],
    col_widths=[5*cm, 2.8*cm, 7*cm],
)

story += h2("2.2  Sample MRI Slices")
story += img_block("normal_samples.png",
    "Figure 1 — Sample normal (tumour-free) MRI slices from the training set.",
    max_h=9*cm)
story += img_block("abnormal_samples.png",
    "Figure 2 — Sample abnormal (tumour-containing) MRI slices held out for testing.",
    max_h=9*cm)

story += h2("2.3  Labelling, Augmentation & Normalisation")
story += [
    body("A slice is labelled <b>abnormal</b> if and only if its mask contains ≥ 1 "
         "foreground pixel.  Images are resized to 128×128, converted to grayscale, "
         "and normalised to [−1, 1] (mean=0.5, std=0.5).  Training images receive "
         "random horizontal flips."),
]
story += code_block([
    "train_tf = T.Compose([",
    "    T.Resize((128, 128)),",
    "    T.RandomHorizontalFlip(),",
    "    T.ToTensor(),",
    "    T.Normalize([0.5], [0.5])   # maps to [-1, 1]",
    "])",
], "Transform pipelines for training (augmented) and evaluation")
story += [
    body("The training set yields <b>68 batches</b>, validation <b>12 batches</b>, "
         "and the abnormal test set <b>43 batches</b> per epoch (batch size 32)."),
    Spacer(1, 8),
]

# ── SECTION 3: Architecture ───────────────────────────────────────────────────
story += h1("3.  Model Architecture")
story += h2("3.1  Variational Autoencoder (VAE)")
story += h3("3.1.1  Architecture Overview")
story += [
    body("The VAE maps each 128×128 grayscale MRI to a pair of 128-dimensional vectors "
         "(μ, log σ²) parameterising a Gaussian distribution in latent space, then decodes "
         "a sampled latent vector back to image space via the reparameterisation trick:"),
    Paragraph(
        "<b>  z  =  μ  +  σ ⊙ ε ,    ε ~ N(0, I)</b>",
        ParagraphStyle("eq", parent=BodyS, alignment=TA_CENTER,
                       spaceBefore=4, spaceAfter=4)),
]
story += h3("3.1.2  Encoder")
story += code_block([
    "class VAEEncoder(nn.Module):",
    "    def __init__(self, latent_dim=128):",
    "        super().__init__()",
    "        self.enc = nn.Sequential(",
    "            nn.Conv2d(1,  32, 4, 2, 1),  nn.LeakyReLU(0.2),           # 64x64",
    "            nn.Conv2d(32,  64, 4, 2, 1), nn.BatchNorm2d(64),  nn.LeakyReLU(0.2), # 32x32",
    "            nn.Conv2d(64, 128, 4, 2, 1), nn.BatchNorm2d(128), nn.LeakyReLU(0.2), # 16x16",
    "            nn.Conv2d(128,256, 4, 2, 1), nn.BatchNorm2d(256), nn.LeakyReLU(0.2), # 8x8",
    "            nn.Flatten()",
    "        )",
    "        self.fc_mu  = nn.Linear(256 * 8 * 8, latent_dim)",
    "        self.fc_log = nn.Linear(256 * 8 * 8, latent_dim)  # log-variance",
], "VAE Encoder — four strided convolution blocks")

story += h3("3.1.3  Decoder")
story += code_block([
    "class VAEDecoder(nn.Module):",
    "    def __init__(self, latent_dim=128):",
    "        super().__init__()",
    "        self.proj = nn.Linear(latent_dim, 256 * 8 * 8)",
    "        self.dec  = nn.Sequential(",
    "            nn.ConvTranspose2d(256,128, 4, 2, 1), nn.BatchNorm2d(128), nn.ReLU(), # 16",
    "            nn.ConvTranspose2d(128, 64, 4, 2, 1), nn.BatchNorm2d(64),  nn.ReLU(), # 32",
    "            nn.ConvTranspose2d( 64, 32, 4, 2, 1), nn.BatchNorm2d(32),  nn.ReLU(), # 64",
    "            nn.ConvTranspose2d( 32,  1, 4, 2, 1), nn.Tanh()                       # 128",
    "        )",
], "VAE Decoder — four transposed convolution blocks")

story += h3("3.1.4  Loss Function (ELBO)")
story += [
    body("The model minimises the Evidence Lower Bound (ELBO):"),
    Paragraph(
        "<b>L_VAE = (1/N) Σ ‖x - x̂‖² + β · ( −½ Σⱼ (1 + log σⱼ² − μⱼ² − σⱼ²) )</b>",
        ParagraphStyle("eq", parent=BodyS, alignment=TA_CENTER,
                       fontName="Courier", spaceBefore=4, spaceAfter=4,
                       fontSize=9)),
    body("With β = 1.0 (standard VAE), reconstruction (MSE) and KL terms are weighted equally."),
    Spacer(1, 6),
]

story += h2("3.2  GAN — U-Net Generator + PatchGAN Discriminator")
story += h3("3.2.1  Generator")
story += [
    body("The generator is a U-Net style encoder-decoder.  Skip connections concatenate "
         "corresponding encoder feature maps to the decoder to preserve spatial detail.  "
         "Dropout (p = 0.5) in the first decoder block discourages mode collapse."),
]
story += code_block([
    "class GANGenerator(nn.Module):",
    "    def __init__(self):",
    "        super().__init__()",
    "        self.e1 = nn.Sequential(nn.Conv2d(1,  64,4,2,1), nn.LeakyReLU(0.2))  # 64",
    "        self.e2 = nn.Sequential(nn.Conv2d(64,128,4,2,1), nn.BatchNorm2d(128), nn.LeakyReLU(0.2)) # 32",
    "        self.e3 = nn.Sequential(nn.Conv2d(128,256,4,2,1),nn.BatchNorm2d(256), nn.LeakyReLU(0.2)) # 16",
    "        self.e4 = nn.Sequential(nn.Conv2d(256,512,4,2,1),nn.BatchNorm2d(512), nn.LeakyReLU(0.2)) # 8",
    "        self.bn = nn.Sequential(nn.Conv2d(512,512,4,2,1),nn.ReLU())                               # 4",
    "        # Decoder with skip connections via torch.cat",
    "        self.d1  = nn.Sequential(nn.ConvTranspose2d(512,512,4,2,1),",
    "                                  nn.BatchNorm2d(512),nn.ReLU(),nn.Dropout(0.5))",
    "        self.d2  = nn.Sequential(nn.ConvTranspose2d(1024,256,4,2,1),...)",
    "        self.out = nn.Sequential(nn.ConvTranspose2d(128,1,4,2,1),nn.Tanh())    # 128",
], "GAN Generator (U-Net, abbreviated)")

story += h3("3.2.2  PatchGAN Discriminator")
story += [
    body("Rather than producing a single real/fake scalar, the PatchGAN discriminator outputs "
         "a spatial grid where each value classifies a local receptive field, encouraging "
         "high-frequency texture fidelity."),
]
story += code_block([
    "class GANDiscriminator(nn.Module):",
    "    def __init__(self):",
    "        super().__init__()",
    "        self.net = nn.Sequential(",
    "            nn.Conv2d(1,   64,4,2,1), nn.LeakyReLU(0.2),",
    "            nn.Conv2d(64, 128,4,2,1), nn.BatchNorm2d(128), nn.LeakyReLU(0.2),",
    "            nn.Conv2d(128,256,4,2,1), nn.BatchNorm2d(256), nn.LeakyReLU(0.2),",
    "            nn.Conv2d(256,512,4,1,1), nn.BatchNorm2d(512), nn.LeakyReLU(0.2),",
    "            nn.Conv2d(512,  1,4,1,1)   # PatchGAN output",
    "        )",
], "PatchGAN Discriminator")

story += h3("3.2.3  GAN Loss Functions")
story += [
    body("With label smoothing (0.9 for real, 0.1 for fake):"),
    Paragraph(
        "  L_D = ½ ( BCE(D(x), 1)  +  BCE(D(G(x)), 0) )",
        ParagraphStyle("eq", parent=BodyS, fontName="Courier", fontSize=9,
                       alignment=TA_CENTER, spaceBefore=2, spaceAfter=2)),
    Paragraph(
        "  L_G = BCE(D(G(x)), 1)  +  λ_recon · L1(G(x), x),    λ_recon = 100",
        ParagraphStyle("eq", parent=BodyS, fontName="Courier", fontSize=9,
                       alignment=TA_CENTER, spaceBefore=2, spaceAfter=6)),
]
story += h3("3.2.4  Model Parameter Counts")
story += data_table(
    ["Component", "Parameters"],
    [
        ["VAE (Encoder + Decoder)",  "≈ 36.7 M"],
        ["GAN Generator",            "≈ 54.4 M"],
        ["GAN Discriminator",        "≈ 2.8 M"],
    ],
    col_widths=[8*cm, 4*cm],
)

# ── SECTION 4: Training ───────────────────────────────────────────────────────
story += [PageBreak()]
story += h1("4.  Training Configuration")
story += h2("4.1  VAE Training Hyperparameters")
story += data_table(
    ["Hyperparameter", "Value"],
    [
        ["Optimiser",           "Adam"],
        ["Learning rate",       "1 × 10⁻⁴"],
        ["KL weight β",         "1.0"],
        ["Latent dimension",    "128"],
        ["Epochs",              "50"],
        ["Gradient clip",       "‖g‖₂ ≤ 1.0"],
        ["LR scheduler",        "ReduceLROnPlateau (patience 5, factor 0.5)"],
        ["Best model saved by", "Minimum validation loss"],
    ],
    col_widths=[6*cm, 8*cm],
)

story += h2("4.2  GAN Training Hyperparameters")
story += data_table(
    ["Hyperparameter", "Value"],
    [
        ["Generator LR",          "2 × 10⁻⁴"],
        ["Discriminator LR",      "1 × 10⁻⁴"],
        ["Optimiser (both)",      "Adam (β₁ = 0.5, β₂ = 0.999)"],
        ["Reconstruction weight", "λ_recon = 100"],
        ["Label smoothing",       "Real → 0.9, Fake → 0.1"],
        ["Epochs",                "50"],
    ],
    col_widths=[6*cm, 8*cm],
)

# ── SECTION 5: Results ────────────────────────────────────────────────────────
story += h1("5.  Results and Analysis")

story += h2("5.1  Training Loss Curves")
story += img_block("training_loss_curves.png",
    "Figure 3 — Training loss curves for 50 epochs.  "
    "Top-left: VAE total ELBO (train vs. val).  "
    "Top-right: VAE component losses (reconstruction MSE & KL divergence).  "
    "Bottom-left: GAN generator vs. discriminator.  "
    "Bottom-right: GAN generator components (adversarial & L1 reconstruction).",
    max_h=12*cm)
story += [
    body("<b>VAE:</b>  The ELBO decreases monotonically for both train and validation "
         "sets, demonstrating stable convergence.  The KL divergence initially rises as "
         "the posterior diverges from the unit Gaussian prior, then stabilises."),
    body("<b>GAN:</b>  Generator loss is dominated by the reconstruction term (λ = 100), "
         "forcing faithful anatomy reproduction.  Discriminator loss stabilises near 0.5 "
         "(healthy adversarial balance)."),
    Spacer(1, 6),
]

story += h2("5.2  Latent Space Visualisation (VAE)")
story += img_block("latent_space.png",
    "Figure 4 — Left: t-SNE projection of VAE latent means μ for 200 normal (blue) "
    "and up to 640 abnormal (red) slices.  "
    "Right: Histogram of first three latent dimensions for both classes.",
    max_h=9*cm)
story += [
    note("Latent-space separation without anomaly labels is the hallmark of a successful "
         "VAE for anomaly detection.  The KL penalty constrains normal representations to "
         "a compact region; tumour slices map to out-of-distribution positions, shown as "
         "the separate red cluster in the t-SNE plot."),
    bullet_list([
        "Normal slices follow near-Gaussian distributions centred at zero (KL-enforced).",
        "Abnormal slices produce shifted, wider, or bimodal distributions in several latent "
        "dimensions.",
    ]),
    Spacer(1, 6),
]

story += h2("5.3  Reconstruction Error Distribution")
story += img_block("reconstruction_error.png",
    "Figure 5 — Per-image MSE reconstruction error histograms for normal (blue) and "
    "abnormal (red) slices.  Dashed lines mark class means.  "
    "Both VAE and GAN show clearly higher errors for abnormal slices.",
    max_h=8*cm)
story += data_table(
    ["Model", "Normal errors", "Abnormal errors"],
    [
        ["VAE", "Low, tight distribution", "Higher, shifted right"],
        ["GAN", "Low, tight distribution",
         "Higher, shifted right (larger absolute gap)"],
    ],
    col_widths=[2.5*cm, 6*cm, 5.5*cm],
)
story += [
    body("The GAN shows a larger gap between class means because the adversarial objective "
         "demands per-pixel precision for normal anatomy, amplifying the anomaly signal on "
         "tumour regions."),
    Spacer(1, 6),
]

story += [PageBreak()]
story += h2("5.4  ROI Generation and Heatmaps")
story += [
    body("The anomaly map is the pixel-wise absolute difference between the original and its "
         "reconstruction.  A binary ROI mask is produced by thresholding at the 85th percentile:"),
    Paragraph(
        "  D(x) = |x − x̂|        ROI(x) = 1[ D(x) > P₈₅(D(x)) ]",
        ParagraphStyle("eq", parent=BodyS, fontName="Courier", fontSize=9,
                       alignment=TA_CENTER, spaceBefore=4, spaceAfter=6)),
]
story += code_block([
    "def get_roi(orig, recon, threshold_pct=85):",
    "    diff   = (orig - recon).abs()              # [B, 1, H, W]",
    "    thresh = np.percentile(diff.numpy(), threshold_pct)",
    "    roi    = (diff > thresh).float()",
    "    return diff, roi",
], "ROI extraction via absolute difference + percentile threshold")

story += h3("5.4.1  VAE Results")
story += img_block("roi_vae.png",
    "Figure 6 — VAE anomaly detection results.  Each row shows one abnormal MRI: "
    "(1) original, (2) VAE reconstruction, (3) absolute difference, "
    "(4) binary ROI mask, (5) jet-coloured heatmap.  "
    "The VAE produces smooth, well-connected tumour blobs.",
    max_h=18*cm)

story += h3("5.4.2  GAN Results")
story += img_block("roi_gan.png",
    "Figure 7 — GAN anomaly detection results (same five-column layout).  "
    "GAN reconstructions are sharper, yielding crisper but noisier ROI masks.",
    max_h=18*cm)

story += [
    bullet_list([
        "<b>VAE</b> produces softer difference maps; the binary ROI forms smooth, "
        "connected blob(s) closely corresponding to the tumour location.",
        "<b>GAN</b> produces sharper difference maps (adversarial loss penalises "
        "per-pixel error on normal anatomy); the ROI has crisper edges but may "
        "fragment into multiple small components.",
        "Both models correctly focus the highest reconstruction error on the tumour "
        "region, confirming the anomaly-detection paradigm.",
    ]),
    Spacer(1, 6),
]

story += [PageBreak()]
story += h2("5.5  ROI Quality Metrics")
story += [
    body("Three metrics quantify ROI quality (averaged over 6 random samples):"),
    numbered_list([
        "<b>Smoothness</b> (Laplacian std, ↓ better) — std of discrete Laplacian; "
        "lower = smoother, more connected blobs.",
        "<b>Edge pixel count</b> — number of boundary pixels; reflects boundary complexity.",
        "<b>Noise ratio</b> (↓ better) — fraction of connected components with < 20 pixels; "
        "high values = fragmented, noisy masks.",
    ]),
]
story += two_imgs(
    "roi_quality_comparison.png", "edge_pixel_comparison.png",
    "Figure 8a — Smoothness and noise ratio (both lower is better).",
    "Figure 8b — Mean edge pixel count.",
    "Figure 8 — ROI quality metrics — VAE vs. GAN.",
)
story += data_table(
    ["Model", "Smoothness (↓)", "Edge Pixels", "Noise Ratio (↓)"],
    [
        ["VAE", "Lower (smoother blobs)", "Moderate", "Lower (more connected)"],
        ["GAN", "Higher (sharper, noisier)", "Higher",  "Higher (more fragments)"],
    ],
    col_widths=[2.5*cm, 5.5*cm, 3*cm, 3*cm],
)

# ── SECTION 6: Comparison ─────────────────────────────────────────────────────
story += h1("6.  Comprehensive Comparison: VAE vs. GAN")
story += data_table(
    ["Aspect", "VAE", "GAN"],
    [
        ["Loss functions",
         "MSE reconstruction + KL divergence (ELBO)",
         "Discriminator (BCE) + Generator (Adversarial + λ L₁)"],
        ["Latent space",
         "Smooth, Gaussian-regularised (explicit μ, σ)",
         "Implicit; no explicit distribution"],
        ["Reconstruction quality",
         "Slightly blurry, consistent",
         "Sharper edges (adversarial pressure)"],
        ["ROI smoothness",
         "Smoother, connected blobs (better)",
         "Sharper but noisier masks"],
        ["Noise ratio",
         "Lower; prior prevents fragmentation",
         "Higher; adversarial training can fragment"],
        ["Training stability",
         "Stable, monotonic loss decrease",
         "Sensitive to LR_G / LR_D balance"],
        ["Interpretability",
         "Latent space inspectable via t-SNE",
         "Black-box; no direct latent access"],
    ],
    col_widths=[3.5*cm, 5.8*cm, 4.7*cm],
)
story += [
    key("VAE ROIs are smoother and better regularised due to the KL prior.  "
        "GAN ROIs detect sharper boundaries but are noisier.  "
        "Ensembling the two difference maps (averaging D_VAE and D_GAN) typically "
        "outperforms either model alone by combining their complementary strengths."),
    Spacer(1, 8),
]

# ── SECTION 7: Artefacts ──────────────────────────────────────────────────────
story += h1("7.  Saved Artefacts")
story += h2("7.1  Plot Files")
story += data_table(
    ["File", "Description"],
    [
        ["training_loss_curves.png",       "4-panel loss curves (VAE ELBO + GAN G/D)"],
        ["latent_space_visualization.png", "t-SNE scatter + latent histogram"],
        ["reconstruction_error_plot.png",  "MSE histograms: normal vs. abnormal"],
        ["roi_vae.png",                    "VAE 5-column ROI panel (4 samples)"],
        ["roi_gan.png",                    "GAN 5-column ROI panel (4 samples)"],
        ["roi_quality_comparison.png",     "Bar chart: smoothness and noise ratio"],
        ["edge_pixel_comparison.png",      "Bar chart: edge pixel counts"],
    ],
    col_widths=[6.5*cm, 7.5*cm],
)
story += h2("7.2  NumPy Tensors and Model Weights")
story += data_table(
    ["File", "Content"],
    [
        ["npy/vae_roi.npy",        "VAE binary masks (N, 1, 128, 128)"],
        ["npy/vae_diff.npy",       "VAE raw difference maps"],
        ["npy/vae_abn_orig.npy",   "Abnormal originals for VAE"],
        ["npy/vae_abn_recon.npy",  "VAE reconstructions"],
        ["npy/gan_roi.npy",        "GAN binary masks (N, 1, 128, 128)"],
        ["npy/gan_diff.npy",       "GAN raw difference maps"],
        ["npy/gan_abn_orig.npy",   "Abnormal originals for GAN"],
        ["npy/gan_abn_recon.npy",  "GAN reconstructions"],
        ["vae_weights.pth",        "Saved VAE model weights"],
        ["gan_G_weights.pth",      "Saved GAN generator weights"],
        ["gan_D_weights.pth",      "Saved GAN discriminator weights"],
    ],
    col_widths=[6.5*cm, 7.5*cm],
)

# ── SECTION 8: Conclusion ─────────────────────────────────────────────────────
story += h1("8.  Conclusion")
story += [
    body("This lab successfully demonstrated unsupervised anomaly detection in brain MRI scans "
         "using two generative architectures trained exclusively on normal data.  "
         "The core assumption was validated: models trained on normal anatomy struggle to "
         "reconstruct pathological regions, producing large reconstruction errors localised "
         "at tumour sites."),
    Spacer(1, 4),
]
story += [Paragraph("<b>Key Findings:</b>", BodyS)]
story += [numbered_list([
    "<b>Both VAE and GAN</b> confirm the anomaly-detection hypothesis: abnormal slices "
    "consistently produce higher reconstruction errors than normal slices (Figure 5).",
    "<b>VAE latent space</b> exhibits clear cluster separation between normal and abnormal "
    "samples (Figure 4), providing interpretable evidence without anomaly labels.",
    "<b>VAE ROIs</b> (Figure 6) are smoother and less noisy than GAN ROIs (Figure 7), "
    "as quantified by lower Laplacian std and noise ratio (Figure 8).",
    "<b>GAN ROIs</b> capture sharper boundaries due to the adversarial loss, at the cost "
    "of higher fragmentation.",
    "<b>Ensembling</b> the two difference maps is recommended for best results.",
])]
story += [
    Spacer(1, 6),
    Paragraph("<b>Future Directions:</b>", BodyS),
    bullet_list([
        "β-VAE (β > 1) for more disentangled latent representations.",
        "Conditional GAN variants guided by coarse class labels.",
        "Morphological post-processing of ROI masks (erosion/dilation) to reduce noise "
        "while preserving sharp boundaries.",
    ]),
    Spacer(1, 8),
]

# ── References ────────────────────────────────────────────────────────────────
story += h1("References")
refs = [
    "[1] D. P. Kingma and M. Welling, 'Auto-Encoding Variational Bayes,' ICLR 2014. arXiv:1312.6114",
    "[2] I. Goodfellow et al., 'Generative Adversarial Nets,' NeurIPS 2014. arXiv:1406.2661",
    "[3] P. Isola, J.-Y. Zhu, T. Zhou, and A. A. Efros, 'Image-to-Image Translation with "
    "Conditional Adversarial Networks,' CVPR 2017. arXiv:1611.07004",
    "[4] C. Baur et al., 'Deep Autoencoding Models for Unsupervised Anomaly Segmentation in "
    "Brain MR Images,' MICCAI Workshop 2018.",
    "[5] M. Buda, A. Saha, and M. A. Mazurowski, 'Association of genomic subtypes of "
    "lower-grade gliomas with shape features...,' Computers in Biology and Medicine, 2019.",
]
for r in refs:
    story.append(Paragraph(r, ParagraphStyle("ref", parent=BodyS,
                 leftIndent=20, firstLineIndent=-20, spaceAfter=3)))

# ── Build ─────────────────────────────────────────────────────────────────────

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(STEELBLUE)
    canvas.setLineWidth(0.5)
    # Header line
    canvas.line(doc.leftMargin, A4[1] - doc.topMargin + 4*mm,
                A4[0] - doc.rightMargin, A4[1] - doc.topMargin + 4*mm)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(DARKBLUE)
    canvas.drawString(doc.leftMargin, A4[1] - doc.topMargin + 6*mm,
                      "Lab 06 — Anomaly Detection using VAE & GAN")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(A4[0] - doc.rightMargin, A4[1] - doc.topMargin + 6*mm,
                           "Deep Learning Lab")
    # Footer
    canvas.line(doc.leftMargin, doc.bottomMargin - 4*mm,
                A4[0] - doc.rightMargin, doc.bottomMargin - 4*mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, doc.bottomMargin - 8*mm - 2,
                             str(doc.page))
    canvas.restoreState()

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"\nPDF created: {OUT}")
