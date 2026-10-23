import re

import pytest

from playwright.sync_api import expect

EMAIL = "Harryebuka7@gmail.com"
PAGES = ["/", "/betalmighty", "/activation-rescue", "/myestate", "/soundyaad"]


def test_loads_with_hero(home):
    expect(home).to_have_title("Chukwuebuka Ogoke · Product Designer")
    expect(home.locator(".who .nm")).to_have_text("Chukwuebuka Ogoke")
    expect(home.locator("h1:visible")).to_have_count(1)  # the hidden case study page has its own h1
    expect(home.locator("h1:visible")).to_have_text("I turn complex product problems into clear, usable experiences.")
    expect(home.locator(".who .rl")).to_have_text("Product Designer · AI-powered products · Complex workflows")


def test_link_preview_tags(home, base_url):
    og = home.locator('meta[property="og:image"]').get_attribute("content")
    assert og.endswith("/og.jpg")
    assert home.request.get(base_url + "/og.jpg").ok
    assert home.locator('meta[name="twitter:card"]').get_attribute("content") == "summary_large_image"


def test_nav_links_scroll_to_sections(home):
    for target in ("work", "process", "about", "contact"):
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


def test_hero_actions(home):
    actions = home.locator(".intro .actions > *")
    expect(actions).to_have_count(2)
    expect(actions.first).to_have_text(re.compile(r"^Explore my work"))
    expect(actions.first).to_have_attribute("href", "#work")
    expect(actions.nth(1)).to_have_text("Get in touch")
    actions.nth(1).click()
    expect(home.locator("#mailpop")).to_be_visible()
    expect(home.locator(".intro")).not_to_contain_text("Currently")
    expect(home.locator(".intro")).not_to_contain_text("Previously")


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


WORK = [("Activation Rescue", "/activation-rescue"), ("MyEstates", "/myestate"), ("Soundyaad", "/soundyaad"), ("BetAlmighty", "/betalmighty")]


def test_selected_work(home):
    rows = home.locator("#work .proj")
    expect(rows).to_have_count(4)
    for i, (name, path) in enumerate(WORK):
        row = rows.nth(i)
        expect(row.locator("h3")).to_have_text(name)
        expect(row.locator(".pj-cta")).to_have_attribute("href", path)
        expect(row.locator("dt")).to_have_text(["Role", "Shows"])
    expect(home.locator("main")).not_to_contain_text("Hassanah")  # hidden for now


def test_process_and_contact(home):
    expect(home.locator("#process .pipe li")).to_have_count(5)
    expect(home.locator("#process h2")).to_have_text("I use AI to explore faster. I use design judgment to decide what ships.")
    expect(home.locator("#process .aiex a")).to_have_attribute("href", "/betalmighty#cs-workflow")
    expect(home.locator("#beyond h2")).to_have_text("Beyond my own designs")
    expect(home.locator("#contact h2")).to_have_text("Have a complex product problem to solve?")
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


def test_city_is_in_the_first_screen(home):
    city = home.locator("#hcity")
    expect(city).to_be_in_viewport()
    box = city.bounding_box()
    assert box["y"] + box["height"] / 2 < home.viewport_size["height"], "most of the city sits above the fold"
    expect(home.locator("#heroLabels .plabel")).to_have_count(5)
    assert home.locator("#heroScene [data-id]").count() >= 4


def test_city_follows_the_site_theme(home):
    html = home.locator("html")
    start_dark = home.evaluate("document.documentElement.getAttribute('data-theme') === 'dark' || (!document.documentElement.getAttribute('data-theme') && matchMedia('(prefers-color-scheme: dark)').matches)")
    sky = home.locator("#hcity")
    expect(sky).to_have_attribute("data-sky", "night" if start_dark else "day")
    home.click("#theme")
    expect(sky).to_have_attribute("data-sky", "day" if start_dark else "night")
    # the site-plan explorer and the hero draw the same palette
    assert home.evaluate("document.querySelector('#heroScene polygon').getAttribute('fill') === document.querySelector('#scene polygon').getAttribute('fill')")


def test_city_has_no_time_or_location_caption(home):
    city = home.locator("#hcity")
    expect(city.locator("figcaption")).to_have_count(0)
    expect(city).not_to_contain_text("WAT")
    expect(city).not_to_contain_text("Lagos")


def test_hero_building_opens_the_explorer(home):
    home.locator('#heroLabels .plabel[data-id="hq"]').click()
    expect(home.locator(".plan")).to_have_class("plan full")
    expect(home.locator("#panel h2")).to_have_text("Chukwuebuka Ogoke")
    home.keyboard.press("Escape")
    expect(home.locator(".plan")).to_have_class("plan")
    expect(home.locator("#hcity")).to_be_in_viewport()  # you land back where you were


@pytest.mark.parametrize("trigger", [".hexplore"])
def test_explore_buttons_open_full_screen(home, trigger):
    home.click(trigger)
    expect(home.locator(".plan")).to_have_class("plan full")


def test_hero_label_opens_its_case_study(home, base_url):
    label = home.locator('#heroLabels .plabel[data-id="myestate"]')
    expect(label.locator("small")).to_have_text("Case study ↗")
    label.click()
    expect(home).to_have_url(base_url + "/myestate")


@pytest.mark.parametrize("path", PAGES)
def test_no_location_or_timezone_anywhere(page, base_url, path):
    page.goto(base_url + path)
    text = page.evaluate("document.documentElement.outerHTML")
    assert "Lagos" not in text and "WAT" not in text and "UTC+" not in text


@pytest.mark.parametrize("width", [1920, 1280, 1100, 961, 768, 375])
def test_hero_text_never_runs_into_the_city(browser, base_url, width):
    page = browser.new_page(viewport={"width": width, "height": 900})
    page.goto(base_url + "/")
    r = page.evaluate("""() => { const h = document.querySelector('.intro h1'), c = document.getElementById('hcity').getBoundingClientRect();
      const range = document.createRange(); range.selectNodeContents(h);
      const right = Math.max(...[...document.querySelectorAll('.itext *')].filter(e => e.getClientRects().length).map(e => e.getBoundingClientRect().right), ...[...range.getClientRects()].map(x => x.right));
      return {right, bottom: h.getBoundingClientRect().bottom, left: c.left, top: c.top} }""")
    page.close()
    if width > 960:
        assert r["right"] <= r["left"], r  # side by side: text stays in its column
    else:
        assert r["bottom"] <= r["top"] and r["right"] <= width, r  # stacked: headline sits above the city
