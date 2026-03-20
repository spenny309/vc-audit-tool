from schemas.request import Sector

MIN_COMPS = 2

MOCK_COMPS: dict[Sector, list[dict]] = {
    Sector.SAAS: [
        {"name": "Salesforce", "enterprise_value_mm": 200_000, "revenue_mm": 31_352},
        {"name": "Workday",    "enterprise_value_mm": 45_000,  "revenue_mm": 7_260},
        {"name": "HubSpot",    "enterprise_value_mm": 18_000,  "revenue_mm": 2_250},
        {"name": "Zoom",       "enterprise_value_mm": 20_000,  "revenue_mm": 4_390},
    ],
    Sector.FINTECH: [
        {"name": "PayPal",  "enterprise_value_mm": 65_000, "revenue_mm": 29_771},
        {"name": "Block",   "enterprise_value_mm": 35_000, "revenue_mm": 21_919},
        {"name": "Adyen",   "enterprise_value_mm": 40_000, "revenue_mm": 1_625},
        {"name": "Affirm",  "enterprise_value_mm": 8_000,  "revenue_mm": 2_319},
    ],
    Sector.ECOMMERCE: [
        {"name": "Shopify",     "enterprise_value_mm": 80_000, "revenue_mm": 7_060},
        {"name": "BigCommerce", "enterprise_value_mm": 700,    "revenue_mm": 327},
        {"name": "Etsy",        "enterprise_value_mm": 8_000,  "revenue_mm": 2_748},
    ],
    Sector.HEALTHTECH: [
        {"name": "Veeva Systems",   "enterprise_value_mm": 30_000, "revenue_mm": 2_358},
        {"name": "Doximity",        "enterprise_value_mm": 5_000,  "revenue_mm": 470},
        {"name": "Health Catalyst", "enterprise_value_mm": 600,    "revenue_mm": 290},
    ],
}
