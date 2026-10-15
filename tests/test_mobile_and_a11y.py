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


def test_phone_explorer_card_is_a_bottom_sheet(phone, base_url):
    phone.goto(base_url + "/")
    phone.locator('#heroLabels .plabel[data-id="hassanah"]').tap()
    expect(phone.locator("#explorer")).to_be_visible()
    card = phone.locator("#panel").bounding_box()
    assert card["y"] + card["height"] <= 812 + 1 and card["y"] > 812 * 0.45, card
    assert card["width"] > 375 * 0.9
    phone.wait_for_timeout(700)
    label = phone.locator('#plabels .plabel[data-id="hassanah"]').bounding_box()
    assert label["y"] + label["height"] < card["y"], "selected building sits above the sheet"


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
    expect(page).to_have_url(base_url + "/betalmighty")
    expect(page.locator("#csTitle")).to_be_visible()
    page.keyboard.press("Tab")
    expect(page.locator(":focus")).to_be_visible()


@pytest.mark.parametrize("where", ["hero", "explorer"])
def test_map_labels_readable_on_phone(phone, base_url, where):
    phone.goto(base_url + "/")
    if where == "explorer":
        phone.locator(".hexplore").tap()
    labels = phone.locator(("#heroLabels" if where == "hero" else "#plabels") + " .plabel:not([hidden])")
    assert labels.count() == 5
    sizes = labels.evaluate_all("els => els.map(e => parseFloat(getComputedStyle(e).fontSize))")
    assert min(sizes) >= 12, sizes
    boxes = [labels.nth(i).bounding_box() for i in range(labels.count())]
    overlaps = [(i, j) for i in range(len(boxes)) for j in range(i + 1, len(boxes))
                if not (boxes[i]["x"] + boxes[i]["width"] <= boxes[j]["x"] or boxes[j]["x"] + boxes[j]["width"] <= boxes[i]["x"]
                        or boxes[i]["y"] + boxes[i]["height"] <= boxes[j]["y"] or boxes[j]["y"] + boxes[j]["height"] <= boxes[i]["y"])]
    assert overlaps == [], f"labels overlap on a phone: {overlaps}"


CONTRAST_JS = r"""() => {
  const lum = c => { const m = c.match(/[\d.]+/g).map(Number); const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4 }; return .2126 * f(m[0]) + .7152 * f(m[1]) + .0722 * f(m[2]) };
  const bgOf = e => { for (let n = e; n; n = n.parentElement) { const a = getComputedStyle(n).backgroundColor.match(/[\d.]+/g); if (a && (a[3] === undefined || +a[3] > .5)) return getComputedStyle(n).backgroundColor } return getComputedStyle(document.body).backgroundColor };
  const bad = {}; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let t;
  while (t = w.nextNode()) {
    const e = t.parentElement; if (!t.textContent.trim() || !e.getClientRects().length || e.closest('svg,[aria-hidden=true],#lb,[hidden]')) continue;
    const s = getComputedStyle(e); if (s.visibility === 'hidden') continue;
    const a = lum(s.color), b = lum(bgOf(e)), r = (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
    const big = parseFloat(s.fontSize) >= 24 || (parseFloat(s.fontSize) >= 18.66 && +s.fontWeight >= 700);
    if (r < (big ? 3 : 4.5)) bad[t.textContent.trim().slice(0, 40)] = `${r.toFixed(2)}:1 at ${s.fontSize}`;
  }
  return bad;
}"""


@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("path", ["/", "/betalmighty"])
def test_text_contrast_meets_wcag_aa(browser, base_url, scheme, path):
    ctx = browser.new_context(color_scheme=scheme, viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + path)
    page.wait_for_timeout(300)
    if path == "/":
        page.locator("#heroLabels .plabel[data-id='hq']").click()  # include the About card in the explorer
        page.wait_for_timeout(400)  # let the label's colour transition finish
    failures = page.evaluate(CONTRAST_JS)
    ctx.close()
    assert failures == {}, failures


def test_phone_shows_the_city_in_the_first_screen(phone, base_url):
    phone.goto(base_url + "/")
    top = phone.locator("#hcity").bounding_box()["y"]
    assert top < 844 * 0.75, f"city starts at {top}px on a 844px-tall phone"


def test_phone_escrow_states_sit_above_their_screen(phone, base_url):
    phone.goto(base_url + "/betalmighty")
    tab = phone.locator("#esx-t3")
    tab.scroll_into_view_if_needed()
    tab.tap()
    screen = phone.locator(".esx-phone").bounding_box()
    assert screen["y"] < 812 and screen["y"] + 40 > tab.bounding_box()["y"], "the screen a state controls is visible right after tapping"
    expect(phone.locator(".esx-text h3")).to_have_text("Disputed")
