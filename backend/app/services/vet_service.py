import json
import logging
import urllib.parse
import urllib.request
from typing import Any

from app.config import get_settings

logger = logging.getLogger(__name__)


def _query_osm_overpass(lat: float, lon: float, radius_m: int = 15000) -> list[dict]:
    """Query real OpenStreetMap data for verified veterinary facilities."""
    try:
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json][timeout:3];
        (
          node["amenity"="veterinary"](around:{radius_m},{lat},{lon});
          way["amenity"="veterinary"](around:{radius_m},{lat},{lon});
          node["healthcare"="veterinary"](around:{radius_m},{lat},{lon});
        );
        out center 10;
        """
        data = urllib.parse.urlencode({"data": query}).encode("utf-8")
        req = urllib.request.Request(
            overpass_url,
            data=data,
            headers={"User-Agent": "BOVIMED-VeterinarianFinder/1.0"},
        )
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            elements = res.get("elements", [])
            providers = []
            for elem in elements:
                tags = elem.get("tags", {})
                name = tags.get("name")
                if not name:
                    continue
                addr_parts = [
                    tags.get("addr:street"),
                    tags.get("addr:suburb"),
                    tags.get("addr:city"),
                    tags.get("addr:postcode"),
                ]
                addr = ", ".join([p for p in addr_parts if p]) or tags.get("address") or "Address on file in OpenStreetMap"
                phone = tags.get("phone") or tags.get("contact:phone")
                providers.append(
                    {
                        "id": str(elem.get("id")),
                        "name": name,
                        "address": addr,
                        "phone": phone if phone else None,
                        "source": "OpenStreetMap (Verified)",
                    }
                )
            return providers
    except Exception as exc:
        logger.debug("OSM Overpass lookup skipped/failed: %s", exc)
        return []


class VeterinarianService:
    """
    Structure ready for Google Places / Overpass / official VCI directories.

    Without verified records, returns an empty verified list and honest messaging —
    never fabricated contacts.
    """

    def search(
        self,
        *,
        state: str | None = None,
        district: str | None = None,
        city: str | None = None,
        pincode: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> dict[str, Any]:
        query_parts = [p for p in [city, district, state, pincode] if p]
        query = ", ".join(query_parts) if query_parts else None

        providers: list[dict] = []
        status = "unavailable"
        message = (
            "Veterinarian availability could not be verified. "
            "Verify availability before visiting."
        )

        # Attempt OSM verified lookup if GPS coordinates are provided
        if latitude is not None and longitude is not None:
            osm_results = _query_osm_overpass(latitude, longitude)
            if osm_results:
                providers = osm_results
                status = "verified_found"
                message = f"Found {len(providers)} verified veterinary facility(ies) near your coordinates."
            else:
                status = "geo_no_results"
                message = "Veterinarian availability could not be verified for your exact location."
        elif query:
            status = "query_no_results"
            message = f"Veterinarian availability could not be verified for '{query}'."

        directions_query = query or (
            f"{latitude},{longitude}" if latitude is not None and longitude is not None else "veterinary hospital"
        )
        directions_url = (
            "https://www.google.com/maps/search/?api=1&query="
            + str(directions_query).replace(" ", "+")
            + "+veterinary+hospital"
        )

        return {
            "success": True,
            "status": status,
            "message": message,
            "verify_notice": "Verify availability before visiting.",
            "providers": providers,
            "directions_url": directions_url,
            "query": {
                "state": state,
                "district": district,
                "city": city,
                "pincode": pincode,
                "latitude": latitude,
                "longitude": longitude,
            },
        }


def get_veterinarian_service() -> VeterinarianService:
    return VeterinarianService()
