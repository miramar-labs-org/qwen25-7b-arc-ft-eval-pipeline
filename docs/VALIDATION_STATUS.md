# Validation Status — qwen25-7b-arc-ft-eval-pipeline

**Model:** `Qwen/Qwen2.5-7B-Instruct`
**Task:** ARC-Challenge multiple-choice QA fine-tuning via LoRA
**Platform:** Kubeflow Pipelines on NVIDIA DGX Spark (GB10, 128 GB unified memory)
**Last updated:** 2026-06-15

---

## Current Status

| Component              | Status                    |
| ---------------------- | ------------------------- |
| `baseline_eval`        | ✅ Passing (run-001)      |
| `fine_tune`            | ✅ Passing (run-001)      |
| `post_finetune_eval`   | ✅ Passing (run-001)      |
| `baseline_safety_eval` | ✅ Passing (run-001)      |
| `safety_eval`          | ✅ Passing (run-001)      |
| `deployment_gate`      | ✅ PASS (run-001)         |

**run-001 PASS** — baseline 90.09% → post-FT 91.89% (+2.0%); safety 4.99 → 5.0; train loss 0.7022 over 3 epochs.

---

## Run Table

| Run | Purpose | Result | Baseline Accuracy | Key Finding |
| --- | ------- | ------ | ----------------- | ----------- |
| [run-001](../runs/run-001.md) | First e2e run — Qwen2.5-7B-Instruct, ARC-Challenge, LoRA r=16 | ✅ PASS | 0.9009 | Post-FT +2.0% (0.9189); safety near-perfect (5.0/5.0); train_loss 0.7022 |

> Update this table after each run. Pull from `runs/RUNS.md` — keep this doc as the sanitized public summary.

---

## What Is Implemented

### Infrastructure (inherited from platform template)
- KFP v2 pipeline scaffold with all 8 stages wired
- MLflow run-per-stage tracking
- `purge_kfp_mlflow.py`
- Nsight Operator integration — add `kubernetes.add_pod_label(task, "nvidia-nsight-profile", "enabled")` to profile any stage
- BF16 direct loading with `max_memory={0: "100GiB"}` (Blackwell GB10 unified memory)

### Project-specific
- `config.yaml` — Qwen2.5-7B-Instruct, ARC-Challenge (allenai/ai2_arc), LoRA r=16/alpha=32, 3 epochs
- `formatters.py` / `loaders.py` — ARC-Challenge MCQ formatter (choices dict → letter answer)
- `eval_helpers.py` — MCQ letter extraction (A–E regex), `make_infer_fn` with chat template
- `notebook.ipynb` — all 7 USER CODE BLOCKs implemented

---

## What Is Still Pending

- Nsight profiling run (run-002)
- FP8 quantization validation
- GKE serving integration

---

## Known Issues

None.

> **Platform-level fixes** (bitsandbytes on Blackwell, trl 0.29 API, PIP_CONSTRAINT, nsys mmap, CUPTI privileges) are already incorporated in this template. See [qwen25-7b-arc-ft-eval-pipeline/docs/VALIDATION_STATUS.md](https://github.com/miramar-labs-org/qwen25-7b-arc-ft-eval-pipeline/blob/main/docs/VALIDATION_STATUS.md) for the full fix history (first green run).

---

## Fixed Issues

- **`train_dataset` required** — SFTTrainer stub in `fine_tune` USER CODE BLOCK was missing `train_dataset=` arg; fixed during initial implementation.
- **`torch_dtype` deprecation** — `post_finetune_eval` uses `torch_dtype=torch.bfloat16`; should use `dtype=`. Non-breaking (warning only); fix in next notebook edit.
- **PVC `hf-model-cache` missing** — PV/PVC deleted during prior hostPath cleanup but `deploy-kubeflow.yaml` was not re-run; manually recreated with `hostPath=/home/aaron/shared/huggingface-kfp`.

---

## Latest Nsight Finding

No profiling runs yet.
