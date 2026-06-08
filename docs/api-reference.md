# API Reference

Auto-generated from source docstrings via Sphinx `autodoc`. Edit the docstrings
in `src/windfarm_sdk.py` and this page updates on the next build.

## WindFarmClient

```{eval-rst}
.. autoclass:: windfarm_sdk.WindFarmClient
   :members:
   :undoc-members:
   :show-inheritance:
```

## Helper functions

```{eval-rst}
.. autofunction:: windfarm_sdk.capacity_factor
```

## REST Endpoints

```{eval-rst}
.. http:get:: /api/v1/turbines/(turbine_id)/telemetry

   Fetch the latest telemetry reading for a turbine.

   **Response:**

   .. code-block:: json

      {
        "turbine_id": "WTG-014",
        "metric": "power",
        "value": 4.2,
        "unit": "MW"
      }

.. http:post:: /api/v1/sites/(site_id)/compliance-report

   Generate a compliance summary for a site.

   **Response:**
