import requests
import xml.etree.ElementTree as ET

WSDL = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
URL = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx"

def emitir_factura(datos, ta):
    # Simulación del número de comprobante a emitir
    cbte_nro = 1

    # Armar el encabezado SOAP para el request a WSFEv1
    soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Header>
    <wsse:Security soap:mustUnderstand="1" xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/12/secext">
    </wsse:Security>
  </soap:Header>
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
          <PtoVta>{datos['punto_venta']}</PtoVta>
          <CbteTipo>{datos.get('tipo_cbte', 11)}</CbteTipo>
        </FeCabReq>
        <FeDetReq>
          <FECAEDetRequest>
            <Concepto>{datos.get('concepto', 3)}</Concepto>
            <DocTipo>{datos.get('docTipo', 80)}</DocTipo>
            <DocNro>{datos['cuit']}</DocNro>
            <CbteDesde>{cbte_nro}</CbteDesde>
            <CbteHasta>{cbte_nro}</CbteHasta>
            <CbteFch>{datos['cbteFch']}</CbteFch>
            <ImpTotal>{datos['impTotal']}</ImpTotal>
            <ImpTotConc>0.00</ImpTotConc>
            <ImpNeto>{datos['impTotal']}</ImpNeto>
            <ImpOpEx>0.00</ImpOpEx>
            <ImpIVA>{datos.get('impIVA', 0)}</ImpIVA>
            <ImpTrib>0.00</ImpTrib>
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

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://ar.gov.afip.dif.FEV1/FECAESolicitar"
    }

    response = requests.post(URL, data=soap_body.encode("utf-8"), headers=headers)
    response.raise_for_status()

    # Parsear respuesta SOAP
    tree = ET.fromstring(response.text)
    cae = tree.find('.//CAE').text
    vto_cae = tree.find('.//CAEFchVto').text

    return {
        "cae": cae,
        "vtoCae": vto_cae,
        "fecha_emision": datos["cbteFch"],
        "pdf": f"https://fakepdf.afip.gob.ar/factura/{cae}.pdf",
        "vencimiento_factura": datos["fchVtoPago"]
    }
