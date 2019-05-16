import sys
import json
import os
import generate_schema
import resolver_builder

def main(argv):
    endpoints_file = argv[0]
    wrapper_name = argv[1]

    print(endpoints_file)

    endpoints = json.loads(open(endpoints_file).read())

    os.mkdir(wrapper_name)

    os.chdir( os.getcwd() + os.path.sep + wrapper_name)

    generate_schema.generate_schema(endpoints)
    resolver_builder.code_generator(endpoints)
    resolver_builder.server_gererator()

if __name__ == "__main__":
   main(sys.argv[1:])