# QR Logo Generator
Custom styled QR code generator with centered logo text and SVG output.

## Features

* High-error correction QR
* Center circle logo
* Auto-scaling text
* SVG vector output
* Fully customizable

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Output

Generates:

```
qr.svg
```

## Customize

Edit settings in `main.py`:

```python
TEXT_TOP = "HELLO"
TEXT_BOTTOM = "WORLD"
```

---

Made with Python + Segno
