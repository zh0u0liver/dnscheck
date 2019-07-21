#
# read a host list, check dns resolve A recorder. get time and get ip address one by one
#
# author: 0liver

import dns.resolver
import time
import argparse

class Domain:

    def __init__(self, domain_name):
        self.__lst_ip_addr = []
        self.__str_ip_addr = str()
        self.__resolve_time = float()
        self.__consume_time = float()
        self.__domain_name = domain_name

    def get_str_ip_addr(self):
        return self.__str_ip_addr

    def get_resolve_time(self):
        return self.__resolve_time

    def get_consume_time(self):
        return self.__consume_time

    ip_addr = property(get_str_ip_addr, None)
    resolve_time = property(get_resolve_time, None)

    def resolve(self, q_type):
        t_start = time.perf_counter()

        result = dns.resolver.query(self.__domain_name, q_type)
        t_end = time.perf_counter()
        for iter_ip_addr in result.rrset.items:
            self.__lst_ip_addr.append(iter_ip_addr.address)
            self.__str_ip_addr += iter_ip_addr.address + ","
        self.__resolve_time = result.response.time*1000

        # dns.resolver.Cache.flush()
        self.__consume_time = t_end - t_start


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument("echo")
    parser.add_argument("host_file_name", action="store", help="spcify a hosts file name which need be resolved")
    parser.add_argument("-o", action="store", dest="output_file_name", help="output file name")
    try:
        parse_result = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        exit(0)
    except argparse.ArgumentTypeError:
        parser.print_help()
        exit(0)
    except:
        parser.print_help()
        exit(0)

    host_file_name = parse_result.host_file_name
    output_file_name = parse_result.output_file_name

    str_time = time.strftime("%Y%m%d%H%M%S",time.localtime())
    try:
        with open(host_file_name) as host_file, open(str_time + ".txt", "w") as output_file:
            for host_name in host_file.readlines():
                sub = host_name.strip('\n')
                if not sub: #or sub in host_name:
                    continue
                dns_check_name =Domain(sub)
                dns_check_name.resolve('A')
                print("dns_resolve_time:%8.2fms" % dns_check_name.resolve_time, "ip_list:", dns_check_name.ip_addr)
                output_file.write("%50s\t%8.2f\t%s\n"%(sub,dns_check_name.resolve_time,dns_check_name.ip_addr))
    except IOError as err:
        print("File Error:" + str(err))
