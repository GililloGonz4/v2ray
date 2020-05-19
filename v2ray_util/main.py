#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
import pkg_resources

from .util_core.v2ray import V2ray
from .util_core.utils import ColorStr, open_port
from .global_setting import stats_ctr, iptables_ctr, ban_bt, update_timer
from .config_modify import base, multiple, ss, stream, tls

def loop_input_choice_number(input_tip, number_max):
    """
    循环输入选择的序号,直到符合规定为止
    """
    while True:
        print("")
        choice = input(input_tip)
        if not choice:
            break
        if choice.isnumeric():
            choice = int(choice)
        else:
            print(ColorStr.red(_("input error, please input again")))
            continue
        if (choice <= number_max and choice > 0):
            return choice
        else:
            print(ColorStr.red(_("input error, please input again")))

def help():
    exec_name = sys.argv[0]
    from .util_core.config import Config
    lang = Config().get_data('lang')
    if lang == 'zh':
        print("""
{0} [-h|--help] [options]
    -h, --help             get help
    -v, --version        get version
    start              encender V2Ray
    stop               parar V2Ray
    restart           restart V2Ray
    status            verificar status V2Ray
    new                crear nueva cuenta json
    update           actualizar v2ray
    add                  random create mkcp + (srtp | wechat-video | utp | dtls) fake header group
    add [wechat|utp|srtp|dtls|wireguard|socks|mtproto|ss]     create special protocol, random new port
    del                   eliminar puerto del grupo
    info                 verificar cuenta v2ray
    port                 modificar puerto
    tls                    modificar tls
    tfo                   modificar tcpFastOpen
    stream          modificar protocolo
    stats               iptables traffic statistics
    clean              borrar log v2ray
    log                  verificar log v2ray
        """.format(exec_name[exec_name.rfind("/") + 1:]))
    else:
        print("""
{0} [-h|--help] [options]
    -h, --help             get help
    -v, --version        get version
    start              encender V2Ray
    stop               parar V2Ray
    restart           restart V2Ray
    status            verificar status V2Ray
    new                crear nueva cuenta json
    update           actualizar v2ray
    add                  random create mkcp + (srtp | wechat-video | utp | dtls) fake header group
    add [wechat|utp|srtp|dtls|wireguard|socks|mtproto|ss]     create special protocol, random new port
    del                   eliminar puerto del grupo
    info                 verificar cuenta v2ray
    port                 modificar puerto
    tls                    modificar tls
    tfo                   modificar tcpFastOpen
    stream          modificar protocolo
    stats               iptables traffic statistics
    clean              borrar log v2ray
    log                  verificar log v2ray
        """.format(exec_name[exec_name.rfind("/") + 1:]))

def parse_arg():
    if len(sys.argv) == 1:
        return
    elif len(sys.argv) == 2:
        if sys.argv[1] == "start":
            V2ray.start()
        elif sys.argv[1] == "stop":
            V2ray.stop()
        elif sys.argv[1] == "restart":
            V2ray.restart()
        elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
            help()
        elif sys.argv[1] == "-v" or sys.argv[1] == "--version":
            V2ray.version()
        elif sys.argv[1] == "status":
            V2ray.status()
        elif sys.argv[1] == "info":
            V2ray.info()
        elif sys.argv[1] == "port":
            base.port()
            open_port()
            V2ray.restart()
        elif sys.argv[1] == "tls":
            tls.modify()
            V2ray.restart()
        elif sys.argv[1] == "tfo":
            base.tfo()
            V2ray.restart()
        elif sys.argv[1] == "stream":
            stream.modify()
            V2ray.restart()
        elif sys.argv[1] == "stats":
            iptables_ctr.manage()
        elif sys.argv[1] == "clean":
            V2ray.cleanLog()
        elif sys.argv[1] == "del":
            multiple.del_port()
            V2ray.restart()
        elif sys.argv[1] == "add":
            multiple.new_port()
            open_port()
            V2ray.restart()
        elif sys.argv[1] == "update":
            V2ray.update()
        elif sys.argv[1] == "new":
            V2ray.new()
        elif sys.argv[1] == "convert":
            V2ray.convert()
        elif sys.argv[1] == "log":
            V2ray.log()
    else:
        if sys.argv[1] == "add":
            multiple.new_port(sys.argv[2])
            V2ray.restart()
    sys.exit(0)

def service_manage():
    show_text = (_("encender v2ray"), _("parar v2ray"), _("reiniciar v2ray"), _("v2ray status"), _("v2ray log"))
    print("")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("selecione una opcion: "), len(show_text))
    if choice == 1:
        V2ray.start()
    elif choice == 2:
        V2ray.stop()
    elif choice == 3:
        V2ray.restart()
    elif choice == 4:
        V2ray.status()
    elif choice == 5:
        V2ray.log()

def user_manage():
    show_text = (_("agregar usuario"), _("agregar puerto"), _("eliminar usuario"), _("eliminar puerto"))
    print("")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("seleccione una opcion: "), len(show_text))
    if not choice:
        return
    elif choice == 1:
        multiple.new_user()
    elif choice == 2:
        multiple.new_port()
        open_port()
    elif choice == 3:
        multiple.del_user()
    elif choice == 4:
        multiple.del_port()
    V2ray.restart()

def profile_alter():
    show_text = (_("modificar email"), _("modificar UUID"), _("modificar alterID"), _("modifcar port"), _("modificar stream"), _("modificar tls"), 
                _("modificar tcpFastOpen"), _("modificar dyn_port"), _("modificar metodo shadowsocks "), _("modificar contraseña shadowsocks"))
    print("")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("seleccione una opcion: "), len(show_text))
    if not choice:
        return
    elif choice == 1:
        base.new_email()
    elif choice == 2:
        base.new_uuid()
    elif choice == 3:
        base.alterid()
    elif choice == 4:
        base.port()
        open_port()
    elif choice == 5:
        stream.modify()
    elif choice == 6:
        tls.modify()
    elif choice == 7:
        base.tfo()
    elif choice == 8:
        base.dyn_port()
    elif choice == 9:
        ss.modify('method')
    elif choice == 10:
        ss.modify('password')
    V2ray.restart()

def global_setting():
    show_text = (_("V2ray Traffic Statistics"), _("Iptables Traffic Statistics"), _("Ban Bittorrent"), _("Schedule Update V2ray"), _("Clean Log"), _("Cambiar Idioma"))
    print("")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("selecione una opcion: "), len(show_text))
    if choice == 1:
        stats_ctr.manage()
    elif choice == 2:
        iptables_ctr.manage()
    elif choice == 3:
        ban_bt.manage()
        V2ray.restart()
    elif choice == 4:
        update_timer.manage()
    elif choice == 5:
        V2ray.cleanLog()
    elif choice == 6:
        from .util_core.config import Config
        config = Config()
        lang = config.get_data("lang")
        config.set_data("lang", "zh" if lang == "en" else "en")
        print(ColorStr.yellow(_("¡corre de nuevo para ser efectivo!")))
        sys.exit(0)

def menu():
    V2ray.check()
    parse_arg()
    while True:
        print("")
        print(ColorStr.cyan(_("Bienvenido a v2ray-util")))
        print("")
        show_text = (_("1.Administrar v2ray"), _("2.Administrar Grupo"), _("3.Modificar Config"), _("4.Comprobar Config"), _("5.Configuracion Global"), _("6.Actualizar V2Ray"), _("7.Generar Cliente Json"))
        for index, text in enumerate(show_text): 
            if index % 2 == 0:
                print('{:<20}'.format(text), end="")   
            else:
                print(text)
                print("")
        print("")
        choice = loop_input_choice_number(_("seleccione una opcion: "), len(show_text))
        if choice == 1:
            service_manage()
        elif choice == 2:
            user_manage()
        elif choice == 3:
            profile_alter()
        elif choice == 4:
            V2ray.info()
        elif choice == 5:
            global_setting()
        elif choice == 6:
            V2ray.update()
        elif choice == 7:
            from .util_core import client
            client.generate()
        else:
            break

if __name__ == "__main__":
    menu()