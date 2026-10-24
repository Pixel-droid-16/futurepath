"""Offline Chromium checks: public Signals UI, protected admin API and independent paging."""
import re

import pytest
from playwright.sync_api import expect


@pytest.mark.parametrize('server', ['signals'], indirect=True)
def test_read_only_signals_ui_preserves_protected_approval_api(page, server):
    page.goto(server + '/signals')
    expect(page.get_by_role('heading', name='The evidence behind every score')).to_be_visible()
    for label in ('Reload saved signals', 'Admin: refresh live feeds', 'Review pending evidence'):
        expect(page.get_by_role('button', name=label)).to_have_count(0)

    api = page.request
    initial = api.get(server + '/api/signals').json()
    # Legacy review items count as held evidence (quarantined_count) in the current status API.
    assert api.get(server + '/api/signals/review').status == 401
    assert api.get(server + '/api/signals/status').json()['quarantined_count'] == 2

    # Manual approval is retired: even an authorised admin cannot publish or reject held items.
    headers = {'Authorization': 'Bearer synthetic-browser-admin'}
    queue_response = api.get(server + '/api/signals/review', headers=headers)
    assert queue_response.ok
    items = queue_response.json()['items']
    held = next(i for i in items if i['signal']['title'] == 'Malaysia needs cybersecurity workers')
    for action in ('approve', 'reject'):
        assert api.post(server + f"/api/signals/review/{held['id']}/{action}", headers=headers).status == 410
    assert api.get(server + '/api/signals').json() == initial
    assert api.get(server + '/api/signals/status').json()['quarantined_count'] == 2

    page.reload()
    page.get_by_role('tablist').get_by_role('button', name='Signals', exact=True).click()
    expect(page.get_by_role('heading', name='Malaysia needs cybersecurity workers')).to_have_count(0)
    assert 'synthetic-browser-admin' not in page.evaluate(
        'JSON.stringify([Object.entries(localStorage),Object.entries(sessionStorage)])'
    )
    assert api.get(server + '/api/signals/status').json()['enabled'] is True


@pytest.mark.parametrize('server', ['signals'], indirect=True)
def test_unauthorized_review_cannot_mutate_evidence(page, server):
    page.goto(server + '/signals')
    queue = page.request.get(
        server + '/api/signals/review',
        headers={'Authorization': 'Bearer synthetic-browser-admin'},
    ).json()['items']
    review_id = queue[0]['id']
    assert page.request.post(server + f'/api/signals/review/{review_id}/approve').status == 401
    assert page.request.post(
        server + f'/api/signals/review/{review_id}/approve',
        headers={'Authorization': 'Bearer wrong-token'},
    ).status == 401
    assert page.request.get(server + '/api/signals/status').json()['quarantined_count'] == 2
    expect(page.get_by_role('button', name='Review pending evidence')).to_have_count(0)


def test_signals_v2_three_independent_paginations(page, server):
    page.goto(server + '/signals')
    source = page.request.get(server + '/api/skill-trends').json()
    rising = page.get_by_role('navigation', name='Rising skills pages')
    declining = page.get_by_role('navigation', name='Declining skills and jobs pages')
    expect(rising.locator('button[aria-current="page"]')).to_have_text('1')
    expect(declining.locator('button[aria-current="page"]')).to_have_text('1')
    if len(source['rising']) > 5:
        rising.get_by_role('button', name=re.compile(r'^Page 2 of ')).click()
        expect(rising.locator('button[aria-current="page"]')).to_have_text('2')
        expect(declining.locator('button[aria-current="page"]')).to_have_text('1')
    if len(source['declining']) > 5:
        declining.get_by_role('button', name=re.compile(r'^Page 2 of ')).click()
        expect(declining.locator('button[aria-current="page"]')).to_have_text('2')
        if len(source['rising']) > 5:
            expect(rising.locator('button[aria-current="page"]')).to_have_text('2')

    page.get_by_role('tablist').get_by_role('button', name='Signals', exact=True).click()
    saved = page.request.get(server + '/api/signals').json()
    pager = page.get_by_role('navigation', name='Signal evidence pages')
    expect(pager.locator('button[aria-current="page"]')).to_have_text('1')
    cards = page.locator('main[data-screen-label="Signals"] article')
    expect(cards).to_have_count(min(8, len(saved)))
    if len(saved) > 8:
        pager.get_by_role('button', name=re.compile(r'^Page 2 of ')).click()
        expect(pager.locator('button[aria-current="page"]')).to_have_text('2')
        expect(cards).to_have_count(min(8, len(saved) - 8))
    page.get_by_role('button', name='↑ Emerging').click()
    expect(pager.locator('button[aria-current="page"]')).to_have_text('1')
