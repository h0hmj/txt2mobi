# coding=utf8

import os
import sys
import unittest
import traceback
import shutil
sys.path.append('..')

class TestTxt2MobiFunction(unittest.TestCase):
    def setUp(self):
        pass

    def test_00_init_project(self):
        """
        测试初始化项目目录的功能
        :return:
        :rtype:
        """
        from txt2mobi import utilities
        utilities.init_project()
        file_path = os.path.join(utilities.current_working_dir(), '.project.ini')
        project_file_exists = os.path.isfile(file_path)
        self.assertEqual(project_file_exists, True)
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0].strip(), '[txt2mobi]')
        self.assertEqual(lines[1].strip(), 'kindlegen=kindlegen')
        self.assertEqual(lines[2].strip(), '')
        self.assertEqual(lines[3].strip(), '[book]')
        self.assertEqual(lines[4].strip(), 'cover-img=cover.png')
        self.assertEqual(lines[5].strip(), 'title=书名')
        self.assertEqual(lines[6].strip(), 'author=作者')

        cover_file_path = os.path.join(utilities.current_working_dir(), 'cover.png')
        cover_file_exists = os.path.isfile(cover_file_path)
        self.assertEqual(cover_file_exists, True)

    def test_01_check_kindlegen(self):
        """
        测试检测kindlegen是否已经安装的功能,(成功运行测试需要正确安装kindlegen)
        :return:
        :rtype:
        """
        from txt2mobi import utilities
        from txt2mobi.exceptions import KindleGenNotInstalledError
        utilities.check_kindlgen()
        try:
            utilities.check_kindlgen(command='error_command')
            self.assertFalse(True)
        except KindleGenNotInstalledError as e:
            pass

    def test_02_load_project_config(self):
        """
        检测加载项目配置文件
        :return:
        :rtype:
        """
        from txt2mobi.utilities import ProjectConfig
        config = ProjectConfig()
        self.assertEqual(config.gen_command, 'kindlegen')
        self.assertEqual(config.cover_image, 'cover.png')
        self.assertEqual(config.title, '书名')
        self.assertEqual(config.author, '作者')


    def test_03_gen(self):
        from txt2mobi.scaffold import generate_project
        dist_path = os.path.join(os.getcwd(), 'book.txt')
        dir_path = os.path.join(os.getcwd(), 'samples')
        onlyfiles = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('txt')]
        for file_path in onlyfiles:
            shutil.copy(file_path, dist_path)
            generate_project()
            break


if __name__ == '__main__':
    unittest.main()
