from nose.tools import assert_equals

from app import app
from app.lib.parse_messages import parse_message
from app.models import db
from app.models.message import Message, EmailAddress
from app.tests import TestBase


class TestParseMessages(TestBase):
    """Tests app/lib/parse_messages.py functions."""

    def test_parse_headers(self):
        with self.app.application.app_context():
            msg = Message(
                message_id='12345',
                thread_id='67890',
                raw_resource=RAW_RESOURCE
            )
            db.session.add(msg)
            db.session.commit()

            msg = parse_message(msg)

            # Ensure email addresses were created
            assert_equals(
                len(EmailAddress.query.all()), 6
            )

            # Ensure names of email addresses were captured
            assert_equals(
                EmailAddress.query.filter_by(email_address='from@test.com').one().name,
                'From Name'
            )

            # Ensure header connections exist
            assert_equals(
                len(msg.email_addresses()), 6
            )
            assert_equals(
                msg.from_email_address,
                EmailAddress.query.filter_by(email_address='from@test.com').one()
            )
            assert_equals(
                msg.email_addresses('to'),
                EmailAddress.query.filter_by(email_address='to@test.com').all()
            )
            assert_equals(
                len(msg.email_addresses('cc')), 3
            )
            assert_equals(
                msg.email_addresses('delivered-to'),
                EmailAddress.query.filter_by(email_address='delivered-to@test.com').all()
            )


RAW_RESOURCE = {
  "sizeEstimate" : 50735,
  "labelIds" : [
    "CATEGORY_UPDATES",
    "INBOX"
  ],
  "id" : "16a06c32d17e8f8d",
  "snippet" : "Thank you for using Harvest! Billed To Payment Info Alexander Pease Alexander Pease 272 First Avenue, 8C New York, NY 10009 United States Receipt ID: H-DC70D50A57 Visa ending in 4901 Charged on 10 Apr",
  "internalDate" : "1554891612000",
  "historyId" : "10563324",
  "payload" : {
    "mimeType" : "multipart\/mixed",
    "body" : {
      "size" : 0
    },
    "filename" : "",
    "headers" : [
        {
        "name" : "From",
        "value" : "From Name <from@test.com>"
      },
      {
        "name" : "To",
        "value" : "To Name <to@test.com>"
      },
      {
        "name" : "CC",
        "value" : "CC 1 <cc@test.com>, CC 2 <cc2@test.com>, <cc3@test.com>"
      },
      {
        "name" : "Delivered-To",
        "value" : "delivered-to@test.com"
      },
      {
        "name" : "Received",
        "value" : "by 2002:aed:3c75:0:0:0:0:0 with SMTP id u50csp6189818qte;        Wed, 10 Apr 2019 03:20:15 -0700 (PDT)"
      },
      {
        "name" : "Return-Path",
        "value" : "<bounce+d42149.596c39-me=alexanderpease.com@harvestapp.com>"
      },
      {
        "name" : "Date",
        "value" : "Wed, 10 Apr 2019 10:20:12 +0000"
      },
      {
        "name" : "Sender",
        "value" : "From Name <from@test.com>"
      },
      {
        "name" : "Reply-To",
        "value" : "Harvest Support <support@harvestapp.com>"
      },
      {
        "name" : "Message-ID",
        "value" : "<5cadc35ce87c7_4e4a3feefd45d7fc118054b@app7.sc.harvest.host.mail>"
      },
      {
        "name" : "Subject",
        "value" : "Sample Subject"
      },
    ],
    "partId" : "",
    "parts" : [
      {
        "mimeType" : "multipart\/alternative",
        "body" : {
          "size" : 0
        },
        "filename" : "",
        "headers" : [
          {
            "name" : "Content-Type",
            "value" : "multipart\/alternative; boundary=\"--==_mimepart_5cadc35cd18f8_4e4a3feefd45d7fc118037d\"; charset=UTF-8"
          },
          {
            "name" : "Content-Transfer-Encoding",
            "value" : "7bit"
          }
        ],
        "partId" : "0",
        "parts" : [
          {
            "mimeType" : "text\/plain",
            "body" : {
              "size" : 1059,
              "data" : "VGhhbmsgeW91IGZvciB1c2luZyBIYXJ2ZXN0IQ0NCj09PT09PT09PT09PT09PT09PT09PT09PT09PT0NDQoNDQpCaWxsZWQgVG86DQ0KLS0tLS0tLS0tLQ0NCkFsZXhhbmRlciBQZWFzZQ0NCkFsZXhhbmRlciBQZWFzZQ0NCjI3MiBGaXJzdCBBdmVudWUsIDhDDQ0KTmV3IFlvcmssIE5ZIDEwMDA5DQ0KVW5pdGVkIFN0YXRlcw0NCg0NClBheW1lbnQgSW5mbzoNDQotLS0tLS0tLS0tLS0tDQ0KUmVjZWlwdCBJRDogSC1EQzcwRDUwQTU3DQ0KVmlzYSBlbmRpbmcgaW4gNDkwMQ0NCkNoYXJnZWQgb24gMTAgQXByIDIwMTkNDQoNDQoNDQpTZXJ2aWNlOg0NCi0tLS0tLS0tDQ0KTW9udGhseSBIYXJ2ZXN0IFNpbXBsZSBQbGFuOiAxIHVzZXJzIGZvciBodHRwczovL3phbmRlcmNvLmhhcnZlc3RhcHAuY29tDQ0KDQ0KUHJpY2UgKFVTRCk6DQ0KLS0tLS0tLS0tLS0tDQ0KJDEyLjAwDQ0KDQ0KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0NDQpTdWJ0b3RhbDogICAgICAgICAgICAgICAgICAgICAgICAgICAgJDEyLjAwDQ0KDQ0KU2FsZXMgVGF4OiAgICAgICAgICAgICAgICAgICAgICAgICAgICQxLjA3DQ0KDQ0KVG90YWw6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICQxMy4wNw0NCg0NCkFtb3VudCBQYWlkOiAgICAgICAgICAgICAgICAgICAgICAgICAkMTMuMDcNDQotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQ0NCg0NCg0NCg0NClF1ZXN0aW9ucz8NDQoNDQpWaXNpdCB0aGUgSGVscCBDZW50ZXINDQpodHRwczovL2hlbHAuZ2V0aGFydmVzdC5jb20vaGFydmVzdA0NCg0NCkNvbnRhY3QgSGFydmVzdCBTdXBwb3J0DQ0KaHR0cHM6Ly93d3cuZ2V0aGFydmVzdC5jb20vY29udGFjdA0NCg0NClVwZGF0ZSB5b3VyIGJpbGxpbmcgaW5mb3JtYXRpb24gZnJvbSBBY2NvdW50IFNldHRpbmdzDQ0KaHR0cHM6Ly96YW5kZXJjby5oYXJ2ZXN0YXBwLmNvbS9jb21wYW55L2FjY291bnQNDQoNDQpIYXJ2ZXN0IOKAoiAxNiBXIDIybmQgU3QsIDh0aCBGbCDigKIgTmV3IFlvcmssIE5ZIDEwMDEwDQ0K"
            },
            "filename" : "",
            "headers" : [
              {
                "name" : "Content-Type",
                "value" : "text\/plain; charset=UTF-8"
              },
              {
                "name" : "Content-Transfer-Encoding",
                "value" : "quoted-printable"
              }
            ],
            "partId" : "0.0"
          },
          {
            "mimeType" : "text\/html",
            "body" : {
              "size" : 13261,
              "data" : "PCFET0NUWVBFIGh0bWw-DQ0KPGh0bWw-DQ0KICA8aGVhZD4NDQogICAgPG1ldGEgbmFtZT0icmVmZXJyZXIiIGNvbnRlbnQ9Im9yaWdpbiI-DQ0KICAgIDxtZXRhIGh0dHAtZXF1aXY9IkNvbnRlbnQtVHlwZSIgY29udGVudD0idGV4dC9odG1sOyBjaGFyc2V0PVVURi04Ij4NDQogICAgPG1ldGEgbmFtZT0idmlld3BvcnQiIGNvbnRlbnQ9ImluaXRpYWwtc2NhbGU9MSwgdXNlci1zY2FsYWJsZT1ubyI-DQ0KDQ0KICAgIA0NCg0NCiAgICA8c3R5bGUgZGF0YS1pbW11dGFibGU-DQ0KICAgICAgQG1lZGlhIG9ubHkgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA2MDBweCl7DQ0KICAgICAgICBib2R5LCB0YWJsZSwgdGQsIHAsIGEsIGxpLCBibG9ja3F1b3Rlew0NCiAgICAgICAgICAtd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6bm9uZSAhaW1wb3J0YW50Ow0NCiAgICAgICAgICAtbXMtdGV4dC1zaXplLWFkanVzdDpub25lICFpbXBvcnRhbnQ7DQ0KICAgICAgICB9DQ0KICAgICAgICBib2R5LCAjYm9keVRhYmxlew0NCiAgICAgICAgICBtaW4td2lkdGg6MTAwJSAhaW1wb3J0YW50Ow0NCiAgICAgICAgICB3aWR0aDoxMDAlICFpbXBvcnRhbnQ7DQ0KICAgICAgICB9DQ0KICAgICAgICAjdGVtcGxhdGVIZWFkZXIsIC5oZWFkZXJDb250ZW50ew0NCiAgICAgICAgICBib3JkZXItcmFkaXVzOjAgIWltcG9ydGFudDsNDQogICAgICAgICAgYm9yZGVyLXdpZHRoOjFweCAwIDFweCAwICFpbXBvcnRhbnQ7DQ0KICAgICAgICAgIG1hcmdpbjowICFpbXBvcnRhbnQ7DQ0KICAgICAgICB9DQ0KICAgICAgICAuYm9keUNvbnRlbnR7DQ0KICAgICAgICAgIGJvcmRlci1yYWRpdXM6MCAhaW1wb3J0YW50Ow0NCiAgICAgICAgICBib3JkZXItd2lkdGg6MCAwIDFweCAwICFpbXBvcnRhbnQ7DQ0KICAgICAgICB9DQ0KICAgICAgICAuZm9vdGVyQ29udGVudHsNDQogICAgICAgICAgdGV4dC1hbGlnbjpsZWZ0ICFpbXBvcnRhbnQ7DQ0KICAgICAgICB9DQ0KICAgICAgfQ0NCiAgICA8L3N0eWxlPg0NCiAgPHN0eWxlPi5ib2R5Q29udGVudCBhOmxpbmt7Y29sb3I6IzMzNjhhYyAhaW1wb3J0YW50O3RleHQtZGVjb3JhdGlvbjp1bmRlcmxpbmUgIWltcG9ydGFudH0NDQouYm9keUNvbnRlbnQgYTp2aXNpdGVke2NvbG9yOiMzMzY4YWMgIWltcG9ydGFudDt0ZXh0LWRlY29yYXRpb246dW5kZXJsaW5lICFpbXBvcnRhbnR9DQ0KYS5tYWluTGluazpsaW5re2NvbG9yOiNmZmYgIWltcG9ydGFudDt0ZXh0LWRlY29yYXRpb246bm9uZSAhaW1wb3J0YW50fQ0NCmEubWFpbkxpbms6dmlzaXRlZHtjb2xvcjojZmZmICFpbXBvcnRhbnQ7dGV4dC1kZWNvcmF0aW9uOm5vbmUgIWltcG9ydGFudH0NDQouZm9vdGVyQ29udGVudCBhOmxpbmt7Y29sb3I6Izg4OCAhaW1wb3J0YW50O3RleHQtZGVjb3JhdGlvbjp1bmRlcmxpbmV9DQ0KLmZvb3RlckNvbnRlbnQgYTp2aXNpdGVke2NvbG9yOiM4ODggIWltcG9ydGFudDt0ZXh0LWRlY29yYXRpb246dW5kZXJsaW5lfTwvc3R5bGU-PC9oZWFkPg0NCg0NCiAgPGJvZHkgbGVmdG1hcmdpbj0iMCIgbWFyZ2lud2lkdGg9IjAiIHRvcG1hcmdpbj0iMCIgbWFyZ2luaGVpZ2h0PSIwIiBvZmZzZXQ9IjAiIHN0eWxlPSItd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlO21hcmdpbjowO3BhZGRpbmc6MDtiYWNrZ3JvdW5kLWNvbG9yOiNmZmY7Y29sb3I6IzU1NTtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjtmb250LXNpemU6MTZweDtsaW5lLWhlaWdodDoxNTAlOy13ZWJraXQtZm9udC1zbW9vdGhpbmc6YW50aWFsaWFzZWQ7LW1vei1vc3gtZm9udC1zbW9vdGhpbmc6Z3JheXNjYWxlO3dpZHRoOjEwMCUgIWltcG9ydGFudDttaW4td2lkdGg6MTAwJSAhaW1wb3J0YW50Ij4NDQogICAgPGNlbnRlcj4NDQogICAgICA8dGFibGUgYWxpZ249ImNlbnRlciIgYm9yZGVyPSIwIiBjZWxscGFkZGluZz0iMCIgY2VsbHNwYWNpbmc9IjAiIGhlaWdodD0iMTAwJSIgd2lkdGg9IjEwMCUiIGlkPSJib2R5VGFibGUiIHN0eWxlPSJtc28tdGFibGUtbHNwYWNlOjBwdDttc28tdGFibGUtcnNwYWNlOjBwdDstd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlO21hcmdpbjowO3BhZGRpbmc6MDttYXJnaW46YXV0bzt3aWR0aDo1MDBweDtiYWNrZ3JvdW5kLWNvbG9yOiNmZmY7Y29sb3I6IzU1NTtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjtmb250LXNpemU6MTZweDtsaW5lLWhlaWdodDoxNTAlOy13ZWJraXQtZm9udC1zbW9vdGhpbmc6YW50aWFsaWFzZWQ7LW1vei1vc3gtZm9udC1zbW9vdGhpbmc6Z3JheXNjYWxlO2JvcmRlci1jb2xsYXBzZTpzZXBhcmF0ZSAhaW1wb3J0YW50Ij4NDQogICAgICAgIDx0cj4NDQogICAgICAgICAgPHRkIGFsaWduPSJsZWZ0IiB2YWxpZ249InRvcCIgaWQ9ImJvZHlDZWxsIiBzdHlsZT0ibXNvLXRhYmxlLWxzcGFjZTowcHQ7bXNvLXRhYmxlLXJzcGFjZTowcHQ7Zm9udC1mYW1pbHk6SGVsdmV0aWNhLEFyaWFsLHNhbnMtc2VyaWY7LXdlYmtpdC10ZXh0LXNpemUtYWRqdXN0OjEwMCU7LW1zLXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTttYXJnaW46MDtwYWRkaW5nOjAiPg0NCg0NCiAgICAgICAgICAgIDwhLS0gQkVHSU4gVEVNUExBVEUgLy8gLS0-DQ0KICAgICAgICAgICAgPHRhYmxlIGJvcmRlcj0iMCIgY2VsbHBhZGRpbmc9IjAiIGNlbGxzcGFjaW5nPSIwIiBpZD0idGVtcGxhdGVDb250YWluZXIiIHN0eWxlPSJtc28tdGFibGUtbHNwYWNlOjBwdDttc28tdGFibGUtcnNwYWNlOjBwdDtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjstd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlO21hcmdpbjowO3BhZGRpbmc6MDt3aWR0aDoxMDAlO2JvcmRlci1jb2xsYXBzZTpzZXBhcmF0ZSAhaW1wb3J0YW50Ij4NDQoNDQogICAgICAgICAgICAgIDwhLS0gQkVHSU4gSEVBREVSIC8vIC0tPg0NCiAgICAgICAgICAgICAgPHRyPg0NCiAgICAgICAgICAgICAgICA8dGQgc3R5bGU9Im1zby10YWJsZS1sc3BhY2U6MHB0O21zby10YWJsZS1yc3BhY2U6MHB0O2ZvbnQtZmFtaWx5OkhlbHZldGljYSxBcmlhbCxzYW5zLXNlcmlmOy13ZWJraXQtdGV4dC1zaXplLWFkanVzdDoxMDAlOy1tcy10ZXh0LXNpemUtYWRqdXN0OjEwMCUiPg0NCiAgICAgICAgICAgICAgICAgIDx0YWJsZSBib3JkZXI9IjAiIGNlbGxwYWRkaW5nPSIwIiBjZWxsc3BhY2luZz0iMCIgd2lkdGg9IjEwMCUiIGlkPSJ0ZW1wbGF0ZUhlYWRlciIgYmFja2dyb3VuZD0iaHR0cDovL2hhcnZlc3RwdWJsaWMuczMuYW1hem9uYXdzLmNvbS9lbWFpbC9lbWFpbC1vcmFuZ2UtaGVhZGVyLnBuZyIgc3R5bGU9Im1zby10YWJsZS1sc3BhY2U6MHB0O21zby10YWJsZS1yc3BhY2U6MHB0O2ZvbnQtZmFtaWx5OkhlbHZldGljYSxBcmlhbCxzYW5zLXNlcmlmOy13ZWJraXQtdGV4dC1zaXplLWFkanVzdDoxMDAlOy1tcy10ZXh0LXNpemUtYWRqdXN0OjEwMCU7bWFyZ2luOjA7cGFkZGluZzowO2JhY2tncm91bmQtY29sb3I6I2YzNmMwMDtiYWNrZ3JvdW5kLXBvc2l0aW9uOjAgMXB4O2JhY2tncm91bmQtcmVwZWF0OnJlcGVhdDtib3JkZXItdG9wLWxlZnQtcmFkaXVzOjRweDtib3JkZXItdG9wLXJpZ2h0LXJhZGl1czo0cHg7aGVpZ2h0OjYycHg7bWFyZ2luLXRvcDoxLjVlbTt3aWR0aDoxMDAlO2JvcmRlci1jb2xsYXBzZTpzZXBhcmF0ZSAhaW1wb3J0YW50O3dpZHRoOjEwMCUgIWltcG9ydGFudCI-DQ0KICAgICAgICAgICAgICAgICAgICA8dHI-DQ0KICAgICAgICAgICAgICAgICAgICAgIDx0ZCBjbGFzcz0iaGVhZGVyQ29udGVudCIgc3R5bGU9Im1zby10YWJsZS1sc3BhY2U6MHB0O21zby10YWJsZS1yc3BhY2U6MHB0O2ZvbnQtZmFtaWx5OkhlbHZldGljYSxBcmlhbCxzYW5zLXNlcmlmOy13ZWJraXQtdGV4dC1zaXplLWFkanVzdDoxMDAlOy1tcy10ZXh0LXNpemUtYWRqdXN0OjEwMCU7Ym9yZGVyOjFweCBzb2xpZCAjY2U1ZDAwO2JvcmRlci10b3AtbGVmdC1yYWRpdXM6NHB4O2JvcmRlci10b3AtcmlnaHQtcmFkaXVzOjRweDtwYWRkaW5nOjAgMjBweCAwIDIwcHgiPjxpbWcgc3JjPSJodHRwOi8vaGFydmVzdHB1YmxpYy5zMy5hbWF6b25hd3MuY29tL2VtYWlsL2VtYWlsLWhhcnZlc3QtbG9nby1oaWRwaS5wbmciIGlkPSJoZWFkZXJMb2dvIiBhbHQ9IkhhcnZlc3QiIHdpZHRoPSIxNDVweCIgaGVpZ2h0PSI2NXB4IiBzdHlsZT0iYm9yZGVyOjA7aGVpZ2h0OmF1dG87bGluZS1oZWlnaHQ6MTAwJTtvdXRsaW5lOm5vbmU7dGV4dC1kZWNvcmF0aW9uOm5vbmU7Y29sb3I6I0ZGRjtkaXNwbGF5OmJsb2NrO2hlaWdodDo2MnB4O2ZvbnQtc2l6ZToxOHB4O3dpZHRoOjE0NXB4Ij48L3RkPg0NCiAgICAgICAgICAgICAgICAgICAgPC90cj4NDQogICAgICAgICAgICAgICAgICA8L3RhYmxlPg0NCiAgICAgICAgICAgICAgICA8L3RkPg0NCiAgICAgICAgICAgICAgPC90cj4NDQogICAgICAgICAgICAgIDwhLS0gLy8gRU5EIEhFQURFUiAtLT4NDQoNDQogICAgICAgICAgICAgIDwhLS0gQkVHSU4gQk9EWSAvLyAtLT4NDQogICAgICAgICAgICAgIDx0cj4NDQogICAgICAgICAgICAgICAgPHRkIHN0eWxlPSJtc28tdGFibGUtbHNwYWNlOjBwdDttc28tdGFibGUtcnNwYWNlOjBwdDtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjstd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlIj4NDQogICAgICAgICAgICAgICAgICA8dGFibGUgYm9yZGVyPSIwIiBjZWxscGFkZGluZz0iMCIgY2VsbHNwYWNpbmc9IjAiIHdpZHRoPSIxMDAlIiBpZD0idGVtcGxhdGVCb2R5IiBzdHlsZT0ibXNvLXRhYmxlLWxzcGFjZTowcHQ7bXNvLXRhYmxlLXJzcGFjZTowcHQ7Zm9udC1mYW1pbHk6SGVsdmV0aWNhLEFyaWFsLHNhbnMtc2VyaWY7LXdlYmtpdC10ZXh0LXNpemUtYWRqdXN0OjEwMCU7LW1zLXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTttYXJnaW46MDtwYWRkaW5nOjA7Zm9udC1zaXplOjE2cHg7bGluZS1oZWlnaHQ6MTUwJTt0ZXh0LWFsaWduOmxlZnQ7d2lkdGg6MTAwJTtib3JkZXItY29sbGFwc2U6c2VwYXJhdGUgIWltcG9ydGFudCI-DQ0KICAgICAgICAgICAgICAgICAgICA8dHI-DQ0KICAgICAgICAgICAgICAgICAgICAgIDx0ZCBjbGFzcz0iYm9keUNvbnRlbnQiIG1jOmVkaXQ9ImJvZHlfY29udGVudCIgc3R5bGU9Im1zby10YWJsZS1sc3BhY2U6MHB0O21zby10YWJsZS1yc3BhY2U6MHB0O2ZvbnQtZmFtaWx5OkhlbHZldGljYSxBcmlhbCxzYW5zLXNlcmlmOy13ZWJraXQtdGV4dC1zaXplLWFkanVzdDoxMDAlOy1tcy10ZXh0LXNpemUtYWRqdXN0OjEwMCU7YmFja2dyb3VuZDojZmZmO2JvcmRlci1jb2xvcjojZGRkO2JvcmRlci1yYWRpdXM6MCAwIDRweCA0cHg7Ym9yZGVyLXN0eWxlOnNvbGlkO2JvcmRlci13aWR0aDowIDFweCAxcHggMXB4O3BhZGRpbmctdG9wOjAuNWVtO3BhZGRpbmctcmlnaHQ6MjBweDtwYWRkaW5nLWJvdHRvbTowLjVlbTtwYWRkaW5nLWxlZnQ6MjBweCI-DQ0KICAgICAgICAgICAgICAgICAgICAgICAgPCEtLSBCRUdJTiBDT05URU5UIC8vIC0tPg0NCiAgICAgICAgICAgICAgICAgICAgICAgIDxoMSBzdHlsZT0iZGlzcGxheTpibG9jaztmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjtmb250LXNpemU6MjRweDtmb250LXdlaWdodDpib2xkO2xpbmUtaGVpZ2h0OjEyNSU7bWFyZ2luOjAuNzVlbSAwIDAuNzVlbSAwO3BhZGRpbmc6MDt0ZXh0LWFsaWduOmxlZnQ7Y29sb3I6IzMzMyAhaW1wb3J0YW50Ij5UaGFuayB5b3UgZm9yIHVzaW5nIEhhcnZlc3QhPC9oMT4NDQoNDQo8dGFibGUgYm9yZGVyPSIwIiBjZWxscGFkZGluZz0iMCIgY2VsbHNwYWNpbmc9IjAiIHdpZHRoPSIxMDAlIiBpZD0iaW5mb1RhYmxlIiBzdHlsZT0ibXNvLXRhYmxlLWxzcGFjZTowcHQ7bXNvLXRhYmxlLXJzcGFjZTowcHQ7Zm9udC1mYW1pbHk6SGVsdmV0aWNhLEFyaWFsLHNhbnMtc2VyaWY7LXdlYmtpdC10ZXh0LXNpemUtYWRqdXN0OjEwMCU7LW1zLXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTttYXJnaW46MDtwYWRkaW5nOjA7bWFyZ2luOjEuNWVtIDAgMS41ZW0gMDt3aWR0aDoxMDAlO2JvcmRlci1jb2xsYXBzZTpzZXBhcmF0ZSAhaW1wb3J0YW50Ij4NDQogIDx0aGVhZD4NDQogICAgPHRyPg0NCiAgICAgIDx0aCBhbGlnbj0ibGVmdCIgd2lkdGg9IjQ3JSIgc3R5bGU9ImZvbnQtZmFtaWx5OkhlbHZldGljYSxBcmlhbCxzYW5zLXNlcmlmO2JvcmRlci1ib3R0b206MXB4IHNvbGlkICNkZGQ7Zm9udC1zaXplOjE0cHgiPkJpbGxlZCBUbzwvdGg-DQ0KICAgICAgPHRoIHdpZHRoPSI2JSIgY2xhc3M9Iml0LXNwYWNlIiBzdHlsZT0iZm9udC1mYW1pbHk6SGVsdmV0aWNhLEFyaWFsLHNhbnMtc2VyaWY7Ym9yZGVyLWJvdHRvbToxcHggc29saWQgI2RkZDtmb250LXNpemU6MTRweDtib3JkZXItYm90dG9tOjAiPjwvdGg-DQ0KICAgICAgPHRoIGFsaWduPSJsZWZ0IiB3aWR0aD0iNDclIiBzdHlsZT0iZm9udC1mYW1pbHk6SGVsdmV0aWNhLEFyaWFsLHNhbnMtc2VyaWY7Ym9yZGVyLWJvdHRvbToxcHggc29saWQgI2RkZDtmb250LXNpemU6MTRweCI-UGF5bWVudCBJbmZvPC90aD4NDQogICAgPC90cj4NDQogIDwvdGhlYWQ-DQ0KICA8dGJvZHk-DQ0KICAgIDx0cj4NDQogICAgICA8dGQgdmFsaWduPSJ0b3AiIHN0eWxlPSJtc28tdGFibGUtbHNwYWNlOjBwdDttc28tdGFibGUtcnNwYWNlOjBwdDtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjstd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlO3BhZGRpbmc6MC41ZW0gMCAwLjVlbSAwIj4NDQogICAgICAgIEFsZXhhbmRlciBQZWFzZTxicj4NDQogICAgICAgIEFsZXhhbmRlciBQZWFzZTxicj4NDQogICAgICAgIDI3MiBGaXJzdCBBdmVudWUsIDhDPGJyPg0NCiAgICAgICAgTmV3IFlvcmssIE5ZIDEwMDA5PGJyPg0NCiAgICAgICAgVW5pdGVkIFN0YXRlcw0NCiAgICAgIDwvdGQ-DQ0KICAgICAgPHRkIGNsYXNzPSJpdC1zcGFjZSIgc3R5bGU9Im1zby10YWJsZS1sc3BhY2U6MHB0O21zby10YWJsZS1yc3BhY2U6MHB0O2ZvbnQtZmFtaWx5OkhlbHZldGljYSxBcmlhbCxzYW5zLXNlcmlmOy13ZWJraXQtdGV4dC1zaXplLWFkanVzdDoxMDAlOy1tcy10ZXh0LXNpemUtYWRqdXN0OjEwMCU7cGFkZGluZzowLjVlbSAwIDAuNWVtIDA7Ym9yZGVyLWJvdHRvbTowIj48L3RkPg0NCiAgICAgIDx0ZCB2YWxpZ249InRvcCIgc3R5bGU9Im1zby10YWJsZS1sc3BhY2U6MHB0O21zby10YWJsZS1yc3BhY2U6MHB0O2ZvbnQtZmFtaWx5OkhlbHZldGljYSxBcmlhbCxzYW5zLXNlcmlmOy13ZWJraXQtdGV4dC1zaXplLWFkanVzdDoxMDAlOy1tcy10ZXh0LXNpemUtYWRqdXN0OjEwMCU7cGFkZGluZzowLjVlbSAwIDAuNWVtIDAiPg0NCiAgICAgICAgUmVjZWlwdCBJRDogPHNwYW4gc3R5bGU9IndoaXRlLXNwYWNlOiBub3dyYXA7Ij5ILURDNzBENTBBNTc8L3NwYW4-PGJyPg0NCiAgICAgICAgVmlzYSBlbmRpbmcgaW4gNDkwMTxicj4NDQogICAgICAgIENoYXJnZWQgb24gMTAgQXByIDIwMTkNDQogICAgICA8L3RkPg0NCiAgICA8L3RyPg0NCiAgPC90Ym9keT4NDQo8L3RhYmxlPg0NCg0NCg0NCg0NCjx0YWJsZSBib3JkZXI9IjAiIGNlbGxwYWRkaW5nPSIwIiBjZWxsc3BhY2luZz0iMCIgd2lkdGg9IjEwMCUiIGlkPSJyZWNlaXB0VGFibGUiIHN0eWxlPSJtc28tdGFibGUtbHNwYWNlOjBwdDttc28tdGFibGUtcnNwYWNlOjBwdDtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjstd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlO21hcmdpbjowO3BhZGRpbmc6MDt3aWR0aDoxMDAlO2JvcmRlci1jb2xsYXBzZTpzZXBhcmF0ZSAhaW1wb3J0YW50Ij4NDQogIDx0aGVhZD4NDQogICAgPHRyPg0NCiAgICAgIDx0aCBhbGlnbj0ibGVmdCIgd2lkdGg9Ijc1JSIgc3R5bGU9ImZvbnQtZmFtaWx5OkhlbHZldGljYSxBcmlhbCxzYW5zLXNlcmlmO2JvcmRlci1ib3R0b206MXB4IHNvbGlkICNkZGQ7Zm9udC1zaXplOjE0cHgiPlNlcnZpY2U8L3RoPg0NCiAgICAgIDx0aCBhbGlnbj0icmlnaHQiIHdpZHRoPSIyNSUiIHN0eWxlPSJmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjtib3JkZXItYm90dG9tOjFweCBzb2xpZCAjZGRkO2ZvbnQtc2l6ZToxNHB4Ij5QcmljZSAoVVNEKTwvdGg-DQ0KICAgIDwvdHI-DQ0KICA8L3RoZWFkPg0NCiAgPHRib2R5Pg0NCiAgICA8dHI-DQ0KICAgICAgPHRkIGFsaWduPSJsZWZ0IiB2YWxpZ249InRvcCIgc3R5bGU9Im1zby10YWJsZS1sc3BhY2U6MHB0O21zby10YWJsZS1yc3BhY2U6MHB0O2ZvbnQtZmFtaWx5OkhlbHZldGljYSxBcmlhbCxzYW5zLXNlcmlmOy13ZWJraXQtdGV4dC1zaXplLWFkanVzdDoxMDAlOy1tcy10ZXh0LXNpemUtYWRqdXN0OjEwMCU7Ym9yZGVyLWJvdHRvbToxcHggc29saWQgI2RkZDtwYWRkaW5nOjAuNzVlbSAwIDAuNzVlbSAwIj4NDQogICAgICAgIE1vbnRobHkgSGFydmVzdCBTaW1wbGUgUGxhbjogMSB1c2VycyBmb3IgaHR0cHM6Ly96YW5kZXJjby5oYXJ2ZXN0YXBwLmNvbQ0NCiAgICAgIDwvdGQ-DQ0KICAgICAgPHRkIGFsaWduPSJyaWdodCIgdmFsaWduPSJ0b3AiIHN0eWxlPSJtc28tdGFibGUtbHNwYWNlOjBwdDttc28tdGFibGUtcnNwYWNlOjBwdDtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjstd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlO2JvcmRlci1ib3R0b206MXB4IHNvbGlkICNkZGQ7cGFkZGluZzowLjc1ZW0gMCAwLjc1ZW0gMCI-DQ0KICAgICAgICAkMTIuMDANDQogICAgICA8L3RkPg0NCiAgICA8L3RyPg0NCiAgPC90Ym9keT4NDQogIDx0Zm9vdD4NDQogICAgPHRyPg0NCiAgICAgIDx0ZCBhbGlnbj0icmlnaHQiIGNsYXNzPSJydC1zdWJ0b3RhbCBydC1maXJzdGxpbmUiIHN0eWxlPSJtc28tdGFibGUtbHNwYWNlOjBwdDttc28tdGFibGUtcnNwYWNlOjBwdDtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjstd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlO3BhZGRpbmctdG9wOjAuNWVtIj5TdWJ0b3RhbDwvdGQ-DQ0KICAgICAgPHRkIGFsaWduPSJyaWdodCIgY2xhc3M9InJ0LXN1YnRvdGFsIHJ0LWZpcnN0bGluZSIgc3R5bGU9Im1zby10YWJsZS1sc3BhY2U6MHB0O21zby10YWJsZS1yc3BhY2U6MHB0O2ZvbnQtZmFtaWx5OkhlbHZldGljYSxBcmlhbCxzYW5zLXNlcmlmOy13ZWJraXQtdGV4dC1zaXplLWFkanVzdDoxMDAlOy1tcy10ZXh0LXNpemUtYWRqdXN0OjEwMCU7cGFkZGluZy10b3A6MC41ZW0iPiQxMi4wMDwvdGQ-DQ0KICAgIDwvdHI-DQ0KICAgIDx0cj4NDQogICAgICA8dGQgYWxpZ249InJpZ2h0IiBjbGFzcz0icnQtdGF4IiBzdHlsZT0ibXNvLXRhYmxlLWxzcGFjZTowcHQ7bXNvLXRhYmxlLXJzcGFjZTowcHQ7Zm9udC1mYW1pbHk6SGVsdmV0aWNhLEFyaWFsLHNhbnMtc2VyaWY7LXdlYmtpdC10ZXh0LXNpemUtYWRqdXN0OjEwMCU7LW1zLXRleHQtc2l6ZS1hZGp1c3Q6MTAwJSI-U2FsZXMgVGF4PC90ZD4NDQogICAgICA8dGQgYWxpZ249InJpZ2h0IiBjbGFzcz0icnQtdGF4IiBzdHlsZT0ibXNvLXRhYmxlLWxzcGFjZTowcHQ7bXNvLXRhYmxlLXJzcGFjZTowcHQ7Zm9udC1mYW1pbHk6SGVsdmV0aWNhLEFyaWFsLHNhbnMtc2VyaWY7LXdlYmtpdC10ZXh0LXNpemUtYWRqdXN0OjEwMCU7LW1zLXRleHQtc2l6ZS1hZGp1c3Q6MTAwJSI-JDEuMDc8L3RkPg0NCiAgICA8L3RyPg0NCiAgICA8dHI-DQ0KICAgICAgPHRkIGFsaWduPSJyaWdodCIgY2xhc3M9InJ0LXRvdGFsIiBzdHlsZT0ibXNvLXRhYmxlLWxzcGFjZTowcHQ7bXNvLXRhYmxlLXJzcGFjZTowcHQ7Zm9udC1mYW1pbHk6SGVsdmV0aWNhLEFyaWFsLHNhbnMtc2VyaWY7LXdlYmtpdC10ZXh0LXNpemUtYWRqdXN0OjEwMCU7LW1zLXRleHQtc2l6ZS1hZGp1c3Q6MTAwJSI-VG90YWw8L3RkPg0NCiAgICAgIDx0ZCBhbGlnbj0icmlnaHQiIGNsYXNzPSJydC10b3RhbCIgc3R5bGU9Im1zby10YWJsZS1sc3BhY2U6MHB0O21zby10YWJsZS1yc3BhY2U6MHB0O2ZvbnQtZmFtaWx5OkhlbHZldGljYSxBcmlhbCxzYW5zLXNlcmlmOy13ZWJraXQtdGV4dC1zaXplLWFkanVzdDoxMDAlOy1tcy10ZXh0LXNpemUtYWRqdXN0OjEwMCUiPiQxMy4wNzwvdGQ-DQ0KICAgIDwvdHI-DQ0KICAgIDx0cj4NDQogICAgICA8dGQgYWxpZ249InJpZ2h0IiBjbGFzcz0icnQtYW1vdW50LXBhaWQiIHN0eWxlPSJtc28tdGFibGUtbHNwYWNlOjBwdDttc28tdGFibGUtcnNwYWNlOjBwdDtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjstd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlO2ZvbnQtd2VpZ2h0OmJvbGQ7cGFkZGluZy1ib3R0b206MWVtIj5BbW91bnQgUGFpZDwvdGQ-DQ0KICAgICAgPHRkIGFsaWduPSJyaWdodCIgY2xhc3M9InJ0LWFtb3VudC1wYWlkIiBzdHlsZT0ibXNvLXRhYmxlLWxzcGFjZTowcHQ7bXNvLXRhYmxlLXJzcGFjZTowcHQ7Zm9udC1mYW1pbHk6SGVsdmV0aWNhLEFyaWFsLHNhbnMtc2VyaWY7LXdlYmtpdC10ZXh0LXNpemUtYWRqdXN0OjEwMCU7LW1zLXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTtmb250LXdlaWdodDpib2xkO3BhZGRpbmctYm90dG9tOjFlbSI-JDEzLjA3PC90ZD4NDQogICAgPC90cj4NDQogIDwvdGZvb3Q-DQ0KPC90YWJsZT4NDQoNDQogICAgICAgICAgICAgICAgICAgICAgICA8IS0tIC8vIEVORCBDT05URU5UIC0tPg0NCiAgICAgICAgICAgICAgICAgICAgICA8L3RkPg0NCiAgICAgICAgICAgICAgICAgICAgPC90cj4NDQogICAgICAgICAgICAgICAgICA8L3RhYmxlPg0NCiAgICAgICAgICAgICAgICA8L3RkPg0NCiAgICAgICAgICAgICAgPC90cj4NDQogICAgICAgICAgICAgIDwhLS0gLy8gRU5EIEJPRFkgLS0-DQ0KDQ0KICAgICAgICAgICAgICA8IS0tIEJFR0lOIEZPT1RFUiAvLyAtLT4NDQogICAgICAgICAgICAgIDx0cj4NDQogICAgICAgICAgICAgICAgPHRkIHN0eWxlPSJtc28tdGFibGUtbHNwYWNlOjBwdDttc28tdGFibGUtcnNwYWNlOjBwdDtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjstd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlIj4NDQogICAgICAgICAgICAgICAgICA8dGFibGUgYm9yZGVyPSIwIiBjZWxscGFkZGluZz0iMCIgY2VsbHNwYWNpbmc9IjAiIHdpZHRoPSIxMDAlIiBpZD0idGVtcGxhdGVGb290ZXIiIHN0eWxlPSJtc28tdGFibGUtbHNwYWNlOjBwdDttc28tdGFibGUtcnNwYWNlOjBwdDtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjstd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlO21hcmdpbjowO3BhZGRpbmc6MDtjb2xvcjojODg4O2ZvbnQtc2l6ZToxNHB4O2xpbmUtaGVpZ2h0OjIwMCU7d2lkdGg6MTAwJTtib3JkZXItY29sbGFwc2U6c2VwYXJhdGUgIWltcG9ydGFudCI-DQ0KICAgICAgICAgICAgICAgICAgICA8dHI-DQ0KICAgICAgICAgICAgICAgICAgICAgIDx0ZCBhbGlnbj0iY2VudGVyIiB2YWxpZ249InRvcCIgY2xhc3M9ImZvb3RlckNvbnRlbnQiIHN0eWxlPSJtc28tdGFibGUtbHNwYWNlOjBwdDttc28tdGFibGUtcnNwYWNlOjBwdDtmb250LWZhbWlseTpIZWx2ZXRpY2EsQXJpYWwsc2Fucy1zZXJpZjstd2Via2l0LXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTstbXMtdGV4dC1zaXplLWFkanVzdDoxMDAlO2JhY2tncm91bmQ6I2ZmZjtwYWRkaW5nLXRvcDoxLjc1ZW07cGFkZGluZy1yaWdodDoyMHB4O3BhZGRpbmctYm90dG9tOjNlbTtwYWRkaW5nLWxlZnQ6MjBweCI-DQ0KDQ0KICAgICAgICAgICAgICAgICAgICAgICAgPHAgc3R5bGU9Ii13ZWJraXQtdGV4dC1zaXplLWFkanVzdDoxMDAlOy1tcy10ZXh0LXNpemUtYWRqdXN0OjEwMCU7bWFyZ2luOjFlbSAwIDFlbSAwO21hcmdpbjowO3BhZGRpbmc6MCI-DQ0KICAgICAgICAgICAgICAgICAgICAgICAgICA8c3Ryb25nPlF1ZXN0aW9ucz88L3N0cm9uZz4gVmlzaXQgdGhlIDxhIGhyZWY9Imh0dHBzOi8vaGVscC5nZXRoYXJ2ZXN0LmNvbS9oYXJ2ZXN0IiBzdHlsZT0iLXdlYmtpdC10ZXh0LXNpemUtYWRqdXN0OjEwMCU7LW1zLXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTt0ZXh0LWRlY29yYXRpb246dW5kZXJsaW5lO2NvbG9yOiM4ODggIWltcG9ydGFudCI-SGVscCBDZW50ZXI8L2E-IG9yIGNvbnRhY3QgPGEgaHJlZj0iaHR0cHM6Ly93d3cuZ2V0aGFydmVzdC5jb20vY29udGFjdCIgc3R5bGU9Ii13ZWJraXQtdGV4dC1zaXplLWFkanVzdDoxMDAlOy1tcy10ZXh0LXNpemUtYWRqdXN0OjEwMCU7dGV4dC1kZWNvcmF0aW9uOnVuZGVybGluZTtjb2xvcjojODg4ICFpbXBvcnRhbnQiPkhhcnZlc3QgU3VwcG9ydDwvYT4uPGJyPg0NCiAgICAgICAgICAgICAgICAgICAgICAgICAgVXBkYXRlIHlvdXIgYmlsbGluZyBpbmZvcm1hdGlvbiBmcm9tIDxhIGhyZWY9Imh0dHBzOi8vemFuZGVyY28uaGFydmVzdGFwcC5jb20vY29tcGFueS9hY2NvdW50IiBzdHlsZT0iLXdlYmtpdC10ZXh0LXNpemUtYWRqdXN0OjEwMCU7LW1zLXRleHQtc2l6ZS1hZGp1c3Q6MTAwJTt0ZXh0LWRlY29yYXRpb246dW5kZXJsaW5lO2NvbG9yOiM4ODggIWltcG9ydGFudCI-QWNjb3VudCBTZXR0aW5nczwvYT4uPGJyPg0NCiAgICAgICAgICAgICAgICAgICAgICAgICAgSGFydmVzdCDigKIgMTYgVyAyMm5kIFN0LCA4dGggRmwg4oCiIE5ldyBZb3JrLCBOWSAxMDAxMA0NCiAgICAgICAgICAgICAgICAgICAgICAgIDwvcD4NDQoNDQogICAgICAgICAgICAgICAgICAgICAgPC90ZD4NDQogICAgICAgICAgICAgICAgICAgIDwvdHI-DQ0KICAgICAgICAgICAgICAgICAgPC90YWJsZT4NDQogICAgICAgICAgICAgICAgPC90ZD4NDQogICAgICAgICAgICAgIDwvdHI-DQ0KICAgICAgICAgICAgICA8IS0tIC8vIEVORCBGT09URVIgLS0-DQ0KDQ0KICAgICAgICAgICAgPC90YWJsZT4NDQogICAgICAgICAgICA8IS0tIC8vIEVORCBURU1QTEFURSAtLT4NDQoNDQogICAgICAgICAgPC90ZD4NDQogICAgICAgIDwvdHI-DQ0KICAgICAgPC90YWJsZT4NDQogICAgPC9jZW50ZXI-DQ0KICA8L2JvZHk-DQ0KPC9odG1sPg0NCg=="
            },
            "filename" : "",
            "headers" : [
              {
                "name" : "Content-Type",
                "value" : "text\/html; charset=UTF-8"
              },
              {
                "name" : "Content-Transfer-Encoding",
                "value" : "quoted-printable"
              }
            ],
            "partId" : "0.1"
          }
        ]
      },
      {
        "mimeType" : "application\/pdf",
        "body" : {
          "size" : 21739,
          "attachmentId" : "ANGjdJ_rmAJeTl6AVyrCKuw9Ub5oNEtJSmJ1nxvyprkH2OlB7eLgng4oc4lxyVjvJ-X1sjWoQdcPL4mEnx5GQs03CCSPaUPgqFGd7LUxpXfxLLa8pXlEEZXVgWa1StBZLLOTIEC4HGxHdbrRX6e_uCLFIExjopyEH19eRqp-xA7faOMvVUnK11bYk7RPKQ8pKtM1Q9bE1JvXqDZVPDtGFgcbxcgjyPWz4W-_uwjOCi72qdWEC2-mopzoXuCNyiKBlI0AS1OMttDl3lmbCe6qxekJYT8AypJRaifXTjhnxkXr2gSQghN64uWLB0qC_bNZNguzaEcIEff-HwW_n-e7jX2ogplwUImZbQTetKaL9zyJKSvMWckYs11kzZwkFd0YDXicTZKxSoJLe6hCubhy"
        },
        "filename" : "2019-04-10_harvest_sales_receipt_zanderco.pdf",
        "headers" : [
          {
            "name" : "Content-Type",
            "value" : "application\/pdf; filename=2019-04-10_harvest_sales_receipt_zanderco.pdf"
          },
          {
            "name" : "Content-Transfer-Encoding",
            "value" : "base64"
          },
          {
            "name" : "Content-Disposition",
            "value" : "attachment; filename=2019-04-10_harvest_sales_receipt_zanderco.pdf"
          },
          {
            "name" : "Content-ID",
            "value" : "<5cadc35ce9f8c_4e4a3feefd45d7fc1180640@app7.sc.harvest.host.mail>"
          }
        ],
        "partId" : "1"
      }
    ]
  },
  "threadId" : "16a06c32d17e8f8d"
}

