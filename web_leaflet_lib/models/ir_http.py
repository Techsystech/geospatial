# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        result = super().session_info()
        config = self.env["ir.config_parameter"].sudo()
        tile_url = config.get_param("leaflet.tile_url", default="")
        if not tile_url or tile_url == "False":
            tile_url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        copyright_notice = config.get_param("leaflet.copyright", default="")
        if not copyright_notice or copyright_notice == "False":
            copyright_notice = (
                "&copy; <a href='http://www.openstreetmap.org/copyright'>"
                "OpenStreetMap</a>"
            )
        result.update(
            {
                "leaflet.tile_url": tile_url,
                "leaflet.copyright": copyright_notice,
            }
        )
        return result
