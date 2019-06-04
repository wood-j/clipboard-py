import os


def get_user_home() -> str:
    """ return the user home path, support windows and linux """
    if os.name == 'nt':
        return os.environ['USERPROFILE']
    else:
        return os.environ['HOME']


def get_data_root() -> str:
    """ return the data root path """
    # home = get_user_home()
    home = os.path.abspath('')
    return os.path.join(home, 'data')


if __name__ == '__main__':
    print(f'user home dir is {get_user_home()}')
    print(f'data root dir is {get_data_root()}')
