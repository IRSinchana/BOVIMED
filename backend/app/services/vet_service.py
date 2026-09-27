import json
import logging
import urllib.parse
import urllib.request
from typing import Any

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
                addr = ", ".join([p for p in addr_parts if p]) or tags.get("address")
                phone = tags.get("phone") or tags.get("contact:phone")
                providers.append(
                    {
                        "id": str(elem.get("id")),
                        "name": name,
                        "address": addr if addr else None,
                        "phone": phone if phone else None,
                        "source": "OpenStreetMap (Verified)",
                    }
                )
            return providers
    except Exception as exc:
        logger.debug("OSM Overpass lookup skipped/failed: %s", exc)
        return []


def _maps_url(*, query: str | None, latitude: float | None, longitude: float | None) -> str:
    """Build Google Maps search URL from real GPS or entered location text."""
    if latitude is not None and longitude is not None:
        # Prefer exact coordinates when GPS was used.
        q = f"{latitude},{longitude}+veterinary+hospital"
    elif query:
        q = f"{query} veterinary hospital".replace(" ", "+")
    else:
        q = "veterinary+hospital"
    return f"https://www.google.com/maps/search/?api=1&query={q}"


class VeterinarianService:
    """
    Never invents veterinarian contacts.

    Returns verified OSM results only when a live Overpass lookup succeeds.
    Otherwise returns an empty provider list with honest status codes.
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
        location_detected = latitude is not None and longitude is not None
        status = "no_verified"
        # Machine-readable codes; frontend maps these to i18n strings.
        message_key = "noVerified"

        if location_detected:
            osm_results = _query_osm_overpass(latitude, longitude)
            if osm_results:
                providers = osm_results
                status = "verified_found"
                message_key = "foundVerified"
            else:
                # GPS worked — that is NOT the same as finding a verified vet.
                status = "location_detected_no_verified"
                message_key = "noVerifiedAtLocation"
        elif query:
            # No verified directory configured for text search — honest empty state.
            status = "no_verified"
            message_key = "noVerified"
        else:
            status = "no_verified"
            message_key = "notVerified"

        return {
            "success": True,
            "status": status,
            "message_key": message_key,
            "location_detected": location_detected,
            "verified_found": status == "verified_found",
            "providers": providers,
            "directions_url": _maps_url(
                query=query, latitude=latitude, longitude=longitude
            ),
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
