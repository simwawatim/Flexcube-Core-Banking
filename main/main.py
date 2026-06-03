from flask import Flask, request, Response
import xml.etree.ElementTree as ET
from datetime import date, datetime

app = Flask(__name__)


def get_text(root, tag):

    for elem in root.iter():
        if elem.tag.endswith(tag):
            return elem.text.strip() if elem.text else None
    return None


def get_all(root, tag):
    """Find all elements by local tag name, ignoring namespace."""
    return [elem for elem in root.iter() if elem.tag.endswith(tag)]


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
        print("\n===== CUSTOMER (CIF) REQUEST =====")
        print(xml_data)

        root = ET.fromstring(xml_data)
        msgid = get_text(root,"MSGID")     or "0"
        correlid = get_text(root, "CORRELID")  or "0"
        userid = get_text(root, "USERID")    or "BANKON"
        branch = get_text(root, "BRANCH")    or "001"
        service  = get_text(root, "SERVICE")   or "FCUBSCustomerService"
        operation = get_text(root, "OPERATION") or "CreateCustomer"
        ctype = get_text(root, "CTYPE")      or "I"
        name = get_text(root, "NAME")       or ""
        fullname = get_text(root, "FULLNAME")   or ""
        addrln1 = get_text(root, "ADDRLN1")    or ""
        addrln2 = get_text(root, "ADDRLN2")    or ""
        addrln3 = get_text(root, "ADDRLN3")    or ""
        addrln4 = get_text(root, "ADDRLN4")    or ""
        country = get_text(root, "COUNTRY")    or "ZM"
        nlty = get_text(root, "NLTY")       or "ZM"
        sname = get_text(root, "SNAME")      or ""
        uidname = get_text(root, "UIDNAME")    or "NRC"
        uidval = get_text(root, "UIDVAL")     or ""
        lbrn = get_text(root, "LBRN")       or branch
        ccateg = get_text(root, "CCATEG")     or "INDIVIDUAL"
        iselcmcust = get_text(root, "ISELCMCUST") or "Y"
        expcntry = get_text(root, "EXPCNTRY")   or "ZM"
        frozen  = get_text(root, "FROZEN")     or "N"
        dead = get_text(root, "DEAD")       or "N"
        whrunkn = get_text(root, "WHRUNKN")    or "N"
        media = get_text(root, "MEDIA")      or "MAIL"
        loc = get_text(root, "LOC")        or "ZM"
        track_limits = get_text(root, "TRACK_LIMITS") or "Y"
        sstaff = get_text(root, "SSTAFF")     or "N"
        taxidentity = get_text(root, "TAXIDENTITY") or ""
        fstname = get_text(root, "FSTNAME")     or ""
        lstname = get_text(root, "LSTNAME")     or ""
        dob = get_text(root, "DOB")         or ""
        gendr = get_text(root, "GENDR")       or "M"
        nationid = get_text(root, "NATIONID")    or ""
        emailid = get_text(root, "EMAILID")     or ""
        benefaddr1 = get_text(root, "BENEFADDR1")  or addrln1
        benefaddr2 = get_text(root, "BENEFADDR2")  or addrln2
        addrs3 = get_text(root, "ADDRS3")      or addrln3
        dcntry = get_text(root, "DCNTRY")      or "ZM"
        pcntry = get_text(root, "PCNTRY")      or "ZM"
        resstatus = get_text(root, "RESSTATUS")   or "R"
        mobnum = get_text(root, "MOBNUM")      or ""
        mobisdno = get_text(root, "MOBISDNO")    or "260"
        comm_mode = get_text(root, "CUST_COMM_MODE") or "M"
        lang = get_text(root, "LANG")        or "ENG"
        minor = get_text(root, "MINOR")       or "N"
        title = get_text(root, "TITLE")       or "MR"
        placeofbirth = get_text(root, "PLACEOFBIRTH")  or ""
        birthcountry = get_text(root, "BIRTHCOUNTRY")  or "ZM"
        edustat = get_text(root, "EDUSTAT")       or "G"
        maritalstat = get_text(root, "MARITALSTAT")   or "M"
        empstat = get_text(root, "EMPSTAT")       or "F"

        mis_blocks = ""
        mis_elems = [e for e in root.iter() if e.tag.endswith("Customermis")]
        for mis in mis_elems:
            miscls = ""
            miscd  = ""
            for child in mis:
                local = child.tag.split("}")[-1]
                if local == "MISCLS":
                    miscls = child.text.strip() if child.text else ""
                elif local == "MISCD":
                    miscd = child.text.strip() if child.text else ""
            mis_blocks += f"""
                  <Customermis>
                     <MISCLS>{miscls}</MISCLS>
                     <MISCD>{miscd}</MISCD>
                  </Customermis>"""


        custno = "0199537"

        today      = date.today().isoformat()
        now_stamp  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        body = f"""
            <CREATECUSTOMER_FSFS_RES xmlns="http://fcubs.ofss.com/service/FCUBSCustomerService">
               <FCUBS_HEADER>
                  <SOURCE>FLEXCUBE</SOURCE>
                  <UBSCOMP>FCUBS</UBSCOMP>
                  <MSGID>{msgid}</MSGID>
                  <CORRELID>{correlid}</CORRELID>
                  <USERID>{userid}</USERID>
                  <ENTITY>null</ENTITY>
                  <BRANCH>{branch}</BRANCH>
                  <MODULEID>ST</MODULEID>
                  <SERVICE>{service}</SERVICE>
                  <OPERATION>{operation}</OPERATION>
                  <DESTINATION>{userid}</DESTINATION>
                  <FUNCTIONID>STDCIF</FUNCTIONID>
                  <ACTION>NEW</ACTION>
                  <MSGSTAT>SUCCESS</MSGSTAT>
               </FCUBS_HEADER>
               <FCUBS_BODY>
                  <Customer-Full>
                     <CUSTNO>{custno}</CUSTNO>
                     <CTYPE>{ctype}</CTYPE>
                     <NAME>{name}</NAME>
                     <ADDRLN1>{addrln1}</ADDRLN1>
                     <ADDRLN2>{addrln2}</ADDRLN2>
                     <ADDRLN3>{addrln3}</ADDRLN3>
                     <ADDRLN4>{addrln4}</ADDRLN4>
                     <COUNTRY>{country}</COUNTRY>
                     <SNAME>{sname}</SNAME>
                     <NLTY>{nlty}</NLTY>
                     <LBRN>{lbrn}</LBRN>
                     <CCATEG>{ccateg}</CCATEG>
                     <FULLNAME>{fullname}</FULLNAME>
                     <CIFCREATIONDT>{today}</CIFCREATIONDT>
                     <ISELCMCUST>{iselcmcust}</ISELCMCUST>
                     <AR_AP_TRACKING>N</AR_AP_TRACKING>
                     <EXPCNTRY>{expcntry}</EXPCNTRY>
                     <UIDNAME>{uidname}</UIDNAME>
                     <UIDVAL>{uidval}</UIDVAL>
                     <FROZEN>{frozen}</FROZEN>
                     <DEAD>{dead}</DEAD>
                     <WHRUNKN>{whrunkn}</WHRUNKN>
                     <MEDIA>{media}</MEDIA>
                     <LOC>{loc}</LOC>
                     <MAILRSREQD>N</MAILRSREQD>
                     <CLSPARTICIPANT>N</CLSPARTICIPANT>
                     <FXNETTCUST>{custno}</FXNETTCUST>
                     <CRMCUST>N</CRMCUST>
                     <ISSUCUST>N</ISSUCUST>
                     <TRSRYCUST>N</TRSRYCUST>
                     <RELPRICING>N</RELPRICING>
                     <MT920_STMT>N</MT920_STMT>
                     <FLGJOINT>N</FLGJOINT>
                     <CREATEACC>N</CREATEACC>
                     <TRACK_LIMITS>{track_limits}</TRACK_LIMITS>
                     <LIABID>{custno}</LIABID>
                     <LMCCY>ZMW</LMCCY>
                     <FLGUTLTYPRVDR>N</FLGUTLTYPRVDR>
                     <AMLREQD>N</AMLREQD>
                     <CHKDIGITVALREQD>N</CHKDIGITVALREQD>
                     <FTACCASOF>M</FTACCASOF>
                     <CUSTUNADV>N</CUSTUNADV>
                     <CONSTAXCERTRQD>N</CONSTAXCERTRQD>
                     <INDTAXCERTRQD>N</INDTAXCERTRQD>
                     <CLSCCYALLWD>D</CLSCCYALLWD>
                     <INVESTCUST>N</INVESTCUST>
                     <ALLOWVRTLACCNTS>N</ALLOWVRTLACCNTS>
                     <SSTAFF>{sstaff}</SSTAFF>
                     <TAXIDENTITY>{taxidentity}</TAXIDENTITY>
                     <SPECIAL_CUST>N</SPECIAL_CUST>
                     <MAKER>{userid}</MAKER>
                     <MAKERSTAMP>{now_stamp}</MAKERSTAMP>
                     <CHECKER>{userid}</CHECKER>
                     <CHECKERSTAMP>{now_stamp}</CHECKERSTAMP>
                     <MODNO>1</MODNO>
                     <TXNSTAT>O</TXNSTAT>
                     <AUTHSTAT>A</AUTHSTAT>
                     <Custpersonal>
                        <FSTNAME>{fstname}</FSTNAME>
                        <LSTNAME>{lstname}</LSTNAME>
                        <DOB>{dob}</DOB>
                        <GENDR>{gendr}</GENDR>
                        <NATIONID>{nationid}</NATIONID>
                        <EMAILID>{emailid}</EMAILID>
                        <BENEFADDR1>{benefaddr1}</BENEFADDR1>
                        <BENEFADDR2>{benefaddr2}</BENEFADDR2>
                        <ADDRS3>{addrs3}</ADDRS3>
                        <DCNTRY>{dcntry}</DCNTRY>
                        <PCNTRY>{pcntry}</PCNTRY>
                        <RESSTATUS>{resstatus}</RESSTATUS>
                        <MOBNUM>{mobnum}</MOBNUM>
                        <MOBISDNO>{mobisdno}</MOBISDNO>
                        <CUST_COMM_MODE>{comm_mode}</CUST_COMM_MODE>
                        <LANG>{lang}</LANG>
                        <SBMTAGEPROOF>N</SBMTAGEPROOF>
                        <MINOR>{minor}</MINOR>
                        <KYCSTAT>N</KYCSTAT>
                        <TITLE>{title}</TITLE>
                        <PLACEOFBIRTH>{placeofbirth}</PLACEOFBIRTH>
                        <BIRTHCOUNTRY>{birthcountry}</BIRTHCOUNTRY>
                        <Custdomestic>
                           <CUSTNO>{custno}</CUSTNO>
                           <EDUSTAT>{edustat}</EDUSTAT>
                           <MARITALSTAT>{maritalstat}</MARITALSTAT>
                        </Custdomestic>
                        <Custprof>
                           <CUSTNO>{custno}</CUSTNO>
                           <EMPSTAT>{empstat}</EMPSTAT>
                        </Custprof>
                     </Custpersonal>
                     <Custcorp/>
                     <Cust-Liab>
                        <LIABILITY_NUMBER>{custno}</LIABILITY_NUMBER>
                        <LIABILTY_NAME>{fullname}</LIABILTY_NAME>
                        <LIAB_BRANCH>{lbrn}</LIAB_BRANCH>
                        <LIAB_CCY>ZMW</LIAB_CCY>
                        <OVERLIMIT>0</OVERLIMIT>
                        <UNADV>N</UNADV>
                        <NETTING_REQUIRED>N</NETTING_REQUIRED>
                        <OVERALL_SCORE>0</OVERALL_SCORE>
                        <UTIL_AMOUNT>0</UTIL_AMOUNT>
                     </Cust-Liab>
                     <Custmis>
                        <CUST>{custno}</CUST>
                        <CUSTNO>{custno}</CUSTNO>
                        <BRNCD>{lbrn}</BRNCD>{mis_blocks}
                        <Customermis>
                           <MISCLS>MINISTRY</MISCLS>
                        </Customermis>
                        <Customermis>
                           <MISCLS>RISK_CAT</MISCLS>
                        </Customermis>
                        <Customermis>
                           <MISCLS>ECONOMIC</MISCLS>
                        </Customermis>
                     </Custmis>
                     <Jointcustomer>
                        <CUSTNO>{custno}</CUSTNO>
                     </Jointcustomer>
                     <Cust-Acc-Det>
                        <CUSTNO>{custno}</CUSTNO>
                     </Cust-Acc-Det>
                     <Custaccdet>
                        <CUSTNO>{custno}</CUSTNO>
                        <Relationship-Linkage>
                           <CUSTOMER>{custno}</CUSTOMER>
                           <RELATIONSHIP>PRIMARY</RELATIONSHIP>
                           <INHERIT>N</INHERIT>
                           <DESCP>{fullname}</DESCP>
                        </Relationship-Linkage>
                        <Reverse-Relationship>
                           <INHERIT>N</INHERIT>
                           <REF_NO>{custno}</REF_NO>
                           <RELATIONSHIP>PRIMARY</RELATIONSHIP>
                           <BRANCH>{lbrn}</BRANCH>
                           <CUSTOMER>{custno}</CUSTOMER>
                           <CATEGORY>C</CATEGORY>
                        </Reverse-Relationship>
                     </Custaccdet>
                     <Custacdetail>
                        <CUSTNO>{custno}</CUSTNO>
                     </Custacdetail>
                     <UDFDETAILS>
                        <FLDNAM>CITY</FLDNAM>
                     </UDFDETAILS>
                     <Master>
                        <KEY_ID>{custno}</KEY_ID>
                        <FUNCTION_ID>STDCIF</FUNCTION_ID>
                     </Master>
                  </Customer-Full>
                  <FCUBS_WARNING_RESP>
                     <WARNING>
                        <WCODE>FT-SSN000</WCODE>
                        <WDESC>SSN Value should be entered</WDESC>
                     </WARNING>
                     <WARNING>
                        <WCODE>ST-SAVE-002</WCODE>
                        <WDESC>Record Successfully Saved and Authorized</WDESC>
                     </WARNING>
                  </FCUBS_WARNING_RESP>
               </FCUBS_BODY>
            </CREATECUSTOMER_FSFS_RES>
            """
        print("\n===== CUSTOMER (CIF) RESPONSE =====")
        print(soap_wrap(body))
        return Response(soap_wrap(body), mimetype="text/xml")

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            soap_wrap(f"""
               <ERROR_RESPONSE>
                  <MESSAGE>{str(e)}</MESSAGE>
               </ERROR_RESPONSE>
               """),
            status=500,
            mimetype="text/xml",
        )


@app.route("/FCUBSAccService/FCUBSAccService", methods=["POST"])
def create_account():
    try:
        xml_data = request.data.decode("utf-8")
        print("\n===== ACCOUNT OPENING REQUEST =====")
        print(xml_data)

        root = ET.fromstring(xml_data)

        msgid = get_text(root, "MSGID")     or "0"
        correlid = get_text(root, "CORRELID")  or "0"
        userid = get_text(root, "USERID")    or "BANKON"
        branch = get_text(root, "BRANCH")    or "002"
        service = get_text(root, "SERVICE")   or "FCUBSAccService"
        operation = get_text(root, "OPERATION") or "CreateCustAcc"
        
        brn = get_text(root, "BRN")         or branch
        acc_req = get_text(root, "ACC")         or ""
        custno = get_text(root, "CUSTNO")      or ""
        accls = get_text(root, "ACCLS")       or "201"
        ccy = get_text(root, "CCY")         or "ZMW"
        adesc = get_text(root, "ADESC")       or ""
        acstatnodr = get_text(root, "ACSTATNODR")  or "N"
        acstatnocr = get_text(root, "ACSTATNOCR")  or "N"
        acstatstpay = get_text(root, "ACSTATSTPAY") or "N"
        frozen = get_text(root, "FROZEN")      or "N"
        loc = get_text(root, "LOC")         or "ZAMBIA"
        media = get_text(root, "MEDIA")       or "MAIL"
        autoprovreq = get_text(root, "AUTOPROVREQ") or "Y"
        country_code = get_text(root, "COUNTRY_CODE") or "ZM"
        salary_account = get_text(root, "SALARY_ACCOUNT") or "N"
        dorm = get_text(root, "DORM")        or "N"
        poolcd = get_text(root, "POOLCD")      or "DFLTPOOL"

        if acc_req and acc_req.isdigit() and len(acc_req) >= 2:
            acc_new = str(int(acc_req) + 5)
        else:
            acc_new = acc_req or "1010000000001"

        prov_acc = acc_req or acc_new

        today     = date.today().isoformat()
        now_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        body = f"""
            <CREATECUSTACC_FSFS_RES xmlns="http://fcubs.ofss.com/service/FCUBSAccService">
               <FCUBS_HEADER>
                  <SOURCE>FLEXCUBE</SOURCE>
                  <UBSCOMP>FCUBS</UBSCOMP>
                  <MSGID>{msgid}</MSGID>
                  <CORRELID>{correlid}</CORRELID>
                  <USERID>{userid}</USERID>
                  <ENTITY>null</ENTITY>
                  <BRANCH>{branch}</BRANCH>
                  <MODULEID>ST</MODULEID>
                  <SERVICE>{service}</SERVICE>
                  <OPERATION>{operation}</OPERATION>
                  <DESTINATION>{userid}</DESTINATION>
                  <FUNCTIONID>STDCUSAC</FUNCTIONID>
                  <ACTION>NEW</ACTION>
                  <MSGSTAT>SUCCESS</MSGSTAT>
               </FCUBS_HEADER>
               <FCUBS_BODY>
                  <Cust-Account-Full>
                     <BRN>{brn}</BRN>
                     <ACC>{acc_new}</ACC>
                     <CUSTNO>{custno}</CUSTNO>
                     <ACCLS>{accls}</ACCLS>
                     <CCY>{ccy}</CCY>
                     <CUSTNAME>{adesc}</CUSTNAME>
                     <ACCLSTYP>U</ACCLSTYP>
                     <ADESC>{adesc}</ADESC>
                     <ACSTATNODR>{acstatnodr}</ACSTATNODR>
                     <ACSTATNOCR>{acstatnocr}</ACSTATNOCR>
                     <ACSTATSTPAY>{acstatstpay}</ACSTATSTPAY>
                     <ACCTYPE>S</ACCTYPE>
                     <ACCOPENDT>{today}</ACCOPENDT>
                     <ALTACC>{acc_new}</ALTACC>
                     <FROZEN>{frozen}</FROZEN>
                     <ADDRESS_1>123</ADDRESS_1>
                     <ADDRESS_2>Lusaka</ADDRESS_2>
                     <ADDRESS_3>KASAMA ROAD</ADDRESS_3>
                     <ADDRESS_4>LUSAK_PRV</ADDRESS_4>
                     <POSTALLOWED>Y</POSTALLOWED>
                     <CLRACNO>{acc_new}</CLRACNO>
                     <TRKREC>Y</TRKREC>
                     <REFREQ>N</REFREQ>
                     <ACCSTAT>NORM</ACCSTAT>
                     <STATSINCE>{today}</STATSINCE>
                     <INHERITREP>N</INHERITREP>
                     <AUTOSTATCHANGE>Y</AUTOSTATCHANGE>
                     <DORMPRM>M</DORMPRM>
                     <LOC>{loc}</LOC>
                     <MEDIA>{media}</MEDIA>
                     <CHQBOOK>Y</CHQBOOK>
                     <PASSBOOK>N</PASSBOOK>
                     <CASACC>N</CASACC>
                     <MT210REQD>N</MT210REQD>
                     <AUTOREORDERCHKREQ>N</AUTOREORDERCHKREQ>
                     <LODGEBKFAC>N</LODGEBKFAC>
                     <ALLWBKPERENTRY>Y</ALLWBKPERENTRY>
                     <AUTOPROVREQ>{autoprovreq}</AUTOPROVREQ>
                     <EXPCATEG>GENERAL</EXPCATEG>
                     <PROVCCYTYPE>A</PROVCCYTYPE>
                     <DEFRECON>N</DEFRECON>
                     <CONSREQD>N</CONSREQD>
                     <FUNDING>N</FUNDING>
                     <ATMBRN>{brn}</ATMBRN>
                     <ACSTMTDAY>31</ACSTMTDAY>
                     <ACSTMTCYCLE>M</ACSTMTCYCLE>
                     <ATM>Y</ATM>
                     <ACSTMTTYPEP>D</ACSTMTTYPEP>
                     <DISPIBANINADV>N</DISPIBANINADV>
                     <ACSTMTTYPS>N</ACSTMTTYPS>
                     <ACSTMTTYPE3>N</ACSTMTTYPE3>
                     <FLGEXCLRVRTRANS>Y</FLGEXCLRVRTRANS>
                     <SWPTYPE>1</SWPTYPE>
                     <REGDAPP>N</REGDAPP>
                     <REGDPER>N</REGDPER>
                     <PRDLST>D</PRDLST>
                     <TXNLST>D</TXNLST>
                     <SPCONDLST>N</SPCONDLST>
                     <SPCONDTXN>N</SPCONDTXN>
                     <ODREQ>Y</ODREQ>
                     <DAYLIGHTLIMIT>0</DAYLIGHTLIMIT>
                     <WAIVE_ACC_OPEN_CHARGE>N</WAIVE_ACC_OPEN_CHARGE>
                     <COUNTRY_CODE>{country_code}</COUNTRY_CODE>
                     <ESCROWTRN>N</ESCROWTRN>
                     <SALARY_ACCOUNT>{salary_account}</SALARY_ACCOUNT>
                     <REPL_CUST_SIG>N</REPL_CUST_SIG>
                     <ACCOUNTAUTOCLOSED>N</ACCOUNTAUTOCLOSED>
                     <CRS_STST_REQD>N</CRS_STST_REQD>
                     <PROJACC>N</PROJACC>
                     <PRIVATE_CUSTOMER>N</PRIVATE_CUSTOMER>
                     <LIMIT_AUTO_CREATE_POOL>N</LIMIT_AUTO_CREATE_POOL>
                     <DFLT_WAIVER>N</DFLT_WAIVER>
                     <AUTO_DEBIT_CARD_REQUEST>N</AUTO_DEBIT_CARD_REQUEST>
                     <AUTO_CHEQUE_BOOK_REQ>N</AUTO_CHEQUE_BOOK_REQ>
                     <INTERMEDIARY_REQUIRED>N</INTERMEDIARY_REQUIRED>
                     <ENABLE_SWEEP_IN>N</ENABLE_SWEEP_IN>
                     <ENABLE_REV_SWEEP_IN>N</ENABLE_REV_SWEEP_IN>
                     <SPDANLSYS>N</SPDANLSYS>
                     <IBANREQURED>N</IBANREQURED>
                     <DIRECT_BANKING>Y</DIRECT_BANKING>
                     <DROVD>N</DROVD>
                     <CROVD>N</CROVD>
                     <SPL_AC_GEN>N</SPL_AC_GEN>
                     <DORM>{dorm}</DORM>
                     <MAKER>{userid}</MAKER>
                     <MAKERSTAMP>{now_stamp}</MAKERSTAMP>
                     <CHECKER>{userid}</CHECKER>
                     <CHECKERSTAMP>{now_stamp}</CHECKERSTAMP>
                     <MODNO>1</MODNO>
                     <TXNSTAT>O</TXNSTAT>
                     <AUTHSTAT>A</AUTHSTAT>
                     <Provision-Main>
                        <PRVACCUI>{prov_acc}</PRVACCUI>
                     </Provision-Main>
                     <Provdetails>
                        <PRVSTATUS>NORM</PRVSTATUS>
                        <PRVPC>0</PRVPC>
                        <DISCPC>0</DISCPC>
                     </Provdetails>
                     <Accmaintinstr>
                        <BRN>{brn}</BRN>
                        <ACC>{acc_new}</ACC>
                        <DTOFLSTMAINT>{today}</DTOFLSTMAINT>
                     </Accmaintinstr>
                     <Multi-Account-Generation/>
                     <Interim-Details>
                        <GENINTRMSTMT>N</GENINTRMSTMT>
                        <GENINTRMSTMTMVMT>N</GENINTRMSTMTMVMT>
                        <GENBALRPT>N</GENBALRPT>
                        <BALRPTSINCE>950</BALRPTSINCE>
                     </Interim-Details>
                     <Acstatuslines>
                        <ACSTATUS>DFLC</ACSTATUS>
                        <DRHOLINE>HO0000001</DRHOLINE>
                        <CRHOLINE>HO0000001</CRHOLINE>
                        <CRCBLINE>CB0000001</CRCBLINE>
                        <DRCBLINE>CB0000001</DRCBLINE>
                        <DRGL>121010103</DRGL>
                        <CRGL>202010101</CRGL>
                        <DESC>Defaulting Customers - 90 to 119</DESC>
                     </Acstatuslines>
                     <Acstatuslines>
                        <ACSTATUS>IMPR</ACSTATUS>
                        <DRHOLINE>HO0000001</DRHOLINE>
                        <CRHOLINE>HO0000001</CRHOLINE>
                        <CRCBLINE>CB0000001</CRCBLINE>
                        <DRCBLINE>CB0000001</DRCBLINE>
                        <DRGL>121010103</DRGL>
                        <CRGL>202010101</CRGL>
                        <DESC>Impairments - 120 to 179</DESC>
                     </Acstatuslines>
                     <Acstatuslines>
                        <ACSTATUS>NORM</ACSTATUS>
                        <DRHOLINE>HO0000001</DRHOLINE>
                        <CRHOLINE>HO0000001</CRHOLINE>
                        <CRCBLINE>CB0000001</CRCBLINE>
                        <DRCBLINE>CB0000001</DRCBLINE>
                        <DRGL>202010101</DRGL>
                        <CRGL>202010101</CRGL>
                        <DESC>NORMAL STATUS</DESC>
                     </Acstatuslines>
                     <Acstatuslines>
                        <ACSTATUS>WRTF</ACSTATUS>
                        <DRHOLINE>HO0000001</DRHOLINE>
                        <CRHOLINE>HO0000001</CRHOLINE>
                        <CRCBLINE>CB0000001</CRCBLINE>
                        <DRCBLINE>CB0000001</DRCBLINE>
                        <DRGL>121010103</DRGL>
                        <CRGL>202010101</CRGL>
                        <DESC>Write Off - 180+</DESC>
                     </Acstatuslines>
                     <Intdetails>
                        <CALCACC>{acc_new}</CALCACC>
                        <BOOKACC>{acc_new}</BOOKACC>
                        <HASIS>N</HASIS>
                        <INTSTARTDT>{today}</INTSTARTDT>
                        <BOOKACCBRN>{brn}</BOOKACCBRN>
                        <DRCRADV>Y</DRCRADV>
                        <CHGBOOKACCBRN>{brn}</CHGBOOKACCBRN>
                        <CHGBOOKACC>{acc_new}</CHGBOOKACC>
                        <CHGSTARTDT>{today}</CHGSTARTDT>
                        <BRN>{brn}</BRN>
                        <ACC>{acc_new}</ACC>
                        <CONSOLCHGBRN>{brn}</CONSOLCHGBRN>
                     </Intdetails>
                     <Tddetails>
                        <AUTOROLL>N</AUTOROLL>
                        <CLONMAT>N</CLONMAT>
                        <MOVINTUNCLM>N</MOVINTUNCLM>
                        <ROLLTYPE>P</ROLLTYPE>
                        <MOVPRIUNCLM>N</MOVPRIUNCLM>
                        <INTSTDT>{today}</INTSTDT>
                     </Tddetails>
                     <Amount-Dates>
                        <LCY>ZMW</LCY>
                        <ACY>ZMW</ACY>
                        <DR_INT_DUE>0</DR_INT_DUE>
                        <PROVAMT>0</PROVAMT>
                        <CHG_DUE>0</CHG_DUE>
                        <WITHDRAWABLE_UNCOLLED_FUND>0</WITHDRAWABLE_UNCOLLED_FUND>
                        <ACY_OPENING_BAL>0</ACY_OPENING_BAL>
                        <LCY_OPENING_BAL>0</LCY_OPENING_BAL>
                        <ACY_TODAY_TOVER_DR>0</ACY_TODAY_TOVER_DR>
                        <LCY_TODAY_TOVER_DR>0</LCY_TODAY_TOVER_DR>
                        <ACY_TODAY_TOVER_CR>0</ACY_TODAY_TOVER_CR>
                        <LCY_TODAY_TOVER_CR>0</LCY_TODAY_TOVER_CR>
                        <ACY_TANK_CR>0</ACY_TANK_CR>
                        <ACY_TANK_DR>0</ACY_TANK_DR>
                        <LCY_TANK_CR>0</LCY_TANK_CR>
                        <LCY_TANK_DR>0</LCY_TANK_DR>
                        <ACY_TANK_UNCOLLECTED>0</ACY_TANK_UNCOLLECTED>
                        <ACY_CURR_BALANCE>0</ACY_CURR_BALANCE>
                        <LCY_CURR_BALANCE>0</LCY_CURR_BALANCE>
                        <ACY_BLOCKED_AMOUNT>0</ACY_BLOCKED_AMOUNT>
                        <ACY_AVL_BAL>0</ACY_AVL_BAL>
                        <ACY_UNAUTH_DR>0</ACY_UNAUTH_DR>
                        <ACY_UNAUTH_TANK_DR>0</ACY_UNAUTH_TANK_DR>
                        <ACY_UNAUTH_CR>0</ACY_UNAUTH_CR>
                        <ACY_UNAUTH_TANK_CR>0</ACY_UNAUTH_TANK_CR>
                        <ACY_UNAUTH_UNCOLLECTED>0</ACY_UNAUTH_UNCOLLECTED>
                        <ACY_UNAUTH_TANK_UNCOLLECTED>0</ACY_UNAUTH_TANK_UNCOLLECTED>
                        <ACY_ACCRUED_DR_IC>0</ACY_ACCRUED_DR_IC>
                        <ACY_ACCRUED_CR_IC>0</ACY_ACCRUED_CR_IC>
                        <ACY_UNCOLLECTED>0</ACY_UNCOLLECTED>
                        <AMTAVL>0</AMTAVL>
                        <DIS_UNUTILIZED_AMT>0</DIS_UNUTILIZED_AMT>
                        <DIS_TOT_AVL_AMOUNT>0</DIS_TOT_AVL_AMOUNT>
                        <ACY_UNAUTH>ZMW</ACY_UNAUTH>
                        <UTILIZED_AMT>0</UTILIZED_AMT>
                        <LIMIT_AMOUNT>0</LIMIT_AMOUNT>
                        <ILM_SWEEP_BAL>0</ILM_SWEEP_BAL>
                        <SWEEP_ELIG_BAL>0</SWEEP_ELIG_BAL>
                        <PRINC_OUTSTAND>0</PRINC_OUTSTAND>
                        <INT_OUTSTAND>0</INT_OUTSTAND>
                        <CHG_OUTSTAND>0</CHG_OUTSTAND>
                        <AMTDUE>0</AMTDUE>
                        <Turnovers>
                           <ACY_MTD_TOVER_DR>0</ACY_MTD_TOVER_DR>
                           <LCY_MTD_TOVER_DR>0</LCY_MTD_TOVER_DR>
                           <ACY_MTD_TOVER_CR>0</ACY_MTD_TOVER_CR>
                           <LCY_MTD_TOVER_CR>0</LCY_MTD_TOVER_CR>
                           <ACY_TOV>ZMW</ACY_TOV>
                           <LCY_TOV>ZMW</LCY_TOV>
                        </Turnovers>
                     </Amount-Dates>
                     <Noticepref>
                        <BRN>{brn}</BRN>
                        <ACC>{acc_new}</ACC>
                        <ADVINTREQD>N</ADVINTREQD>
                     </Noticepref>
                     <Tod-Renew>
                        <RNW_FLG>N</RNW_FLG>
                     </Tod-Renew>
                     <Doctype-Remarks>
                        <BRANCH_CODE>{brn}</BRANCH_CODE>
                        <CUST_AC_NO>{acc_new}</CUST_AC_NO>
                     </Doctype-Remarks>
                     <Cust-Acc-Check/>
                     <Summary>
                        <PASSBOOK>N</PASSBOOK>
                        <CHQBOOK>Y</CHQBOOK>
                        <ACCLS>{accls}</ACCLS>
                        <ATM>Y</ATM>
                        <ACSTATNODR>{acstatnodr}</ACSTATNODR>
                        <ACC>{acc_new}</ACC>
                        <ACSTATNOCR>{acstatnocr}</ACSTATNOCR>
                        <ACCLSTYP>U</ACCLSTYP>
                        <PROJECTACCNT>N</PROJECTACCNT>
                        <DORM>{dorm}</DORM>
                        <FROZEN>{frozen}</FROZEN>
                        <ALTACC>{acc_new}</ALTACC>
                        <ACCOPENDT>{today}</ACCOPENDT>
                        <ACSTATSTPAY>{acstatstpay}</ACSTATSTPAY>
                        <CCY>{ccy}</CCY>
                        <CUSTNO>{custno}</CUSTNO>
                        <ADESC>{adesc}</ADESC>
                        <BRN>{brn}</BRN>
                     </Summary>
                     <Custacc>
                        <BRN>{brn}</BRN>
                        <CUSTACNO>{acc_new}</CUSTACNO>
                        <LinkedEntities>
                           <CUSTOMER>{custno}</CUSTOMER>
                           <RELATIONSHIP>PRIMARY</RELATIONSHIP>
                           <INHERIT>N</INHERIT>
                           <CUSTNAME>{adesc}</CUSTNAME>
                        </LinkedEntities>
                     </Custacc>
                     <Custacc-Icccspcn>
                        <BRNCD>{brn}</BRNCD>
                        <ACCNO>{acc_new}</ACCNO>
                     </Custacc-Icccspcn>
                     <Custacc-Icchspcn>
                        <BRN>{brn}</BRN>
                        <ACC>{acc_new}</ACC>
                     </Custacc-Icchspcn>
                     <Custacc-Iccinstr>
                        <BRN>{brn}</BRN>
                        <ACC>{acc_new}</ACC>
                        <Autodepdetails>
                           <ACCCCY>{ccy}</ACCCCY>
                           <CUSTOMER>{custno}</CUSTOMER>
                           <SEQNO>1</SEQNO>
                        </Autodepdetails>
                     </Custacc-Iccinstr>
                     <CustAcc>
                        <BRN>{brn}</BRN>
                        <ACC>{acc_new}</ACC>
                        <Misdetails>
                           <POOLCD>{poolcd}</POOLCD>
                           <REFRTTYPE>X</REFRTTYPE>
                           <CALCMETH>1</CALCMETH>
                           <RTFLAG>P</RTFLAG>
                        </Misdetails>
                     </CustAcc>
                     <Custacc-Sicdiary>
                        <BRNCD>{brn}</BRNCD>
                        <ACCNO>{acc_new}</ACCNO>
                     </Custacc-Sicdiary>
                     <Custacc-Stccusbl>
                        <BRN>{brn}</BRN>
                        <ACCNO>{acc_new}</ACCNO>
                     </Custacc-Stccusbl>
                     <UDFDETAILS>
                        <FLDNAM>REL_MAN_01</FLDNAM>
                     </UDFDETAILS>
                     <UDFDETAILS>
                        <FLDNAM>GRZ_ACCOUNT_CATEGORY</FLDNAM>
                     </UDFDETAILS>
                     <Acc-Svcacsig>
                        <ACBRN1>{brn}</ACBRN1>
                        <ACTNO>{acc_new}</ACTNO>
                        <ACDESC>{adesc}</ACDESC>
                        <ACCCY>{ccy}</ACCCY>
                     </Acc-Svcacsig>
                     <Custacc-Iccintpo>
                        <BRANCH_CODE>{brn}</BRANCH_CODE>
                        <CUST_AC_NO>{acc_new}</CUST_AC_NO>
                        <CCY>{ccy}</CCY>
                     </Custacc-Iccintpo>
                     <Customer-Acc>
                        <BRANCH_CODE>{brn}</BRANCH_CODE>
                        <CUST_AC_NO>{acc_new}</CUST_AC_NO>
                     </Customer-Acc>
                     <Master>
                        <KEY_ID>{brn}:{acc_new}</KEY_ID>
                        <FUNCTION_ID>STDCUSAC</FUNCTION_ID>
                     </Master>
                     <Sttms-Cust-Acc-Swp>
                        <BRANCH_CODE>{brn}</BRANCH_CODE>
                        <CUST_AC_NO>{acc_new}</CUST_AC_NO>
                     </Sttms-Cust-Acc-Swp>
                     <Acc-Chnl>
                        <BRANCH_CODE>{brn}</BRANCH_CODE>
                        <CUST_AC_NO>{acc_new}</CUST_AC_NO>
                     </Acc-Chnl>
                  </Cust-Account-Full>
                  <FCUBS_WARNING_RESP>
                     <WARNING>
                        <WCODE>ST-SAVE-002</WCODE>
                        <WDESC>Record Successfully Saved and Authorized</WDESC>
                     </WARNING>
                  </FCUBS_WARNING_RESP>
               </FCUBS_BODY>
            </CREATECUSTACC_FSFS_RES>
            """
        print(soap_wrap(body))
        return Response(soap_wrap(body), mimetype="text/xml")

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            soap_wrap(f"""
               <ERROR_RESPONSE>
                  <MESSAGE>{str(e)}</MESSAGE>
               </ERROR_RESPONSE>
               """),
            status=500,
            mimetype="text/xml",
        )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9532,
        debug=True,
    )