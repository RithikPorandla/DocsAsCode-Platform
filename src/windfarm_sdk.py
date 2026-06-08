"""
DocsAsCode - Example SDK (offshore wind domain)

A small, realistic SDK used to demonstrate auto-generated API reference docs.
Every public symbol is fully documented so the custom docs-policy validator
(``tools/validate_docs.py``) passes, and pure functions carry doctest examples
that run in CI.
"""

from __future__ import annotations


def capacity_factor(actual_mwh: float, rated_mw: float, hours: int) -> float:
    """
    Compute the capacity factor of a turbine or wind farm.

    Capacity factor is actual energy produced divided by the theoretical
    maximum if the asset ran at rated power for the whole period.

    :param actual_mwh: Actual energy produced over the period, in MWh.
    :param rated_mw: Nameplate (rated) capacity, in MW.
    :param hours: Number of hours in the period.
    :returns: Capacity factor as a fraction between 0 and 1.
    :rtype: float

    Example:

    >>> capacity_factor(4380.0, 5.0, 8760)
    0.1
    """
    if rated_mw <= 0 or hours <= 0:
        raise ValueError("rated_mw and hours must be positive")
    return actual_mwh / (rated_mw * hours)


class WindFarmClient:
    """
    Client for the (fictional) Offshore Wind Telemetry API.

    Provides access to turbine telemetry, site-level energy yield, and
    compliance reporting. Designed to mirror how a real developer-facing
    SDK is documented under a docs-as-code workflow.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.example-wind.io/v1"):
        """
        Initialize the client.

        :param api_key: API key used to authenticate requests.
        :param base_url: Base URL of the telemetry API.
        """
        self.api_key = api_key
        self.base_url = base_url

    def get_turbine_telemetry(self, turbine_id: str, metric: str = "power") -> dict:
        """
        Fetch the latest telemetry reading for a single turbine.

        :param turbine_id: Unique identifier of the turbine (e.g. ``"WTG-014"``).
        :param metric: Telemetry channel - ``power``, ``wind_speed``, or ``rpm``.
        :returns: A dict with keys ``turbine_id``, ``metric``, ``value``, and ``unit``.
        :rtype: dict
        """
        return {"turbine_id": turbine_id, "metric": metric, "value": 0.0, "unit": "MW"}

    def energy_yield(self, site_id: str, start: str, end: str) -> float:
        """
        Return total energy yield for a site over a date range.

        :param site_id: Identifier of the wind farm site.
        :param start: Start date in ISO format (``YYYY-MM-DD``).
        :param end: End date in ISO format (``YYYY-MM-DD``).
        :returns: Total energy produced in MWh.
        :rtype: float
        """
        return 0.0

    def compliance_report(self, site_id: str, standard: str = "IEC 61400-1:2019") -> dict:
        """
        Generate a compliance summary for a site against an engineering standard.

        :param site_id: Identifier of the wind farm site.
        :param standard: Standard to assess against, including edition/year.
        :returns: A dict with keys ``site_id``, ``standard``, and ``compliant``.
        :rtype: dict
        """
        return {"site_id": site_id, "standard": standard, "compliant": True}
