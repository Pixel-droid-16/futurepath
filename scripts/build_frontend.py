"""Assemble the original v2 HTML from independent editable screen source files.

Run: python scripts/build_frontend.py
This is a lossless split: before you edit, built output is byte-for-byte identical
with the original v2 mockup, including styles and scripts.
"""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'frontend'/'mockup_source'
def assemble_home(source=None):
    source = SOURCE if source is None else Path(source)
    pieces=[source/'shell'/'document_before_css.html',source/'styles'/'v2_theme.css',source/'shell'/'document_after_css.html']
    pieces += [source/'pages'/(name+'.html') for name in ('home','start','results','pathway','signals','about')]
    pieces += [source/'shell'/'after_pages.html',*[source/'logic'/name for name in ('translations.js','sdg_colors.js','career_cards.js','declining_careers.js','navigation_labels.js')],source/'logic'/'live_career_adapter.js',source/'logic'/'state_and_actions.js',*[source/'logic'/name for name in ('state_values_start.js','career_ranking_view.js','start_confirm_view.js','signal_filters_view.js','skill_trends_view.js','home_signal_feed_view.js','sdg_mapping_view.js','live_scenario_comparison_view.js','page_bindings_view.js')],source/'shell'/'document_end.html']
    return ''.join(p.read_text(encoding='utf8') for p in pieces)
def main():
    for out,raw in ((ROOT/'frontend'/'index.html',assemble_home()),):
        old=out.read_text(encoding='utf8')
        if old==raw:
            print(f'UNCHANGED {out.relative_to(ROOT)} SHA256={hashlib.sha256(raw.encode()).hexdigest()}')
        else:
            out.write_text(raw,encoding='utf8')
            print(f'REBUILT {out.relative_to(ROOT)} SHA256={hashlib.sha256(raw.encode()).hexdigest()}')
if __name__=='__main__':main()
