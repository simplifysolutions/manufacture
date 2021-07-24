# Copyright (C) 2021 Simplify Solutions. All Rights Reserved
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Production Order - Sale Order Line Link",
    "version": "12.0.0.1.0",
    "author": "Simplify Solutions",
    "maintainer": "Simplify Solutions",
    "website": "http://www.simplifycloud.com",
    "license": "AGPL-3",
    "category": "Sale",
    "contributors": ["Joel Benjamin <joel.benjamin@simplifycloud.com>"],
    "depends": ["sale_stock", "mrp"],
    "external_dependencies": {"python": []},
    "data": ["views/mrp_view.xml"],
    "qweb": [],
    "demo": [],
    "test": [],
    "installable": True,
    "auto_install": False,
}
