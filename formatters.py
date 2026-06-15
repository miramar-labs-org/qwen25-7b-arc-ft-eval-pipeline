# Project-supplied dataset formatters.
#
# Each function signature: (example: dict) -> {"instruction": str, "response": str, "source": str}
# Add one function per dataset listed in config.yaml, then register it in FORMATTERS below.
#
# The Build cell inlines this entire file into the prepare_dataset KFP component body.
# Any imports used here must be available inside the component container — add them
# to prepare_dataset's packages_to_install if they are not already there.


def format_arc_challenge(example):
    question = example.get("question", "")
    texts = example["choices"]["text"]
    labels = example["choices"]["label"]
    choices = "\n".join(f"{labels[i]}. {texts[i]}" for i in range(len(texts)))
    answer = str(example.get("answerKey", "A")).strip().upper()
    return {
        "instruction": f"{question}\n\nOptions:\n{choices}\n\nAnswer with the letter only.",
        "response": answer,
        "source": "arc-challenge",
    }


# Map config.yaml dataset names → formatter functions.
# Each key must match a `name:` entry in config.yaml datasets.
FORMATTERS = {
    "arc-challenge": format_arc_challenge,
}
