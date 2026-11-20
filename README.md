# Documentation claim auditor

This offline static auditor compares documentation of the checked capability with Python source patterns. It scans the root README and Markdown under docs. Fenced code is excluded; inline code counts. Source is parsed without execution. Tests are reported separately; fixtures, examples, documentation and symlinks are excluded from production evidence.

```sh
pdf-merging-claim-audit audit . --json --fail-on medium --ignore vendor/
python3 -m pdf_merging_claim_audit --version
```

Exit 0 means PASS, 2 means a finding meets the threshold, and 1 means a usage or I/O error. The default threshold is high. Ignore prefixes can be repeated.

```
documented-pdf-merging-claim-false
documented-no-pdf-merging-claim-false
```

## Limitations

Exact phrases can refer to form fields, annotations, or an N-up page layout instead of the checked capability. They can also describe a job title or a wrapper. A phrase can describe attaching a file to email or a database record, or a version control conflict. External-command implementations can lead to findings.

Pairs are matched within a module, not on the same variable: unrelated calls can satisfy a pair. A writer with an append or merge call counts even when only one file is appended. The same holds for a merger object. An argument-free PyMuPDF opener counts with insert_pdf. A new empty pikepdf document counts with pages.extend.

A writer or merger construction alone does not count. A writer or merger followed only by write does not count. Bare append or merge calls need a matching construction. Bare insert_pdf needs a matching PyMuPDF opener. Bare pages.extend needs a matching pikepdf opener. A pikepdf pages.append call does not count. Bare addpages needs a matching pdfrw writer. Singular pdfrw addpage does not count. A writer's add_page does not count. A reader alone does not count. An opener followed only by save does not count. Splitting files is not detected. Generation with reportlab or openpyxl is not detected. Commands invoking pdfunite, qpdf or Ghostscript are not detected.

Mindee calls are not detected. Azure model calls are not detected. Veryfi calls are not detected. Google Document AI processor calls are not detected. Eden AI model calls are not detected. Textract calls are not detected. LlamaParse calls are not detected. Nanonets calls are not detected. Docsumo calls are not detected. ABBYY Vantage calls are not detected. Rossum calls are not detected. Klippa calls are not detected. Parseur calls are not detected. Extend calls are not detected. These services use extraction operations or opaque identifiers. Hand-written object-stream parsing is not detected. Encrypted inputs need decryption; this tool cannot determine whether inputs are encrypted.

Static patterns are not semantic judgment. Dead code counts; some alias chains are missed. Denial handling depends on the listed phrases, and each pair must occur in one module. Other claims involving extraction, generation, splitting, OCR, document cropping, electronic signatures, payment processing, and the many document types handled by other auditors are outside the phrase lists.

The following claim categories are outside the phrase lists:

- PDF extraction.
- PDF generation.
- Spreadsheet reading.
- Spreadsheet generation.
- Word document reading.
- Word document generation.
- Presentation reading.
- Presentation generation.
- Table extraction.
- PDF splitting.
- Invoice extraction.
- Receipt extraction.
- Identity document extraction.
- Bank check extraction.
- Bank statement extraction.
- Tax form extraction.
- Pay stub extraction.
- Health insurance card extraction.
- Business card extraction.
- Credit card extraction.
- Contract extraction.
- Mortgage extraction.
- Resume extraction.
- Bill of lading extraction.
- Delivery note extraction.
- Carte grise extraction.
- Energy bill extraction.
- Marriage certificate extraction.
- Bank account details extraction.
- Nutrition facts label extraction.
- Material certificate extraction.
- US mail extraction.
- Invoice splitting.
- Multiple receipt detection.
- French health card extraction.
- Indian passport extraction.
- Driver license extraction.
- Vaccination card extraction.
- Document cropping.
- Electronic signatures.
- Payment processing.
- OCR.
