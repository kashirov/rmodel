#coding: utf8
from rmodel.fields.rhash import rhash
from rmodel.fields.unbound import Unbound
from rmodel.sessions.rsession import RSession
from rmodel.tests.base_test import BaseTest
from rmodel.tests.base_test import TModel


class rhashBaseTest(BaseTest):
    def setUp(self):
        super(rhashBaseTest, self).setUp()
        self.unbound = rhash(int, 0)
        self.model.init_fields((('hash', self.unbound),))
        self.field = self.model.hash


class rhashTest(rhashBaseTest):

    def test_unbound(self):
        self.assertIsInstance(rhash('test', int, 0), Unbound)
        self.assertIsInstance(self.unbound, Unbound)

    def test_bound(self):
        bound_field = self.unbound.bound(self.model, 'test')
        self.assertIsInstance(bound_field, rhash)

        bound_field['q'] = 1
        self.assertEqual(bound_field.data(), {'q': 1})
        self.assertEqual(bound_field.prefix, 'test')

    def test_two_model(self):
        model2 = TModel(prefix='2', redis=self.redis)
        model2.init_fields([('hash', self.unbound)])

        model2.hash['1'] = 1

        self.eq(self.model.data(), {'hash': {}})
        self.eq(model2.data(), {'hash': {'1': 1}})

    def test_contains(self):
        self.false('some_key' in self.model.hash)
        self.model.hash['some_key'] = None
        self.true('some_key' in self.model.hash)

    def test_incr(self):
        self.field.incr('some_key')
        self.eq(self.field['some_key'], 1)
        self.field.incr('some_key', 20)
        self.eq(self.field['some_key'], 21)


class rhashSessionTest(rhashBaseTest):

    def setUp(self):
        super(rhashSessionTest, self).setUp()
        self.session = self.field._session = RSession()

    def test_incr(self):
        self.field['some_key'] = 11
        self.field.incr('some_key')
        self.eq(self.session.changes(), {'model': {'hash': {'some_key': 12}}})