# Copyright (C) 2021 Simplify Solutions. All Rights Reserved
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, common


class TestMrpProductionDraft(common.TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestMrpProductionDraft, self).setUp(*args, **kwargs)
        self.StockMove = self.env["stock.move"]
        self.UoM = self.env["uom.uom"]
        self.MrpProduction = self.env["mrp.production"]
        self.Inventory = self.env["stock.inventory"]
        self.InventoryLine = self.env["stock.inventory.line"]
        self.ProductProduce = self.env["mrp.product.produce"]
        self.ProductCategory = self.env["product.category"]

        self.uom_unit = self.env.ref("uom.product_uom_unit")
        self.stock_location = self.env.ref("stock.stock_location_stock")
        self.warehouse = self.env.ref("stock.warehouse0")
        self.route_manufacture = self.warehouse.manufacture_pull_id.route_id
        self.route_mto = self.warehouse.mto_pull_id.route_id

        def create_product(name, routes=False):
            routes = routes or []
            f = Form(self.env["product.product"])
            f.name = name
            f.type = "product"
            f.uom_id = self.uom_unit
            for route in routes:
                f.route_ids.add(route)
            return f.save()

        self.product_finished = create_product(
            "Finished", [self.route_manufacture, self.route_mto]
        )
        self.product_raw = create_product("Raw")

        self._update_product_qty(self.product_raw, self.stock_location, 1)

        with Form(self.env["mrp.bom"]) as f:
            f.product_tmpl_id = self.product_finished.product_tmpl_id
            f.product_qty = 1
            f.product_uom_id = self.uom_unit
            with f.bom_line_ids.new() as line:
                line.product_id = self.product_raw
                line.product_qty = 1
                line.product_uom_id = self.uom_unit

    def _update_product_qty(self, product, location, quantity):
        """Update Product quantity."""
        product_qty = self.env["stock.change.product.qty"].create(
            {
                "location_id": location.id,
                "product_id": product.id,
                "new_quantity": quantity,
            }
        )
        product_qty.change_product_qty()
        return product_qty

    def test_01_mrp_sale_line_link(self):
        """Test if sale order line is on manufacturing order"""

        order_form = Form(self.env["sale.order"])
        order_form.partner_id = self.env.ref("base.res_partner_2")
        with order_form.order_line.new() as line:
            line.product_id = self.product_finished
            line.product_uom_qty = 1
        order = order_form.save()
        order.action_confirm()
        self.env["procurement.group"].run_scheduler()
        mo = self.env["mrp.production"].search(
            [("product_id", "=", self.product_finished.id)]
        )

        self.assertTrue(mo, "Manufacturing order not created.")
        self.assertEqual(
            mo.sale_line_id,
            order.order_line,
            "Sale Order Line not set on Production Order",
        )
