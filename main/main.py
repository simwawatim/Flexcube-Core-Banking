from flask import Flask, request, Response
import xml.etree.ElementTree as ET

app = Flask(__name__)


def get_text(root, tag):
    """
    Find an element by local tag name, ignoring namespace.
    """
    for elem in root.iter():
        if elem.tag.endswith(tag):
            return elem.text.strip() if elem.text else None
    return None


def soap_wrap(body_xml):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
   <S:Body>
      {body_xml}
   </S:Body>
</S:Envelope>"""


@app.route("/FCUBSCustomerService/FCUBSCustomerService", methods=["POST"])
def create_customer():
    try:
        xml_data = request.data.decode("utf-8")
        print("\n===== CUSTOMER REQUEST =====")
        print(xml_data)

        root = ET.fromstring(xml_data)

        msgid = get_text(root, "MSGID")
        correlid = get_text(root, "CORRELID")
        userid = get_text(root, "USERID")
        branch = get_text(root, "BRANCH")
        service = get_text(root, "SERVICE")
        operation = get_text(root, "OPERATION")

        name = get_text(root, "NAME")
        fullname = get_text(root, "FULLNAME")
        country = get_text(root, "COUNTRY")

        # Mock generated CIF
        custno = "0199001"

        body = f"""
<CREATECUSTOMER_FSFS_RES xmlns="http://fcubs.ofss.com/service/FCUBSCustomerService">
   <FCUBS_HEADER>
      <SOURCE>FLEXCUBE</SOURCE>
      <UBSCOMP>FCUBS</UBSCOMP>
      <MSGID>{msgid}</MSGID>
      <CORRELID>{correlid}</CORRELID>
      <USERID>{userid}</USERID>
      <BRANCH>{branch}</BRANCH>
      <SERVICE>{service}</SERVICE>
      <OPERATION>{operation}</OPERATION>
      <MSGSTAT>SUCCESS</MSGSTAT>
   </FCUBS_HEADER>

   <FCUBS_BODY>
      <Customer-Full>
         <CUSTNO>{custno}</CUSTNO>
         <NAME>{name}</NAME>
         <FULLNAME>{fullname}</FULLNAME>
         <COUNTRY>{country}</COUNTRY>
      </Customer-Full>

      <FCUBS_WARNING_RESP>
         <WARNING>
            <WCODE>ST-SAVE-002</WCODE>
            <WDESC>Customer Created Successfully</WDESC>
         </WARNING>
      </FCUBS_WARNING_RESP>
   </FCUBS_BODY>
</CREATECUSTOMER_FSFS_RES>
"""

        return Response(soap_wrap(body), mimetype="text/xml")

    except Exception as e:
        return Response(
            soap_wrap(
                f"""
<ERROR_RESPONSE>
    <MESSAGE>{str(e)}</MESSAGE>
</ERROR_RESPONSE>
"""
            ),
            status=500,
            mimetype="text/xml",
        )


@app.route("/FCUBSAccService/FCUBSAccService", methods=["POST"])
def create_account():
    try:
        xml_data = request.data.decode("utf-8")
        print("\n===== ACCOUNT REQUEST =====")
        print(xml_data)

        root = ET.fromstring(xml_data)

        msgid = get_text(root, "MSGID")
        correlid = get_text(root, "CORRELID")
        userid = get_text(root, "USERID")
        branch = get_text(root, "BRANCH")
        service = get_text(root, "SERVICE")
        operation = get_text(root, "OPERATION")

        acc = get_text(root, "ACC")
        custno = get_text(root, "CUSTNO")
        ccy = get_text(root, "CCY") or "ZMW"
        loc = get_text(root, "LOC") or "ZAMBIA"

        print(f"MSGID: {msgid}")
        print(f"CUSTNO: {custno}")
        print(f"ACC: {acc}")

        body = f"""
<CREATECUSTACC_FSFS_RES xmlns="http://fcubs.ofss.com/service/FCUBSAccService">
   <FCUBS_HEADER>
      <SOURCE>FLEXCUBE</SOURCE>
      <UBSCOMP>FCUBS</UBSCOMP>
      <MSGID>{msgid}</MSGID>
      <CORRELID>{correlid}</CORRELID>
      <USERID>{userid}</USERID>
      <BRANCH>{branch}</BRANCH>
      <SERVICE>{service}</SERVICE>
      <OPERATION>{operation}</OPERATION>
      <MSGSTAT>SUCCESS</MSGSTAT>
   </FCUBS_HEADER>

   <FCUBS_BODY>
      <Cust-Account-Full>
         <BRN>{branch}</BRN>
         <ACC>{acc}</ACC>
         <CUSTNO>{custno}</CUSTNO>
         <CCY>{ccy}</CCY>
         <LOC>{loc}</LOC>
      </Cust-Account-Full>

      <FCUBS_WARNING_RESP>
         <WARNING>
            <WCODE>ST-SAVE-002</WCODE>
            <WDESC>Account Created Successfully</WDESC>
         </WARNING>
      </FCUBS_WARNING_RESP>
   </FCUBS_BODY>
</CREATECUSTACC_FSFS_RES>
"""

        return Response(soap_wrap(body), mimetype="text/xml")

    except Exception as e:
        return Response(
            soap_wrap(
                f"""
<ERROR_RESPONSE>
    <MESSAGE>{str(e)}</MESSAGE>
</ERROR_RESPONSE>
"""
            ),
            status=500,
            mimetype="text/xml",
        )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9532,
        debug=True,
    )