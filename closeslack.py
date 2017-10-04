import requests
import json
import os


def close(id,resolution):
    r=" "
    url = "https://YOURDOMAIN.custhelp.com/services/rest/connect/v1.3/incidents?q=lookupName='"+id+"'"
    r=requests.get(url,auth=('USER', 'PASSWORD')).text
    rAsJSON=json.loads(r)
    

    payload1 = """
<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Header>
<h:ClientInfoHeader xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:messages.ws.rightnow.com/v1_3" xmlns:h="urn:messages.ws.rightnow.com/v1_3">
<AppID>Basic Update</AppID>
</h:ClientInfoHeader>
<o:Security xmlns:o="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" s:mustUnderstand="1">
<o:UsernameToken>
<o:Username>USER</o:Username>
<o:Password>PASSWORD</o:Password>
</o:UsernameToken>
</o:Security>
</s:Header>
<s:Body xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<Update xmlns="urn:messages.ws.rightnow.com/v1_3">
<RNObjects xmlns:q1="urn:objects.ws.rightnow.com/v1_3" xsi:type="q1:Incident">"""

    payload2='<ID xmlns="urn:base.ws.rightnow.com/v1_3" id="'+str(rAsJSON["items"][0]["id"])+'" />'

    payload3="""
<q1:CustomFields>
   <ObjectType xmlns="urn:generic.ws.rightnow.com/v1_3">
      <Namespace xsi:nil="true"/>
      <TypeName>IncidentCustomFields</TypeName>
   </ObjectType>
  <GenericFields dataType="OBJECT" name="c" xmlns="urn:generic.ws.rightnow.com/v1_3">
      <DataValue>
         <ObjectValue>
            <ObjectType>
                <Namespace xsi:nil="true"/>
                <TypeName>IncidentCustomFieldsc</TypeName>
            </ObjectType>
               <GenericFields dataType="STRING" name="additional_notes">
                  <DataValue>"""
    payload4='<StringValue>'+resolution+'</StringValue>'
                  
    payload5="""
</DataValue>
               </GenericFields>
            </ObjectValue>
      </DataValue>
   </GenericFields>
</q1:CustomFields>
<q1:StatusWithType><q1:Status><ID xmlns="urn:base.ws.rightnow.com/v1_3" id="2"/>
</q1:Status>
</q1:StatusWithType>
</RNObjects>
<ProcessingOptions>
<SuppressExternalEvents>false</SuppressExternalEvents>
<SuppressRules>false</SuppressRules>
</ProcessingOptions>
</Update>
</s:Body>
</s:Envelope>"""
    d= payload1+payload2+payload3+payload4+payload5




    urlclose = "https://YOURDOMAIN.custhelp.com/cgi-bin/YOURDOMAIN.cfg/services/soap"
    head = {'Content-Type': 'text/xml; charset=utf-8','soapAction':'basicUpdate; charset=utf-8'}
    closed=requests.post(urlclose,auth=('USER', 'PASSWORD'),headers=head,data=d).text
    
    if "Fault" in closed:
         r = str(rAsJSON["items"][0]["id"])
    else:
       r = "Closed case "+ id
    
    return r




    
