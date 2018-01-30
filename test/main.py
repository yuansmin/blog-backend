# -*- coding: utf-8 -*-
import requests
import unittest

HOST = 'http://localhost:8000'

class BlogTest(unittest.TestCase):

    def test_index(self):
        uri = '/api/blogs'
        res = requests.get(HOST+uri)
        self.assertEqual(200, res.status_code)

    def test_read(self):
        blog_id = 1
        uri = '/api/blogs/%s' % blog_id
        res = requests.get(HOST+uri)
        self.assertEqual(200, res.status_code)

    def test_create(self):
        data = {
            'title': '楼继伟：面对金融乱象 不禁感佩朱镕基当年的英明预见',
            'content': '''凤凰网财经讯 1月28日，全国社保基金理事会官网发布了全国社保基金理事长、原财政部长楼继伟在第十六届企业发展高层论坛上的讲话，他提到了上世纪90年代整顿金融秩序对当下的启示，“上世纪90年代，朱镕基同志坚持分业经营。我曾委婉地提出，是不是先观察一下，但他坚持认为，现阶段公民规范守法意识不足、机构监管能力不足，混业必乱。正是在他的坚持下，才有“三会分设”和金融机构按主业拆分。''',
            'category': 1,
            'labels': [1]
        }
        uri = '/api/blogs'
        res = requests.post(HOST+uri, json=data)
        self.assertEqual(201, res.status_code)


class CategoryTest(unittest.TestCase):

    def test_index(self):
        uri = '/api/category'
        res = requests.get(HOST + uri)
        self.assertEqual(200, res.status_code)

    def test_create(self):
        uri = '/api/category'
        data = {'name': '实事'}
        res = requests.post(HOST + uri, json=data)
        self.assertEqual(201, res.status_code)


if __name__ == '__main__':
    unittest.main()

