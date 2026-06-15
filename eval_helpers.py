# Eval helper functions — inlined into baseline_eval and post_finetune_eval
# by scripts/build_pipeline.py at the # <<< EVAL_HELPERS_INJECT >>> marker.
# Customize extract_answer and _make_user_content for your dataset.
# Do not add imports here that aren't available in the component container.

import re as _re


def extract_answer(text):
    t = text.strip()
    m = _re.match(r'^([A-Ea-e])\b', t)
    if m:
        return m.group(1).upper()
    m = _re.search(r'\b([A-Ea-e])\b', t)
    if m:
        return m.group(1).upper()
    return t[:1].upper() if t else ""


def _make_user_content(row):
    return row["instruction"]


def make_infer_fn(tokenizer, model, system_message, max_new_tokens, do_sample):
    import torch

    def _infer(row):
        messages = [{"role": "user", "content": _make_user_content(row)}]
        ids = tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt"
        ).to(model.device)
        with torch.no_grad():
            out = model.generate(
                ids, max_new_tokens=max_new_tokens, do_sample=do_sample,
                pad_token_id=tokenizer.eos_token_id,
            )
        return tokenizer.decode(out[0][ids.shape[-1]:], skip_special_tokens=True).strip()

    return _infer
