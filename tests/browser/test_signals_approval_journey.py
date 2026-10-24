"""Isolated Chromium approval gate, with synthetic DB and no live feeds/providers."""
import pytest
from playwright.sync_api import expect


@pytest.mark.parametrize('server', ['signals'], indirect=True)
def test_admin_review_journey_and_saved_reload(page, server):
    requests = []
    page.on('request', lambda request: requests.append((request.method, request.url)))
    page.goto(server + '/signals')
    expect(page.get_by_role('heading', name='The evidence behind every score')).to_be_visible()
    review = page.get_by_role('button', name='Review pending evidence')
    expect(review).to_be_visible()
    assert not any('/api/signals/review' in url for method, url in requests)
    initial = page.request.get(server + '/api/signals').json()
    assert page.request.get(server + '/api/signals/review').status == 401
    assert page.request.get(server + '/api/signals/status').json()['pending_count'] == 2

    def dialogs(dialog):
        if dialog.type == 'confirm':
            dialog.accept()
        elif 'ADMIN_TOKEN' in dialog.message:
            dialog.accept('synthetic-browser-admin')
        else:
            dialog.accept('Reviewed synthetic evidence')
    page.on('dialog', dialogs)
    review.click()
    expect(page.get_by_role('heading', name='Malaysia needs cybersecurity workers')).to_be_visible()
    item = page.locator('article').filter(has_text='Malaysia needs cybersecurity workers')
    item.get_by_role('button', name='Approve evidence').click()
    expect(page.get_by_role('heading', name='Malaysia needs cybersecurity workers')).to_have_count(0)
    assert len(page.request.get(server + '/api/signals').json()) == len(initial) + 1
    assert page.request.get(server + '/api/signals/status').json()['pending_count'] == 1
    item = page.locator('article').filter(has_text='Malaysia expands data analyst hiring')
    item.get_by_role('button', name='Reject evidence').click()
    expect(page.get_by_role('heading', name='Malaysia expands data analyst hiring')).to_have_count(0)
    assert page.request.get(server + '/api/signals/status').json()['pending_count'] == 0
    assert len(page.request.get(server + '/api/signals').json()) == len(initial) + 1
    before = len(requests)
    page.get_by_role('button', name='Reload saved signals').click()
    expect(page.get_by_text('Saved signals reloaded. No live news or research was fetched.')).to_be_visible()
    assert not any(method == 'POST' for method, url in requests[before:])
    stores = page.evaluate('JSON.stringify([Object.entries(localStorage),Object.entries(sessionStorage)])')
    assert 'synthetic-browser-admin' not in stores
    assert page.request.get(server + '/api/signals/status').json()['enabled'] is True


@pytest.mark.parametrize('server', ['signals'], indirect=True)
def test_review_unauthorized_error_is_visible(page, server):
    page.goto(server + '/signals')
    page.on('dialog', lambda dialog: dialog.accept('wrong-token'))
    page.get_by_role('button', name='Review pending evidence').click()
    expect(page.get_by_text('Administrator authentication failed (401). Check the token and try again.')).to_be_visible()
    assert page.request.get(server + '/api/signals/status').json()['pending_count'] == 2
