import json
from urllib.parse import urlparse, parse_qs

def link2v2ray(url):
    config = {}
    inbounds = [
            {
              "port": 1080,
              "listen": "127.0.0.1",
              "protocol": "socks",
              "settings": {
                "auth": "noauth",
                "udp": True
              }
            }
    ]
    
    config["inbounds"] = inbounds

    parsed = urlparse(url)
    protocol = parsed.scheme
    if protocol == "vless":
        UUID, host_port = parsed.netloc.split("@")
        host, port = host_port.split(":")
        port = int(port)

        query = parse_qs(parsed.query)
        print(query)

        streamSettings = {
            "network": query["type"][0],
            "security": query["security"][0],
        }
        if query["type"][0] == "ws":
            streamSettings["wsSettings"] = {
                "path": query["path"][0]
            }

        outbounds = [
                {
                    "protocol":protocol,
                    "settings":{
                        "vnext":[
                            {
                                "address": host,
                                "port": port,
                                "users":[
                                    {
                                        "id": UUID,
                                        "encryption": query["encryption"][0] 
                                    }
                                ]
                            }
                        ]
                    },
                    "streamSettings":streamSettings
                }
        ]
        
        config["outbounds"] = outbounds
        json_config = json.dumps(config, indent=2)
        return json_config


