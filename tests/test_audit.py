EXPECTED_PDFMERGING = ('pdf merging', 'merge pdf', 'merges pdf', 'merging pdf', 'merge pdfs', 'merges pdfs', 'merging pdfs', 'merge pdf file', 'merges pdf file', 'merging pdf file', 'merge pdf files', 'merges pdf files', 'merging pdf files', 'merge pdf document', 'merges pdf document', 'merging pdf document', 'merge pdf documents', 'combine pdf', 'combines pdf', 'combining pdf', 'combine pdfs', 'combines pdfs', 'combining pdfs', 'combine pdf files', 'combines pdf files', 'combining pdf files', 'combine pdf documents', 'join pdf', 'joins pdf', 'joining pdf', 'join pdfs', 'joins pdfs', 'joining pdfs', 'join pdf files', 'concatenate pdf', 'concatenates pdf', 'concatenating pdf', 'concatenate pdfs', 'concatenates pdfs', 'concatenating pdfs', 'pdf merger', 'pdf combiner', 'pdf combining', 'pdf concatenation', 'merge multiple pdfs', 'merges multiple pdfs', 'merging multiple pdfs', 'combine multiple pdfs', 'merge pdfs into one', 'pdf merge')
EXPECTED_NOPDFMERGING = ('no pdf merging', 'does not merge pdf', 'does not merge pdfs', 'does not merge pdf files', 'does not merge pdf document', 'does not merge pdf documents', 'does not combine pdf', 'does not combine pdfs', 'does not combine pdf files', 'does not combine pdf documents', 'does not join pdf', 'does not join pdfs', 'does not join pdf files', 'does not concatenate pdf', 'does not concatenate pdfs', 'no pdf merger', 'no pdf combiner', 'does not support pdf merging', 'without pdf merging', 'pdf merging not supported', 'no pdf merging support', 'does not merge multiple pdfs', 'does not combine multiple pdfs', 'does not merge pdfs into one')
EXPECTED_GENERIC = ('merge_pdf', 'merge_pdfs', 'merge_pdf_file', 'merge_pdf_files', 'merge_pdf_document', 'merge_pdf_documents', 'combine_pdf', 'combine_pdfs', 'combine_pdf_file', 'combine_pdf_files', 'combine_pdf_document', 'combine_pdf_documents', 'join_pdf', 'join_pdfs', 'join_pdf_file', 'join_pdf_files', 'concatenate_pdf', 'concatenate_pdfs', 'concat_pdf', 'concat_pdfs', 'pdf_merger', 'pdf_combiner', 'pdf_merge', 'merge_pdfs_into_one')

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from pdf_merging_claim_audit.audit import audit, evidence
from pdf_merging_claim_audit.phrases import PDFMERGING, NOPDFMERGING, GENERIC_NAMES

class AuditTests(unittest.TestCase):
    def test_phrase_oracle(self):
        self.assertEqual(PDFMERGING, EXPECTED_PDFMERGING)
        self.assertEqual(NOPDFMERGING, EXPECTED_NOPDFMERGING)
        self.assertEqual(GENERIC_NAMES, EXPECTED_GENERIC)

    def test_routes(self):
        cases = [
            'from pypdf import PdfWriter\nPdfWriter().append(x)', 'import pypdf\npypdf.PdfWriter().append(x)',
            'import pypdf as p\np.PdfWriter().merge(x)', 'from pypdf import PdfWriter\nPdfWriter(fileobj=x).append(x)',
            'from PyPDF2 import PdfWriter\nPdfWriter().append(x)', 'import PyPDF2\nPyPDF2.PdfWriter().merge(x)',
            'from PyPDF2 import PdfFileWriter\nPdfFileWriter().append(x)', 'from PyPDF2 import PdfMerger\nPdfMerger().append(x)',
            'import PyPDF2\nPyPDF2.PdfMerger().merge(x)', 'from PyPDF2 import PdfFileMerger\nPdfFileMerger().append(x)',
            'import PyPDF2 as p\np.PdfMerger().append(x)', 'from fitz import open as op\nop(x).insert_pdf(x)',
            'import fitz\nfitz.open(x).insert_pdf(x)', 'import fitz\nfitz.open().insert_pdf(x)',
            'from fitz import Document\nDocument(x).insert_pdf(x)', 'import fitz\nfitz.Document(x).insert_pdf(x)',
            'import pymupdf\npymupdf.open(x).insert_pdf(x)', 'import pymupdf\npymupdf.Document(x).insert_pdf(x)',
            'import pikepdf\npikepdf.Pdf.open(x).pages.extend(x)', 'from pikepdf import open as op\nop(x).pages.extend(x)',
            'import pikepdf\npikepdf.Pdf.new().pages.extend(x)', 'from pikepdf import new\nnew().pages.extend(x)',
            'from pdfrw import PdfWriter\nPdfWriter().addpages(x)', 'import pdfrw\npdfrw.PdfWriter().addpages(x)',
            'from pdfrw import PdfFileWriter\nPdfFileWriter().addpages(x)', 'from pikepdf import Pdf as P\nP.open(x).pages.extend(x)',
            'from other import merge_pdfs as m\nm(x)']
        cases += ['x.' + name + '(x)' for name in EXPECTED_GENERIC]
        for source in cases:
            with self.subTest(source=source): self.assertTrue(evidence(source))

    def test_not_evidence(self):
        cases = ['import '+x for x in ('pypdf','PyPDF2','fitz','pymupdf','pikepdf','pdfrw')]
        cases += ['import pypdf\npypdf.PdfWriter()', 'import PyPDF2\nPyPDF2.PdfMerger()', 'import PyPDF2\nPyPDF2.PdfFileMerger()', 'x.append(y)', 'x.merge(y)', 'import pypdf\npypdf.PdfWriter().write(x)', 'import PyPDF2\nPyPDF2.PdfMerger().write(x)', 'import fitz\nfitz.open(x)', 'import fitz\nfitz.open()', 'x.insert_pdf(y)', 'import pikepdf\npikepdf.Pdf.open(x)', 'import pikepdf\npikepdf.new()', 'x.pages.extend(y)', 'import pikepdf\npikepdf.new().pages.append(x)', 'import pdfrw\npdfrw.PdfWriter()', 'x.addpages(y)', 'import pdfrw\npdfrw.PdfWriter().addpage(x)', 'import pypdf\npypdf.PdfReader(x)', 'import pypdf\npypdf.PdfWriter().add_page(x)', 'import pdfplumber\npdfplumber.open(x)', 'from pdfminer.high_level import extract_text\nextract_text(x)', 'import reportlab\nreportlab.Canvas(x).save()', 'import fitz\nfitz.open().insert_text(x)\nx.save()', 'import fitz\nfitz.open(x).save(x)', '"pdf"', 'x.merge_pdfs', 'import pypdf\ndef PdfWriter(): pass\npypdf.PdfWriter().append(x)', 'import pypdf\npypdf=1\npypdf.PdfWriter().append(x)', 'def merge_pdfs(): pass\nx.merge_pdfs()', 'import pikepdf\npikepdf.open().pages.extend(x)', 'import pypdf\npypdf.PdfMerger().append(x)', 'def broken(']
        cases += ['import subprocess\nsubprocess.run(["'+x+'", "x"])' for x in ('pdfunite','qpdf','gs')]
        cases += [x+'(x)' for x in ('mindee.parse','azure.begin_analyze_document','veryfi.Client','documentai.process_document','textract.analyze_document','eden.universal_ai','llamaparse.parse','nanonets.ocr','docsumo.upload','abbYY.process','rossum.process','klippa.parse','parseur.parse','extend.parse')]
        for source in cases:
            with self.subTest(source=source): self.assertFalse(evidence(source))

    def test_audit_scenarios(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); readme=p/'README.md'; src=p/'app.py'
            readme.write_text('merge pdf files'); self.assertEqual(audit(d)['findings'][0]['severity'],'HIGH')
            src.write_text('import pypdf\npypdf.PdfWriter().append(x)'); self.assertEqual(audit(d)['verdict'],'PASS')
            readme.write_text('does not merge pdf files'); result=audit(d); self.assertEqual(result['findings'][0]['rule'],'documented-no-pdf-merging-claim-false'); self.assertEqual(result['claims'],[])
            src.unlink(); self.assertEqual(audit(d)['verdict'],'PASS')
            readme.write_text('```\nmerge pdf files\n```'); self.assertEqual(audit(d)['verdict'],'PASS')
            readme.write_text('`merge pdf files`'); self.assertEqual(audit(d)['verdict'],'FAIL')
            (p/'tests').mkdir(); (p/'tests/test_app.py').write_text('import pypdf\npypdf.PdfWriter().append(x)')
            self.assertEqual(audit(d)['findings'][0]['severity'],'MEDIUM'); self.assertEqual(audit(d)['verdict'],'PASS'); self.assertEqual(audit(d, fail_on='medium')['verdict'],'FAIL')
            src.write_text('import pypdf\npypdf.PdfWriter()'); (p/'other.py').write_text('x.append(y)'); self.assertEqual(audit(d)['findings'][0]['severity'],'MEDIUM')
            readme.write_text('Nothing claimed'); self.assertEqual(audit(d)['verdict'],'PASS')

    def test_exclusions(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('merge pdf')
            for name in ('fixtures', 'examples', 'docs'):
                (p/name).mkdir(); (p/name/'code.py').write_text('x.merge_pdfs()')
            (p/'test_file.py').write_text('x.merge_pdfs()'); (p/'app_test.py').write_text('x.merge_pdfs()')
            (p/'link.py').symlink_to(p/'test_file.py'); (p/'linked').symlink_to(p/'fixtures', target_is_directory=True)
            r=audit(d); self.assertFalse(r['production_evidence']); self.assertEqual(len(r['test_evidence']),2)
            self.assertEqual(audit(d, ignore=('test_', 'app_'))['findings'][0]['severity'], 'HIGH')

    def test_cli(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('merge pdf')
            cmd=[sys.executable, '-m', 'pdf_merging_claim_audit']
            r=subprocess.run(cmd+['audit',d,'--json'], capture_output=True,text=True); self.assertEqual(r.returncode,2)
            data=json.loads(r.stdout); self.assertEqual(data['verdict'],'FAIL'); self.assertEqual(data['findings'][0]['rule'],'documented-pdf-merging-claim-false'); self.assertTrue(data['findings'][0]['message'])
            self.assertEqual(subprocess.run(cmd+['--version'],capture_output=True,text=True).stdout.strip(),'0.1.0')
            self.assertEqual(subprocess.run(cmd+['audit',d,'--fail-on','HIGH'],capture_output=True).returncode,1)
            self.assertEqual(subprocess.run(cmd+['audit',d+'/missing'],capture_output=True).returncode,1)
