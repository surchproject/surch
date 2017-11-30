import re
import os
import sh
import sys

from . import utils
from . import constants

import git
import giturlparse


COMMON_EXPRESSIONS = {
    # 'AWS_API': re.compile('AKIA[0-9A-Z]{16}')
    'AWS_API': re.compile('import')
}

logger = utils.setup_logger()


def _clone(repo_url, repo_path):
    logger.info('Cloning %s to %s...', repo_url, repo_path)
    git.Repo.clone_from(repo_url, repo_path)


def _pull(repo):
    logger.info('Pulling...')
    # repo.remotes.origin.pull()
    sh.git.pull()


def _get_branches(repo):
    return repo.remotes.origin.fetch()


def _get_branch_name(branch):
    return branch.name.split('/')[1]


def _checkout(repo, branch, branch_name):
    repo.git.checkout(branch)


def _get_commits(repo):
    return repo.iter_commits()


def _reduce_checked(list1, list2):
    return set([item for item in list1 if item not in list2])


def _get_repo_path(repo_url, meta):
    repo_path = os.path.join(
        constants.CLONED_REPOS_PATH, meta.owner, meta.name)
    return repo_path


def _surch_common(data):
    results = []

    for key_type, expression in COMMON_EXPRESSIONS.items():
        result = expression.findall(data)
        if result:
            results.append(result)
            print(result)
            sys.exit()


def _surch_list(data):
    pass


def surch(repo_url, search_list=None, search_common=True, verbose=False):
    """Search for a list of strings or secret oriented regex in a repo

    Example output:

    {
        [
            "blob_url": "https://github.com/nir0s/ghost/blob/.../ghost",
            "commit_sha": "b788a889e484d57451944f93e2b65ed425d6bf65",
            "commit_date": "Wed Aug 24 11:11:56 2016",
            "email": "nir36g@gmail.com",
            "branch": "slack",
            "repo": "ghost",
            "username": "nir0s",
            "result": [
                { "path": "blah.py", "line": "30", "string": "AKI..." },
                ...
            ]
        ],
        ...
    }
    """
    repo_meta = giturlparse.parse(repo_url)
    clone = _get_repo_path(repo_url, repo_meta)
    cloned_now = False
    if not os.path.isdir(clone):
        _clone(repo_url, clone)
        cloned_now = True
    repo = git.Repo(clone)
    reduction_list = []
    # Move to _surch_branches()
    for branch in _get_branches(repo):
        if not cloned_now:
            _pull(repo)
        branch_name = _get_branch_name(branch)
        _checkout(repo, branch, branch_name)
        commits = _get_commits(repo)
        commits = _reduce_checked(commits, reduction_list)
        # TODO: Move to _surch_commits()
        previous_commit = None
        for commit in commits:
            reduction_list.append(commit)
            if not previous_commit:
                pass
            else:
                diff = previous_commit.diff(commit, create_patch=True)
                for blob in diff:
                    dir(blob)
                    sys.exit(1)
                    data = blob.diff.decode('utf-8', errors='replace')
                    if search_common:
                        _surch_common(data)
                    if search_list:
                        _surch_list(data)
            previous_commit = commit
