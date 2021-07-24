# Copyright (C) 2021 Simplify Solutions. All Rights Reserved
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    sale_line_id = fields.Many2one(
        "sale.order.line",
        "Sale Order Line",
        compute="_compute_sale_line_id",
        store=True,
    )

    @api.multi
    @api.depends("move_finished_ids")
    def _compute_sale_line_id(self):
        for production in self:
            sale_line = production.get_sale_order_line_from_move(
                production.move_finished_ids[:1]
            )
            production.sale_line_id = sale_line.id

    @api.model
    def get_sale_order_line_from_move(self, move):

        def get_parent_move(move):
            for parent_move in move.move_dest_ids:
                if parent_move.sale_line_id:
                    return parent_move
                return get_parent_move(move.move_dest_ids[:1])
            return move

        sale_move = get_parent_move(move)
        return sale_move.sale_line_id
