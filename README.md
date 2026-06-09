# 🌾 Crop Recommendation — Workflow CI (Advance)

Repositori ini berisi implementasi **Workflow CI/CD** tingkat **Advance** untuk kursus *Membangun Sistem Machine Learning*, menggunakan dataset **Crop Recommendation** dengan model **Random Forest + GridSearchCV**.

---

## 📁 Struktur Repositori

```
Workflow-CI/
├── .github/
│   └── workflows/
│       └── ci.yml                          ← GitHub Actions Workflow (ADVANCE)
├── MLProject/
│   ├── crop_recommendation_preprocessing/
│   │   └── crop_recommendation_preprocessing.csv   ← Dataset
│   ├── model_output/                       ← Generated saat training (git-ignored)
│   ├── modelling.py                        ← Script training utama
│   ├── conda.yaml                          ← Environment Conda/pip
│   ├── MLProject                           ← Definisi MLflow Project
│   ├── Dockerfile                          ← Docker image definition
│   └── requirements.txt                    ← Dependencies pip
├── .gitignore
└── README.md
```

---

## ✅ Level Kriteria yang Dipenuhi: **ADVANCE (4 pts)**

| Kriteria | Status |
|----------|--------|
| Membuat folder MLProject | ✅ |
| Workflow CI dapat membuat model ketika trigger dipantik | ✅ |
| Menyimpan artefak ke repositori (GitHub Actions Artifact) | ✅ |
| Membuat Docker Image ke Docker Hub via `mlflow models build-docker` | ✅ |

### Steps dalam Workflow (sesuai screenshot Advance):

| # | Step | Keterangan |
|---|------|------------|
| 1 | Set up job | Otomatis oleh GitHub Actions |
| 2 | Run actions/checkout@v3 | Clone repository |
| 3 | Set up Python 3.10 | Setup Python environment |
| 4 | Check Env | Verifikasi environment |
| 5 | Install dependencies | Install semua library |
| 6 | Run mlflow project | Jalankan training + GridSearchCV |
| 7 | Get latest MLflow run_id | Ambil run_id dari MLflow |
| 8 | Install Python dependencies | Verifikasi dependencies artifact |
| 9 | Upload to GitHub | Upload artifact ke GitHub Actions |
| 10 | Build Docker Model | `mlflow models build-docker` |
| 11 | Log in to Docker Hub | Autentikasi Docker Hub |
| 12 | Tag Docker Image | Tag dengan run number & SHA |
| 13 | Push Docker Image | Push ke Docker Hub |
| 14 | Post Log in to Docker Hub | Otomatis (cleanup) |
| 15 | Post Set up Python | Otomatis (cleanup) |
| 16 | Post Run actions/checkout@v3 | Otomatis (cleanup) |
| 17 | Complete job | Otomatis |

---

## 🚀 Setup dari Nol hingga Final

### **FASE 1 — Persiapan Akun & Tools**

#### 1.1 Buat Akun yang Diperlukan

1. **GitHub** → [https://github.com/signup](https://github.com/signup)  
   Pastikan email sudah terverifikasi.

2. **DagsHub** → [https://dagshub.com](https://dagshub.com)  
   Sign up → Connect with GitHub → Buat repository baru:
   - Nama: `crop-recommendation-mlflow` (bebas)
   - Centang: *Initialize this repository*
   - Setelah dibuat, klik **Remote** → salin **MLflow Tracking URL**  
     Format: `https://dagshub.com/<username>/<repo>.mlflow`

3. **Docker Hub** → [https://hub.docker.com/signup](https://hub.docker.com/signup)  
   Setelah login, buat **Access Token**:
   - Klik avatar → Account Settings → Security → New Access Token
   - Nama token: `github-actions`
   - Permission: **Read, Write, Delete**
   - **SIMPAN token-nya** (hanya tampil sekali!)

#### 1.2 Install Tools Lokal (Opsional, untuk testing lokal)

```bash
# Install Python 3.10+
# Download: https://www.python.org/downloads/

# Install dependencies
pip install mlflow==2.12.2 scikit-learn==1.4.2 pandas==2.2.2 numpy==1.26.4

# Install Docker Desktop
# Download: https://www.docker.com/products/docker-desktop/

# Verifikasi
python --version
mlflow --version
docker --version
```

---

### **FASE 2 — Buat Repository GitHub**

#### 2.1 Buat Repository Baru

1. Buka [https://github.com/new](https://github.com/new)
2. Isi:
   - **Repository name**: `Workflow-CI`
   - **Visibility**: ✅ **Public** (wajib agar bisa direview)
   - **Add a README file**: ❌ (jangan centang, kita sudah punya)
3. Klik **Create repository**

#### 2.2 Clone & Setup Lokal

```bash
# Clone repository kosong
git clone https://github.com/<USERNAME_GITHUB>/Workflow-CI.git
cd Workflow-CI
```

---

### **FASE 3 — Setup Secrets GitHub**

> ⚠️ **PENTING**: Secrets WAJIB diisi sebelum workflow dijalankan!

1. Buka repository di GitHub
2. Klik **Settings** → **Secrets and variables** → **Actions**
3. Klik **New repository secret** untuk masing-masing:

| Secret Name | Nilai | Cara Mendapatkan |
|-------------|-------|------------------|
| `MLFLOW_TRACKING_URI` | `https://dagshub.com/<user>/<repo>.mlflow` | DagsHub → Remote → MLflow |
| `MLFLOW_TRACKING_USERNAME` | username DagsHub kamu | Profile DagsHub |
| `MLFLOW_TRACKING_PASSWORD` | token DagsHub | DagsHub → Settings → Tokens → New Token (scope: `repo`) |
| `DOCKERHUB_USERNAME` | username Docker Hub kamu | Profile Docker Hub |
| `DOCKERHUB_TOKEN` | access token Docker Hub | Account Settings → Security → Access Token |

**Cara buat DagsHub Token:**
1. Login DagsHub → klik avatar → **User Settings**
2. **Tokens** → **Generate New Token**
3. Nama: `github-actions-token`, centang `repo`
4. Generate → Salin token

---

### **FASE 4 — Upload File ke Repository**

#### 4.1 Struktur File yang Perlu di-Upload

Salin semua file dari folder `Workflow-CI/` ini ke dalam repository yang sudah di-clone:

```
Workflow-CI/               ← root repository
├── .github/
│   └── workflows/
│       └── ci.yml
├── MLProject/
│   ├── crop_recommendation_preprocessing/
│   │   └── crop_recommendation_preprocessing.csv
│   ├── modelling.py
│   ├── conda.yaml
│   ├── MLProject
│   ├── Dockerfile
│   └── requirements.txt
├── .gitignore
└── README.md
```

#### 4.2 Push ke GitHub

```bash
cd Workflow-CI

# Tambahkan semua file
git add .

# Commit
git commit -m "feat: initial setup Workflow-CI advance level"

# Push ke main (trigger CI otomatis!)
git push origin main
```

> ✅ **Push ke `main` otomatis memicu GitHub Actions workflow!**

---

### **FASE 5 — Monitoring Workflow**

#### 5.1 Pantau di GitHub Actions

1. Buka repository → klik tab **Actions**
2. Klik workflow run yang sedang berjalan
3. Klik job **train-and-deploy**
4. Pantau setiap step real-time

#### 5.2 Estimasi Waktu per Step

| Step | Estimasi Waktu |
|------|----------------|
| Checkout | < 1 menit |
| Setup Python | < 1 menit |
| Install dependencies | 2–3 menit |
| Run mlflow project (GridSearchCV) | 3–8 menit |
| Get run_id | < 1 menit |
| Upload to GitHub | < 1 menit |
| Build Docker Model | 5–10 menit |
| Push Docker Image | 2–3 menit |
| **Total** | **~15–25 menit** |

#### 5.3 Verifikasi Hasil

Setelah workflow selesai (✅ hijau):

**GitHub Actions Artifacts:**
1. Klik workflow run → scroll ke bawah → bagian **Artifacts**
2. Download `crop-recommendation-artifacts-<run_number>`
3. Berisi: `model_output/`, `classification_report.txt`, `confusion_matrix.csv`, `run_id.txt`

**Docker Hub:**
1. Login [https://hub.docker.com](https://hub.docker.com)
2. Cari repository `<username>/crop-recommendation-model`
3. Harus ada tag: `latest` dan `run-<number>`

**DagsHub MLflow:**
1. Buka `https://dagshub.com/<username>/<repo>`
2. Klik tab **MLflow**
3. Lihat experiment `crop-recommendation-rf`
4. Cek metrics: accuracy, f1_score, precision, recall

---

### **FASE 6 — Testing Lokal (Opsional)**

Jika ingin mencoba jalankan secara lokal sebelum push:

```bash
cd MLProject

# Install dependencies
pip install -r requirements.txt

# Set environment variables MLflow (opsional, tanpa ini pakai local tracking)
export MLFLOW_TRACKING_URI="https://dagshub.com/<user>/<repo>.mlflow"
export MLFLOW_TRACKING_USERNAME="<dagshub_username>"
export MLFLOW_TRACKING_PASSWORD="<dagshub_token>"

# Jalankan MLflow Project
mlflow run . --env-manager=local

# Atau dengan parameter custom:
mlflow run . \
  --env-manager=local \
  -P n_estimators="[100, 200, 300]" \
  -P max_depth="[null, 10]" \
  -P cv_folds=3
```

**Hasil yang diharapkan:**
```
[INFO] Loading data from: crop_recommendation_preprocessing/...
[INFO] Shape: (2112, 9)
[INFO] Running GridSearchCV ...
[RESULT] Accuracy  : ~0.99
[RESULT] F1 Score  : ~0.99
[RESULT] CV Mean   : ~0.99
[DONE] MLflow run completed: <run_id>
```

#### Test Docker Image Lokal:
```bash
cd MLProject

# Build image
docker build -t crop-recommendation-model:local .

# Jalankan container
docker run -p 5001:5001 crop-recommendation-model:local

# Test endpoint (buka terminal baru)
curl -X POST http://localhost:5001/invocations \
  -H "Content-Type: application/json" \
  -d '{"dataframe_split": {"columns": ["N","P","K","temperature","humidity","ph","rainfall"], "data": [[0.64, 0.26, 0.19, 0.32, 0.79, 0.47, 0.66]]}}'
```

---

### **FASE 7 — Trigger Manual Workflow**

Selain otomatis via push, bisa trigger manual dengan parameter custom:

1. GitHub → Actions → **CI - Crop Recommendation (Advance)**
2. Klik **Run workflow**
3. Isi parameter:
   - `n_estimators`: `[100, 200, 300]`
   - `max_depth`: `[null, 5, 10, 20]`
   - `min_samples_split`: `[2, 5, 10]`
4. Klik **Run workflow** (hijau)

---

## 📊 Model Details

| Item | Detail |
|------|--------|
| **Dataset** | Crop Recommendation (preprocessing) |
| **Records** | 2.112 baris |
| **Features** | N, P, K, temperature, humidity, ph, rainfall |
| **Target** | `label_encoded` (22 kelas tanaman) |
| **Algorithm** | Random Forest Classifier |
| **Optimization** | GridSearchCV (5-fold CV) |
| **Expected Accuracy** | ~0.99 |

### Kelas Tanaman (22):
rice, maize, chickpea, kidneybeans, pigeonpeas, mothbeans, mungbean, blackgram, lentil, pomegranate, banana, mango, grapes, watermelon, muskmelon, apple, orange, papaya, coconut, cotton, jute, coffee

---

## 🔧 Troubleshooting

### ❌ Error: `mlflow.exceptions.MlflowException: DagsHub credentials`
**Solusi:** Pastikan secrets `MLFLOW_TRACKING_USERNAME` dan `MLFLOW_TRACKING_PASSWORD` sudah benar. DagsHub password harus berupa **token**, bukan password login.

### ❌ Error: `docker: permission denied`
**Solusi:** Step "Build Docker Model" memerlukan Docker daemon. GitHub-hosted runners (`ubuntu-latest`) sudah include Docker, jadi tidak perlu setup tambahan.

### ❌ Error: `mlflow models build-docker: model_output not found`
**Solusi:** Pastikan step "Run mlflow project" berhasil dan `model_output/` terbuat. Cek log di step 6.

### ❌ Error: `denied: requested access to the resource is denied` (Docker push)
**Solusi:** Cek secret `DOCKERHUB_TOKEN` — harus berupa **Access Token**, bukan password Docker Hub biasa.

### ❌ Error: `No files were found with the provided path` (Upload artifact)
**Solusi:** Beberapa file seperti `mlruns/` mungkin tidak ada jika MLflow menggunakan remote tracking. Ini tidak critical — artifact utama (`model_output/`) tetap akan ter-upload.

### ❌ Workflow tidak terpantik saat push
**Solusi:** 
- Pastikan file `ci.yml` ada di path `.github/workflows/ci.yml` (persis)
- Pastikan push ke branch `main` (bukan `master`)

---

## 🐳 Docker Hub

Setelah workflow berhasil, Docker image tersedia di:

```
https://hub.docker.com/r/<DOCKERHUB_USERNAME>/crop-recommendation-model
```

**Pull image:**
```bash
docker pull <DOCKERHUB_USERNAME>/crop-recommendation-model:latest
```

**Jalankan container:**
```bash
docker run -p 5001:5001 <DOCKERHUB_USERNAME>/crop-recommendation-model:latest
```

---

## 📈 MLflow Tracking (DagsHub)

Semua eksperimen tersimpan di DagsHub:

```
https://dagshub.com/<DAGSHUB_USERNAME>/<REPO_NAME>
```

Metrics yang di-track:
- `accuracy` — akurasi test set
- `f1_score` — F1 weighted
- `precision` — precision weighted
- `recall` — recall weighted
- `cv_mean_accuracy` — rata-rata cross-validation
- `cv_std_accuracy` — standar deviasi cross-validation
- `best_cv_score` — skor terbaik GridSearchCV

---

## 📝 Lisensi

MIT License — bebas digunakan untuk keperluan akademik.

---

*Dibuat untuk submission kursus Membangun Sistem Machine Learning — Kriteria 3 (Advance)*
