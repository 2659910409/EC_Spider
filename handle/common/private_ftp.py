import paramiko
import os


class PrivateSFTP:
    def __init__(self, host, port, username, password):
        self.sf = paramiko.Transport((host, port))
        self.sf.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.sf)

    def __remote_file_exists(self, remote_path, remote_file):
        files = self.sftp.listdir(remote_path)
        if remote_file in files:
            return True
        return False

    def __remove(self, remote_file):
        self.sftp.remove(remote_file)

    def upload(self, local_file, remote_path, remote_file, file_exists_del=False):
        print('上传文件：', local_file, ' TO', os.path.join(remote_path, remote_file), ' start!')
        if os.path.isfile(local_file):
            if self.__remote_file_exists(remote_path, remote_file):
                if file_exists_del:
                    print('WARNING -- file:', os.path.join(remote_path, remote_file), ' 上传文件时目标文件已存在删除！')
                    self.__remove(os.path.join(remote_path, remote_file))
                else:
                    print('ERROR -- file:', os.path.join(remote_path, remote_file), ' 上传文件时目标文件已存在！')
                    raise FileExistsError
            self.sftp.put(local_file, os.path.join(remote_path, remote_file))
        else:
            print('ERROR -- file:', local_file, ' 上传文件时本地文件不存在！')
            raise FileNotFoundError
        print('上传文件：', local_file, ' TO', os.path.join(remote_path, remote_file), ' end!')

    def download(self, remote_path, remote_file, local_file, file_exists_del=False):
        print('下载文件：', os.path.join(remote_path, remote_file), ' TO', local_file, ' start!')
        if self.__remote_file_exists(remote_path, remote_file):
            if os.path.exists(local_file):
                if file_exists_del:
                    print('WARNING -- file:', local_file, ' 下载文件时本地文件已存在删除！')
                    os.remove(local_file)
                else:
                    print('ERROR -- file:', local_file, ' 下载文件时本地文件已存在删除！')
                    raise FileExistsError
            self.sftp.get(os.path.join(remote_path, remote_file), local_file)
        else:
            print('ERROR -- file:', os.path.join(remote_path, remote_file), ' 下载文件时目标文件不存在！')
            raise FileNotFoundError
        print('下载文件：', os.path.join(remote_path, remote_file), ' TO', local_file, ' end!')


if __name__ == '__main__':
    # 218.97.27.17:ADMasterPRD/Yz395Dj750wNGqR
    # 218.97.27.17:ADMasterUAT/3K7pF8P30QzlzVR
    host = '218.97.27.17'
    port = 22
    username = 'ADMasterPRD'
    password = 'Yz395Dj750wNGqR'
    sftp = PrivateSFTP(host, port, username, password)
    # 上传文件
    local_file = r'C:\PROJECT\共创平台\RPA\百库\RPAData\tmp\test.csv'
    remote_path = '/test'
    remote_file = 'test1.csv'
    sftp.upload(local_file, remote_path, remote_file, True)
    # 下载文件
    remote_path = '/'
    remote_file = '商品流量来源_20190610.csv'
    local_file = r'C:\PROJECT\共创平台\RPA\百库\RPAData\tmp\test1.csv'
    sftp.download(remote_path, remote_file, local_file, True)
