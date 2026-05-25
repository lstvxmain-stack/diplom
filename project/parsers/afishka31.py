"""Parser for afishka31.ru - Belgorod cultural events poster."""
import re
import requests
from bs4 import BeautifulSoup
from project.parsers.base import BaseParser, ParsedVenue, ParsedEvent


class Afishka31Parser(BaseParser):
    name = "afishka31.ru"

    BASE_URL = "https://afishka31.ru"
    SECTIONS = {
        "theatre": "Театры",
        "cinema": "Кинотеатры",
        "filarmoni": "Концертные залы",
        "concerts": "Концертные залы",
        "children": "Театры",
        "vernisaz": "Музеи и выставки",
        "sport": "Стадионы и спорткомплексы",
        "tour": "Концертные залы",
        "nepropusti": "Фестивали и городские мероприятия",
    }

    def parse_venues(self) -> list[ParsedVenue]:
        return []

    def parse_events(self) -> list[ParsedEvent]:
        events = []
        for section in self.SECTIONS:
            try:
                events.extend(self._parse_section(section))
            except Exception as e:
                print(f"[{self.name}] Error parsing section {section}: {e}")
        return events

    def _parse_section(self, section: str) -> list[ParsedEvent]:
        url = f"{self.BASE_URL}/actions/{section}/"
        events = []

        try:
            resp = requests.get(url, timeout=15)
            resp.encoding = "utf-8"
            if not resp.ok:
                return events

            soup = BeautifulSoup(resp.text, "lxml")
            items = soup.select("ul.item-list > li.item")

            for item in items:
                link_el = item.select_one("a[href]")
                if not link_el:
                    continue
                href = link_el.get("href", "")
                full_url = f"{self.BASE_URL}{href}" if not href.startswith("http") else href

                title_el = item.select_one(".title-block h3")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                age_spans = title_el.select("small")
                age_rating = ""
                for span in age_spans:
                    text = span.get_text(strip=True)
                    if "+" in text:
                        age_rating = text.strip("() ")

                desc_el = item.select_one(".desc-block")
                time_text = ""
                if desc_el:
                    desc_text = desc_el.get_text(strip=True)
                    time_match = re.search(r"(\d{1,2}:\d{2})", desc_text)
                    if time_match:
                        time_text = time_match.group(1)

                venue_el = item.select_one(".mesto-block")
                venue_text = venue_el.get_text(strip=True) if venue_el else ""

                date_el = item.select_one(".date-block")
                date_text = date_el.get_text(strip=True) if date_el else ""

                img_el = item.select_one(".img-block-inner")
                img_url = ""
                if img_el and img_el.has_attr("style"):
                    bg_match = re.search(r"url\(['\"]?(.*?)['\"]?\)", img_el["style"])
                    if bg_match:
                        img_url = bg_match.group(1)

                event = ParsedEvent(
                    title=title,
                    date_start=date_text,
                    time=time_text,
                    age_rating=age_rating,
                    venue_name=venue_text,
                    category_name=self.SECTIONS.get(section, ""),
                    source_url=full_url,
                    image_url=img_url,
                )
                events.append(event)

        except Exception as e:
            print(f"[{self.name}] Error fetching {url}: {e}")

        return events
