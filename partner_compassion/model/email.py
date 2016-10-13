# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino <ecino@compassion.ch>
#
#    The licence is in the file __openerp__.py
#
##############################################################################


from openerp import models, api


class Email(models.Model):
    """ Email message sent through SendGrid """
    _inherit = 'mail.mail'

    @api.multi
    def send_sendgrid(self):
        """ Post the message in partner, with tracking.
        """
        super(Email, self).send_sendgrid()
        for email in self:
            message = email.mail_message_id
            for partner in email.recipient_ids:
                if not (message.model == 'res.partner' and message.res_id ==
                        partner.id):
                    message_id = partner.message_post(
                        message.body, message.subject)
                    p_message = message.browse(message_id)
                    p_message.write({
                        'subtype_id': self.env.ref('mail.mt_comment').id,
                        'notified_partner_ids': [(4, partner.id)],
                        # Set parent to have the tracking working
                        'parent_id': message.id,
                        'author_id': message.author_id.id
                    })


class MailMessage(models.Model):
    """ Enable many thread notifications to track the same e-mail.
        It reads the parent_id of messages to do so.
    """
    _inherit = 'mail.message'

    @api.model
    def _message_read_dict_postprocess(self, messages, message_tree):
        res = super(MailMessage, self)._message_read_dict_postprocess(
            messages, message_tree)
        for message_dict in messages:
            mail_message_id = message_dict.get('id', False)
            if mail_message_id:
                # Add parent and child message ids in the search
                message_ids = [mail_message_id]
                message = self.browse(mail_message_id)
                message_ids.extend(message.child_ids.ids)
                while message.parent_id:
                    message = message.parent_id
                    message_ids.append(message.id)

                # Code copied from mail_tracking module (be aware of updates)
                partner_trackings = {}
                for partner in message_dict.get('partner_ids', []):
                    partner_id = partner[0]
                    tracking_email = self.env['mail.tracking.email'].search([
                        ('mail_message_id', 'in', message_ids),
                        ('partner_id', '=', partner_id),
                    ], limit=1)
                    status = self._partner_tracking_status_get(tracking_email)
                    partner_trackings[str(partner_id)] = (
                        status, tracking_email.id)

            message_dict['partner_trackings'] = partner_trackings
        return res


class EmailTemplate(models.Model):
    """ Remove functionality to search partners given the email_to field.
        This is not good behaviour for Compassion CH where we have
        some partners that share the same e-mail and because we won't
        create a new partner when sending to a static address
    """
    _inherit = 'email.template'

    @api.v7
    def generate_email_batch(self, cr, uid, tpl_id=False, res_ids=None,
                             fields=None, context=None):
        if context and 'tpl_partners_only' in context:
            del context['tpl_partners_only']
        return super(EmailTemplate, self).generate_email_batch(
            cr, uid, tpl_id, res_ids, fields=fields, context=context)


class MailNotification(models.Model):
    _inherit = 'mail.notification'

    @api.multi
    def _notify_email(self, message_id, force_send=False, user_signature=True):
        """ Always send notifications by e-mail. Put parent_id in messages
        in order to enable tracking from the thread.
        """
        mail_ids = super(MailNotification, self)._notify_email(
            message_id, force_send, user_signature)
        if isinstance(mail_ids, list):
            for i in range(0, len(self)):
                emails = self.env['mail.mail'].browse(mail_ids[i])
                message = self[i].message_id
                emails.mapped('mail_message_id').write({
                    'parent_id': message.id
                })
                emails.send()
        return mail_ids
