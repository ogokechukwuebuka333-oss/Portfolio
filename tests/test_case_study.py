import re

import pytest

from playwright.sync_api import expect

CASE_TITLE = "BetAlmighty case study · Ogoke Works"


def test_featured_card_opens_case_and_back_returns(home, base_url):
    home.click("#openCase")
    expect(home).to_have_url(base_url + "/betalmighty")
    expect(home).to_have_title(CASE_TITLE)
    expect(home.locator("#case")).to_be_visible()
    home.go_back()
    expect(home).to_have_url(base_url + "/")
    expect(home).to_have_title("Chukwuebuka Ogoke · Product Designer")
    expect(home.locator("#case")).to_have_count(0)
    home.go_forward()
    expect(home.locator("#case")).to_be_visible()


def test_back_from_case_returns_to_the_same_spot(home, base_url):
    home.evaluate("document.querySelector('#openCase').scrollIntoView({block:'center'})")
    y = home.evaluate("scrollY")
    home.click("#openCase")
    expect(home).to_have_url(base_url + "/betalmighty")
    home.click("#csClose")
    expect(home).to_have_url(base_url + "/")
    home.wait_for_function(f"Math.abs(scrollY - {y}) < 4")


def test_direct_link_and_close(case, base_url):
    expect(case).to_have_title(CASE_TITLE)
    expect(case.locator("#csTitle")).to_contain_text("BetAlmighty")
    case.click("#csClose")
    expect(case).to_have_url(base_url + "/")
    expect(case.locator("#hcity")).to_be_visible()


def test_header_facts(case):
    meta = case.locator(".cs .meta")
    for label, value in (("Team", "Solo, client project"), ("Timeline", "Jul – Sep 2026"), ("Status", "In development")):
        expect(meta.locator("div", has=case.locator(f"span:text-is('{label}')")).locator("b")).to_have_text(value)
    expect(case.locator(".cs .glance > div")).to_have_count(3)
    expect(case.locator(".cs .owned li")).to_have_count(5)
    expect(case.locator(".cs")).not_to_contain_text("To confirm")


def test_story_sections_in_order(case):
    ids = case.eval_on_selector_all("#csBody section[id]", "els => els.map(e => e.id)")
    assert ids == ["cs-brief", "cs-workflow", "cs-decisions", "cs-escrow", "cs-safety", "cs-more", "cs-system", "cs-handoff", "cs-outcome"]
    expect(case.locator("#cs-decisions .dec")).to_have_count(4)
    expect(case.locator("#cs-workflow h2")).to_have_text("From user stories to final screens")
    expect(case.locator("#cs-outcome .pull")).to_contain_text("simplicity and usability")


def test_no_exact_commercial_figures(case):
    text = case.locator("#cs-handoff").inner_text()
    assert not re.search(r"\d+\s?%|₦\s?\d|\b14[- ]day", text), "handoff should describe decisions without figures"


def test_contents_links_jump_and_highlight(case):
    for href in ("#cs-decisions", "#cs-handoff", "#cs-brief"):
        case.click(f'#csToc a[href="{href}"]')
        # lands at the section heading (scroll-margin-top is 70px), not partway
        case.wait_for_function(f"Math.abs(document.querySelector('{href}').getBoundingClientRect().top - 70) < 4")
        expect(case.locator(f'#csToc a[href="{href}"]')).to_have_class(re.compile(r"\bon\b"))


def test_every_image_loads(case):
    broken = case.evaluate("""async () => {
        const imgs = [...document.querySelectorAll('#csBody img')];
        imgs.forEach(i => i.loading = 'eager');
        await Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
        return imgs.filter(i => !i.naturalWidth).map(i => i.getAttribute('src'));
    }""")
    assert broken == []
    assert case.locator("#csBody img").count() >= 40


def test_lightbox_phone_and_wide_board(case):
    lb = case.locator("#lb")
    shot = case.locator("#cs-brief ~ section .shot button").first
    shot.scroll_into_view_if_needed()
    shot.click()
    expect(lb).to_be_visible()
    expect(lb).not_to_have_class(re.compile(r"\bwide\b"))
    lb.click()
    expect(lb).to_be_hidden()

    board = case.locator(".board button").first
    board.scroll_into_view_if_needed()
    board.click()
    expect(lb).to_have_class(re.compile(r"\bwide\b"))
    case.wait_for_function("document.getElementById('lbImg').complete")
    assert case.evaluate("document.getElementById('lb').scrollWidth > document.getElementById('lb').clientWidth"), "wide boards should scroll, not shrink"

    case.keyboard.press("Escape")
    expect(lb).to_be_hidden()
    expect(case.locator("#case")).to_be_visible()  # first Escape only closes the viewer
    case.keyboard.press("Escape")
    expect(case).to_have_url(re.compile(r"/$"))  # second Escape goes back to all work


def test_end_button_returns_to_work(case, base_url):
    btn = case.locator("#csClose2")
    btn.scroll_into_view_if_needed()
    btn.click()
    expect(case).to_have_url(base_url + "/")


def test_case_study_is_its_own_page(page, base_url):
    page.goto(base_url + "/")
    assert page.locator("#case, #csBody").count() == 0, "the homepage no longer carries the case study"
    page.goto(base_url + "/betalmighty")
    assert page.locator("#hcity, #explorer").count() == 0
    assert page.evaluate("document.documentElement.scrollHeight > innerHeight * 5"), "the page itself scrolls"
    page.mouse.wheel(0, 1500)
    page.wait_for_function("scrollY > 0")


def test_case_page_has_its_own_preview_card(page, base_url):
    page.goto(base_url + "/betalmighty")
    meta = lambda prop: page.locator(f'meta[property="{prop}"]').get_attribute("content")
    assert meta("og:url").endswith("/betalmighty")
    assert meta("og:image").endswith("/og-betalmighty.jpg")
    assert "BetAlmighty" in meta("og:title")
    assert page.locator('link[rel="canonical"]').get_attribute("href").endswith("/betalmighty")
    assert page.request.get(base_url + "/og-betalmighty.jpg").ok
    page.goto(base_url + "/")
    assert page.locator('meta[property="og:image"]').get_attribute("content").endswith("/og.jpg")


def test_case_images_reserve_their_space(case):
    """Images without width/height shift the page as they lazy-load and break contents-link jumps."""
    assert case.eval_on_selector_all("#csBody img", "els => els.filter(i => !i.getAttribute('width') || !i.getAttribute('height')).map(i => i.src)") == []


def test_contents_jump_with_smooth_scrolling(browser, base_url):
    page = browser.new_page(reduced_motion="no-preference")
    page.goto(base_url + "/betalmighty")
    for href in ("#cs-decisions", "#cs-handoff", "#cs-escrow", "#cs-brief"):
        page.click(f'#csToc a[href="{href}"]')
        page.wait_for_function(f"Math.abs(document.querySelector('{href}').getBoundingClientRect().top - 70) < 4", timeout=8000)
    page.close()


def test_cover_shows_the_product_in_the_first_screen(case):
    art = case.locator(".cs .cart img")
    expect(art).to_have_count(3)
    box = art.nth(1).bounding_box()
    assert box["y"] < 900 * 0.5, f"cover phones start at {box['y']}px"
    expect(case.locator(".cs .summary .glance > div")).to_have_count(3)


def test_each_decision_shows_drafts_finals_and_callouts(case):
    decs = case.locator("#cs-decisions .dec")
    expect(decs).to_have_count(4)
    for i in range(4):
        d = decs.nth(i)
        assert d.locator(".evo-col:not(.fin) .shot.mf").count() >= 2, f"decision {i+1} needs July drafts"
        assert d.locator(".evo-col.fin .shot").count() >= 1, f"decision {i+1} needs a final screen"
        markers = d.locator(".mk").count()
        assert markers >= 2 and markers == d.locator(".callouts li").count(), f"decision {i+1}: {markers} markers"


def test_full_flow_board_buttons_open_wide(case):
    btns = case.locator("#cs-decisions .boardlink")
    expect(btns).to_have_count(4)
    btns.nth(2).scroll_into_view_if_needed()
    btns.nth(2).click()
    lb = case.locator("#lb")
    expect(lb).to_have_class(re.compile(r"\bwide\b"))
    expect(case.locator("#lbImg")).to_have_attribute("src", "ba/wf/withdraw-board.jpg")
    case.keyboard.press("Escape")
    expect(lb).to_be_hidden()


def test_before_after_slider(case):
    slider = case.locator(".cs .slider")
    slider.scroll_into_view_if_needed()
    pos = lambda: slider.evaluate("e => e.style.getPropertyValue('--pos')")
    assert pos() == "50%"
    box = slider.bounding_box()
    case.mouse.click(box["x"] + box["width"] * 0.2, box["y"] + box["height"] / 2)
    assert int(float(pos().rstrip("%"))) < 35
    slider.locator("input").focus()
    case.keyboard.press("End")
    assert pos() == "100%"
    case.keyboard.press("Home")
    assert pos() == "0%"



@pytest.mark.parametrize("via", ["label", "building"])
def test_gold_building_opens_the_case_study(home, base_url, via):
    if via == "label":
        home.locator('#heroLabels .plabel[data-id="betalmighty"]').click()
    else:
        home.locator('#heroScene g.bld:not(.pin)[data-id="betalmighty"]').click()
    expect(home).to_have_url(base_url + "/betalmighty")
    expect(home.locator("#case")).to_be_visible()


def test_case_study_expands_from_where_you_clicked(browser, base_url):
    page = browser.new_page(reduced_motion="no-preference", viewport={"width": 1440, "height": 900})
    # record animations as the case page starts them
    page.add_init_script("""(() => { const a = Element.prototype.animate; window.__anims = [];
      Element.prototype.animate = function (k, o) { window.__anims.push({ id: this.id, k: JSON.stringify(k) }); return a.call(this, k, o); }; })()""")
    page.goto(base_url + "/")
    page.locator('#heroLabels .plabel[data-id="betalmighty"]').click()
    page.wait_for_url(base_url + "/betalmighty")
    page.wait_for_load_state("domcontentloaded")
    anims = page.evaluate("window.__anims")
    assert any(a["id"] == "case" and "inset(" in a["k"] for a in anims), anims
    assert page.evaluate("sessionStorage.getItem('ow-from')") is None, "the origin is used once"
    page.close()


def test_escrow_state_explorer(case):
    tabs = case.locator("#cs-escrow [role=tab]")
    expect(tabs).to_have_count(6)
    expect(tabs.nth(0)).to_have_attribute("aria-selected", "true")
    tabs.nth(3).scroll_into_view_if_needed()
    tabs.nth(3).click()
    expect(case.locator("#cs-escrow .esx-text h3")).to_have_text("Disputed")
    expect(case.locator("#cs-escrow .esx-k")).to_have_text("State 4 of 6 · Conflict")
    expect(case.locator("#cs-escrow .esx-phone img.on")).to_have_attribute("src", "ba/dispute.jpg")
    expect(case.locator("#esxPanel")).to_have_attribute("aria-labelledby", "esx-t3")
    # keyboard: arrows move between states, Home/End jump
    case.keyboard.press("ArrowDown")
    expect(case.locator("#cs-escrow .esx-text h3")).to_have_text("On hold")
    expect(tabs.nth(4)).to_be_focused()
    case.keyboard.press("End")
    expect(case.locator("#cs-escrow .esx-text h3")).to_have_text("Mutual cancel")
    case.keyboard.press("ArrowDown")  # wraps
    expect(case.locator("#cs-escrow .esx-text h3")).to_have_text("Locked")
    assert case.locator("#cs-escrow [role=tab][tabindex='0']").count() == 1


def test_engineering_diagram_still_available(case):
    btn = case.locator("#cs-escrow .boardlink")
    btn.scroll_into_view_if_needed()
    btn.click()
    expect(case.locator("#lbImg")).to_have_attribute("src", "ba/escrow.jpg")


def test_callout_text_stays_on_one_column(case):
    """Each callout is a two-column grid (number, text); mixed bold text must not split into extra cells."""
    rows = case.eval_on_selector_all("#cs-decisions .callouts li", "els => els.map(li => li.children.length)")
    assert rows and all(n == 1 for n in rows), rows
