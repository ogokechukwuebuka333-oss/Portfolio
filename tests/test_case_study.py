import re

from playwright.sync_api import expect

CASE_TITLE = "BetAlmighty case study · Ogoke Works"


def test_featured_card_opens_case_and_back_returns(home, base_url):
    home.click("#openCase")
    expect(home.locator("#case")).to_be_visible()
    expect(home).to_have_url(base_url + "/betalmighty")
    expect(home).to_have_title(CASE_TITLE)
    home.go_back()
    expect(home.locator("#case")).to_be_hidden()
    expect(home).to_have_url(base_url + "/")
    expect(home).to_have_title("Ogoke Works")
    home.go_forward()
    expect(home.locator("#case")).to_be_visible()


def test_panel_link_opens_case(home, base_url):
    home.locator("#panel a", has_text="Read the case study").click()
    expect(home).to_have_url(base_url + "/betalmighty")
    expect(home.locator("#case")).to_be_visible()


def test_direct_link_and_close(case, base_url):
    expect(case).to_have_title(CASE_TITLE)
    expect(case.locator("#csTitle")).to_contain_text("BetAlmighty")
    case.click("#csClose")
    expect(case.locator("#case")).to_be_hidden()
    expect(case).to_have_url(base_url + "/")


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
    expect(case.locator("#cs-workflow")).to_contain_text("AI drafted the flows")
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
    expect(case.locator("#case")).to_be_visible()  # first Escape only closes the lightbox
    case.keyboard.press("Escape")
    expect(case.locator("#case")).to_be_hidden()


def test_end_button_returns_to_work(case, base_url):
    btn = case.locator("#csClose2")
    btn.scroll_into_view_if_needed()
    btn.click()
    expect(case.locator("#case")).to_be_hidden()
    expect(case).to_have_url(base_url + "/")


def test_page_behind_does_not_scroll(case):
    y = case.evaluate("scrollY")
    case.mouse.move(400, 400)
    case.mouse.wheel(0, 2000)
    case.wait_for_timeout(200)
    assert case.evaluate("scrollY") == y
    assert case.evaluate("document.getElementById('csBody').scrollTop") > 0


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
