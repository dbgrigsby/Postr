import git


def git_root_dir() -> str:
    git_repo = git.Repo('.', search_parent_directories=True)
    git_root = git_repo.git.rev_parse('--show-toplevel')
    return str(git_root)
