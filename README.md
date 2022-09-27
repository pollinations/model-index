# Model index

This repository is automatically updated by the CIs of the cog-model repositories.

## How it works
### Pollinations models with their own repo
- have their own ci
- ci builds image and gets inspect.json
- then clones this repo and adds the `<repo/path>/meta.json` and `<repo/path>/inspect.json`
- calls `python add_model.py <repo> <registry url>`
    - updates `images.json` and `metadata.json`

### External models
- trigger `python .github/workflows/get_openapi.py` from the ci
- 