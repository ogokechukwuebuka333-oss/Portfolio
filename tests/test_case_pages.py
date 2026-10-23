"""The Activation Rescue, MyEstates and Soundyaad case studies share one template."""
import pytest
from playwright.sync_api import expect

CASES = {
    "/activation-rescue": ("Activation Rescue", "Activation Rescue case study · Chukwuebuka Ogoke"),
    "/myestate": ("MyEstates", "MyEstates case study · Chukwuebuka Ogoke"),
    "/soundyaad": ("Soundyaad", "Soundyaad case study · Chukwuebuka Ogoke"),
}


@pytest.mark.parametrize("path", CASES)
def test_case_page_loads_cleanly(page, problems, base_url, path):
    h1, title = CASES[path]
    page.goto(base_url + path)
    expect(page).to_have_title(title)
    expect(page.locator("#csTitle")).to_have_text(h1)
    assert page.locator('meta[name="description"]').get_attribute("content")
    assert page.locator('link[rel="canonical"]').get_attribute("href").endswith(path)
    page.wait_for_load_state("networkidle")


@pytest.mark.parametrize("path", CASES)
def test_notes_needing_input_stay_hidden_from_visitors(page, base_url, path):
    page.goto(base_url + path)
    notes = page.locator(".todo, .todo-sec, .todo-link")
    assert notes.count() > 0
    assert notes.evaluate_all("els => els.filter(e => e.getClientRects().length).length") == 0
    page.goto(base_url + path + "?draft")
    expect(page.locator(".todo").first).to_be_visible()


@pytest.mark.parametrize("path", CASES)
def test_every_contents_link_has_a_section(page, base_url, path):
    page.goto(base_url + path)
    for href in page.locator("#csToc a").evaluate_all("els => els.map(a => a.getAttribute('href'))"):
        expect(page.locator(href)).to_have_count(1)


def test_back_link_returns_home(page, base_url):
    page.goto(base_url + "/")
    page.locator('#work .pj-cta[href="/soundyaad"]').click()
    expect(page).to_have_url(base_url + "/soundyaad")
    page.locator("#csClose").click()
    expect(page).to_have_url(base_url + "/")


def test_screens_open_in_the_viewer(page, base_url):
    page.goto(base_url + "/myestate")
    page.locator("#cs-edges .shot button").first.click()
    expect(page.locator("#lb")).to_be_visible()
    expect(page.locator("#lbCap")).to_contain_text("No online payment")
