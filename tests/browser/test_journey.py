"""Exercise the shipped UI, not a mocked page or copied application logic."""
import re

import pytest
from playwright.sync_api import expect


def profiles(page):
    return page.request.get("/api/profiles").json()


def continue_to_quiz(page):
    page.get_by_label("I have checked these skills").check()
    page.get_by_text("Continue to the interest quiz →", exact=True).click()
    expect(page.get_by_text("What do you enjoy? (optional)", exact=True)).to_be_visible()


def finish(page, quiz=False):
    if quiz:
        questions = page.request.get("/api/interest-quiz").json()
        label = questions["likert"][-1]["label"]
        buttons = page.get_by_role("button", name=label, exact=True)
        expect(buttons).to_have_count(18)
        for i in range(18):
            buttons.nth(i).click()
        page.get_by_text("See my results →", exact=True).click()
    else:
        page.get_by_text("Skip the quiz", exact=True).click()
    expect(page.locator('main[data-screen-label="Results"]')).to_be_visible()
    expect(page.get_by_text("See pathway →", exact=True).first).to_be_visible()
    pid = page.evaluate("localStorage.getItem('fp.activeProfile')")
    return page.request.get("/api/profiles/" + pid).json()


def manual(page, name, quiz=False):
    page.goto("/start")
    page.get_by_role("button", name=re.compile("Fill a short form")).click()
    page.get_by_label("Current Job Title", exact=True).fill("Synthetic Analyst")
    page.get_by_label("Years of Relevant Experience", exact=True).fill("3")
    page.get_by_label(re.compile("^Education Level")).select_option("Diploma")
    search = page.get_by_placeholder("+ Search skills…", exact=True)
    search.fill("Python")
    page.get_by_role("button", name="+ Python programming", exact=True).click()
    page.get_by_text("Continue →", exact=True).click()
    page.get_by_label("Profile name").fill(name)
    page.get_by_role("button", name="Strong", exact=True).click()
    continue_to_quiz(page)
    return finish(page, quiz)


def test_manual_quiz_results_switching_and_deep_links(page):
    first = manual(page, "Synthetic Alpha", quiz=True)
    assert first["skills"] == {"SK005": 4}
    assert first["qualification"] == "Diploma"
    assert len(first["quiz_answers"]) == 18 and first["riasec"]
    second = manual(page, "Synthetic Beta")
    assert not second["quiz_answers"]
    assert len(profiles(page)) == 2
    page.goto("/start")
    row = page.locator("div").filter(has=page.get_by_text("Synthetic Alpha", exact=True))
    row.filter(has=page.get_by_text("See results →", exact=True)).last.get_by_text(
        "See results →", exact=True).click()
    expect(page.locator('main[data-screen-label="Results"]')).to_be_visible()
    page.wait_for_function("id => localStorage.getItem('fp.activeProfile') === id", arg=first["id"])
    expect(page.locator("main section").first.locator("p")).to_have_text("Synthetic Alpha")
    for label, scenario in (("Fast AI disruption", "rapid"), ("Moderate AI disruption", "moderate")):
        records = page.request.get(f"/api/matches?scenario={scenario}&profile={first['id']}").json()
        # Default slider weights, including the completed quiz's 20% share.
        ranked = sorted(records, key=lambda r: (
            .44 * r["match"]["skill"] + .36 * r["match"]["demand"]
            + .2 * r["match"]["interest"]), reverse=True)
        page.get_by_role("button", name=label, exact=True).click()
        expect(page.locator("main article h3").first).to_have_text(ranked[0]["title"])
        expect(page.get_by_text(
            "AI adoption speeds up." if scenario == "rapid" else "Baseline estimate",
            exact=False).first).to_be_visible()
    selected_title = page.locator("main article h3").first.inner_text()
    page.get_by_text("See pathway →", exact=True).first.click()
    expect(page).to_have_url(re.compile("/pathway$"))
    expect(page.locator("main h1")).to_have_text(selected_title)
    page.get_by_text("← Back to results", exact=True).click()
    expect(page.locator('main[data-screen-label="Results"]')).to_be_visible()
    for route, screen in (("pathway", "Pathway"), ("results", "Results"),
                          ("signals", "Signals"), ("about", "About")):
        page.goto("/" + route)
        page.reload()
        expect(page.locator(f'main[data-screen-label="{screen}"]')).to_be_visible()
        assert page.evaluate("localStorage.getItem('fp.activeProfile')") == first["id"]


def test_upload_review_requires_confirmation_and_removal(page):
    page.goto("/start")
    page.get_by_role("button", name=re.compile("Upload a CV")).click()
    # The input advertises PDF, but the real endpoint also supports synthetic TXT.
    page.locator('input[type="file"]').set_input_files({
        "name": "synthetic.txt", "mimeType": "text/plain",
        "buffer": b"SUMMARY\nSynthetic developer\nTECHNICAL SKILLS\nPython and SQL",
    })
    page.get_by_text("Read my CV", exact=True).click()
    expect(page.get_by_text("Check your profile", exact=True)).to_be_visible()
    expect(page.get_by_text(re.compile("Qwen on RunPod suggested 1 skills"))).to_be_visible()
    expect(page.get_by_text("CV evidence (Qwen AI): “Python”", exact=True)).to_be_visible()
    assert profiles(page) == []
    page.get_by_text("Continue to the interest quiz →", exact=True).click()
    expect(page.get_by_text("Tick the box to confirm these skills describe you.")).to_be_visible()
    page.get_by_label("I have checked these skills").check()
    page.get_by_text("Continue to the interest quiz →", exact=True).click()
    expect(page.get_by_text("Choose Basic, Working or Strong for every AI-suggested skill before continuing.")).to_be_visible()
    # Remove the dictionary suggestion, retain the stubbed AI suggestion.
    page.get_by_role("button", name="Remove", exact=True).last.click()
    expect(page.get_by_role("button", name="Remove", exact=True)).to_have_count(1)
    expect(page.get_by_label("I have checked these skills")).not_to_be_checked()
    page.get_by_role("button", name="Working", exact=True).click()
    page.get_by_label("Profile name").fill("Synthetic Upload")
    continue_to_quiz(page)
    saved = finish(page)
    assert saved["skills"] == {"SK005": 3}


def test_mobile_theme_and_manual_flow(page):
    page.set_viewport_size({"width": 390, "height": 844})
    saved = manual(page, "Synthetic Mobile")
    assert saved["name"] == "Synthetic Mobile"
    theme = page.locator("[data-theme]").first
    expect(theme).to_have_attribute("data-theme", "light")
    page.get_by_role("button", name=re.compile("◐")).click()
    expect(theme).to_have_attribute("data-theme", "dark")
    page.get_by_text("See pathway →", exact=True).first.click()
    expect(theme).to_have_attribute("data-theme", "dark")
    page.get_by_role("button", name=re.compile("◐")).click()
    expect(theme).to_have_attribute("data-theme", "light")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")


@pytest.mark.parametrize("server", ["1"], indirect=True)
def test_public_demo_password_and_admin_lockdown(browser, server):
    for password in (None, "wrong"):
        context = browser.new_context(
            base_url=server,
            **({"http_credentials": {"username": "judge", "password": password}}
               if password else {}),
        )
        for path in ("/start", "/results", "/api/skills"):
            response = context.request.get(path)
            assert response.status == 401
            assert "Basic" in response.headers["www-authenticate"]
        context.close()
    context = browser.new_context(base_url=server, http_credentials={
        "username": "judge", "password": "synthetic-browser-password",
    })
    try:
        page = context.new_page()
        page.goto("/start")
        expect(page.get_by_role("button", name=re.compile("Fill a short form"))).to_be_visible()
        assert context.request.get("/api/skills").status == 200
        for path in ("/api/curator/approve/S1", "/api/signals/refresh"):
            assert context.request.post(path).status == 403
    finally:
        context.close()


@pytest.mark.parametrize("server", ["unconfigured"], indirect=True)
def test_demo_without_password_fails_closed(browser, server):
    context = browser.new_context(base_url=server)
    try:
        page = context.new_page()
        response = page.goto("/start")
        assert response.status == 503
        expect(page.get_by_text(re.compile("Demo is not configured"))).to_be_visible()
        assert context.request.get("/api/profiles").status == 503
    finally:
        context.close()
