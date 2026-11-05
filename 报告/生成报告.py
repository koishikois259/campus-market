"""Build the UML and UI report from Markdown and selected PNGs.

Run with the Codex bundled Python runtime (python-docx and Pillow required).
All pages use A4 portrait; figures retain their original aspect ratios.
"""
from pathlib import Path
import argparse
import re

from docx import Document
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / '实验报告.md'
OUTPUT = ROOT / '实验报告.docx'


def font(run, size=10.5, bold=False, east_asia='宋体'):
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)
    props = run._element.get_or_add_rPr()
    fonts = props.rFonts
    if fonts is None:
        fonts = OxmlElement('w:rFonts')
        props.insert(0, fonts)
    fonts.set(qn('w:ascii'), 'Times New Roman')
    fonts.set(qn('w:hAnsi'), 'Times New Roman')
    fonts.set(qn('w:eastAsia'), east_asia)


def table(doc, rows):
    result = doc.add_table(rows=1, cols=2)
    result.alignment = WD_TABLE_ALIGNMENT.CENTER
    result.autofit = False
    result.columns[0].width = Cm(5.1)
    result.columns[1].width = Cm(11.9)
    props = result._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        border = OxmlElement('w:' + side)
        for key, value in {'val': 'single', 'sz': '4', 'color': 'D9D9D9'}.items():
            border.set(qn('w:' + key), value)
        borders.append(border)
    props.append(borders)
    margins = OxmlElement('w:tblCellMar')
    for side, value in [('top', '60'), ('bottom', '60'), ('left', '110'), ('right', '110')]:
        child = OxmlElement('w:' + side)
        child.set(qn('w:w'), value)
        child.set(qn('w:type'), 'dxa')
        margins.append(child)
    props.append(margins)
    for index, data in enumerate(rows):
        cells = result.rows[0].cells if index == 0 else result.add_row().cells
        row = result.rows[index]
        row_props = row._tr.get_or_add_trPr()
        no_split = OxmlElement('w:cantSplit')
        row_props.append(no_split)
        if index == 0:
            row_props.append(OxmlElement('w:tblHeader'))
        for col, text in enumerate(data):
            cells[col].width = Cm(5.1 if col == 0 else 11.9)
            cells[col].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cells[col].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.line_spacing = Pt(14)
            font(p.add_run(text), 10, index == 0)
            if index == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                shading = OxmlElement('w:shd')
                shading.set(qn('w:fill'), 'EDEDED')
                cells[col]._tc.get_or_add_tcPr().append(shading)
    return result


def new_section(doc, figure=False):
    section = doc.add_section(WD_SECTION_START.NEW_PAGE)
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin = section.bottom_margin = Cm(1.2 if figure else 1.6)
    section.left_margin = section.right_margin = Cm(1.2 if figure else 2)
    return section


def normalize_text_colors(doc):
    """Use explicit black for text, including linked heading/strong styles."""
    def black(properties):
        color = properties.get_or_add_color()
        # Remove themeColor/themeTint/themeShade as well as cached RGB values.
        color.attrib.clear()
        color.set(qn('w:val'), '000000')

    for style in doc.styles:
        if style.type in (WD_STYLE_TYPE.PARAGRAPH, WD_STYLE_TYPE.CHARACTER):
            black(style.element.get_or_add_rPr())
    for properties in doc.styles.element.xpath('./w:docDefaults/w:rPrDefault/w:rPr'):
        black(properties)
    parts = [doc.part] + [part for part in doc.part.related_parts.values()
                         if part.content_type.endswith(('header+xml', 'footer+xml'))]
    for part in parts:
        for run in part.element.xpath('.//w:r'):
            black(run.get_or_add_rPr())


def main(output=OUTPUT):
    doc = Document()
    # The bundled Word base can carry a blue bottom border on Title/Normal.
    # Remove inherited paragraph rules as well as direct paragraph borders.
    for border in list(doc.styles.element.xpath('.//w:pBdr')):
        border.getparent().remove(border)
    for border in list(doc.element.xpath('.//w:pBdr')):
        border.getparent().remove(border)
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin, section.bottom_margin = Cm(1.6), Cm(1.6)
    section.left_margin, section.right_margin = Cm(2), Cm(2)
    section.header_distance, section.footer_distance = Cm(.6), Cm(.7)
    for name, size in [('Normal', 10.5), ('Title', 18), ('Heading 1', 13), ('Heading 2', 11)]:
        style = doc.styles[name]
        style.font.name = 'Times New Roman'
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), '宋体' if name == 'Normal' else '黑体')
        if name.startswith('Heading'):
            style.font.bold = True
            style.paragraph_format.space_before = Pt(7)
            style.paragraph_format.space_after = Pt(4)
        style.paragraph_format.widow_control = True
    doc.styles['Normal'].paragraph_format.line_spacing = Pt(16)
    doc.styles['Normal'].paragraph_format.space_after = Pt(4)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    font(footer.add_run('软件工程实验二  UML与UI设计    '), 9)
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'), 'PAGE')
    footer._p.append(field)
    lines = SOURCE.read_text(encoding='utf-8').splitlines()
    i = 0
    figure_page = False
    figure_width = None
    ui_mode = False
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        if line == '<!-- figure-page -->':
            figure_page = True
            continue
        elif line.startswith('<!-- figure-width:'):
            figure_width = float(line.removeprefix('<!-- figure-width:').removesuffix('-->').strip())
            assert figure_width > 0
            continue
        elif line == '<!-- page-break -->':
            section = new_section(doc)
            ui_mode = False
            continue
        elif line == '<!-- ui-start -->':
            section = new_section(doc, figure=True)
            ui_mode = True
            continue
        elif line.startswith('# '):
            p = doc.add_paragraph(style='Title')
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(5)
            font(p.add_run(line[2:]), 18, True, '黑体')
        elif line.startswith('### '):
            p = doc.add_paragraph(line[4:], style='Heading 2')
            if ui_mode:
                p.paragraph_format.space_before = Pt(5)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = Pt(14)
        elif line.startswith('## '):
            p = doc.add_paragraph(line[3:], style='Heading 1')
        elif line.startswith('|'):
            rows = []
            i -= 1
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = [cell.strip() for cell in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', cell) for cell in row):
                    rows.append(row)
                i += 1
            table(doc, rows)
        elif line.startswith('!['):
            match = re.fullmatch(r'!\[(.*?)\]\((.*?)\)', line)
            assert match
            caption, relative_path = match.groups()
            figure = (ROOT / relative_path).resolve()
            if figure_page:
                section = new_section(doc, figure=True)
                figure_page = False
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1
            p.paragraph_format.keep_with_next = True
            with Image.open(figure) as image:
                w, h = image.size
            available_width = (section.page_width - section.left_margin - section.right_margin) / Cm(1)
            image_width = min(available_width, figure_width or available_width, 25.6 * w / h)
            if ui_mode:
                # Stack related UI blocks in the normal text flow, with room for
                # their headings, descriptions and captions on A4 portrait.
                image_width = min(image_width, 15.5, 10.6 * w / h)
            figure_width = None
            picture = p.add_run().add_picture(str(figure), width=Cm(image_width))
            picture._inline.docPr.set('descr', caption)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            if ui_mode:
                p.paragraph_format.line_spacing = Pt(12)
                p.paragraph_format.space_after = Pt(4)
            font(p.add_run(caption), 9.5 if ui_mode else 10.5)
        else:
            p = doc.add_paragraph()
            if line.startswith('学号 ') or line.startswith('阶段稿'):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.line_spacing = Pt(14)
                font(p.add_run(line), 9.5)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.first_line_indent = Pt(21)
                if ui_mode:
                    p.paragraph_format.line_spacing = Pt(14)
                    p.paragraph_format.space_after = Pt(3)
                    # Keep the introduction with its picture, and the picture
                    # with its caption; do not strand text at the page bottom.
                    p.paragraph_format.keep_with_next = True
                font(p.add_run(line))
    doc.core_properties.author = '贾一帆'
    doc.core_properties.title = '校园二手交易系统实验二报告'
    doc.core_properties.subject = '四种UML图 八模块UI及AI辅助改进'
    normalize_text_colors(doc)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    print(str(output))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=OUTPUT)
    main(parser.parse_args().output)
