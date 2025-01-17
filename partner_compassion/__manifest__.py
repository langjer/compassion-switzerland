##############################################################################
#
#       ______ Releasing children from poverty      _
#      / ____/___  ____ ___  ____  ____ ___________(_)___  ____
#     / /   / __ \/ __ `__ \/ __ \/ __ `/ ___/ ___/ / __ \/ __ \
#    / /___/ /_/ / / / / / / /_/ / /_/ (__  |__  ) / /_/ / / / /
#    \____/\____/_/ /_/ /_/ .___/\__,_/____/____/_/\____/_/ /_/
#                        /_/
#                            in Jesus' name
#
#    Copyright (C) 2014-2023 Compassion CH (http://www.compassion.ch)
#    @author: Emanuel Cino <ecino@compassion.ch>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# pylint: disable=C8101
{
    "name": "Compassion CH Partners",
    "summary": "Upgrade Partners for Compassion Switzerland",
    "version": "14.0.1.0.1",
    "development_status": "Production/Stable",
    "category": "Partner Management",
    "author": "Compassion CH",
    "license": "AGPL-3",
    "website": "https://github.com/CompassionCH/compassion-switzerland",
    "depends": [
        "mail",
        # compassion-modules
        "crm_compassion",
        "partner_segmentation",
        "child_protection",
        "sbc_compassion",
        "thankyou_letters",
        "partner_communication_compassion",
        # OCA/partner-contact
        "base_location",
        "partner_address_street3",
        "partner_contact_birthdate",
        "partner_contact_in_several_companies",
        # OCA/bank-payment
        "account_banking_mandate",
        # OCA/bank-statement-import
        "account_statement_import_camt54",
        # OCA/social
        "mail_tracking",
        # OCA/web
        "web_notify",
        # OCA/server-tools
        "base_search_fuzzy",
        "auditlog",
        # OCA/connector-telephony
        "base_phone",
        # OCA/geospatial
        "web_view_google_map",
    ],
    "external_dependencies": {"python": ["pandas", "pyminizip", "pysftp"]},
    "data": [
        "security/ir.model.access.csv",
        "security/criminal_record_groups.xml",
        "data/partner_category_data.xml",
        "data/partner_title_data.xml",
        "data/advocate_engagement_data.xml",
        "data/calendar_event_type.xml",
        "data/ir_cron.xml",
        "data/gist_indexes.xml",
        "views/advocate_details.xml",
        "views/search_bank_address_wizard.xml",
        "views/partner_compassion_view.xml",
        "views/product_view.xml",
        "views/partner_check_double.xml",
        "views/notification_settings_view.xml",
        "views/tag_merge_wizard_action.xml",
        "views/mail_mail.xml",
    ],
    "qweb": [],
    "installable": True,
    "auto_install": False,
    "post_init_hook": "post_init_hook",
}
