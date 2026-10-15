import pytest
from playwright.sync_api import expect

PHONE = {"viewport": {"width": 375, "height": 812}, "is_mobile": True, "has_touch": True, "device_scale_factor": 2}


@pytest.fixture
def phone(browser, base_url):
    ctx = browser.new_context(**PHONE, reduced_motion="reduce")
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: m.type == "error" and errors.append(m.text))
    yield page
    ctx.close()
    assert not errors, errors


def no_sideways_scroll(page, scroller="document.documentElement"):
    return page.evaluate(f"(() => {{ const e = {scroller}; return e.scrollWidth <= e.clientWidth; }})()")


@pytest.mark.parametrize("path", ["/", "/betalmighty"])
def test_phone_has_no_horizontal_overflow(phone, base_url, path):
    phone.goto(base_url + path)
    phone.wait_for_load_state("networkidle")
    assert no_sideways_scroll(phone)
    if path == "/betalmighty":
        assert no_sideways_scroll(phone, "document.getElementById('csBody')")


def test_phone_layout_basics(phone, base_url):
    phone.goto(base_url + "/")
    expect(phone.locator(".nav")).to_be_hidden()
    expect(phone.locator(".top [data-mail]")).to_be_visible()
    zoom = phone.locator(".zoom").bounding_box()
    scene = phone.locator(".map").bounding_box()
    assert zoom["y"] > scene["y"] + scene["height"] / 2, "zoom controls sit at the bottom of the map on phones"


def test_phone_full_screen_stacks_panel_below(phone, base_url):
    phone.goto(base_url + "/")
    phone.locator("#zfull").tap()
    expect(phone.locator(".plan")).to_have_class("plan full")
    m, p = phone.locator(".map").bounding_box(), phone.locator("#panel").bounding_box()
    assert p["y"] >= m["y"] + m["height"] - 1
    assert p["y"] + p["height"] <= 812 + 1


def test_phone_flow_boards_scroll_sideways(phone, base_url):
    phone.goto(base_url + "/betalmighty")
    btn = phone.locator(".board button").first
    btn.scroll_into_view_if_needed()
    phone.wait_for_function("document.querySelector('.board img').complete")
    assert btn.evaluate("b => b.scrollWidth > b.clientWidth")


@pytest.mark.parametrize("path", ["/", "/betalmighty"])
def test_images_have_alt_and_controls_have_names(page, base_url, path):
    page.goto(base_url + path)
    missing_alt = page.eval_on_selector_all("img", "els => els.filter(e => !e.hasAttribute('alt')).map(e => e.src)")
    assert missing_alt == []
    unnamed = page.eval_on_selector_all(
        "button, a[href]",
        "els => els.filter(e => e.getClientRects().length && !e.closest('[aria-hidden=true]') && !(e.getAttribute('aria-label') || e.textContent.trim() || e.querySelector('img[alt]:not([alt=\"\"])'))).map(e => e.outerHTML.slice(0, 80))",
    )
    assert unnamed == []


def test_landmarks_and_headings(page, base_url):
    page.goto(base_url + "/")
    expect(page.locator("main")).to_have_count(1)
    expect(page.locator("header.top")).to_have_count(1)
    levels = page.eval_on_selector_all("main h1, main h2, main h3", "els => els.map(e => +e.tagName[1])")
    assert levels[0] == 1
    jumps = [b - a for a, b in zip(levels, levels[1:]) if b - a > 1]
    assert jumps == [], f"heading levels skip: {levels}"


def test_keyboard_reaches_case_study(page, base_url):
    page.goto(base_url + "/")
    page.locator("#openCase").focus()
    page.keyboard.press("Enter")
    expect(page.locator("#case")).to_be_visible()
    expect(page.locator("#csClose")).to_be_focused()
