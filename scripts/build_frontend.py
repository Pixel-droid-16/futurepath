"""Assemble the original v2 HTML from independent editable screen source files.

Run: python scripts/build_frontend.py
This is a lossless split: before you edit, built output is byte-for-byte identical
with the original v2 mockup, including styles and scripts.
"""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'frontend'/'mockup_source'
def assemble_home():
    pieces=[SOURCE/'shell'/'document_before_css.html',SOURCE/'styles'/'v2_theme.css',SOURCE/'shell'/'document_after_css.html']
    pieces += [SOURCE/'pages'/(name+'.html') for name in ('home','intake','results','pathway','signals','about','login')]
    pieces += [SOURCE/'shell'/'after_pages.html',*[SOURCE/'logic'/name for name in ('sdg_colors.js','career_cards.js','declining_careers.js','intake_sample_skills.js','navigation_labels.js')],SOURCE/'logic'/'live_career_adapter.js',SOURCE/'logic'/'state_and_actions.js',*[SOURCE/'logic'/name for name in ('state_values_start.js','career_ranking_view.js','intake_skill_view.js','signal_filters_view.js','home_signal_feed_view.js','sdg_mapping_view.js','live_scenario_comparison_view.js','radar_view.js','page_bindings_view.js')],SOURCE/'shell'/'document_end.html']
    return ''.join(p.read_text(encoding='utf8') for p in pieces)
def assemble_ai_lab():
    return ''.join((SOURCE/'ai_lab'/name).read_text(encoding='utf8') for name in ('01_document_before_css.html','02_style.css','03_document_after_css.html','04_interactions.js','05_document_end.html'))
def main():
    for out,raw in ((ROOT/'frontend'/'index.html',assemble_home()),(ROOT/'frontend'/'ai-lab.html',assemble_ai_lab())):
        old=out.read_text(encoding='utf8')
        if old==raw:
            print(f'UNCHANGED {out.relative_to(ROOT)} SHA256={hashlib.sha256(raw.encode()).hexdigest()}')
        else:
            out.write_text(raw,encoding='utf8')
            print(f'REBUILT {out.relative_to(ROOT)} SHA256={hashlib.sha256(raw.encode()).hexdigest()}')
if __name__=='__main__':main()
