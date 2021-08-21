import configparser
from tools.pathconfig import PathConfig


class RWConfig:

    @classmethod
    def read_config(cls, section, option):
        conf = configparser.ConfigParser()
        conf.read(PathConfig.configpath, encoding='utf-8')
        return conf[section][option]

    @classmethod
    def read_logininfo(cls, option, section='info'):
        conf = configparser.ConfigParser()
        conf.read(PathConfig.loginpath, encoding='utf-8')
        return conf[section][option]

    @classmethod
    def write_config(cls, kwargs, section='info'):  # 传入字典类型的键值对
        conf = configparser.ConfigParser()
        conf.add_section('info')
        for item in kwargs:
            conf.set(section, item, kwargs[item])
        conf.write(fp=open(PathConfig.loginpath, 'w+', encoding='utf-8'))

# if __name__ == '__main__':
#     # print(RWConfig.read_config('platform','platform'))
#     RWConfig.write_config('userID', '1wqdq10')
#     RWConfig.write_config('username', '459qwqw31238748')
#     RWConfig.write_config('name', '与大qdwq四代')
#     RWConfig.flush_config()
