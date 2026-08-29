# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class BaseGeocoder(models.AbstractModel):
    _inherit = "base.geocoder"

    @api.model
    def leaflet_geolocate_missing(
        self, model_name, domain, lat_field, lng_field, limit=80
    ):
        """Find records of ``model_name`` in ``domain`` that have no valid
        coordinates and try to geolocate them from their partner address.

        Coordinates are written on the record's own lat/lng fields when
        available (e.g. res.partner), otherwise on the record's ``partner_id``.
        Returns the count of successfully geolocated records.
        """
        Model = self.env[model_name]
        fields = Model._fields
        if lat_field not in fields or lng_field not in fields:
            return 0
        records = Model.search(domain, limit=limit)
        count = 0
        for record in records.with_context(lang="en_US"):
            partner = (
                record if record._name == "res.partner" else record.partner_id
            )
            if not partner:
                continue
            target = partner
            lat_name = lat_field
            lng_name = lng_field
            # If lat/lng live on the record itself (res.partner) write there,
            # otherwise write on the related partner.
            if record._name != "res.partner":
                lat_name = "partner_latitude"
                lng_name = "partner_longitude"
            if partner[lat_name] or partner[lng_name]:
                continue
            result = partner._geo_localize(
                partner.street,
                partner.zip,
                partner.city,
                partner.state_id.name,
                partner.country_id.name,
            )
            if result:
                target.write(
                    {
                        lat_name: result[0],
                        lng_name: result[1],
                        "date_localization": fields.Date.context_today(record),
                    }
                )
                count += 1
        return count
