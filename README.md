# CFR XML Ingestion, Parsing, and Rendering Pipeline

This project builds a **reliable, auditable pipeline** for working with the U.S. **Code of Federal Regulations (CFR)** using **official bulk XML** published by GPO / OFR, with downstream conversion to **JSON** and **HTML** for application use.

The work deliberately avoids unofficial or lossy sources and stays aligned with the **FDsys / govinfo XML schema**.

---

## What This Project Does

### 1. Downloads Official CFR XML (Bulk Data)
- Source: **https://www.govinfo.gov/bulkdata/CFR/**
- Format: **XML only** (there is no official CFR JSON bulk release)
- Scope: **Full CFR titles** (e.g. 33 CFR, 46 CFR)
- Update cadence: **Annual revision cycle**, not weekly

| Title | Name | Annual Revision |
|-----|-----|-----|
| 33 CFR | Navigation and Navigable Waters | July 1 |
| 46 CFR | Shipping | October 1 |
| 49 CFR | Transportation | October 1 |

> The eCFR is updated daily, but **bulk XML snapshots** are anchored to these revision dates.

---

### 2. Parses CFR XML Using `lxml`
- Tooling: **Python + lxml**
- Why lxml:
  - Preserves document order
  - Handles mixed content (text + tags)
  - Supports XPath and XSLT
- Core structural elements parsed:
  - `DIV1–DIV9` (Titles → Sections)
  - `HEAD`, `P`, `CITA`, tables, etc.

Example XPath usage:
```xpath
//DIV8            # All sections
//DIV8/HEAD       # Section titles
//DIV8/P          # Paragraphs
