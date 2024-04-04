import time
import logging
import argparse

from oven.config import Config, EConfigType
from oven.trans import Translator
from oven.theme import Theme
from oven.site import Site


def build_site(args):
    logging.info("[Oven Site Build Started]")
    config = Config(EConfigType.BUILD)
    run(config)


def gather_trans(args):
    logging.info("[Oven Site Trans Gather Started]")
    config = Config(EConfigType.GATHER)
    run(config)


def run(config: Config) -> None:
    _start_time = time.time()

    # initialize singletons with config
    _ = Translator(config)
    _ = Theme(config)

    site = Site(config)
    if config.is_build_config():
        site.output_content()

    logging.info(f'[Oven Site Finished] {time.time() - _start_time:.3f}s')


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    parser = argparse.ArgumentParser(description='oven - yet another static site generator with markdown support')

    subparsers = parser.add_subparsers(help='commands')

    # Build
    build_parser = subparsers.add_parser('build', help='Build static site')
    build_parser.set_defaults(func=build_site)

    # Gather
    gather_parser = subparsers.add_parser('gather', help='`Gather translations')
    gather_parser.set_defaults(func=gather_trans)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
