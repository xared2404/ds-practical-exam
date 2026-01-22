"""
World Bank API v2 client (requests directo, robusto).

Devuelve DataFrame en formato long:
country_id, iso3, country, year, indicator, indicator_name, value
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Union

import time
import requests
import pandas as pd


@dataclass(frozen=True)
class WBClientConfig:
    base_url: str = "https://api.worldbank.org/v2"
    per_page: int = 200
    timeout_seconds: int = 60
    max_retries: int = 4
    backoff_seconds: float = 0.8
    user_agent: str = "ds-exam-wb-client/1.0"


class WorldBankClient:
    def __init__(self, config: WBClientConfig = WBClientConfig()):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self.config.user_agent,
                "Accept": "application/json",
            }
        )

    def _get_json(self, url: str, params: Dict[str, Any]) -> Any:
        for attempt in range(self.config.max_retries):
            r = self.session.get(
                url,
                params=params,
                timeout=self.config.timeout_seconds,
                allow_redirects=True,
            )

            if r.status_code in {429, 500, 502, 503, 504}:
                time.sleep(self.config.backoff_seconds * (2 ** attempt))
                continue

            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code} for {r.url}")

            # Si el server manda HTML/XML, lo mostramos (no “JSON decoding error” opaco)
            ctype = (r.headers.get("Content-Type") or "").lower()
            if "application/json" not in ctype:
                snippet = (r.text or "")[:200]
                raise RuntimeError(f"Non-JSON response (Content-Type={ctype}). First 200 chars: {snippet}")

            data = r.json()

            if isinstance(data, dict) and "message" in data:
                raise RuntimeError(f"World Bank API error: {data['message']}")

            return data

        raise RuntimeError("Max retries exceeded")

    def _iter_pages(self, endpoint: str, params: Dict[str, Any]) -> Iterable[List[Dict[str, Any]]]:
        url = f"{self.config.base_url}/{endpoint.lstrip('/')}"
        params = dict(params)
        params.setdefault("format", "json")
        params.setdefault("per_page", self.config.per_page)

        page = 1
        while True:
            params["page"] = page
            data = self._get_json(url, params)

            if not isinstance(data, list) or len(data) < 2:
                raise RuntimeError(f"Unexpected API format at {url} params={params}")

            meta, rows = data[0], data[1]
            if rows is None:
                return

            yield rows

            pages = int(meta.get("pages", 1))
            if page >= pages:
                break

            page += 1
            time.sleep(0.15)

    def fetch_indicator_country_year(
        self,
        indicator_code: str,
        countries: Union[str, List[str]] = "all",
        date: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Descarga datos de /country/{countries}/indicator/{indicator_code}

        - countries: "all" o ["MEX","USA"] (ISO3 preferible)
        - date: "2010:2020" o "2010" o None
        """
        if isinstance(countries, list):
            countries_param = ";".join([c.strip().lower() for c in countries])
        else:
            countries_param = countries.strip().lower()

        endpoint = f"country/{countries_param}/indicator/{indicator_code}"
        params: Dict[str, Any] = {}
        if date:
            params["date"] = date

        records: List[Dict[str, Any]] = []
        for rows in self._iter_pages(endpoint, params=params):
            for it in rows:
                country_obj = it.get("country") or {}
                ind_obj = it.get("indicator") or {}

                y = it.get("date")
                try:
                    year = int(y) if y is not None else None
                except ValueError:
                    year = None

                records.append(
                    {
                        "country_id": country_obj.get("id"),
                        "iso3": it.get("countryiso3code"),
                        "country": country_obj.get("value"),
                        "year": year,
                        "indicator": ind_obj.get("id"),
                        "indicator_name": ind_obj.get("value"),
                        "value": it.get("value"),
                    }
                )

        df = pd.DataFrame(records)
        if not df.empty:
            df = df.dropna(subset=["country_id", "year"])
        return df
