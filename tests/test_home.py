import re

from playwright.sync_api import expect

EMAIL = "Harryebuka7@gmail.com"


def test_loads_with_hero(home):
    expect(home).to_have_title("Ogoke Works")
    expect(home.locator(".who .nm")).to_have_text("Chukwuebuka Ogoke")
    expect(home.locator("h1:visible")).to_have_count(1)  # the hidden case study page has its own h1
    expect(home.locator("h1:visible")).to_contain_text("messy specs")
    expect(home.locator(".intro .live")).to_contain_text("Open to work")
    expect(home.locator("#clock")).to_have_text(re.compile(r"^\d{2}:\d{2}$"))


def test_link_preview_tags(home, base_url):
    og = home.locator('meta[property="og:image"]').get_attribute("content")
    assert og.endswith("/og.jpg")
    assert home.request.get(base_url + "/og.jpg").ok
    assert home.locator('meta[name="twitter:card"]').get_attribute("content") == "summary_large_image"


def test_nav_links_scroll_to_sections(home):
    for target in ("work", "plan", "about"):
        home.click(f'.nav a[href="#{target}"]')
        expect(home.locator(f"#{target}")).to_be_in_viewport()


def test_theme_toggle_persists(home):
    html = home.locator("html")
    start = home.evaluate("document.documentElement.getAttribute('data-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')")
    flipped = "light" if start == "dark" else "dark"
    home.click("#theme")
    expect(html).to_have_attribute("data-theme", flipped)
    home.reload()
    expect(html).to_have_attribute("data-theme", flipped)


def test_hero_copy_email(home):
    home.click("#cp")
    expect(home.locator("#cp")).to_have_text("Copied")
    assert home.evaluate("navigator.clipboard.readText()") == EMAIL


def test_email_menu_options(home):
    trigger = home.locator(".top [data-mail]")
    menu = home.locator("#mailpop")
    trigger.click()
    expect(menu).to_be_visible()
    expect(trigger).to_have_attribute("aria-expanded", "true")
    expect(menu.get_by_role("menuitem", name=re.compile("Open in Gmail"))).to_have_attribute("href", re.compile(r"^https://mail\.google\.com/.*to=" + re.escape(EMAIL)))
    expect(menu.get_by_role("menuitem", name=re.compile("Open mail app"))).to_have_attribute("href", "mailto:" + EMAIL)
    box = menu.bounding_box()
    vp = home.viewport_size
    assert box["x"] >= 0 and box["x"] + box["width"] <= vp["width"]

    home.keyboard.press("Escape")
    expect(menu).to_be_hidden()
    expect(trigger).to_have_attribute("aria-expanded", "false")

    trigger.click()
    home.mouse.click(5, vp["height"] - 5)  # outside
    expect(menu).to_be_hidden()


def test_email_menu_copy_and_every_trigger(home):
    triggers = home.locator("[data-mail]")
    assert triggers.count() >= 2
    home.locator(".contact [data-mail]").click()
    home.click("#mailCopy")
    expect(home.locator("#mailCopy small")).to_have_text("Copied to clipboard")
    assert home.evaluate("navigator.clipboard.readText()") == EMAIL
    expect(home.locator("#mailpop")).to_be_hidden(timeout=3000)


def test_drafting_table_cards(home):
    cards = home.locator(".draft")
    expect(cards).to_have_count(3)
    for name in ("Dataset Nexus Tech", "Hassanah Shonibare", "Soundyaad"):
        expect(cards.filter(has_text=name)).to_have_count(1)
    cards.filter(has_text="Soundyaad").click()
    expect(home.locator("#panel h2")).to_have_text("Soundyaad")
    expect(home.locator("#plan")).to_be_in_viewport()


def test_principles_and_contact(home):
    expect(home.locator(".prin li")).to_have_count(3)
    expect(home.locator(".contact .addr")).to_have_text(EMAIL)
    expect(home.locator(".foot")).to_contain_text("Chukwuebuka Ogoke")


def test_email_menu_follows_its_button_while_scrolling(home):
    trigger = home.locator(".top [data-mail]")  # sticky top bar, so it stays on screen
    trigger.click()
    menu = home.locator("#mailpop")
    home.mouse.wheel(0, 600)
    home.wait_for_timeout(300)
    expect(menu).to_be_visible()
    t, m = trigger.bounding_box(), menu.bounding_box()
    assert abs(m["y"] - (t["y"] + t["height"] + 8)) < 2, "menu should stay anchored under its button"

    home.keyboard.press("Escape")
    home.evaluate("scrollTo(0, 0)")
    contact = home.locator(".contact [data-mail]")
    contact.click()
    expect(menu).to_be_visible()
    home.evaluate("scrollTo(0, 0)")  # contact section scrolls off screen
    expect(menu).to_be_hidden()
