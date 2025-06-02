import requests
import xml.etree.ElementTree as ET

URL = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx"

def emitir_factura(datos, ta):
    # Paso 1: obtener último comprobante autorizado
    ultimo_req = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <FECompUltimoAutorizado xmlns="http://ar.gov.afip.dif.FEV1/">
          <Auth>
            <Token>{ta['token']}</Token>
            <Sign>{ta['sign']}</Sign>
            <Cuit>{datos['cuit']}</Cuit>
          </Auth>
          <PtoVta>{datos['puntoVenta']}</PtoVta>
          <CbteTipo>{datos['tipo_cbte']}</CbteTipo>
        </FECompUltimoAutorizado>
      </soap:Body>
    </soap:Envelope>
    """

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://ar.gov.afip.dif.FEV1/FECompUltimoAutorizado"
    }

    resp_ultimo = requests.post(URL, data=ultimo_req.encode("utf-8"), headers=headers)
    resp_ultimo.raise_for_status()

    tree = ET.fromstring(resp_ultimo.text)
    cbte_nro = int(tree.find('.//CbteNro').text) + 1

    # Paso 2: emitir nuevo comprobante
    soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <FECAESolicitar xmlns="http://ar.gov.afip.dif.FEV1/">
          <Auth>
            <Token>{ta['token']}</Token>
            <Sign>{ta['sign']}</Sign>
            <Cuit>{datos['cuit']}</Cuit>
          </Auth>
          <FeCAEReq>
            <FeCabReq>
              <CantReg>1</CantReg>
              <PtoVta>{datos['puntoVenta']}</PtoVta>
              <CbteTipo>{datos['tipo_cbte']}</CbteTipo>
            </FeCabReq>
            <FeDetReq>
              <FECAEDetRequest>
                <Concepto>{datos['concepto']}</Concepto>
                <DocTipo>{datos['docTipo']}</DocTipo>
                <DocNro>{datos['docNro']}</DocNro>
                <CbteDesde>{cbte_nro}</CbteDesde>
                <CbteHasta>{cbte_nro}</CbteHasta>
                <CbteFch>{datos['cbteFch']}</CbteFch>
                <ImpTotal>{datos['impTotal']}</ImpTotal>
                <ImpNeto>{datos['impTotal']}</ImpNeto>
                <ImpIVA>{datos.get('impIVA', 0)}</ImpIVA>
                <MonId>{datos.get('moneda', 'PES')}</MonId>
                <MonCotiz>1.00</MonCotiz>
                <FchServDesde>{datos['fchServDesde']}</FchServDesde>
                <FchServHasta>{datos['fchServHasta']}</FchServHasta>
                <FchVtoPago>{datos['fchVtoPago']}</FchVtoPago>
              </FECAEDetRequest>
            </FeDetReq>
          </FeCAEReq>
        </FECAESolicitar>
      </soap:Body>
    </soap:Envelope>
    """

    headers["SOAPAction"] = "http://ar.gov.afip.dif.FEV1/FECAESolicitar"
    resp_emitir = requests.post(URL, data=soap_body.encode("utf-8"), headers=headers)
    resp_emitir.raise_for_status()

    tree = ET.fromstring(resp_emitir.text)
    cae = tree.find('.//CAE').text
    vto_cae = tree.find('.//CAEFchVto').text

    return {
        "cae": cae,
        "vtoCae": vto_cae,
        "cbte_nro": cbte_nro,
        "fecha_emision": datos["cbteFch"],
        "vencimiento_factura": datos["fchVtoPago"],
        "pdf": f"https://fakepdf.afip.gob.ar/factura/{cae}.pdf"  # ← Esto se reemplazará por PDF real en Drive
    }
