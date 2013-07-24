# -*- encoding: utf-8 -*-

# add extplugins to the Python sys.path
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../extplugins'))

from unittest import TestCase
from mock import patch, call, Mock
from b3 import TEAM_BLUE, TEAM_RED
from b3.fake import FakeConsole, FakeClient
from b3.config import XmlConfigParser, CfgConfigParser
from b3.clients import Client
from asl import AslPlugin


class Test_Asl(TestCase):

    def setUp(self):
        # create a B3 FakeConsole
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString(r"""<configuration/>""")
        self.console = FakeConsole(self.parser_conf)
        # create our plugin instance
        self.plugin_conf = CfgConfigParser()
        self.p = AslPlugin(self.console, self.plugin_conf)
        # initialise the plugin
        self.plugin_conf.loadFromString(r'''
[settings]
action: kick
[messages]
kick_reason: This GUID is already connected.
''')
        self.p.onLoadConfig()
        self.p.onStartup()
        # prepare a few players
        #self.joe = FakeClient(self.console, name="Joe", exactName="Joe", guid="zaerezarezar", groupBits=1, team=TEAM_RED)
        #self.simon = FakeClient(self.console, name="Simon", exactName="Simon", guid="qsdfdsqfdsqf", groupBits=0, team=TEAM_BLUE)
        #self.badsimon = FakeClient(self.console, name="badSimon", exactName="badSimon", guid="qsdfdsqfdsqf", groupBits=0, team=TEAM_BLUE)
        #self.admin = FakeClient(self.console, name="Level-40-Admin", exactName="Level-40-Admin", guid="875sasda", groupBits=16,)
        #self.superadmin = FakeClient(self.console, name="God", exactName="God", guid="f4qfer654r", groupBits=128,)

        #self.joe.connects(cid='1')
        #self.simon.connects(cid='2')

    def test_kick_if_guid_exists(self):
        # GIVEN
        joe = FakeClient(console=self.console, name="Joe", guid="joe_guid", team=TEAM_BLUE)
        simon = FakeClient(console=self.console, name="Simon", guid="simon_guid", team=TEAM_RED)
        badsimon = FakeClient(console=self.console, name="badSimon", guid="simon_guid", team=TEAM_RED)

        simon.connects(cid='2')
        # WHEN
        with patch(target='b3.console.kick') as console_kick_mock:
            badsimon.connects(cid=3)
        # THEN
        self.assertTrue(console_kick_mock.called)

        with patch(target='b3.console.kick') as console_kick_mock:
            joe.connects(cid='1')
        self.assertFalse(console_kick_mock.called)
