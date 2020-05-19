#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import os

from ..util_core.writer import GroupWriter
from ..util_core.group import Mtproto, SS
from ..util_core.selector import GroupSelector
from ..util_core.utils import get_ip, gen_cert

class TLSModifier:
    def __init__(self, group_tag, group_index):
        self.writer = GroupWriter(group_tag, group_index)
    
    def turn_on(self):
        print(_("1. Encriptemos el certificado (creación automática, prepare el dominio)"))
        print(_("2. Personalizar certificado (preparar rutas de archivo de certificado)"))
        print("")
        choice=input(_("seleccione: "))
        if choice == "1":
            local_ip = get_ip()
            print(_("dirección ip local vps: ") + local_ip + "\n")
            input_domain=input(_("ingrese su dominio vps: "))
            try:
                input_ip = socket.gethostbyname(input_domain)
            except Exception:
                print(_("error de verificación de dominio!!!"))
                print("")
                return
            if input_ip != local_ip:
                print(_("el dominio no puede analizar a la IP local !!"))
                print("")
                return

            print("")
            print(_("generar automáticamente el certificado SSL, espere.."))
            gen_cert(input_domain)
            crt_file = "/root/.acme.sh/" + input_domain +"_ecc"+ "/fullchain.cer"
            key_file = "/root/.acme.sh/" + input_domain +"_ecc"+ "/"+ input_domain +".key"

            self.writer.write_tls(True, crt_file=crt_file, key_file=key_file, domain=input_domain)

        elif choice == "2":
            crt_file = input(_("ingrese la ruta del archivo de certificado de certificado: "))
            key_file = input(_("ingrese la ruta del archivo de clave de certificado: "))
            if not os.path.exists(crt_file) or not os.path.exists(key_file):
                print(_("certificado cert o clave no existe!"))
                return
            domain = input(_("ingrese el dominio del archivo de certificado de certificado: "))
            if not domain:
                print(_("el dominio es nulo"))
                return
            self.writer.write_tls(True, crt_file=crt_file, key_file=key_file, domain=domain)
        else:
            print(_("error de entrada!"))
    
    def turn_off(self):
        self.writer.write_tls(False)

def modify():
    gs = GroupSelector(_('modificar tls'))
    group = gs.group

    if group == None:
        exit(-1)
    else:
        if type(group.node_list[0]) == Mtproto or type(group.node_list[0]) == SS:
            print(_("El protocolo V2ray MTProto/Shadowsocks no es compatible con https!"))
            print("")
            exit(-1)
        tm = TLSModifier(group.tag, group.index)
        tls_status = 'open' if group.tls == 'tls' else 'close'
        print("{}: {}\n".format(_("estado del grupo tls"), tls_status))
        print("")
        print(_("1.abrir TLS"))
        print(_("2.cerrar TLS"))
        choice = input(_("seleccione: "))
        if choice == '1':
            tm.turn_on()
        elif choice == '2':
            tm.turn_off()
        else:
            print(_("error de entrada, ingrese nuevamente"))