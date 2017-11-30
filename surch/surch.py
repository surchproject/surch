########
# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

import sys

import click

from . import repo
from . import constants
from .exceptions import SurchError


CLICK_CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    token_normalize_func=lambda param: param.lower())

search_string = click.option(
    '-s',
    '--string',
    multiple=True,
    default=[],
    help='String you would like to search for. '
         'This can be passed multiple times')
search_common = click.option(
    '--surch-common',
    default=True,
    help='Whether to search for common patterns as well. Defaults to True')
verbose = click.option('-v', '--verbose', default=False, is_flag=True)


@click.group(context_settings=CLICK_CONTEXT_SETTINGS)
def main():
    pass


@main.command(name='repo')
@click.argument('REPO_URL')
@search_string
@search_common
@verbose
def surch_repo(repo_url, string, surch_common, verbose):
    """Search a single repository.
    You can add user_name and password. Used surch like that:

    "surch repo 'https://<user>:<pass>@github.com/cloudify-cosmo/surch.git'"
    """
    try:
        repo.surch(
            repo_url=repo_url,
            search_list=string,
            search_common=surch_common,
            verbose=verbose)
    except SurchError as ex:
        sys.exit(ex)
