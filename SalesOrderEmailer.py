import random
import Constants
import datetime


def emailProcessDamagedStock(sku, orderNo):


    contents = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <head>
    <!--[if gte mso 9]>
    <xml>
      <o:OfficeDocumentSettings>
        <o:AllowPNG/>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta name="x-apple-disable-message-reformatting">
      <!--[if !mso]><!--><meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
      <title></title>

        <style type="text/css">
          @media only screen and (min-width: 570px) {
      .u-row {
        width: 550px !important;
      }
      .u-row .u-col {
        vertical-align: top;
      }

      .u-row .u-col-100 {
        width: 550px !important;
      }

    }

    @media (max-width: 570px) {
      .u-row-container {
        max-width: 100% !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
      }
      .u-row .u-col {
        min-width: 320px !important;
        max-width: 100% !important;
        display: block !important;
      }
      .u-row {
        width: calc(100% - 40px) !important;
      }
      .u-col {
        width: 100% !important;
      }
      .u-col > div {
        margin: 0 auto;
      }
    }
    body {
      margin: 0;
      padding: 0;
    }

    table,
    tr,
    td {
      vertical-align: top;
      border-collapse: collapse;
    }

    p {
      margin: 0;
    }

    .ie-container table,
    .mso-container table {
      table-layout: fixed;
    }

    * {
      line-height: inherit;
    }

    a[x-apple-data-detectors='true'] {
      color: inherit !important;
      text-decoration: none !important;
    }

    table, td { color: #000000; } @media (max-width: 480px) { #u_column_2 .v-col-padding { padding: 30px 22px 33px !important; } }
        </style>



    </head>

    <body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #3a3737;color: #000000">
      <!--[if IE]><div class="ie-container"><![endif]-->
      <!--[if mso]><div class="mso-container"><![endif]-->
      <table style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #3a3737;width:100%" cellpadding="0" cellspacing="0">
      <tbody>
      <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
        <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #3a3737;"><![endif]-->


    <div class="u-row-container" style="padding: 0px;background-color: transparent">
      <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 550px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
        <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
          <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:550px;"><tr style="background-color: transparent;"><![endif]-->

    <!--[if (mso)|(IE)]><td align="center" width="550" class="v-col-padding" style="width: 550px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]-->
    <div class="u-col u-col-100" style="max-width: 320px;min-width: 550px;display: table-cell;vertical-align: top;">
      <div style="width: 100% !important;">
      <!--[if (!mso)&(!IE)]><!--><div class="v-col-padding" style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]-->

    <table style="font-family:courier new,courier;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
      <tbody>
        <tr>
          <td style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:courier new,courier;" align="left">

    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td style="padding-right: 0px;padding-left: 0px;" align="center">

          <img align="center" border="0" src="cid:0" alt="Hero Image" title="Hero Image"/>

        </td>
      </tr>
    </table>

          </td>
        </tr>
      </tbody>
    </table>

      <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
      </div>
    </div>
    <!--[if (mso)|(IE)]></td><![endif]-->
          <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
        </div>
      </div>
    </div>



    <div class="u-row-container" style="padding: 0px;background-color: transparent">
      <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 550px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;">
        <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
          <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:550px;"><tr style="background-color: #ffffff;"><![endif]-->

    <!--[if (mso)|(IE)]><td align="center" width="550" class="v-col-padding" style="width: 550px;padding: 30px 50px 33px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 10px solid #65b87e;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
    <div id="u_column_2" class="u-col u-col-100" style="max-width: 320px;min-width: 550px;display: table-cell;vertical-align: top;">
      <div style="width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
      <!--[if (!mso)&(!IE)]><!--><div class="v-col-padding" style="padding: 30px 50px 33px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 10px solid #65b87e;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->

    <table style="font-family:courier new,courier;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
      <tbody>
        <tr>
          <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:courier new,courier;" align="left">

      <h1 style="margin: 0px; line-height: 140%; text-align: left; word-wrap: break-word; font-weight: normal; font-family: courier new,courier; font-size: 22px;">
        Hello Sir/Madam,
      </h1>

          </td>
        </tr>
      </tbody>
    </table>

    <table style="font-family:courier new,courier;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
      <tbody>
        <tr>
          <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:courier new,courier;" align="left">

      <div style="line-height: 170%; text-align: left; word-wrap: break-word;">
        <p style="font-size: 14px; line-height: 170%;">A damaged stock item has been sold on Shopify. Please take appropriate action. The following is the details of said transaction:</p>
    <p style="font-size: 14px; line-height: 170%;">&nbsp;</p>
    <p style="font-size: 14px; line-height: 170%;"><span style="font-size: 18px; line-height: 30.6px;"><strong>SKU: """ + str(
        sku) + """</strong></span></p>
    <p style="font-size: 14px; line-height: 170%;"><span style="font-size: 18px; line-height: 30.6px;"><strong>Order Number: """ + str(
        orderNo) + """</strong></span></p>
    <p style="font-size: 14px; line-height: 170%;"><span style="font-size: 18px; line-height: 30.6px;"><strong>Time Of Process: """ + str(
        datetime.datetime.now()) + """</span></p>
    <p style="font-size: 14px; line-height: 170%;">&nbsp;</p>
    <p style="font-size: 14px; line-height: 170%;"><span style="font-family: 'courier new', courier; font-size: 16px; line-height: 27.2px;">Kind Regards,</span></p>
    <p style="font-size: 14px; line-height: 170%;">&nbsp;</p>
    <p style="font-size: 14px; line-height: 170%;">Brodie's Email Bot<br /><span style="font-family: 'courier new', courier; font-size: 10px; line-height: 17px;"><em><strong><span style="line-height: 17px; font-size: 10px;">Beep boop, I am a bot. Did I do well?</span></strong></em></span></p>
      </div>

          </td>
        </tr>
      </tbody>
    </table>

      <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
      </div>
    </div>
    <!--[if (mso)|(IE)]></td><![endif]-->
          <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
        </div>
      </div>
    </div>


        <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
        </td>
      </tr>
      </tbody>
      </table>
      <!--[if mso]></div><![endif]-->
      <!--[if IE]></div><![endif]-->
    </body>

    </html>
    """
    # https://stackoverflow.com/questions/52186048/send-html-email-with-embedded-image-using-python-script
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage

    msg = MIMEMultipart('related')
    msg['Subject'] = "Damaged Stock Ordered - Order No: " + str(orderNo)
    msg['From'] = Constants.Constants.SENDER_EMAIL
    msg['To'] = ", ".join(Constants.Constants.RECEIVERS_1)

    # Record the MIME types of text/html.
    part1 = MIMEText(contents, 'html')

    # Attach parts into message container.
    msg.attach(part1)

    # This example assumes the image is in the current directory
    fp = open('image_resources/robot_img.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '0')
    msg.attach(msgImage)

    mailsrv = smtplib.SMTP(Constants.Constants.SMTP_SERVER)
    mailsrv.sendmail(Constants.Constants.SENDER_EMAIL, Constants.Constants.RECEIVERS_1, msg.as_string())
    mailsrv.quit()


def send_warning_mail(level, error_message, data):
    """
    Send a warning email to the admin
    :param level: The level of the warning
    :param error_message: The error message
    :return:
    """
    contents = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <head>
    <!--[if gte mso 9]>
    <xml>
      <o:OfficeDocumentSettings>
        <o:AllowPNG/>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta name="x-apple-disable-message-reformatting">
      <!--[if !mso]><!--><meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
      <title></title>

        <style type="text/css">
          @media only screen and (min-width: 570px) {
      .u-row {
        width: 550px !important;
      }
      .u-row .u-col {
        vertical-align: top;
      }

      .u-row .u-col-100 {
        width: 550px !important;
      }

    }

    @media (max-width: 570px) {
      .u-row-container {
        max-width: 100% !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
      }
      .u-row .u-col {
        min-width: 320px !important;
        max-width: 100% !important;
        display: block !important;
      }
      .u-row {
        width: calc(100% - 40px) !important;
      }
      .u-col {
        width: 100% !important;
      }
      .u-col > div {
        margin: 0 auto;
      }
    }
    body {
      margin: 0;
      padding: 0;
    }

    table,
    tr,
    td {
      vertical-align: top;
      border-collapse: collapse;
    }

    p {
      margin: 0;
    }

    .ie-container table,
    .mso-container table {
      table-layout: fixed;
    }

    * {
      line-height: inherit;
    }

    a[x-apple-data-detectors='true'] {
      color: inherit !important;
      text-decoration: none !important;
    }

    table, td { color: #000000; } @media (max-width: 480px) { #u_column_2 .v-col-padding { padding: 30px 22px 33px !important; } }
        </style>



    </head>

    <body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #3a3737;color: #000000">
      <!--[if IE]><div class="ie-container"><![endif]-->
      <!--[if mso]><div class="mso-container"><![endif]-->
      <table style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #3a3737;width:100%" cellpadding="0" cellspacing="0">
      <tbody>
      <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
        <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #3a3737;"><![endif]-->


    <div class="u-row-container" style="padding: 0px;background-color: transparent">
      <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 550px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
        <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
          <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:550px;"><tr style="background-color: transparent;"><![endif]-->

    <!--[if (mso)|(IE)]><td align="center" width="550" class="v-col-padding" style="width: 550px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]-->
    <div class="u-col u-col-100" style="max-width: 320px;min-width: 550px;display: table-cell;vertical-align: top;">
      <div style="width: 100% !important;">
      <!--[if (!mso)&(!IE)]><!--><div class="v-col-padding" style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]-->

    <table style="font-family:courier new,courier;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
      <tbody>
        <tr>
          <td style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:courier new,courier;" align="left">

    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td style="padding-right: 0px;padding-left: 0px;" align="center">

          <img align="center" border="0" src="cid:0" alt="Hero Image" title="Hero Image"/>

        </td>
      </tr>
    </table>

          </td>
        </tr>
      </tbody>
    </table>

      <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
      </div>
    </div>
    <!--[if (mso)|(IE)]></td><![endif]-->
          <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
        </div>
      </div>
    </div>



    <div class="u-row-container" style="padding: 0px;background-color: transparent">
      <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 550px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;">
        <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
          <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:550px;"><tr style="background-color: #ffffff;"><![endif]-->

    <!--[if (mso)|(IE)]><td align="center" width="550" class="v-col-padding" style="width: 550px;padding: 30px 50px 33px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 10px solid #65b87e;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
    <div id="u_column_2" class="u-col u-col-100" style="max-width: 320px;min-width: 550px;display: table-cell;vertical-align: top;">
      <div style="width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
      <!--[if (!mso)&(!IE)]><!--><div class="v-col-padding" style="padding: 30px 50px 33px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 10px solid #65b87e;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->

    <table style="font-family:courier new,courier;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
      <tbody>
        <tr>
          <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:courier new,courier;" align="left">

      <h1 style="margin: 0px; line-height: 140%; text-align: left; word-wrap: break-word; font-weight: normal; font-family: courier new,courier; font-size: 22px;">
        Hello Sir/Madam,
      </h1>

          </td>
        </tr>
      </tbody>
    </table>

    <table style="font-family:courier new,courier;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
      <tbody>
        <tr>
          <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:courier new,courier;" align="left">

      <div style="line-height: 170%; text-align: left; word-wrap: break-word;">
        <p style="font-size: 14px; line-height: 170%;">An error has occured within the sales order code. Please take appropriate action (Likely contacting brodie) </p>
    <p style="font-size: 14px; line-height: 170%;">&nbsp;</p>
    <p style="font-size: 14px; line-height: 170%;"><span style="font-size: 18px; line-height: 30.6px;"><strong>Error Severity: """ + str(
        level) + """</strong></span></p>
    <p style="font-size: 14px; line-height: 170%;"><span style="font-size: 18px; line-height: 30.6px;"><strong>Error Message: """ + str(
        error_message) + """</strong></span></p>
    <p style="font-size: 14px; line-height: 170%;"><span style="font-size: 18px; line-height: 30.6px;"><strong>Time Of Incidence: """ + str(
        datetime.datetime.now()) + """</span></p>
    <p style="font-size: 14px; line-height: 170%;"><span style="font-size: 18px; line-height: 30.6px;"><strong>Context: """ + str(
        data) + """</span></p>
    <p style="font-size: 14px; line-height: 170%;">&nbsp;</p>
    <p style="font-size: 14px; line-height: 170%;"><span style="font-family: 'courier new', courier; font-size: 16px; line-height: 27.2px;">Kind Regards,</span></p>
    <p style="font-size: 14px; line-height: 170%;">&nbsp;</p>
    <p style="font-size: 14px; line-height: 170%;">Brodie's Email Bot<br /><span style="font-family: 'courier new', courier; font-size: 10px; line-height: 17px;"><em><strong><span style="line-height: 17px; font-size: 10px;">Beep boop, I am a bot. Did I do well?</span></strong></em></span></p>
      </div>

          </td>
        </tr>
      </tbody>
    </table>

      <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
      </div>
    </div>
    <!--[if (mso)|(IE)]></td><![endif]-->
          <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
        </div>
      </div>
    </div>


        <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
        </td>
      </tr>
      </tbody>
      </table>
      <!--[if mso]></div><![endif]-->
      <!--[if IE]></div><![endif]-->
    </body>

    </html>
    """

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage

    msg = MIMEMultipart('related')
    msg['Subject'] = "Error Caught In Programming - Level " + str(level)
    msg['From'] = Constants.Constants.SENDER_EMAIL
    msg['To'] = ", ".join(Constants.Constants.RECEIVERS_3)

    # Record the MIME types of text/html.
    part1 = MIMEText(contents, 'html')

    # Attach parts into message container.
    msg.attach(part1)

    rdm_number = random.randint(1, 3)
    # This example assumes the image is in the current directory
    fp = open(("image_resources/" + 'code_' + str(rdm_number) + ".png"), 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '0')
    msg.attach(msgImage)

    mailsrv = smtplib.SMTP(Constants.Constants.SMTP_SERVER)
    mailsrv.sendmail(Constants.Constants.SENDER_EMAIL, Constants.Constants.RECEIVERS_3, msg.as_string())
    mailsrv.quit()